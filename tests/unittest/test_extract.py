import pytest
from unittest.mock import patch

from etl.extract.extract import get_request_coingecko_api

mock_api_key = 123


# Test get request to coingecko api
def test_get_request_coingecko_api():
    # Arrange
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '{api-data}'
        # Action
        response = get_request_coingecko_api(mock_api_key)
        # Assert
        assert response == '{api-data}'


# Test get request exception
def test_get_request_exception():
    # Arrange
    expected_error = 'An unexpected error occurred'
    # Action
    with pytest.raises(Exception) as msg:
        get_request_coingecko_api(mock_api_key)
    # Assert
    assert expected_error in str(msg.value)
