import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getDailyEntries, getStudents, createDailyEntry, updateDailyEntry, deleteDailyEntry } from "@/api/endpoints";
import { useToast } from "@/components/Toast";
import { formatDate } from "@/lib/utils";
import { Plus, Pencil, Trash2, X } from "lucide-react";
import type { DailyEntry } from "@/types";

type FormData = Omit<DailyEntry, "id">;
const emptyForm: FormData = { student: "", date: new Date().toISOString().slice(0, 10), subject: "Practical Life", activities: [], skill_level: "Developing", notes: "" };

const SUBJECTS = ["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science", "Social/Emotional"];
const SKILL_LEVELS = ["Introduced", "Developing", "Practicing", "Mastered"];

export default function DailyTracking() {
  const qc = useQueryClient();
  const { toast } = useToast();
  const { data: entries = [], isLoading } = useQuery({ queryKey: ["daily-entries"], queryFn: () => getDailyEntries().then((r) => r.data) });
  const { data: students = [] } = useQuery({ queryKey: ["students"], queryFn: () => getStudents().then((r) => r.data) });

  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<DailyEntry | null>(null);
  const [form, setForm] = useState<FormData>(emptyForm);
  const [activityInput, setActivityInput] = useState("");

  const createMut = useMutation({
    mutationFn: (data: FormData) => createDailyEntry(data),
    onSuccess: (_, vars) => { qc.invalidateQueries({ queryKey: ["daily-entries"] }); toast(`Entry for ${vars.student} saved!`); resetForm(); },
  });
  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: FormData }) => updateDailyEntry(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["daily-entries"] }); toast("Entry updated!"); resetForm(); },
  });
  const deleteMut = useMutation({
    mutationFn: (id: number) => deleteDailyEntry(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["daily-entries"] }); toast("Entry deleted"); },
  });

  function resetForm() { setForm(emptyForm); setShowForm(false); setEditing(null); setActivityInput(""); }

  function startEdit(e: DailyEntry) {
    setEditing(e);
    setForm({ student: e.student, date: e.date, subject: e.subject, activities: [...e.activities], skill_level: e.skill_level, notes: e.notes });
    setShowForm(true);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.student || form.activities.length === 0) return;
    if (editing) updateMut.mutate({ id: editing.id, data: form });
    else createMut.mutate(form);
  }

  if (isLoading) return <div className="flex justify-center py-20"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" /></div>;

  const skillColors: Record<string, string> = {
    Introduced: "bg-gray-100 text-gray-700",
    Developing: "bg-yellow-50 text-yellow-700",
    Practicing: "bg-blue-50 text-blue-700",
    Mastered: "bg-green-50 text-green-700",
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">📝 Daily Tracking</h1>
          <p className="text-sm text-muted-foreground">{entries.length} entries recorded</p>
        </div>
        <button onClick={() => { resetForm(); setShowForm(true); }} className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 cursor-pointer">
          <Plus size={16} /> New Entry
        </button>
      </div>

      {showForm && (
        <div className="bg-card border border-border rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4">{editing ? "Edit Entry" : "New Daily Entry"}</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Student *</label>
                <select value={form.student} onChange={(e) => setForm((f) => ({ ...f, student: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                  <option value="">Select student</option>
                  {students.map((s) => <option key={s.id} value={s.name}>{s.name}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Date</label>
                <input type="date" value={form.date} onChange={(e) => setForm((f) => ({ ...f, date: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Subject</label>
                <select value={form.subject} onChange={(e) => setForm((f) => ({ ...f, subject: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                  {SUBJECTS.map((s) => <option key={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Skill Level</label>
                <select value={form.skill_level} onChange={(e) => setForm((f) => ({ ...f, skill_level: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                  {SKILL_LEVELS.map((s) => <option key={s}>{s}</option>)}
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Activities *</label>
              <div className="flex gap-2 mb-2 flex-wrap">
                {form.activities.map((a, i) => (
                  <span key={i} className="flex items-center gap-1 px-2 py-1 bg-indigo-50 text-indigo-700 rounded-md text-xs">
                    {a} <button type="button" onClick={() => setForm((f) => ({ ...f, activities: f.activities.filter((_, j) => j !== i) }))} className="cursor-pointer"><X size={12} /></button>
                  </span>
                ))}
              </div>
              <input value={activityInput} onChange={(e) => setActivityInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); if (activityInput.trim()) { setForm((f) => ({ ...f, activities: [...f.activities, activityInput.trim()] })); setActivityInput(""); } } }} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="Add activity and press Enter" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Notes</label>
              <textarea value={form.notes} onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))} rows={3} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary resize-none" placeholder="Additional notes..." />
            </div>
            <div className="flex gap-3">
              <button type="submit" disabled={createMut.isPending || updateMut.isPending} className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 cursor-pointer">
                {editing ? "Update" : "Save Entry"}
              </button>
              <button type="button" onClick={resetForm} className="px-4 py-2 bg-secondary text-secondary-foreground rounded-lg text-sm font-medium hover:bg-accent cursor-pointer">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="space-y-3">
        {entries.slice().reverse().map((e) => (
          <div key={e.id} className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="font-semibold">{e.student}</h3>
                <p className="text-xs text-muted-foreground">{formatDate(e.date)} · {e.subject}</p>
              </div>
              <div className="flex items-center gap-2">
                <span className={`px-2 py-0.5 rounded-md text-xs ${skillColors[e.skill_level] ?? "bg-gray-100 text-gray-700"}`}>{e.skill_level}</span>
                <button onClick={() => startEdit(e)} className="p-1.5 rounded-md hover:bg-accent cursor-pointer"><Pencil size={14} /></button>
                <button onClick={() => deleteMut.mutate(e.id)} className="p-1.5 rounded-md hover:bg-red-50 text-destructive cursor-pointer"><Trash2 size={14} /></button>
              </div>
            </div>
            {e.activities.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-2">
                {e.activities.map((a) => <span key={a} className="px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded-md text-xs">{a}</span>)}
              </div>
            )}
            {e.notes && <p className="text-sm text-muted-foreground">{e.notes}</p>}
          </div>
        ))}
      </div>
    </div>
  );
}
