import { useEffect } from 'react';
import { useWebSocket } from '@/context/WebSocketContext';
import { useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';

export const useWebSocketEvents = () => {
  const { socket } = useWebSocket();
  const queryClient = useQueryClient();
  const { toast } = useToast();

  useEffect(() => {
    if (!socket) return;

    const handleDownloadStarted = (data: any) => {
      console.log('Download started:', data);
      queryClient.invalidateQueries({ queryKey: ['downloads'] });
      toast({ title: 'Download Started', description: data.title });
    };

    const handleDownloadProgress = (data: any) => {
      console.log('Download progress:', data);
      queryClient.setQueryData(['downloads', data.id], (oldData: any) => {
        if (!oldData) return oldData;
        return { ...oldData, progress: data.progress, speed: data.speed };
      });
    };

    const handleDownloadCompleted = (data: any) => {
      console.log('Download completed:', data);
      queryClient.invalidateQueries({ queryKey: ['downloads'] });
      queryClient.invalidateQueries({ queryKey: ['videos'] });
      toast({ title: 'Download Completed', description: data.title });
    };
    
    const handleDownloadFailed = (data: any) => {
        console.error('Download failed:', data);
        queryClient.invalidateQueries({ queryKey: ['downloads'] });
        toast({ title: 'Download Failed', description: data.error, variant: 'destructive' });
    };

    socket.on('download_started', handleDownloadStarted);
    socket.on('download_progress', handleDownloadProgress);
    socket.on('download_completed', handleDownloadCompleted);
    socket.on('download_failed', handleDownloadFailed);

    return () => {
      socket.off('download_started', handleDownloadStarted);
      socket.off('download_progress', handleDownloadProgress);
      socket.off('download_completed', handleDownloadCompleted);
      socket.off('download_failed', handleDownloadFailed);
    };
  }, [socket, queryClient, toast]);
};
