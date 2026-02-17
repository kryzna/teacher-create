import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getObservations, getStudents, createObservation, updateObservation, deleteObservation } from "@/api/endpoints";
import { useToast } from "@/components/Toast";
import { formatDate } from "@/lib/utils";
import { Plus, Pencil, Trash2, X } from "lucide-react";
import type { Observation } from "@/types";

type FormData = Omit<Observation, "id">;
const emptyForm: FormData = { student: "", date: new Date().toISOString().slice(0, 10), area: "Practical Life", skills: [], notes: "" };

const AREAS = ["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science", "Social/Emotional"];

export default function Observations() {
  const qc = useQueryClient();
  const { toast } = useToast();
  const { data: observations = [], isLoading } = useQuery({ queryKey: ["observations"], queryFn: () => getObservations().then((r) => r.data) });
  const { data: students = [] } = useQuery({ queryKey: ["students"], queryFn: () => getStudents().then((r) => r.data) });

  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Observation | null>(null);
  const [form, setForm] = useState<FormData>(emptyForm);
  const [skillInput, setSkillInput] = useState("");

  const createMut = useMutation({
    mutationFn: (data: FormData) => createObservation(data),
    onSuccess: (_, vars) => { qc.invalidateQueries({ queryKey: ["observations"] }); toast(`Observation for ${vars.student} saved!`); resetForm(); },
  });
  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: FormData }) => updateObservation(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["observations"] }); toast("Observation updated!"); resetForm(); },
  });
  const deleteMut = useMutation({
    mutationFn: (id: number) => deleteObservation(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["observations"] }); toast("Observation deleted"); },
  });

  function resetForm() { setForm(emptyForm); setShowForm(false); setEditing(null); setSkillInput(""); }

  function startEdit(o: Observation) {
    setEditing(o);
    setForm({ student: o.student, date: o.date, area: o.area, skills: [...o.skills], notes: o.notes });
    setShowForm(true);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.student || !form.notes) return;
    if (editing) updateMut.mutate({ id: editing.id, data: form });
    else createMut.mutate(form);
  }

  if (isLoading) return <div className="flex justify-center py-20"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" /></div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">👁️ Observations</h1>
          <p className="text-sm text-muted-foreground">{observations.length} observations recorded</p>
        </div>
        <button onClick={() => { resetForm(); setShowForm(true); }} className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 cursor-pointer">
          <Plus size={16} /> New Observation
        </button>
      </div>

      {showForm && (
        <div className="bg-card border border-border rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4">{editing ? "Edit Observation" : "New Observation"}</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-3 gap-4">
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
              <div>
                <label className="block text-sm font-medium mb-1">Area</label>
                <select value={form.area} onChange={(e) => setForm((f) => ({ ...f, area: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                  {AREAS.map((a) => <option key={a}>{a}</option>)}
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Skills</label>
              <div className="flex gap-2 mb-2 flex-wrap">
                {form.skills.map((s, i) => (
                  <span key={i} className="flex items-center gap-1 px-2 py-1 bg-green-50 text-green-700 rounded-md text-xs">
                    {s} <button type="button" onClick={() => setForm((f) => ({ ...f, skills: f.skills.filter((_, j) => j !== i) }))} className="cursor-pointer"><X size={12} /></button>
                  </span>
                ))}
              </div>
              <input value={skillInput} onChange={(e) => setSkillInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); if (skillInput.trim()) { setForm((f) => ({ ...f, skills: [...f.skills, skillInput.trim()] })); setSkillInput(""); } } }} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="Add skill and press Enter" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Notes *</label>
              <textarea value={form.notes} onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))} rows={4} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary resize-none" placeholder="Describe the observation..." />
            </div>
            <div className="flex gap-3">
              <button type="submit" disabled={createMut.isPending || updateMut.isPending} className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 cursor-pointer">
                {editing ? "Update" : "Save Observation"}
              </button>
              <button type="button" onClick={resetForm} className="px-4 py-2 bg-secondary text-secondary-foreground rounded-lg text-sm font-medium hover:bg-accent cursor-pointer">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="space-y-3">
        {observations.slice().reverse().map((o) => (
          <div key={o.id} className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="font-semibold">{o.student}</h3>
                <p className="text-xs text-muted-foreground">{formatDate(o.date)} · {o.area}</p>
              </div>
              <div className="flex gap-1">
                <button onClick={() => startEdit(o)} className="p-1.5 rounded-md hover:bg-accent cursor-pointer"><Pencil size={14} /></button>
                <button onClick={() => deleteMut.mutate(o.id)} className="p-1.5 rounded-md hover:bg-red-50 text-destructive cursor-pointer"><Trash2 size={14} /></button>
              </div>
            </div>
            {o.skills.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-2">
                {o.skills.map((s) => <span key={s} className="px-2 py-0.5 bg-green-50 text-green-700 rounded-md text-xs">{s}</span>)}
              </div>
            )}
            <p className="text-sm text-muted-foreground">{o.notes}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
