import socket
import threading
import json
import requests
import ssl
# List to keep track of connected clients
clients_list = []


def save_f_data(data, type, name, request_type):
    # Placeholder function, you need to implement this
    file_name = f"G4_{name}_{type}_{request_type}.json"
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return file_name


# Functions to process client requests

def headlines_request(request_type, filter_criteria, name, article_number):
    ApiKey = "92caab6f774548e2852b1aa6ceed17b7"
    try:
        if request_type in ["country", "q", "category","All"]:
            if article_number == "":
                if request_type != "All":
                    request_url = f"https://newsapi.org/v2/top-headlines?{request_type.lower()}={filter_criteria}&apiKey={ApiKey}&pageSize=15&page=1"
                else:
                    request_url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={ApiKey}&pageSize=15&page=1"
                try:
                    response = requests.get(request_url)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    return f"Request failed: {e}"
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    return "Failed to parse the response JSON."
                if 'articles' in data:
                    articles = data['articles']
                    if articles:
                        try:
                            save_f_data(data,"headlines", name, request_type)
                        except IOError as e:
                            return f"Failed to save data to file: {e}"
                        json_data = json.dumps(data, ensure_ascii=False)
                        return json_data
                    else:
                        return "No articles found in the response."
                else:
                    return "No 'articles' key found in the response."
            else:
                try:
                    with open(f"G4_{name}_headlines_{request_type}.json", 'r', encoding='utf-8') as file:
                        data = json.load(file)
                except FileNotFoundError:
                    return ("File not found.")
                except json.JSONDecodeError:
                    return ("Failed to parse the saved JSON file.")
                except IOError as e:
                    return (f"Failed to read file: {e}")

                articles_info = []
                articles = data.get('articles', [])
                # Check if there are articles in the data
                article_number = int(article_number)-1
                if articles:
                    # Check if the specified index is within the range of available articles
                    if 0 <= article_number < len(articles):
                        article = articles[article_number]

                        published_at = article.get('publishedAt', 'Unknown')
                        if published_at != 'Unknown':
                            date, time = published_at.split('T')
                            time = time.split('Z')[0]
                        else:
                            date, time = 'Unknown', 'Unknown'
                        info = {
                            'source': article.get('source', {}).get('name', 'Unknown'),
                            'author': article.get('author', 'Unknown'),
                            'title': article.get('title', 'No title'),
                            'url': article.get('url', 'Unknown'),
                            'description': article.get('description', 'No description'),  # Get the source name
                            'publish_date': date,
                            'publish_time': time
                        }
                        articles_info.append(info)
                    else:
                        return(f"Article at index {article_number} not found.")
                else:
                    return("No articles found in the data.")
                return json.dumps(articles_info, ensure_ascii=False)
    except Exception as e:
        return f"An unexpected error occurred 1: {e}"
        
def sources_request(request_type, filter_criteria, name, source_number):
    ApiKey = "92caab6f774548e2852b1aa6ceed17b7"
    try:
        if request_type in ["country", "language", "category","All"]:
            if source_number == "":
                if request_type != "All":
                    request_url = f"https://newsapi.org/v2/top-headlines/sources?{request_type.lower()}={filter_criteria}&apiKey={ApiKey}&pageSize=15&page=1"
                else:
                    request_url = f"https://newsapi.org/v2/top-headlines/sources?&apiKey={ApiKey}&pageSize=15&page=1"
                try:
                    response = requests.get(request_url)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    return f"Request failed: {e}"
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    return "Failed to parse the response JSON."
                if 'sources' in data:
                    sources = data['sources']
                    if sources:
                        try:
                            save_f_data(data,"sources", name, request_type)
                        except IOError as e:
                            return f"Failed to save data to file: {e}"
                        json_data = json.dumps(data, ensure_ascii=False)
                        return json_data
                    else:
                        return "No Sources found in the response."
                else:
                    return "No 'Sources' key found in the response."
            else:
                try:
                    with open(f"G4_{name}_sources_{request_type}.json", 'r', encoding='utf-8') as file:
                        data = json.load(file)
                except FileNotFoundError:
                    return ("File not found.")
                except json.JSONDecodeError:
                    return ("Failed to parse the saved JSON file.")
                except IOError as e:
                    return (f"Failed to read file: {e}")

                sources_info = []
                sources = data.get('sources', [])
                source_number = int(source_number)-1
                if sources:
                    if 0 <= source_number < len(sources):
                        source = sources[source_number]
                        info = {
                            'name': source.get('name', 'Unknown'),
                            'country': source.get('country', 'Unknown'),
                            'description': source.get('description', 'No description'),
                            'url': source.get('url', 'Unknown'),
                            'category': source.get('category', 'Unknown'),
                            'language': source.get('language', 'Unknown')
                        }
                        sources_info.append(info)
                    else:
                        return(f"Source at index {source_number} not found.")
                else:
                    return("No sources found in the data.")
                return json.dumps(sources_info, ensure_ascii=False)
    except Exception as e:
        return f"An unexpected error occurred 2: {e}"

# Get Full Data
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
