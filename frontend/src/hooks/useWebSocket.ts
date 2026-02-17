import { useEffect, useRef } from 'react';
import { io, Socket } from 'socket.io-client';

const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || 'ws://localhost:5000';

export const useWebSocket = (eventHandlers: Record<string, (...args: any[]) => void>) => {
  const socket = useRef<Socket | null>(null);

  useEffect(() => {
    const newSocket = io(SOCKET_URL, {
      transports: ['websocket']
    });
    socket.current = newSocket;

    newSocket.on('connect', () => {
      console.log('WebSocket connected');
    });

    newSocket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    for (const event in eventHandlers) {
      newSocket.on(event, eventHandlers[event]);
    }

    return () => {
      newSocket.disconnect();
    };
  }, [eventHandlers]);

  return socket.current;
};
