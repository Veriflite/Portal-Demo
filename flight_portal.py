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
                data = j['data']
                event = j['event']
            except json.decoder.JSONDecodeError:
                print(f"::: {pkt}")
                continue

            if event == 'bounce':
                address = data['sensorAddress']
                seq = data['sequenceNumber']
                tof = data['timeOfFlight']
                tofDelta = data['toFDelta']
                impactTimestamp = int(data['impactTimestamp'])
                isValid = data['isInvalid']
                print(f"{address} {seq} ToF:{tof} tofDelta:{tofDelta} impactTimestamp:{impactTimestamp} isValid:{isValid}")

            elif event == 'idle':
                address = data['sensorAddress']
                seq = data['sequenceNumber']
                idleTimestamp = int(data['idleTimestamp'])
                print(f"{address} {seq} idleTimestamp:{idleTimestamp}")

            elif event == 'missing-data':
                print(pkt)
                address = data['sensorAddress']
                missingSeqNumbers = data['missingSequenceNumbers']
                print(f"{address} missingSeqNumbers:{missingSeqNumbers}")

            elif event == 'sensor-reset':
                print(pkt)
                address = data['sensorAddress']
                print(f"{address} SENSOR RESET - is there any other data to go here???")


            else:
                print(f"Unexpected event: {event} :: {pkt}")
                assert(False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, required=True, help="The IP address of the Veriflite portal")
    args = parser.parse_args()

    asyncio.run(main(f"ws://{args.ip}:4651/flight"))

