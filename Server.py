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
    
# Function to handle a client connection with the server
def handle_connection(connection, name):
    global SERVER
    try:
        # Adding the client's name to the list of connected clients
        clients_list.append(name)
        # Notifying the server about the new thread
        print(name, " Have a Thread in the server now")
        print("Current clients in the server: " + str(clients_list))
        # Sending the updated list of connected clients to the client
        connection.sendall(str(clients_list).encode())
        # Continuous loop to handle client requests
        while True:
            # Receiving the option selected by the client
            received_option = receive_full_data(connection)
            # Handling different options selected by the client
            if str(received_option) == "1":
                keyword = receive_full_data(connection)
                print(str(name)+" has selected Headlines Keyword Option and The Keyword is :"+ keyword)
                connection.sendall(headlines_request("q", keyword, name,"").encode())
                article_number = receive_full_data(connection)
                print(str(name) + " has selected Headlines Keyword Option and The Keyword is :" + keyword + " And Selected Article are: "  + article_number)
                result = headlines_request("q", keyword, name,article_number)
                connection.sendall(result.encode())
            elif str(received_option) == "2":
                category = receive_full_data(connection)
                print(str(name)+" has selected Headlines Category Option and The category is :"+ category)
                connection.sendall(headlines_request("category", category, name,"").encode())
                article_number = receive_full_data(connection)
                print(str(name) + " has selected Headlines Category Option and The category is :" + category + " And Selected Article are: "  + article_number)
                result = headlines_request("category", category, name,article_number)
                connection.sendall(result.encode())
            elif str(received_option) == "3":
                country = receive_full_data(connection)
                print(str(name)+" has selected Headlines Country Option and The country is :"+ country)
                connection.sendall(headlines_request("country", country, name,"").encode())
                article_number = receive_full_data(connection)
                print(str(name) + " has selected Headlines Country Option and The country are :" + country + " And Selected Article are: "  + article_number)
                result = headlines_request("country", country, name,article_number)
                connection.sendall(result.encode())
            elif str(received_option) == "4":
                print(str(name)+" has selected All Top Headlines Option")
                connection.sendall(headlines_request("All", "", name,"").encode())
                article_number = receive_full_data(connection)
                print(str(name) + " has selected All Top Headlines Option And Selected Article are: "  + article_number)
                result = headlines_request("All", "", name,article_number)
                connection.sendall(result.encode())
            elif str(received_option) == "5":
                category = receive_full_data(connection)
                print(str(name)+" has selected Sources Category  Option and The category is :"+ category)
                connection.sendall(sources_request("category", category, name,"").encode())
                source_number = receive_full_data(connection)
                print(str(name) + " has selected Sources Category Option and The category are :" + category + " And Selected Source are: "  + source_number)
                result = sources_request("category", category, name, source_number)
                connection.sendall(result.encode())
            elif str(received_option) == "6":
                country = receive_full_data(connection)
                print(str(name)+" has selected Sources Country Option and The country is :"+ country)
                connection.sendall(sources_request("country", country, name,"").encode())
                source_number = receive_full_data(connection)
                print(str(name) + " has selected Sources Country Option and The category are :" + country + " And Selected Source are: "  + source_number)
                result = sources_request("country", country, name, source_number)
                connection.sendall(result.encode())
            elif str(received_option) == "7":
                language = receive_full_data(connection)
                print(str(name)+" has selected Sources language Option and The Language is :"+ language)
                connection.sendall(sources_request("language", language, name,"").encode())
                source_number = receive_full_data(connection)
                print(str(name) + " has selected Sources language Option and The Language are :" + language + " And Selected Source are: "  + source_number)
                result = sources_request("language", language, name, source_number)
                connection.sendall(result.encode())
            elif str(received_option) == "8":
                print(str(name)+" has selected All Sources Option")
                connection.sendall(sources_request("All", "", name,"").encode())
                source_number = receive_full_data(connection)
                print(str(name) + " has selected All Sources Option And Selected Source are: "  + source_number)
                result = sources_request("All", "", name,source_number)
                connection.sendall(result.encode())
            elif str(received_option) == "9":
                # Notifying the server that the thread for the client is disconnected
                print("Thread for : "+str(name)+" is disconnected")
                # Closing the connection and ending the thread
                connection.close()

# Function to start the server and handle client connections
def start_server():
    global SERVER
    try:
        # Creating an SSL context on the server side
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem",password="22552255")
        # Creating a socket for the server with IPv4 and TCP protocol
        SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Binding the server socket to a specific IP address and port number (127.0.0.1:49995 in my case)
        SERVER.bind(("127.0.0.1", 49995))

        # Setting up the server to listen for client connections
        SERVER.listen(5)

        # Notifying that the server is started
        print("server is started")
