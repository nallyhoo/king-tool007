import type { Download } from '@/lib/types';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface DownloadCardProps {
  download: Download;
}

export function DownloadCard({ download }: DownloadCardProps) {
  const { progress, status, url } = download;
  const percentage = typeof progress.percentage === 'string' ? parseFloat(progress.percentage.replace('%', '')) : progress.percentage;

  return (
    <Card className="mb-4">
      <CardHeader>
        <CardTitle className="truncate">{progress.filename || url}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-500">{status}</span>
          <span className="text-sm font-semibold">{progress.percentage}</span>
        </div>
        <Progress value={percentage} />
        <div className="flex justify-between items-center mt-2">
          <span className="text-sm text-gray-500">{progress.speed}</span>
          <span className="text-sm text-gray-500">{progress.eta}</span>
        </div>
      </CardContent>
      <CardFooter className="flex justify-end space-x-2">
        <Button variant="outline" size="sm" disabled={status !== 'downloading'}>Pause</Button>
        <Button variant="outline" size="sm" disabled={status !== 'paused'}>Resume</Button>
        <Button variant="destructive" size="sm">Cancel</Button>
      </CardFooter>
    </Card>
  );
}
