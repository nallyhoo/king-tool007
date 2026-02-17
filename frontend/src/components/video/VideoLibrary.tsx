import { useState } from 'react';
import { Grid, List, GanttChartSquare } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { FilterSidebar } from './FilterSidebar';
import { useVideoLibrary } from '@/hooks/useVideoLibrary';
import { VideoCard } from './VideoCard';

export type ViewMode = 'grid' | 'list' | 'timeline';

export function VideoLibrary() {
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const { videos, isLoading, error } = useVideoLibrary();

  return (
    <div className="flex h-full">
      <FilterSidebar />
      <main className="flex-1 p-6">
        <header className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">Video Library</h1>
          <div className="flex items-center space-x-2">
            <Button variant={viewMode === 'grid' ? 'secondary' : 'ghost'} size="icon" onClick={() => setViewMode('grid')}>
              <Grid className="h-5 w-5" />
            </Button>
            <Button variant={viewMode === 'list' ? 'secondary' : 'ghost'} size="icon" onClick={() => setViewMode('list')}>
              <List className="h-5 w-5" />
            </Button>
            <Button variant={viewMode === 'timeline' ? 'secondary' : 'ghost'} size="icon" onClick={() => setViewMode('timeline')}>
              <GanttChartSquare className="h-5 w-5" />
            </Button>
          </div>
        </header>

        {isLoading && <p>Loading videos...</p>}
        {error && <p className="text-red-500">Error loading videos.</p>}

        {viewMode === 'grid' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {videos.map(video => (
              <VideoCard key={video.id} video={video} />
            ))}
          </div>
        )}

        {/* Add other view modes here (list, timeline) */}

      </main>
    </div>
  );
}
