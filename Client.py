import socket
import ssl
import json
from tabulate import tabulate

# Creating a client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Creating a new SSL context for the client and disabling certificate verification
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Wrapping the client socket with SSL
client = ssl_context.wrap_socket(client, server_hostname="127.0.0.1")

try:
    # Connecting to the server
    client.connect(("127.0.0.1", 49995))
except ssl.SSLError as e:
    print(f"SSL Error: {e}")
    exit()
except ConnectionRefusedError:
    print("Connection refused. Make sure the server is running.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()


def receive_full_data(client_socket, buffer_size=4096):
    data = b""
    while True:
        part = client_socket.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            break
    try:
        decoded_data = data.decode()  # Try to decode the received data
    except UnicodeDecodeError:
        decoded_data = data  # If decoding fails, use the raw bytes
    return decoded_data

def print_table_articles(articles):
    print("{:<5} {:<30} {:<30} {:<60}".format("No.", "Source", "Author", "Title"))
    print("="*105)
    limit = 1
    for idx, article in enumerate(articles, start=1):
        source = article.get('source', {}).get('name', 'N/A')
        author = article.get('author', 'N/A')
        title = article.get('title', 'N/A')
        
        # Ensure the values are strings (in case of None, replace with 'N/A')
        if author is None:
            author = 'N/A'
        if source is None:
            source = 'N/A'
        
        # Truncate long strings to fit the table format
        title = title if title else 'N/A'
        author = author if author else 'N/A'
        source = source if source else 'N/A'
        if limit <= 15:
            print("{:<5} {:<30} {:<30} {:<60}".format(idx, source[:30], author[:30], title[:60]))
            limit = limit + 1
    return limit-1


def print_table_sources(sources):
    print("{:<5} {:<30}".format("No.", "Source Name"))
    print("=" * 105)
    limit = 1
    for idx, source in enumerate(sources, start=1):
        source_name = source.get('name', 'N/A')

        # Ensure the values are strings (in case of None, replace with 'N/A')
        if source_name is None:
            source_name = 'N/A'

        # Truncate long strings to fit the table format
        source_name = source_name if source_name else 'N/A'
        if limit <= 15:
            print("{:<5} {:<30}".format(idx, source_name[:30]))
            limit = limit + 1
    return limit - 1

def print_selected_article_headlines(data):
    try:
        articles_data = json.loads(data)
        if isinstance(articles_data, dict) and "error" in articles_data:
            print(articles_data["error"])
        else:
            # Prepare data for tabulate
            table_data = [[article['source'], article['author'], article['title'], article['url'], article['description'],article['publish_date'], article['publish_time']] for article in articles_data]
            # Print the table
            print(tabulate(table_data,headers=["Source", "Author", "Title", "URL", "Description", "Publish Date", "Publish Time"],tablefmt="grid"))
    except json.JSONDecodeError:
        print(data)  # Print the raw string data if decoding fails

def print_selected_source(data):
    try:
        sources_data = json.loads(data)
        if isinstance(sources_data, dict) and "error" in sources_data:
            print(sources_data["error"])
        else:
            # Prepare data for tabulate
            table_data = [[source['name'], source['country'], source['description'], source['url'], source['category'], source['language']] for source in sources_data]
            # Print the table
            print(tabulate(table_data,headers=["Source Name", "Country", "Description", "URL", "Category", "Language"], tablefmt="grid"))
    except json.JSONDecodeError:
        print(data)  # Print the raw string data if decoding fails