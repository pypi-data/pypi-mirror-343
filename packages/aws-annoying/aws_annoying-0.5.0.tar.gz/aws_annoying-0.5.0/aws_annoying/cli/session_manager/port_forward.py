from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path  # noqa: TC003

import typer
from rich import print  # noqa: A004

from ._app import session_manager_app
from ._common import SessionManager, get_instance_id_by_name


# https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html
@session_manager_app.command()
def port_forward(  # noqa: PLR0913
    # TODO(lasuillard): Add `--local-host` option, redirect the traffic to non-localhost bind (unsupported by AWS)
    local_port: int = typer.Option(
        ...,
        show_default=False,
        help="The local port to use for port forwarding.",
    ),
    through: str = typer.Option(
        ...,
        show_default=False,
        help="The name or ID of the EC2 instance to use as a proxy for port forwarding.",
    ),
    remote_host: str = typer.Option(
        ...,
        show_default=False,
        help="The remote host to connect to.",
    ),
    remote_port: int = typer.Option(
        ...,
        show_default=False,
        help="The remote port to connect to.",
    ),
    reason: str = typer.Option(
        "",
        help="The reason for starting the port forwarding session.",
    ),
    pid_file: Path = typer.Option(  # noqa: B008
        "./session-manager-plugin.pid",
        help="The path to the PID file to store the process ID of the session manager plugin.",
    ),
    terminate_running_process: bool = typer.Option(  # noqa: FBT001
        False,  # noqa: FBT003
        help="Terminate the process in the PID file if it already exists.",
    ),
    log_file: Path = typer.Option(  # noqa: B008
        "./session-manager-plugin.log",
        help="The path to the log file to store the output of the session manager plugin.",
    ),
) -> None:
    """Start a port forwarding session using AWS Session Manager."""
    session_manager = SessionManager()

    # Check if the PID file already exists
    if pid_file.exists():
        if not terminate_running_process:
            print("🚫 PID file already exists.")
            raise typer.Exit(1)

        pid_content = pid_file.read_text()
        try:
            existing_pid = int(pid_content)
        except ValueError:
            print(f"🚫 PID file content is invalid; expected integer, but got: {type(pid_content)}")
            raise typer.Exit(1) from None

        try:
            print(f"⚠️ Terminating running process with PID {existing_pid}.")
            os.kill(existing_pid, signal.SIGTERM)
            pid_file.write_text("")  # Clear the PID file
        except ProcessLookupError:
            print(f"⚠️ Tried to terminate process with PID {existing_pid} but does not exist.")

    # Resolve the instance name or ID
    instance_id = get_instance_id_by_name(through)
    if instance_id:
        print(f"❗ Instance ID resolved: [bold]{instance_id}[/bold]")
        target = instance_id
    else:
        print(f"🚫 Instance with name '{through}' not found.")
        raise typer.Exit(1)

    # Initiate the session
    command = session_manager.build_command(
        target=target,
        document_name="AWS-StartPortForwardingSessionToRemoteHost",
        parameters={
            "host": [remote_host],
            "portNumber": [str(remote_port)],
            "localPortNumber": [str(local_port)],
        },
        reason=reason,
    )
    stdout: subprocess._FILE
    if log_file is not None:  # noqa: SIM108
        stdout = log_file.open(mode="at+", buffering=1)
    else:
        stdout = subprocess.DEVNULL

    print(
        f"🚀 Starting port forwarding session through [bold]{through}[/bold] with reason: [italic]{reason!r}[/italic].",
    )
    proc = subprocess.Popen(  # noqa: S603
        command,
        stdout=stdout,
        stderr=subprocess.STDOUT,
        text=True,
        close_fds=False,  # FD inherited from parent process
    )
    print(f"✅ Session Manager Plugin started with PID {proc.pid}. Outputs will be logged to {log_file.absolute()}.")

    # Write the PID to the file
    pid_file.write_text(str(proc.pid))
    print(f"💾 PID file written to {pid_file.absolute()}.")
