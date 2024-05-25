import socket
import json

# Server configuration
HOST = '127.0.0.1'
PORT = 2048

# Function to display the main menu and get user input
def display_main_menu():
    print("---------------------- Main Menu: ------------------")
    print("1. Search headlines")
    print("2. List of sources")
    print("3. Quit")
    print("----------------------------------------------------")
    return input("Enter your option: ")

# Function to display the headlines menu and get user input
def display_headlines_menu():
    print("-------------------- Headlines Menu: -----------------")
    print("1. Search for keywords")
    print("2. Search by category")
    print("3. Search by country")
    print("4. List all new headlines")
    print("5. Back to the main menu")
    print("------------------------------------------------------")
    return input("Enter your option: ")

# Function to display the sources menu and get user input
def display_sources_menu():
    print("-------------------- Sources Menu: -----------------")
    print("1. Search by category")
    print("2. Search by country")
    print("3. Search by language")
    print("4. List all")
    print("5. Back to the main menu")
    print("-----------------------------------------------------")
    return input("Enter your option: ")
