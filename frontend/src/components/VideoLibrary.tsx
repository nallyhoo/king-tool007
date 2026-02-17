import { useState } from 'react';
import { FilterSidebar } from './FilterSidebar';
import { VideoCard } from './VideoCard';
import { useVideoLibrary } from '@/hooks/useVideoLibrary';
import { Button } from "@/components/ui/button";
import {- Video -} from "@/lib/types";

export function VideoLibrary() {
  const [layout, setLayout] = useState('grid');
  const { videos, isLoading, isError } = useVideoLibrary();

  return (
    <div className="flex"> 
      <FilterSidebar />
      <main className="flex-1 p-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold">Video Library</h1>
          <div className="flex items-center space-x-2">
            <Button variant={layout === 'grid' ? 'secondary' : 'ghost'} onClick={() => setLayout('grid')}>
              Grid
            </Button>
            <Button variant={layout === 'list' ? 'secondary' : 'ghost'} onClick={() => setLayout('list')}>
              List
            </Button>
          </div>
        </div>
        
        {isLoading && <p>Loading videos...</p>}
        {isError && <p>Error loading videos.</p>}

        <div className={`grid ${layout === 'grid' ? 'grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6' : 'grid-cols-1 gap-4'}`}>
          {videos.map((video: Video) => (
            <VideoCard key={video.id} video={video} layout={layout} />
          ))}
        </div>
      </main>
    </div>
  );
}
