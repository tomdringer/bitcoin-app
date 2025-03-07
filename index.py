import streamlit as st
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

col1, col2 = st.columns(2)

col1.write(""" # Dojo""")

url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
    'symbol': 'BTC,ETH,LTC',  # Example: requesting prices for Bitcoin, Ethereum, and Litecoin
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '<YOUR-API-KEY>',
}

session = Session()
session.headers.update(headers)

# Add title and description
st.title('Cryptocurrency Latest Price List')
st.write("Below are the latest prices for selected cryptocurrencies:")

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)

    # Check if 'data' exists in the response
    if 'data' not in data:
        st.error("The response does not contain 'data'. Please check the API or your request parameters.")
    else:
        # Prepare a list to store the data for display
        crypto_list = []

        for symbol in parameters['symbol'].split(','):
            # Check if the symbol exists within the 'data' dictionary, which is indexed by cryptocurrency IDs (like 'h7nbc0nhqwk')
            for key, crypto in data['data'].items():
                if crypto.get('symbol') == symbol:
                    price = crypto['quote']['USD']['price']
                    crypto_list.append([symbol, price])
                    break
            else:
                # Handle cases where the symbol isn't found
                crypto_list.append([symbol, "Not found", "N/A"])

        # Display the data in a table
        st.dataframe(crypto_list)

except (ConnectionError, Timeout, TooManyRedirects) as e:
    st.error(f"An error occurred: {e}")

except json.JSONDecodeError:
    st.error("Failed to decode JSON response from the API.")
