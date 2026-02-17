import { useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '@/services/api';
import { useWebSocket } from './useWebSocket';
import type { Download } from '@/lib/types';

export const useDownloads = () => {
  const queryClient = useQueryClient();

  const {
    data: downloads = [],
    isLoading,
    isError,
  } = useQuery<Download[]>({
    queryKey: ['downloads'],
    queryFn: apiService.getDownloads,
  });

  const startDownloadMutation = useMutation({
    mutationFn: (url: string) => apiService.startDownload(url),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['downloads'] });
    },
  });

  const handleDownloadProgress = useCallback((progress: Download) => {
    queryClient.setQueryData<Download[]>(['downloads'], (oldData) => {
      const data = oldData ?? [];
      const index = data.findIndex(d => d.id === progress.id);
      if (index !== -1) {
        const newData = [...data];
        newData[index] = { ...newData[index], ...progress };
        return newData;
      } else {
        queryClient.invalidateQueries({ queryKey: ['downloads']});
        return data;
      }
    });
  }, [queryClient]);

  useWebSocket({
    'download_progress': handleDownloadProgress,
  });

  const startDownload = (url: string) => {
    startDownloadMutation.mutate(url);
  };

  const activeDownloads = downloads.filter(d => d.status === 'downloading' || d.status === 'processing');
  const queuedDownloads = downloads.filter(d => d.status === 'queued');
  const completedDownloads = downloads.filter(d => d.status === 'completed');
  const failedDownloads = downloads.filter(d => d.status === 'failed');

  return {
    downloads,
    activeDownloads,
    queuedDownloads,
    completedDownloads,
    failedDownloads,
    isLoading,
    isError,
    startDownload,
  };
};
