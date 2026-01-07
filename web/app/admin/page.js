"use client";
import { useEffect, useState } from 'react';
import io from 'socket.io-client';

let socket;

export default function AdminDashboard() {
    const [buses, setBuses] = useState([]);
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        socket = io('http://localhost:4000');

        socket.emit('request_buses');

        socket.on('bus_update', (data) => {
            setBuses(data);
        });

        socket.on('geofence_alert', (alert) => {
            setAlerts(prev => [alert, ...prev].slice(0, 10)); // Keep last 10
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    return (
        <main style={{ padding: 40, maxWidth: 1200, margin: '0 auto' }}>
            <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: 20 }}>🛠️ Admin Dashboard</h1>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>

                {/* Active Fleet */}
                <div className="glass-panel">
                    <h2>Active Fleet</h2>
                    <table style={{ width: '100%', marginTop: 10, borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ textAlign: 'left', color: '#aaa', fontSize: 13 }}>
                                <th>Bus ID</th>
                                <th>Route</th>
                                <th>Speed</th>
                                <th>Last Loc</th>
                            </tr>
                        </thead>
                        <tbody>
                            {buses.map(bus => (
                                <tr key={bus.id} style={{ borderBottom: '1px solid #333' }}>
                                    <td style={{ padding: '10px 0' }}>{bus.busId}</td>
                                    <td>{bus.routeId}</td>
                                    <td style={{ color: bus.speed > 0 ? '#00ff88' : '#666' }}>
                                        {bus.speed.toFixed(1)} km/h
                                    </td>
                                    <td style={{ fontSize: 12, fontFamily: 'monospace' }}>
                                        {bus.lat.toFixed(4)}, {bus.lon.toFixed(4)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {buses.length === 0 && <p style={{ color: '#666', marginTop: 10 }}>No buses active.</p>}
                </div>

                {/* Geofence Alerts */}
                <div className="glass-panel">
                    <h2>📢 Live Geofence Alerts</h2>
                    <div style={{ marginTop: 15 }}>
                        {alerts.map((alert, i) => (
                            <div key={i} style={{
                                padding: 10,
                                marginBottom: 8,
                                borderRadius: 6,
                                background: 'rgba(255,165,0,0.1)',
                                borderLeft: '4px solid orange'
                            }}>
                                <div style={{ fontWeight: 'bold', color: 'orange' }}>Geofence Entry</div>
                                <div>{alert.message}</div>
                                <div style={{ fontSize: 10, color: '#888', marginTop: 5 }}>
                                    {new Date(alert.timestamp).toLocaleTimeString()}
                                </div>
                            </div>
                        ))}
                        {alerts.length === 0 && <p style={{ color: '#666' }}>No active alerts.</p>}
                    </div>
                </div>

            </div>
        </main>
    );
}
