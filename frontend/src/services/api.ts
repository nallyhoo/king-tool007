import type { Video, Download } from '@/lib/types';

const API_URL = '/api';

async function fetchFromAPI(endpoint: string, options: RequestInit = {}): Promise<any> {
    try {
        const response = await fetch(`${API_URL}/${endpoint}`, options);
        if (!response.ok) {
            throw new Error(`API call failed: ${response.statusText}`);
        }
        return response.json();
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

export const apiService = {
    async getVideos(): Promise<Video[]> {
        return await fetchFromAPI('videos');
    },
    async getDownloads(): Promise<Download[]> {
        return await fetchFromAPI('downloads');
    },
    async startDownload(url: string): Promise<any> {
        return await fetchFromAPI('downloads', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });
    }
};