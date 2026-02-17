import type { Video } from '@/lib/types';

interface VideoPlayerProps {
  video: Video;
  onClose: () => void;
}

export function VideoPlayer({ video, onClose }: VideoPlayerProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] overflow-hidden">
        <div className="relative pb-[56.25%] h-0">
          <video className="absolute top-0 left-0 w-full h-full" controls src=""></video>
        </div>
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-56.25%)]">
          <h2 className="text-2xl font-bold mb-2">{video.title}</h2>
          <p className="text-gray-600 mb-4">By {video.creator}</p>
          <div className="flex flex-wrap gap-2 mb-4">
            {video.tags.map(tag => (
              <span key={tag} className="bg-gray-200 text-gray-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded-full">{tag}</span>
            ))}
          </div>
        </div>
        <button onClick={onClose} className="absolute top-4 right-4 text-white text-2xl">&times;</button>
      </div>
    </div>
  );
}
