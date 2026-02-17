import { useQuery } from '@tanstack/react-query';
import type { Video } from '@/lib/types';

// Mock data for initial development
const mockVideos: Video[] = [
  {
    id: '1',
    title: 'Big Buck Bunny',
    thumbnailUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Big_Buck_Bunny_thumbnail_vlc.png/1200px-Big_Buck_Bunny_thumbnail_vlc.png',
    creator: 'Blender Foundation',
    uploadDate: '2024-05-20',
    downloadDate: '2024-05-21',
    duration: 596,
    fileSize: 150 * 1024 * 1024, // 150 MB
    quality: '1080p',
    views: 1234567,
    tags: ['animation', 'short film', 'blender'],
  },
  {
    id: '2',
    title: 'Sintel',
    thumbnailUrl: 'https://i.ytimg.com/vi/eRsGyueVLvQ/maxresdefault.jpg',
    creator: 'Blender Foundation',
    uploadDate: '2010-09-27',
    downloadDate: '2024-05-20',
    duration: 888,
    fileSize: 250 * 1024 * 1024, // 250 MB
    quality: '1080p',
    views: 543210,
    tags: ['animation', 'fantasy', 'short film'],
  },
    {
    id: '3',
    title: 'Elephants Dream',
    thumbnailUrl: 'https://i.ytimg.com/vi/dv_k1mS9I_w/maxresdefault.jpg',
    creator: 'Blender Foundation',
    uploadDate: '2006-03-24',
    downloadDate: '2024-05-19',
    duration: 653,
    fileSize: 180 * 1024 * 1024, // 180 MB
    quality: '720p',
    views: 987654,
    tags: ['animation', 'sci-fi', 'short film'],
  }
];

export const useVideoLibrary = () => {
  const {
    data: videos = [],
    isLoading,
    isError,
  } = useQuery<Video[]>({ 
    queryKey: ['videos'], 
    queryFn: async () => {
      // This is where you would fetch data from your API
      // For now, we return mock data after a short delay
      await new Promise(resolve => setTimeout(resolve, 500));
      return mockVideos;
    }
  });

  return {
    videos,
    isLoading,
    isError,
  };
};
