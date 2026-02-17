import { Link } from "react-router-dom";
import { ConnectionStatus } from "@/components/ConnectionStatus";
import { Toaster } from "@/components/ui/toaster";

interface LayoutProps {
    children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
    return (
        <div className="min-h-screen bg-background font-sans antialiased">
            <header className="bg-primary text-primary-foreground">
                <div className="container mx-auto px-4">
                    <nav className="flex items-center justify-between py-4">
                        <Link to="/" className="text-2xl font-bold">Downloader</Link>
                        <div className="space-x-4">
                            <Link to="/" className="hover:underline">Downloads</Link>
                            <Link to="/videos" className="hover:underline">Video Library</Link>
                        </div>
                    </nav>
                </div>
            </header>
            <main className="container mx-auto px-4 py-8">
                {children}
            </main>
            <ConnectionStatus />
            <Toaster />
        </div>
    );
}