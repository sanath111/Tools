import requests

def is_internet_available(url='http://8.8.8.8'):
    try:
        requests.head(url, timeout=1)
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Unable to connect to {url}. Please check the URL and try again.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error: An unexpected error occurred - {e}")
        return False

# Example usage:
if is_internet_available():
    print("Internet connection is available")
else:
    print("No internet connection available")
