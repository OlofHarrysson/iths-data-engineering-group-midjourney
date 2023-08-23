import sys


def test_python_version():
    # Here I am using Python's sys module to check the python version
    # version_info returns a list and from this list i chose the second item which is the python minor version
    # Then I use the assert function to compare both values, and throw an assert error if both values are not 10
    minor_version = sys.version_info[1]
    assert (
        minor_version == 10
    ), f"The expected and required Python version for this project is 3.10.*, but got 3.{minor_version}.*"
