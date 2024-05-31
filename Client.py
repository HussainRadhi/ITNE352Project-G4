import socket
import json

# Server configuration
HOST = '127.0.0.1'
PORT = 2048

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
print("Connected to server succeeded")
username= input("Enter username: ")
Client_send=(username, client_socket)
 
 
# Function to display the main menu and get user input
def display_main_menu():
    print("---------------------- Main Menu: ------------------")
    print("1. Search headlines")
    print("2. List of sources")
    print("3. Quit")
    print("----------------------------------------------------")
    return input("Enter your option: ")
    
       

# Function to display the headlines menu and get user input
def display_headlines_menu(client_socket):
    print("-------------------- Headlines Menu: -----------------")
    print("1. Search for keywords")
    print("2. Search by category")
    print("3. Search by country")
    print("4. List all new headlines")
    print("5. Back to the main menu")
    print("------------------------------------------------------")
    return input("Enter your option: ")

# Function to display the sources menu and get user input
def display_sources_menu(client_socket):
    print("-------------------- Sources Menu: -----------------")
    print("1. Search by category")
    print("2. Search by country")
    print("3. Search by language")
    print("4. List all")
    print("5. Back to the main menu")
    print("-----------------------------------------------------")
    return input("Enter your option: ")  


#Parameters:
Categories = ["business", "entertainment", "general", "health", "science" "sports", "technology"]
Countries = ["au", "nz", "ca", "ae", "sa", "gb", "us", "eg", "ma"]
Languages =["ar", "en"]






def headlines(Client_socket):
     HData = Client_socket.recv(200000).decode()
     List_details = json.loads(HData)
     print("-------------------- | The headlines:| -----------------\n")
     for index, item in enumerate(List_details['Articles']):
          print(f"{index+1}. {item['Title']} -{item['description']} ")
     headlines_number = input("Enter the number of articles you want: ")
     headlines_want = List_details['Articles'][headlines_number - 1]

     print("Article NO.{headline_number} details:\n")
     print(f"Source Name: {headlines_want['source']['name']}")
     print(f"Author: {headlines_want['author']}")
     print(f"Title: {headlines_want['title']}")
     print(f"URL: {headlines_want['url']}")
     print(f"Description: {headlines_want['description']}")
     print(f"Published Date & Time: {headlines_want['publishedAt']}")


def sources(Client_socket):
     SData = Client_socket.recv(200000).decode()
     List_details = json.loads(SData)
     print("-------------------- | The sources:| -----------------\n")
     for index, item in enumerate(List_details['sources']):
          print(f"{index+1}. {item['name']}")
     
     sources_number = input("Enter the number of sources you want: ")
     sources_want = List_details['sources'][sources_number - 1]
     
     print("Source NO.{sources_number} details:\n")
     print(f"Name: {sources_want['name']}")
     print(f"Country: {sources_want['country']}")
     print(f"Description: {sources_want['description']}")
     print(f"URL: {sources_want['url']}")
     print(f"Category: {sources_want['category']}")
     print(f"Language: {sources_want['language']}")



while True:
 opt = display_main_menu
 opt_headlines = display_headlines_menu
 opt_sources = display_sources_menu 

 if opt == 1:
       display_headlines_menu(client_socket)
       if opt_headlines == 1:
            keyword = input("Enter keyword: ")
            opt = f"1. {opt_headlines}.{keyword}"
            Client_send = (opt, client_socket)
            headlines(client_socket)
       elif opt_headlines == 2:
      
            print("[business, entertainment, general, health, science, sports, technology]")
            category = input("\nEnter category: ")
            if category not in Categories:
                  print("Invalid Category!")
                 
            opt = f"1. {opt_headlines}.{category}"
            Client_send = (opt, client_socket)
            headlines(client_socket)

       elif opt_headlines == 3:
           print("[au, nz, ca, ae, sa, gb, us, eg, ma]")
           country = input("\nEnter country: ")
           if country not in Countries:
               print("Invalid Country!")
            
           opt = f"1. {opt_headlines}.{country}"
           Client_send = (opt, client_socket)
           headlines(client_socket)
       
       elif opt_headlines == 4:
            opt = f"1. {opt_headlines}.null"
            Client_send(opt,client_socket)
            headlines(client_socket)
       
       elif opt_headlines == 5:
            print("123")
            #return
       else:
            print("Invalid Option!")
            #return

 elif opt == 2:
       display_sources_menu(client_socket)

       if opt_sources == 1:
            print(["business, entertainment, general, health, science, sports, technology"])
            category = input("\nEnter category: ")
            if category not in Categories:
                 print("Invalid Category!")
                 #return
            opt = f"2. {opt_sources}.{category}"
            Client_send = (opt, client_socket)
            sources(client_socket)
            
             
       elif opt_sources == 2:
           print("[au, nz, ca, ae, sa, gb, us, eg, ma]")
           country = input("\nEnter country: ")
           if country not in Countries:
               print("Invalid Country!")
            
           opt = f"1. {opt_sources}.{country}"
           Client_send = (opt, client_socket)
           sources(client_socket)
       
       elif opt_sources == 3:
            print("[ar, en]")
            Language = input("\nEnter language: ")
            if Language not in Languages:
                 print("Invalid Language!")
                 #return
            opt = f"2. {opt_sources}.{Language}"
            Client_send = (opt, client_socket)
            sources(client_socket)
       
       elif opt_sources == 4:
            opt = f"{opt_sources}.null"
            Client_send = (opt, client_socket)
            sources(client_socket)
       elif opt_sources == 5:
            print("123")
            #return
       else:
            print("Invalid Option!")
            #return


 elif opt == 3:
       print("Thank you for using the news aggregator service.","\n Goodbye :)")
       break
 else:
       print("Invalid option. Please try again.")




def Client_send(opt, Client_socket):
     Client_socket.send(opt.encode())



if __name__ == "__main__":
     display_main_menu()


