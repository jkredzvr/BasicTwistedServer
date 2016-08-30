# Basic Twisted Server Template

Python scripts to set up a Twisted Server for asynchronous messaging between Twisted Server and Twisted Clients.  Allows for client registration
and broadcasting messages to individual clients, client_types, or all clients.  Template is extensible to allow additional client types or functions.
Also includes RPC interface to allow for command line operation using a TCP connection to the server.

## Getting Started

These are the base python scripts to handle the backend operation of the twisted server.  
Python server script and RPC client  needs to be configured for open ports on the server.  

### Prerequisities

Twisted and Autobahn python packages will need to be set up to use this server.
http://autobahn.ws/python/

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Original code modified from https://github.com/tank-2/example_twisted_service

