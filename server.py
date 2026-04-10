import socket
import sys
import threading

# this is our shared database (key-value store)
# it stays in memory while the server is running
db = {}

# used to name clients like Client A, Client B, etc.
client_count = 0

# lock so multiple threads don’t mess up client_count
count_lock = threading.Lock()


def process_command(message, client_name):
    # split message into parts
    # maxsplit = 2 so value can have spaces
    parts = message.strip().split(" ", 2)

    if not parts:
        return "ERROR: Invalid command"

    command = parts[0]

    # PUT command: store key-value pair
    if command == "PUT":
        if len(parts) < 3:
            return "ERROR: Invalid command"

        key = parts[1]
        value = parts[2]

        db[key] = value  # store in dictionary
        print(f"[LOG] {client_name} wrote key '{key}'")

        return "OK"

    # GET command: retrieve value from dictionary
    elif command == "GET":
        if len(parts) < 2:
            return "ERROR: Invalid command"

        key = parts[1]

        if key in db:
            print(f"[LOG] {client_name} read key '{key}'")
            return db[key]
        else:
            return "ERROR: Key not found"

    else:
        return "ERROR: Invalid command"


def handle_client(client_socket, client_name):
    # this function runs in a separate thread for each client

    data = client_socket.recv(1024)  # receive message (bytes)

    if data:
        message = data.decode("utf-8")  # convert bytes to string

        response = process_command(message, client_name)

        # send response back to client
        client_socket.send(response.encode("utf-8"))

    # close connection after handling request
    client_socket.close()


def main():
    global client_count

    # make sure user passed in a port number
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])

    # create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind to localhost and given port
    server_socket.bind(("127.0.0.1", port))

    # start listening for clients
    server_socket.listen()

    print(f"[START] Server listening on port {port}")

    try:
        while True:
            # wait for a client to connect
            client_socket, client_address = server_socket.accept()

            # assign a name like Client A, B, C...
            with count_lock:
                client_name = f"Client {chr(ord('A') + client_count)}"
                client_count += 1

            print(f"[LOG] Accepted connection from {client_name}")

            # create a new thread to handle this client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_name)
            )

            # start the thread (this makes it concurrent)
            client_thread.start()

    except KeyboardInterrupt:
        # allows clean shutdown with Ctrl + C
        print("\n[SHUTDOWN] Server stopping...")
        server_socket.close()


if __name__ == "__main__":
    main()