import requests

def fetch_and_store_data(api_url, collection_name):
    """Fetches external API data and stores it in MongoDB."""
    response = requests.get(api_url)
    data = response.json()

    # Insert data into a specific MongoDB collection
    db[collection_name].insert_one({"data": data})
    
    return "Data stored successfully!"

# Example usage
fetch_and_store_data("https://api.exchangerate-api.com/v4/latest/USD", "exchange_rates")
