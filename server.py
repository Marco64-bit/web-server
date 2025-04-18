from socket import *

# Server settings
serverPort = 6789
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print(f"Web server is running on port {serverPort}...")

while True:
    print("\nReady to serve...")
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()
        print("Received request:")
        print(message)

        # Parse HTTP GET request
        filename = message.split()[1]
        if filename == '/':
            filename = '/index.html'  # Default to index.html
        filepath = filename[1:]  # remove leading slash

        # Open and read the requested file
        with open(filepath, 'r') as f:
            outputdata = f.read()

        # Send HTTP headers
        responseHeader = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
        connectionSocket.send(responseHeader.encode())
        print(responseHeader)

        # Send file content
        connectionSocket.send(outputdata.encode())


    except FileNotFoundError:
        # Send 404 Not Found response
        errorMessage = 'HTTP/1.1 404 Not Found\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>'
        connectionSocket.send(errorMessage.encode())
        print(errorMessage)

    finally:
        connectionSocket.close()
