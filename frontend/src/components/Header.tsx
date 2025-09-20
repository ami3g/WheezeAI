import './Header.css';

export default function Header() {
  return (
    <header className="header">
      <div className="logo">WheezeAI Audit</div>
      <nav className="nav">
        <a href="/dashboard">Dashboard</a>
        <a href="/organization">Organization</a>
        <a href="/audit-sessions">Audit Sessions</a>
        <a href="/reporting">Reporting</a>
        <button className="logout-btn" onClick={() => {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }}>Logout</button>
      </nav>
    </header>
  );
}
