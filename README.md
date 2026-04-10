# Concurrent Key-Value Server

## Overview
This project is a concurrent key-value server implemented in Python using TCP sockets and multithreading. It allows multiple clients to connect to a server and perform basic operations such as storing and retrieving key-value pairs.

The system demonstrates core networking and concurrency concepts by handling multiple client connections simultaneously while maintaining a shared in-memory data store.

## Features
- TCP-based client-server communication
- Concurrent handling of multiple clients using threads
- In-memory key-value store
- Support for basic commands:
  - `PUT <key> <value>` — store a value
  - `GET <key>` — retrieve a value
- Simple text-based protocol for communication
- Logging of client interactions

## How It Works
The server listens for incoming TCP connections on a specified port. Each client connection is handled in a separate thread, allowing multiple clients to interact with the server at the same time.

All data is stored in a shared dictionary on the server. Clients send commands as strings, which the server parses and executes before returning a response.

## Tech Stack
- Python
- Socket Programming (TCP)
- Multithreading

## Project Structure
server.py # Handles client connections and processes commands
client.py # Connects to the server and sends commands
