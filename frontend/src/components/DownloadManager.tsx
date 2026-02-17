import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { DownloadCard } from './DownloadCard';
import { useDownloads } from '@/hooks/useDownloads';
import type { Download } from '@/lib/types';


const formSchema = z.object({
  url: z.string().url({ message: "Please enter a valid URL." }),
});

export function DownloadManager() {
  const { activeDownloads, queuedDownloads, completedDownloads, failedDownloads, startDownload } = useDownloads();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      url: "",
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    startDownload(values.url);
    form.reset();
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Download Manager</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 mb-8">
          <div className="space-y-2">
            <Label htmlFor="url">Single URL</Label>
            <Input id="url" {...form.register("url")} placeholder="https://..." />
            {form.formState.errors.url && (
              <p className="text-red-500 text-sm">{form.formState.errors.url.message}</p>
            )}
          </div>
          <Button type="submit">Download</Button>
        </form>

        <Tabs defaultValue="active">
          <TabsList>
            <TabsTrigger value="active">Active ({activeDownloads.length})</TabsTrigger>
            <TabsTrigger value="queued">Queued ({queuedDownloads.length})</TabsTrigger>
            <TabsTrigger value="completed">Completed ({completedDownloads.length})</TabsTrigger>
            <TabsTrigger value="failed">Failed ({failedDownloads.length})</TabsTrigger>
          </TabsList>
          <TabsContent value="active">
            {activeDownloads.map((download) => (
              <DownloadCard key={download.id} download={download} />
            ))}
          </TabsContent>
          <TabsContent value="queued">
            {queuedDownloads.map((download) => (
              <DownloadCard key={download.id} download={download} />
            ))}
          </TabsContent>
          <TabsContent value="completed">
            {completedDownloads.map((download) => (
              <DownloadCard key={download.id} download={download} />
            ))}
          </TabsContent>
          <TabsContent value="failed">
            {failedDownloads.map((download) => (
              <DownloadCard key={download.id} download={download} />
            ))}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
