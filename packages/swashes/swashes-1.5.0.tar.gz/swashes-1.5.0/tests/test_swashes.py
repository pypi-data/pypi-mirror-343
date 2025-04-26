import subprocess


def test_swashes_cli():
    expected_first_line = b"SWASHES version 1.05.00, 2025-04-22"
    output = subprocess.run(["swashes"], capture_output=True).stderr
    first_line = output.splitlines()[0]
    assert first_line == expected_first_line
