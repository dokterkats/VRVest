import asyncio
import websockets
from websocket import create_connection
import json
from time import sleep

# For more information check out
# https://github.com/bhaptics/tact-python


# Create a websocket on the same port games use to connect
# to the bhaptics player
ws = create_connection("ws://192.168.1.53:80/ws")

async def server(websocket, path):
    while True:
        try:
            # Get received data from websocket
            data = await websocket.recv()


            data = json.loads(data.replace("'", "\""))
            # Check the json sent has the correct attributes.
            if 'Submit' in data:
                if 'Frame' in data['Submit'][0]:
                    # Grab the duration to turn the motors on for
                    duration = data['Submit'][0]['Frame']['DurationMillis']
                    # each frame can have multiple motors so map each to our ids
                    motors = []
                    for point in data['Submit'][0]['Frame']['DotPoints']:
                        motors += map_front_motors(point['Index'])

                    # Turn the relevant motors on
                    GPIO.output(Relay_Ch1,GPIO.LOW)

                    # Sleep for the duration in milliseconds
                    sleep(duration/1000)
                    # Then turn all the motors off
                    GPIO.output(Relay_Ch1,GPIO.HIGH)


        except Exception as e:
            print(e)


# Create the websocket server
start_server = websockets.serve(server, "localhost", 15881)

# Start and run websocket server forever
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
