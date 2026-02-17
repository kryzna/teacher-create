import { useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";

export default function Login() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/" replace />;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    const ok = await login(username, password);
    setLoading(false);
    if (ok) {
      navigate("/");
    } else {
      setError("Invalid credentials. Try demo / demo");
    }
  };

  const handleDemoLogin = async () => {
    setError("");
    setLoading(true);
    const ok = await login("demo", "demo");
    setLoading(false);
    if (ok) navigate("/");
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-linear-to-br from-indigo-900 to-teal-700 px-4">
      <div className="text-center mb-8">
        <h1 className="text-5xl font-bold text-white mb-3">Meet Monty</h1>
        <p className="text-xl text-white/80">Your AI-powered Montessori Teaching Assistant</p>
      </div>

      <div className="w-full max-w-sm bg-white rounded-2xl shadow-2xl p-8">
        <h2 className="text-2xl font-bold text-center text-foreground mb-6">Welcome Back</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-1">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          {error && (
            <p className="text-sm text-destructive bg-red-50 px-3 py-2 rounded-lg">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-primary text-primary-foreground rounded-lg font-medium text-sm hover:opacity-90 transition-opacity disabled:opacity-50 cursor-pointer"
          >
            {loading ? "Signing in…" : "Sign In"}
          </button>
        </form>

        <div className="my-4 border-t border-border" />

        <button
          onClick={handleDemoLogin}
          disabled={loading}
          className="w-full py-2.5 bg-secondary text-secondary-foreground rounded-lg font-medium text-sm hover:bg-accent transition-colors cursor-pointer"
        >
          👤 Login as Demo User
        </button>

        <p className="text-xs text-muted-foreground text-center mt-3">
          Demo: username <code className="bg-muted px-1 rounded">demo</code>, password{" "}
          <code className="bg-muted px-1 rounded">demo</code>
        </p>
      </div>

      <div className="grid grid-cols-3 gap-4 mt-10 max-w-2xl w-full">
        {[
          { icon: "📋", title: "Smart Planning", desc: "AI-generated lesson plans tailored to each student" },
          { icon: "👁️", title: "Observation Tracking", desc: "Record and analyze student observations with insights" },
          { icon: "📊", title: "Progress Reports", desc: "Beautiful newsletters and progress reports in seconds" },
        ].map((f) => (
          <div key={f.title} className="bg-white/10 backdrop-blur rounded-xl p-5 text-center text-white">
            <div className="text-3xl mb-2">{f.icon}</div>
            <h3 className="font-semibold mb-1">{f.title}</h3>
            <p className="text-sm text-white/70">{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
