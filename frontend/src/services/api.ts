import { Video } from '@/lib/types';

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
    }
};