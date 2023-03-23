from blocks.presentation.server.std_server.std_server import StdServer
import os
import sys

if __name__ == "__main__":
    server = StdServer()
    server.serve(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))