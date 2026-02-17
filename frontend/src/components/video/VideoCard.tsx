import { Video } from "@/lib/types";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MoreVertical } from "lucide-react";
import { Checkbox } from "@/components/ui/checkbox";

interface VideoCardProps {
  video: Video;
}

export function VideoCard({ video }: VideoCardProps) {
  const formatDuration = (seconds: number) => {
    const h = Math.floor(seconds / 3600).toString().padStart(2, '0');
    const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${h}:${m}:${s}`;
  };

  return (
    <Card className="w-full overflow-hidden">
      <CardHeader className="p-0 relative">
        <img src={video.thumbnailUrl} alt={video.title} className="w-full h-auto" />
        <Badge className="absolute bottom-2 right-2">{formatDuration(video.duration)}</Badge>
        <div className="absolute top-2 left-2">
            <Checkbox />
        </div>
      </CardHeader>
      <CardContent className="p-4">
        <CardTitle className="text-lg font-semibold truncate" title={video.title}>{video.title}</CardTitle>
        <p className="text-sm text-muted-foreground mt-1">{video.creator}</p>
      </CardContent>
      <CardFooter className="p-4 flex justify-between items-center">
        <div className="text-sm text-muted-foreground">
          <p>Downloaded: {new Date(video.downloadDate).toLocaleDateString()}</p>
          <p>Uploaded: {new Date(video.uploadDate).toLocaleDateString()}</p>
        </div>
        <MoreVertical className="cursor-pointer" />
      </CardFooter>
    </Card>
  )
}
