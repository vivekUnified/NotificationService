import { useQuery } from '@tanstack/react-query';
import { getLogs } from '../api/logs';
import { getPreferences } from '../api/preferences';

export const Dashboard = () => {
    const { data: logs } = useQuery({ queryKey: ['logs'], queryFn: getLogs });
    const { data: prefs } = useQuery({ queryKey: ['prefs'], queryFn: getPreferences });

    const totalSent = logs?.filter(l => l.status === 'sent').length || 0;
    const totalFailed = logs?.filter(l => l.status === 'failed').length || 0;

    return (
        <div>
            <h1>Dashboard Overview</h1>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
                <div className="card">
                    <h3>Total Notifications</h3>
                    <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{logs?.length || 0}</p>
                </div>
                <div className="card">
                    <h3>Successful Deliveries</h3>
                    <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#059669' }}>{totalSent}</p>
                </div>
                <div className="card">
                    <h3>Failed Deliveries</h3>
                    <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#dc2626' }}>{totalFailed}</p>
                </div>
                <div className="card">
                    <h3>Active Preferences</h3>
                    <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{prefs?.length || 0}</p>
                </div>
            </div>
        </div>
    );
};
