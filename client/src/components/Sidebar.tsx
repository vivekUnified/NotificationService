import { NavLink } from 'react-router-dom';
import { Home, List, Settings, Bell } from 'lucide-react';

export const Sidebar = () => {
    return (
        <div className="sidebar">
            <div className="sidebar-title">
                <Bell size={24} />
                <span>NotifyService</span>
            </div>
            <nav>
                <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <Home size={20} />
                    Dashboard
                </NavLink>
                <NavLink to="/logs" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <List size={20} />
                    Logs
                </NavLink>
                <NavLink to="/settings" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <Settings size={20} />
                    Settings
                </NavLink>
            </nav>
        </div>
    );
};
