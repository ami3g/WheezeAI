import { useEffect, useState } from "react";
import Header from '../components/Header';

type User = {
  id: number;
  name: string;
  role: string;
};

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/login";
      return;
    }
    fetch("http://localhost:8000/users/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(res => res.json())
      .then(data => {
        if (data.id) setUser(data);
        else setError("Failed to load user");
      })
      .catch(() => setError("Network error"));
  }, []);

  if (error) return <div className="error">{error}</div>;
  if (!user) return <div>Loading...</div>;

  return (
    <>
      <Header />
      <div className="dashboard-container">
        <h2>Welcome, {user.name}</h2>
        <p>Role: {user.role}</p>
        <div className="dashboard-links">
          <a href="/organization">Organization</a>
          <a href="/audit-sessions">Audit Sessions</a>
          <a href="/reporting">Reporting</a>
        </div>
      </div>
    </>
  );
}
