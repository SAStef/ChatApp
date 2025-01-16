# ChatApp
Cyber Technology DTU Assignment

This project was made as an exercise for the DTU subject, Cyber Technology Part 2.

The project is essentially a messaging app. In this project, a TCP server was coded and implemented, acting as a midpoint and controller, along with a client application, which is a Python file to be run by each client on either end of the connection. The entire project was coded solely in Python, where the UI implementation was done using the PyQt6 library, and multithreading was used along with a socket connection.

## Getting Started

1. Open the repository link: [ChatApp Repository](https://github.com/SAStef/ChatApp.git).
   
2. Clone the code from the repository by running the following command in the terminal:
   ```bash
   git clone https://github.com/SAStef/ChatApp.git
3. Open the project folder in VS Code or another IDE.

4. Ensure that the IP address in the Main.py file points to the chat server's IP address (the computer running the Server.py file). This can be configured on line 21.

5. Start the chat server by running the following command in a dedicated terminal within the correct directory: python Server.py

6. Start the client application by running the following command in a dedicated terminal for each user: python main.py
   
7. Cypher+ is now open, and its features are available. These include: a) A text field for entering messages to be sent.
   
b) The Send Message button, which sends the message (or use the Enter key).
c) The Attach File(s) button (note that crashes may occur).
d) The Set Theme button (a theme must be selected before further use).
e) The AutoScroll On/Off buttons for managing the autoscroll function.

8. Send messages to each other in the chatroom and explore the application!
