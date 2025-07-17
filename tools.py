import requests
from langchain_core.tools import tool
from database import get_all_sweets

# Your Node.js backend API URL
API_BASE_URL = "http://localhost:5000"


@tool
def buy_sweet(sweet_name: str, quantity: int) -> str:
    """
    Buys a specified quantity of a single sweet.
    First finds the sweet by name to get its ID, then calls the purchase endpoint.
    """
    try:
        # Find the sweet by name to get its ID
        search_response = requests.get(
            f"{API_BASE_URL}/search", params={"name": sweet_name}
        )
        if search_response.status_code != 200 or not search_response.json():
            return f"Error: Could not find a sweet named '{sweet_name}'."

        sweets = search_response.json()
        if len(sweets) > 1:
            return f"Error: Found multiple sweets matching '{sweet_name}'. Please be more specific."

        sweet_id = sweets[0]["_id"]

        # Call the purchase endpoint with the ID and quantity
        purchase_response = requests.post(
            f"{API_BASE_URL}/purchase/{sweet_id}", json={"quantity": quantity}
        )

        if purchase_response.status_code == 200:
            return f"Successfully purchased {quantity} of {sweet_name}."
        else:
            # Pass the error message from the backend API
            return f"Failed to purchase: {purchase_response.json().get('message', 'Unknown error')}"

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


@tool
def get_available_sweets() -> str:
    """
    Gets the list of all available sweets currently in the database inventory.
    Use this when customers ask about what items are available or what you have in stock.
    """
    try:
        sweets = get_all_sweets()
        if not sweets:
            return "No sweets are currently available in our inventory."

        # Format the sweets list nicely
        sweet_list = []
        for sweet in sweets:
            name = sweet.get("name", "Unknown")
            price = sweet.get("price", "N/A")
            quantity = sweet.get("quantity", 0)

            # Format price with INR symbol
            if price != "N/A":
                try:
                    price_formatted = f"₹{float(price):.2f}"
                except (ValueError, TypeError):
                    price_formatted = f"₹{price}"
            else:
                price_formatted = "Price not available"

            sweet_list.append(f"- {name}: {price_formatted} (Stock: {quantity})")

        return "Here are the sweets currently available:\n" + "\n".join(sweet_list)

    except Exception as e:
        return f"Sorry, I couldn't retrieve the current inventory: {str(e)}"
