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
           # headlines(client_socket)
       elif opt_headlines == 2:
      
            print(["business, entertainment, general, health, science, sports, technology"])
            category = input("\nEnter category: ")
            if category not in Categories:
                  print("Invalid Category!")
                 
            opt = f"1. {opt_headlines}.{category}"
            Client_send = (opt, client_socket)
            # headlines(client_socket)

       elif opt_headlines == 3:
           country = input("[au, nz, ca, ae, sa, gb, us, eg, ma]","\nEnter country: ")
           if country not in Countries:
               print("Invalid Country!")
            
           opt = f"1. {opt_headlines}.{country}"
           Client_send = (opt, client_socket)
           # headlines(client_socket)
       
       elif opt_headlines == 4:
            opt = f"1. {opt_headlines}.null"
            Client_send(opt,client_socket)
            # headlines(client_socket)
       
       elif opt_headlines == 5:
            print("123")
       else:
            print("Invalid Option!")

 elif opt == 2:
       display_sources_menu(client_socket)
 elif opt == 3:
       print("Thank you for using the news aggregator service.","\n Goodbye :)")
       break
 else:
       print("Invalid option. Please try again.")
