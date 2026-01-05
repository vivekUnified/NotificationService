import { apiClient, type EventCreate } from './client';

export const createEvent = async (event: EventCreate): Promise<any> => {
    const response = await apiClient.post('/events/', event);
    return response.data;
};
