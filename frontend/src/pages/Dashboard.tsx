import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useAuth } from "@/context/AuthContext";
import { getStudents, getObservations, getDailyEntries, getSchedules, sendChat } from "@/api/endpoints";
import { getTimeGreeting, formatDate } from "@/lib/utils";
import { Users, Eye, ClipboardList, Package, Plus, MessageSquare, Send } from "lucide-react";
import { Link } from "react-router-dom";
import type { ChatMessage } from "@/types";

export default function Dashboard() {
  const { user } = useAuth();
  const { data: students } = useQuery({ queryKey: ["students"], queryFn: () => getStudents().then((r) => r.data) });
  const { data: observations } = useQuery({ queryKey: ["observations"], queryFn: () => getObservations().then((r) => r.data) });
  const { data: entries } = useQuery({ queryKey: ["daily-entries"], queryFn: () => getDailyEntries().then((r) => r.data) });
  const { data: schedules } = useQuery({ queryKey: ["schedules"], queryFn: () => getSchedules().then((r) => r.data) });

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);

  const today = new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", year: "numeric" });
  const dayName = new Date().toLocaleDateString("en-US", { weekday: "long" });
  const todaySchedule = schedules?.filter((s) => s.day === dayName) ?? [];

  const handleChat = async () => {
    if (!chatInput.trim() || chatLoading) return;
    const msg = chatInput.trim();
    setChatInput("");
    setMessages((prev) => [...prev, { role: "user", content: msg }]);
    setChatLoading(true);
    try {
      const res = await sendChat(msg);
      setMessages((prev) => [...prev, { role: "assistant", content: res.data.response }]);
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I couldn't process that request." }]);
    }
    setChatLoading(false);
  };

  const recentObs = observations?.slice(-5).reverse() ?? [];

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-linear-to-br from-indigo-500 to-purple-600 rounded-2xl p-8 text-white">
        <h1 className="text-3xl font-bold">Good {getTimeGreeting()}! 👋</h1>
        <p className="mt-1 opacity-80">{today}</p>
        <p className="mt-1 opacity-70">Welcome back, {user?.name}. Let's make today count!</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Students", value: students?.length ?? 0, icon: Users, color: "text-blue-600 bg-blue-50" },
          { label: "Observations", value: observations?.length ?? 0, icon: Eye, color: "text-green-600 bg-green-50" },
          { label: "Activities", value: entries?.length ?? 0, icon: ClipboardList, color: "text-orange-600 bg-orange-50" },
          { label: "Materials", value: schedules?.length ?? 0, icon: Package, color: "text-purple-600 bg-purple-50" },
        ].map((s) => (
          <div key={s.label} className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">{s.label}</p>
                <p className="text-2xl font-bold mt-1">{s.value}</p>
              </div>
              <div className={`p-3 rounded-lg ${s.color}`}>
                <s.icon size={20} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-lg font-semibold mb-3">⚡ Quick Actions</h2>
        <div className="grid grid-cols-4 gap-3">
          {[
            { to: "/students", label: "Add Student", icon: Plus },
            { to: "/observations", label: "New Observation", icon: Eye },
            { to: "/daily-tracking", label: "Log Activity", icon: ClipboardList },
            { to: "/reports", label: "View Reports", icon: MessageSquare },
          ].map((a) => (
            <Link
              key={a.to}
              to={a.to}
              className="flex items-center justify-center gap-2 py-3 bg-secondary text-secondary-foreground rounded-lg text-sm font-medium hover:bg-accent transition-colors"
            >
              <a.icon size={16} />
              {a.label}
            </Link>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Today's Schedule */}
        <div className="bg-card border border-border rounded-xl p-5">
          <h2 className="text-lg font-semibold mb-3">📅 Today's Schedule</h2>
          {todaySchedule.length === 0 ? (
            <p className="text-sm text-muted-foreground">No activities scheduled for today.</p>
          ) : (
            <div className="space-y-2">
              {todaySchedule.map((s) => (
                <div key={s.id} className="flex items-center justify-between py-2 border-b border-border last:border-0">
                  <div>
                    <span className="font-medium text-sm">{s.time}</span>
                    <span className="mx-2 text-muted-foreground">—</span>
                    <span className="text-sm">{s.activity}</span>
                  </div>
                  <span className="text-xs text-muted-foreground">{s.students}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Observations */}
        <div className="bg-card border border-border rounded-xl p-5">
          <h2 className="text-lg font-semibold mb-3">👁️ Recent Observations</h2>
          {recentObs.length === 0 ? (
            <p className="text-sm text-muted-foreground">No observations yet.</p>
          ) : (
            <div className="space-y-3">
              {recentObs.map((o) => (
                <div key={o.id} className="border-b border-border pb-2 last:border-0">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{o.student}</span>
                    <span className="text-muted-foreground">{formatDate(o.date)}</span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">{o.area} — {o.notes.slice(0, 80)}…</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Ask Monty */}
      <div className="bg-card border border-border rounded-xl p-5">
        <h2 className="text-lg font-semibold mb-3">🤖 Ask Monty</h2>
        <div className="max-h-60 overflow-y-auto space-y-3 mb-3">
          {messages.length === 0 && (
            <p className="text-sm text-muted-foreground">Ask about lesson plans, observations, materials, or student progress…</p>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[70%] px-3 py-2 rounded-lg text-sm ${
                  m.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted text-foreground"
                }`}
              >
                {m.content}
              </div>
            </div>
          ))}
          {chatLoading && (
            <div className="flex justify-start">
              <div className="bg-muted px-3 py-2 rounded-lg text-sm text-muted-foreground">Thinking…</div>
            </div>
          )}
        </div>
        <div className="flex gap-2">
          <input
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleChat()}
            placeholder="Ask Monty anything…"
            className="flex-1 px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <button
            onClick={handleChat}
            disabled={chatLoading}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 cursor-pointer"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
