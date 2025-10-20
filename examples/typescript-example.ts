import { io } from 'socket.io-client';

async function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  const socket = io('https://api.deltaton.com', {
    auth: {
      token: 'DeltaFeed <YOUR_TOKEN>',
      userId: '<YOUR_USER_ID>'
    },
    transports: ['websocket'],
    autoConnect: false,
    timeout: 20000,
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000
  });

  socket.connect();

  socket.on('connect', async () => {
    console.log('Successfully connected to WebSocket');

    while (true) {
      const feedData = {
        agentType: 'greenhouse',
        data: {
          temperature: Math.floor(Math.random() * 100),
          temperatureUnit: 'celsius',
          humidity: Math.floor(Math.random() * 100),
        }
      };
      socket.emit('deltatonFeedData', feedData, (response: any) => {
        console.log(response);
      });
      await sleep(60000);
    }
  });

  socket.on('connect_error', (error: any) => {
    console.error('Connection failed:', error);
  });

  socket.on('error', (error: any) => {
    console.error(error);
  });

  socket.on('disconnect', () => {
    console.log('Disconnected from WebSocket');
  });
})();
