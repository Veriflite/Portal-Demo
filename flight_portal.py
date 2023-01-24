#!/usr/bin/env python

import argparse
import asyncio
import json
import websockets

async def main(uri):
    print(f"Opening connection to Veriflite portal: {uri}")
    async for websocket in websockets.connect(uri):
        while True:
            pkt = await websocket.recv()

            try:
                j = json.loads(pkt)
            except json.decoder.JSONDecodeError:
                print(f"::: {pkt}")
                continue

            print(f"{j['SensorAddress']} ToF: {j['TimeOfFlight']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, required=True, help="The IP address of the Veriflite portal")
    args = parser.parse_args()

    asyncio.run(main(f"ws://{args.ip}:4651/flight"))

