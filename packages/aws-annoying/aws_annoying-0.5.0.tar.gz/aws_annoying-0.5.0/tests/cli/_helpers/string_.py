import re


def normalize_console_output(output: str) -> str:
    """Normalize the console output for easier comparison."""
    # Remove leading and trailing spaces
    output = output.strip()

    # Unwrap each line
    output = re.sub(r"[ ]+\n", " ", output)

    return output  # noqa: RET504
