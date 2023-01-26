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

            if j['event'] == 'packet':
                pkt = j['data']
                vfEvent = pkt['type']
                address = pkt['address']
                seq = pkt['sequenceNumber']
                data = pkt['data']

                if 'IMPACT' in vfEvent:
                    print(f"{address} {seq} IMPACT at {data}")

                elif 'DEPART' in vfEvent:
                    print(f"{address} {seq} DEPART at {data}")

                elif 'IDLE' in vfEvent:
                    print(f"{address} {seq} IDLE at {data}")

                elif 'BATTERY_VOLTAGE' == vfEvent:
                    print(f"{address} {seq} BATTERY_VOLTAGE is {data}mV")

                elif 'NAME' == vfEvent:
                    print(f"{address} {seq} NAME is {data}")

                else:
                    # Check we don't get any unimplemented packet types
                    print(f"{address} {seq} {vfEvent} {data}")
                    assert(False)

            else:
                print(f"Unexpected event: {j['event']}")
                assert(False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, required=True, help="The IP address of the Veriflite portal")
    args = parser.parse_args()

    asyncio.run(main(f"ws://{args.ip}:4651/raw"))

