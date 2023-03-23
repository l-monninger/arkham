from blocks.presentation.server.std_server.std_server import StdServer
import sys

if __name__ == "__main__":
    server = StdServer()
    server.serve(host="0.0.0.0", port=80)