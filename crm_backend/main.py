# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import sys
import uvicorn
import argparse
#from dotenv import load_dotenv


def signal_handler(sig, frame):
    print("\nSignal handler called with signal", sig)
    print("Program will exit now.")
    sys.exit(0)

# register
signal.signal(signal.SIGINT, signal_handler)


def server():
#    load_dotenv()
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='A simple command-line interface for the CRM backend.')

    # Add arguments
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8100, help='Port to run the server on')

    # Parse the arguments
    args = parser.parse_args()

    from web import app
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    server()
