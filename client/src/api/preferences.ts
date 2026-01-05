import { apiClient, type UserPreference } from './client';

export const getPreferences = async (): Promise<UserPreference[]> => {
    const response = await apiClient.get('/preferences/');
    return response.data;
};

export const createPreference = async (pref: UserPreference): Promise<UserPreference> => {
    const response = await apiClient.post('/preferences/', pref);
    return response.data;
};

export const getUserPreferences = async (userId: string): Promise<UserPreference[]> => {
    const response = await apiClient.get(`/preferences/${userId}`);
    return response.data;
};
