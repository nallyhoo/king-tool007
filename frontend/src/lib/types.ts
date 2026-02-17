export interface Download {
  id: string;
  url: string;
  status: 'queued' | 'downloading' | 'processing' | 'completed' | 'failed' | 'paused' | 'canceled';
  progress: {
    percentage: number | string;
    eta: string;
    speed: string;
    filename: string;
    total_bytes: number;
    downloaded_bytes: number;
  };
  options?: any;
  title?: string;
  channel?: string;
  thumbnail?: string;
}

export interface Video {
  id: string;
  title: string;
  thumbnailUrl: string;
  creator: string;
  uploadDate: string;
  downloadDate: string;
  duration: number;
  fileSize: number;
  quality: string;
  views: number;
  tags: string[];
}
