import type { Video } from "@/lib/types";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "./ui/button";

interface VideoCardProps {
  video: Video;
  layout: 'grid' | 'list';
}

export function VideoCard({ video, layout }: VideoCardProps) {
  if (layout === 'list') {
    return (
      <Card className="flex items-center p-4">
        <img src={video.thumbnailUrl} alt={video.title} className="w-32 h-20 object-cover rounded-md mr-4" />
        <div className="flex-1">
          <h3 className="text-lg font-semibold">{video.title}</h3>
          <p className="text-sm text-gray-500">{video.creator}</p>
          <p className="text-sm text-gray-500">{video.uploadDate}</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm">Play</Button>
          <Button variant="outline" size="sm">Edit</Button>
          <Button variant="destructive" size="sm">Delete</Button>
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="p-0">
        <img src={video.thumbnailUrl} alt={video.title} className="w-full h-48 object-cover rounded-t-lg" />
      </CardHeader>
      <CardContent className="p-4">
        <CardTitle className="text-lg font-semibold truncate">{video.title}</CardTitle>
        <p className="text-sm text-gray-500">{video.creator}</p>
      </CardContent>
      <CardFooter className="p-4 flex justify-between">
        <p className="text-sm text-gray-500">{video.uploadDate}</p>
        <Button size="sm">Play</Button>
      </CardFooter>
    </Card>
  );
}
