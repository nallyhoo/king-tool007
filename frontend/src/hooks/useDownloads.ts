import { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '@/services/api';
import { useWebSocket } from './useWebSocket';
import { Download } from '@/lib/types';

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
    mutationFn: apiService.startDownload,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['downloads'] });
    },
  });

  const handleDownloadProgress = useCallback((progress: any) => {
    queryClient.setQueryData<Download[]>(['downloads'], (oldData) => {
      if (!oldData) return [];
      const index = oldData.findIndex(d => d.id === progress.id);
      if (index !== -1) {
        const newData = [...oldData];
        newData[index] = { ...newData[index], ...progress };
        return newData;
      } else {
        // It's a new download, so we fetch the full list again.
        // A more optimized approach might add the new download directly.
        queryClient.invalidateQueries({ queryKey: ['downloads']});
        return oldData;
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
