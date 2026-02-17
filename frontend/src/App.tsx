import { Routes, Route } from "react-router-dom";
import { DownloadManager } from "@/components/DownloadManager";
import { VideoLibrary } from "@/components/VideoLibrary";
import { useWebSocketEvents } from "./hooks/useWebSocketEvents";

function App() {
  useWebSocketEvents();
  
  return (
    <Routes>
      <Route path="/" element={<DownloadManager />} />
      <Route path="/videos" element={<VideoLibrary />} />
    </Routes>
  );
}

export default App;
