from etl.extract.extract import pytest_confirm


def test_pytest():
    # Arrange
    input = 1
    expected_output = 2
    # Action
    actual_output = pytest_confirm(input)
    # Assert
    assert actual_output == expected_output
