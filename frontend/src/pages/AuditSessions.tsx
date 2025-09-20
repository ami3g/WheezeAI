import { useEffect, useState } from 'react';
import Header from '../components/Header';

type AuditSession = {
  id: number;
  name: string;
  status: string;
  created_at: string;
};

export default function AuditSessions() {
  const [sessions, setSessions] = useState<AuditSession[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [creating, setCreating] = useState(false);

  const fetchSessions = () => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }
    fetch('http://localhost:8000/audit_sessions/', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(res => res.json())
      .then(data => {
        setSessions(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load audit sessions');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    setError('');
    const token = localStorage.getItem('token');
    try {
      const res = await fetch('http://localhost:8000/audit_sessions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ name }),
      });
      if (res.ok) {
        setName('');
        fetchSessions();
      } else {
        const data = await res.json();
        setError(data.detail || 'Failed to create session');
      }
    } catch {
      setError('Network error');
    }
    setCreating(false);
  };

  return (
    <>
      <Header />
      <div className="audit-sessions-container">
        <h2>Audit Sessions</h2>
        <form onSubmit={handleCreate} style={{ margin: '2rem 0', display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <input
            type="text"
            placeholder="New session name"
            value={name}
            onChange={e => setName(e.target.value)}
            required
            style={{ padding: '0.5rem 1rem', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '1rem' }}
          />
          <button type="submit" disabled={creating} style={{ background: '#38bdf8', color: '#fff', border: 'none', borderRadius: '6px', padding: '0.5rem 1.5rem', fontWeight: 600, cursor: 'pointer' }}>
            {creating ? 'Creating...' : 'Create Session'}
          </button>
        </form>
        {loading ? (
          <div>Loading...</div>
        ) : error ? (
          <div className="error">{error}</div>
        ) : (
          <table style={{ width: '100%', marginTop: '2rem', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 8px rgba(30,41,59,0.08)' }}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Status</th>
                <th>Created At</th>
              </tr>
            </thead>
            <tbody>
              {sessions.map(session => (
                <tr key={session.id}>
                  <td>{session.id}</td>
                  <td>{session.name}</td>
                  <td>{session.status}</td>
                  <td>{new Date(session.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}
