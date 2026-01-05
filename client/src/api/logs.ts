import { apiClient, type NotificationLog } from './client';

export const getLogs = async (): Promise<NotificationLog[]> => {
    const response = await apiClient.get('/notifications/');
    return response.data;
};
