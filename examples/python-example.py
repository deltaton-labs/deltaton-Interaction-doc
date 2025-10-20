import socketio
import asyncio
import random
import math
import json


async def sleep(ms):
  await asyncio.sleep(ms / 1000)


async def handle_response(data):
  print('Response received:')
  print(json.dumps(data, indent=2))


async def main():
  socket = socketio.AsyncClient(
    reconnection=True,
    reconnection_attempts=5,
    reconnection_delay=1,
    reconnection_delay_max=5
  )
    
  @socket.event
  async def connect():
    print('Successfully connected to WebSocket')
    while True:
      feed_data = {
        'agentType': 'greenhouse',
        'data': {
          'temperature': math.floor(random.random() * 100),
          'temperatureUnit': 'celsius', 
          'humidity': math.floor(random.random() * 100),
        }
      }
      await socket.emit('deltatonFeedData', feed_data, callback=handle_response)
      await sleep(60000)

  @socket.event
  async def connect_error(error):
    print('Connection failed:', error)

  @socket.event
  async def error(error):
    print('Error:', error)

  @socket.event
  async def disconnect():
    print('Disconnected from WebSocket')

  await socket.connect('http://localhost:4000', 
                        auth={
                          'token': 'DeltaFeed YOUR_TOKEN',
                          'userId': 'YOUR_USER_ID'
                        }, 
                        transports=['websocket'], 
                        wait_timeout=20)

  await socket.wait()


if __name__ == '__main__':
  asyncio.run(main())
