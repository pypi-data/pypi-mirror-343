import requests

def shorten_url(url: str) -> str:
    """
    Shorten a URL using TinyURL's API.
    
    Args:
        url (str): The URL to shorten
        
    Returns:
        str: Shortened URL
        
    Example:
        >>> from urlify import shorten_url
        >>> short_url = shorten_url('https://www.example.com/very/long/url')
    """
    try:
        response = requests.get(f'http://tinyurl.com/api-create.php?url={url}')
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to shorten URL. Status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error shortening URL: {str(e)}")
