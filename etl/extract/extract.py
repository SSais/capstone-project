import requests


def get_request_coingecko_api(api_key):
    try:
        url = "https://api.coingecko.com/api/v3/coins/list"
        headers = {
            "accept": "application/json",
            "x-cg-api-key": api_key
        }

        response = requests.get(url, headers=headers)
        print(response.status_code)
        return response.text
    except Exception as e:
        raise Exception(f'An unexpected error occurred.\nError: {e}.')
