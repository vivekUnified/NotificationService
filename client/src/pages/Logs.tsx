import { useQuery } from '@tanstack/react-query';
import { getLogs } from '../api/logs';

export const Logs = () => {
    const { data: logs, isLoading, error } = useQuery({ queryKey: ['logs'], queryFn: getLogs });

    if (isLoading) return <div>Loading logs...</div>;
    if (error) return <div>Error loading logs</div>;

    return (
        <div>
            <h1>Notification Logs</h1>
            <div className="card">
                <table className="table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>User ID</th>
                            <th>Channel</th>
                            <th>Status</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        {logs?.map((log) => (
                            <tr key={log.id}>
                                <td>{new Date(log.created_at).toLocaleString()}</td>
                                <td>{log.user_id}</td>
                                <td>{log.channel}</td>
                                <td>
                                    <span className={`badge ${log.status === 'sent' ? 'badge-sent' : 'badge-failed'}`}>
                                        {log.status}
                                    </span>
                                </td>
                                <td>
                                    {log.error_message ? (
                                        <span style={{ color: 'red' }}>{log.error_message}</span>
                                    ) : (
                                        <span style={{ color: 'gray' }}>{log.destination}</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
