import socket
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", port))

    message = input("Enter command: ")
    client_socket.send(message.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    print("Server response:", response)

    client_socket.close()

if __name__ == "__main__":
    main()