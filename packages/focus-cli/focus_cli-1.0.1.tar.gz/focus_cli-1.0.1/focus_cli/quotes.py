from utils import load_json, save_json

# Path to quotes.json to track quotes
quotes_file = "data/quotes.json"

def add_quote(quote_content):
    """Adds a new developer quote."""
    quotes = load_json(quotes_file)
    
    quote_id = len(quotes) + 1  # Generate unique quote ID
    quote = {
        "id": quote_id,
        "content": quote_content,
    }
    
    quotes[quote_id] = quote
    save_json(quotes_file, quotes)
    
    print(f"Quote added! Quote ID: {quote_id}")

def list_quotes():
    """Lists all developer quotes."""
    quotes = load_json(quotes_file)
    
    if not quotes:
        print("No quotes available.")
        return
    
    print("Quotes:")
    for quote in quotes.values():
        print(f"ID: {quote['id']} - {quote['content']}")

def delete_quote(quote_id):
    """Deletes a quote by ID."""
    quotes = load_json(quotes_file)
    
    if quote_id not in quotes:
        print(f"Quote with ID {quote_id} not found.")
        return
    
    quote = quotes.pop(quote_id)
    save_json(quotes_file, quotes)
    
    print(f"Quote '{quote['content']}' deleted.")
