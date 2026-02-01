import webbrowser

def search_in_browser(query: str) -> str:
    """Opens the default browser and performs a search with the given query."""
    if not query:
        return "No search query provided."
    try:
        # Encode the query for URL
        encoded_query = query.replace(' ', '+')
        url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(url)
        return f"Opened browser and searched for '{query}'."
    except Exception as e:
        return f"Failed to perform search: {e}"

def open_browser() -> str:
    """Opens the default web browser."""
    try:
        webbrowser.open("https://www.google.com")
        return "Opened default web browser."
    except Exception as e:
        return f"Failed to open browser: {e}"
