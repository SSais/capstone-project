# import pytest
# # from unittest.mock import patch

# from etl.extract.extract_alphavantage_api import get_request,get_request_overview_alphavantage, get_request_daily_alphavantage

# # Could not get mock to work for the new get
# # def test_get_request_coingecko_api():
# #     # Arrange
# #     with patch('requests.get') as mock_get:
# #         mock_get.return_value.status_code = 200
# #         mock_get.return_value.text = '{api-data}'
# #         # Action
# #         response = get_request_coingecko_api(mock_api_key)
# #         # Assert
# #         assert response == '{api-data}'


# # Test get request overview exception
# def test_get_request_overview_exception():
#     # Arrange
#     test_symbol = 1
#     expected_error = 'An unexpected error occurred'
#     # Action
#     with pytest.raises(Exception) as msg:
#         get_request_overview_alphavantage(test_symbol)
#     # Assert
#     assert expected_error in str(msg.value)


# # Test get request exception
# def test_get_request_exception():
#     # Arrange
#     test_symbol = 1
#     test_function = 'test'
#     expected_error = 'An unexpected error occurred'
#     # Action
#     with pytest.raises(Exception) as msg:
#         get_request(test_symbol, test_function)
#     # Assert
#     assert expected_error in str(msg.value)


# # Test get request daily exception
# def test_get_request_daily_exception():
#     # Arrange
#     test_symbol = 1
#     expected_error = 'An unexpected error occurred'
#     # Action
#     with pytest.raises(Exception) as msg:
#         get_request_daily_alphavantage(test_symbol)
#     # Assert
#     assert expected_error in str(msg.value)
