import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface UserPreference {
    id?: number;
    user_id: string;
    channel: string;
    enabled: boolean;
    destination: string;
}

export interface NotificationLog {
    id: number;
    user_id: string;
    channel: string;
    destination: string;
    content: string;
    status: string;
    error_message?: string;
    created_at: string;
}

export interface EventCreate {
    event_type: string;
    user_id: string;
    payload: Record<string, any>;
}
