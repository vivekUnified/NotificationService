import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getPreferences, createPreference } from '../api/preferences';

export const Settings = () => {
    const queryClient = useQueryClient();
    const { data: prefs, isLoading } = useQuery({ queryKey: ['prefs'], queryFn: getPreferences });

    const [userId, setUserId] = useState('');
    const [channel, setChannel] = useState('email');
    const [destination, setDestination] = useState('');

    const mutation = useMutation({
        mutationFn: createPreference,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['prefs'] });
            alert('Preference Saved!');
        },
        onError: () => {
            alert('Error saving preference');
        }
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        mutation.mutate({ user_id: userId, channel, destination, enabled: true });
    };

    if (isLoading) return <div>Loading...</div>;

    return (
        <div>
            <h1>User Preferences</h1>
            <div className="card">
                <h2>Add New Preference</h2>
                <form onSubmit={handleSubmit} style={{ maxWidth: '400px' }}>
                    <div>
                        <label>User ID</label>
                        <input className="input" value={userId} onChange={e => setUserId(e.target.value)} required />
                    </div>
                    <div>
                        <label>Channel</label>
                        <select className="input" value={channel} onChange={e => setChannel(e.target.value)}>
                            <option value="email">Email</option>
                            <option value="slack">Slack</option>
                            <option value="in_app">In-App</option>
                            <option value="teams">Teams</option>
                        </select>
                    </div>
                    <div>
                        <label>Destination</label>
                        <input className="input" value={destination} onChange={e => setDestination(e.target.value)} required placeholder="user@example.com or #channel" />
                    </div>
                    <button type="submit" className="btn" disabled={mutation.isPending}>
                        {mutation.isPending ? 'Saving...' : 'Save Preference'}
                    </button>
                </form>
            </div>

            <div className="card">
                <h2>Existing Preferences</h2>
                <table className="table">
                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Channel</th>
                            <th>Destination</th>
                            <th>Enabled</th>
                        </tr>
                    </thead>
                    <tbody>
                        {prefs?.map((p) => (
                            <tr key={p.id}>
                                <td>{p.user_id}</td>
                                <td>{p.channel}</td>
                                <td>{p.destination}</td>
                                <td>{p.enabled ? 'Yes' : 'No'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
