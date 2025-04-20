# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import sys
import uvicorn
# import yaml
from dotenv import load_dotenv

def signal_handler(sig, frame):
    print("\nSignal handler called with signal", sig)
    print("Program will exit now.")
    sys.exit(0)

# register
signal.signal(signal.SIGINT, signal_handler)


def server():

    load_dotenv()

    # with open('config.yaml', 'r') as f:
    #     config = yaml.safe_load(f)

    # os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'] = config['ALIBABA_CLOUD_ACCESS_KEY_ID']
    # os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'] = config['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
    from web import app
    uvicorn.run(app, host="0.0.0.0", port=8100)


if __name__ == "__main__":
    server()
