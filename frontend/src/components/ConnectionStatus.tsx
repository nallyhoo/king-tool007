import { useWebSocket } from '@/context/WebSocketContext';

export const ConnectionStatus = () => {
  const { isConnected } = useWebSocket();

  return (
    <div className="fixed bottom-4 right-4">
      <div className={`px-4 py-2 rounded-full text-white ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}>
        {isConnected ? 'Connected' : 'Disconnected'}
      </div>
    </div>
  );
};
