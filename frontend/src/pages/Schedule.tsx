import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getSchedules, createSchedule, updateSchedule, deleteSchedule } from "@/api/endpoints";
import { useToast } from "@/components/Toast";
import { Plus, Pencil, Trash2 } from "lucide-react";
import type { Schedule } from "@/types";

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
type FormData = Omit<Schedule, "id">;
const emptyForm: FormData = { day: "Monday", time: "9:00 AM", activity: "", duration: 30, students: "All" };

export default function SchedulePage() {
  const qc = useQueryClient();
  const { toast } = useToast();
  const { data: schedules = [], isLoading } = useQuery({ queryKey: ["schedules"], queryFn: () => getSchedules().then((r) => r.data) });

  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Schedule | null>(null);
  const [form, setForm] = useState<FormData>(emptyForm);

  const createMut = useMutation({
    mutationFn: (data: FormData) => createSchedule(data),
    onSuccess: (_, vars) => { qc.invalidateQueries({ queryKey: ["schedules"] }); toast(`Added ${vars.activity} successfully!`); resetForm(); },
  });
  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: FormData }) => updateSchedule(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["schedules"] }); toast("Activity updated!"); resetForm(); },
  });
  const deleteMut = useMutation({
    mutationFn: (id: number) => deleteSchedule(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["schedules"] }); toast("Activity deleted"); },
  });

  function resetForm() { setForm(emptyForm); setShowForm(false); setEditing(null); }

  function startEdit(s: Schedule) {
    setEditing(s);
    setForm({ day: s.day, time: s.time, activity: s.activity, duration: s.duration, students: s.students });
    setShowForm(true);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.activity) return;
    if (editing) updateMut.mutate({ id: editing.id, data: form });
    else createMut.mutate(form);
  }

  if (isLoading) return <div className="flex justify-center py-20"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" /></div>;

  const grouped = DAYS.reduce<Record<string, Schedule[]>>((acc, day) => {
    acc[day] = schedules.filter((s) => s.day === day).sort((a, b) => a.time.localeCompare(b.time));
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">📅 Weekly Schedule</h1>
          <p className="text-sm text-muted-foreground">{schedules.length} activities scheduled</p>
        </div>
        <button onClick={() => { resetForm(); setShowForm(true); }} className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 cursor-pointer">
          <Plus size={16} /> Add Activity
        </button>
      </div>

      {showForm && (
        <div className="bg-card border border-border rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4">{editing ? "Edit Activity" : "Add Activity"}</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Day</label>
                <select value={form.day} onChange={(e) => setForm((f) => ({ ...f, day: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                  {DAYS.map((d) => <option key={d}>{d}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Time</label>
                <input value={form.time} onChange={(e) => setForm((f) => ({ ...f, time: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="9:00 AM" />
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Activity *</label>
                <input value={form.activity} onChange={(e) => setForm((f) => ({ ...f, activity: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="Activity name" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Duration (min)</label>
                <input type="number" min={5} value={form.duration} onChange={(e) => setForm((f) => ({ ...f, duration: Number(e.target.value) }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Students</label>
                <input value={form.students} onChange={(e) => setForm((f) => ({ ...f, students: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="All" />
              </div>
            </div>
            <div className="flex gap-3">
              <button type="submit" disabled={createMut.isPending || updateMut.isPending} className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 cursor-pointer">
                {editing ? "Update" : "Add Activity"}
              </button>
              <button type="button" onClick={resetForm} className="px-4 py-2 bg-secondary text-secondary-foreground rounded-lg text-sm font-medium hover:bg-accent cursor-pointer">Cancel</button>
            </div>
          </form>
        </div>
      )}

      {DAYS.map((day) => (
        <div key={day}>
          <h3 className="text-md font-semibold mb-2">{day}</h3>
          {grouped[day].length === 0 ? (
            <p className="text-sm text-muted-foreground mb-4">No activities</p>
          ) : (
            <div className="space-y-2 mb-4">
              {grouped[day].map((s) => (
                <div key={s.id} className="flex items-center justify-between bg-card border border-border rounded-lg px-4 py-3">
                  <div className="flex items-center gap-4">
                    <span className="text-sm font-medium w-20">{s.time}</span>
                    <span className="text-sm">{s.activity}</span>
                    <span className="text-xs text-muted-foreground">{s.duration} min</span>
                    <span className="text-xs bg-secondary px-2 py-0.5 rounded">{s.students}</span>
                  </div>
                  <div className="flex gap-1">
                    <button onClick={() => startEdit(s)} className="p-1.5 rounded-md hover:bg-accent cursor-pointer"><Pencil size={14} /></button>
                    <button onClick={() => deleteMut.mutate(s.id)} className="p-1.5 rounded-md hover:bg-red-50 text-destructive cursor-pointer"><Trash2 size={14} /></button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
