# ITNE352-Project-G4


# Our information:
### Sayed Hussain Mohamed 202109507

### Hussain Radhi 20175879


# project overview:
The Client and Server Application is a Python-based system designed to fetch and display news headlines and sources. The server communicates with an external news API to fetch data and saves it in JSON format. The client interacts with the server to request and display this information. The communication between the client and server is secured using SSL.



# Requirements:
Python 3.6+

Required Python libraries:
socket
SSL
JSON
requests
tabulate


# How to run the code:

first, run the "Server.py" by typing in the terminal python Server.py

second, run the "Client.py" by typing in the terminal python Client.py


# Server Functions:

Handle Client Requests: The server handles various requests from the client, such as fetching headlines by different criteria and listing sources.
Save Data to File: The server saves fetched data in JSON format for later use.
Fetch Data from API: The server communicates with the external news API to fetch the latest news headlines and sources.



# The client user interaction:

Enter Username: Upon running the client, you will be prompted to enter your username.

Main Menu:

1- Search Headlines

2- List of Sources

3- Quit

Search Headlines Menu:

1- Search for Keywords

2- Search by Category

3- Search by Country

4- List all new Headlines

5- Back to The Main Menu

List Sources Menu:

1- Search By Category

2- Search by Country

3- Search by Language

4- List all

5- Back to The Main Menu





# Detailed View:

After selecting articles or sources, you can view detailed information by entering the corresponding number.





# Example for user input:

Please write your name: John

clients in the server: ['Alice', 'Bob']

Select One from the options:

1- Search Headlines.

2- List of Sources

3- Quit

1

Search Headlines Menu:

1- Search for Keywords.

2- Search by Category

3- Search by Country

4- List all new Headlines

5- Back to The Main Menu

1

Please input the search keyword: technology




# Error Handling:
The client and server handle common errors such as:

(SSL errors,
Connection errors,
JSON decoding errors,
File I/O errors)



# Conclusion

The Client and Server Application project serves as a comprehensive example of creating a secure and interactive system for fetching and displaying news information. It effectively utilizes Python's networking capabilities, secure socket layer (SSL) for encrypted communication, and external API integration to provide real-time news updates. The project is designed with modularity and user interaction in mind, offering a robust framework for further development and customization.

By adhering to the provided documentation, users can effortlessly set up and run the application, making it accessible for both developers and end-users. The inclusion of detailed menus and data displays ensures a seamless and user-friendly experience. Furthermore, the capability to store and retrieve data locally enhances performance and reliability.

In summary, this project not only functions as a practical tool for accessing news but also as a valuable learning resource for individuals interested in network programming, secure communications, and API integration in Python. Its well-defined structure and comprehensive features make it an excellent foundation for expanding into more complex applications or adapting to different use cases.
