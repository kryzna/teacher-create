import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getStudents, createStudent, updateStudent, deleteStudent } from "@/api/endpoints";
import { useToast } from "@/components/Toast";
import { Plus, Pencil, Trash2, X } from "lucide-react";
import type { Student } from "@/types";

type FormData = Omit<Student, "id">;
const emptyForm: FormData = { name: "", age: 3, interests: [], allergies: [], parent_name: "", parent_email: "" };

export default function Students() {
  const qc = useQueryClient();
  const { toast } = useToast();
  const { data: students = [], isLoading } = useQuery({ queryKey: ["students"], queryFn: () => getStudents().then((r) => r.data) });

  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Student | null>(null);
  const [form, setForm] = useState<FormData>(emptyForm);
  const [interestInput, setInterestInput] = useState("");
  const [allergyInput, setAllergyInput] = useState("");

  const createMut = useMutation({
    mutationFn: (data: FormData) => createStudent(data),
    onSuccess: (_, vars) => { qc.invalidateQueries({ queryKey: ["students"] }); toast(`Added ${vars.name} successfully!`); resetForm(); },
  });

  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: FormData }) => updateStudent(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["students"] }); toast("Student updated successfully!"); resetForm(); },
  });

  const deleteMut = useMutation({
    mutationFn: (id: number) => deleteStudent(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["students"] }); toast("Student deleted"); },
  });

  function resetForm() {
    setForm(emptyForm);
    setShowForm(false);
    setEditing(null);
    setInterestInput("");
    setAllergyInput("");
  }

  function startEdit(s: Student) {
    setEditing(s);
    setForm({ name: s.name, age: s.age, interests: [...s.interests], allergies: [...s.allergies], parent_name: s.parent_name, parent_email: s.parent_email });
    setShowForm(true);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.name) return;
    if (editing) {
      updateMut.mutate({ id: editing.id, data: form });
    } else {
      createMut.mutate(form);
    }
  }

  function addTag(type: "interests" | "allergies", value: string) {
    if (!value.trim()) return;
    setForm((f) => ({ ...f, [type]: [...f[type], value.trim()] }));
    if (type === "interests") setInterestInput("");
    else setAllergyInput("");
  }

  function removeTag(type: "interests" | "allergies", idx: number) {
    setForm((f) => ({ ...f, [type]: f[type].filter((_, i) => i !== idx) }));
  }

  if (isLoading) return <div className="flex justify-center py-20"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" /></div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">👨‍🎓 Student Management</h1>
          <p className="text-sm text-muted-foreground">{students.length} students enrolled</p>
        </div>
        <button onClick={() => { resetForm(); setShowForm(true); }} className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition-opacity cursor-pointer">
          <Plus size={16} /> Add Student
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <div className="bg-card border border-border rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4">{editing ? "Edit Student" : "Add New Student"}</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Name *</label>
                <input value={form.name} onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="Student name" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Age *</label>
                <input type="number" min={2} max={12} value={form.age} onChange={(e) => setForm((f) => ({ ...f, age: Number(e.target.value) }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Parent Name</label>
                <input value={form.parent_name} onChange={(e) => setForm((f) => ({ ...f, parent_name: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="Parent name" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Parent Email</label>
                <input type="email" value={form.parent_email} onChange={(e) => setForm((f) => ({ ...f, parent_email: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="parent@email.com" />
              </div>
            </div>

            {/* Interests */}
            <div>
              <label className="block text-sm font-medium mb-1">Interests</label>
              <div className="flex gap-2 mb-2 flex-wrap">
                {form.interests.map((t, i) => (
                  <span key={i} className="flex items-center gap-1 px-2 py-1 bg-blue-50 text-blue-700 rounded-md text-xs">
                    {t} <button type="button" onClick={() => removeTag("interests", i)} className="cursor-pointer"><X size={12} /></button>
                  </span>
                ))}
              </div>
              <div className="flex gap-2">
                <input value={interestInput} onChange={(e) => setInterestInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addTag("interests", interestInput); } }} className="flex-1 px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="Add interest and press Enter" />
              </div>
            </div>

            {/* Allergies */}
            <div>
              <label className="block text-sm font-medium mb-1">Allergies</label>
              <div className="flex gap-2 mb-2 flex-wrap">
                {form.allergies.map((t, i) => (
                  <span key={i} className="flex items-center gap-1 px-2 py-1 bg-red-50 text-red-700 rounded-md text-xs">
                    {t} <button type="button" onClick={() => removeTag("allergies", i)} className="cursor-pointer"><X size={12} /></button>
                  </span>
                ))}
              </div>
              <div className="flex gap-2">
                <input value={allergyInput} onChange={(e) => setAllergyInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addTag("allergies", allergyInput); } }} className="flex-1 px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="Add allergy and press Enter" />
              </div>
            </div>

            <div className="flex gap-3">
              <button type="submit" disabled={createMut.isPending || updateMut.isPending} className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 cursor-pointer">
                {editing ? "Update Student" : "Add Student"}
              </button>
              <button type="button" onClick={resetForm} className="px-4 py-2 bg-secondary text-secondary-foreground rounded-lg text-sm font-medium hover:bg-accent cursor-pointer">
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Student Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {students.map((s) => (
          <div key={s.id} className="bg-card border border-border rounded-xl p-5 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="font-semibold">{s.name}</h3>
                <p className="text-sm text-muted-foreground">Age: {s.age}</p>
              </div>
              <div className="flex gap-1">
                <button onClick={() => startEdit(s)} className="p-1.5 rounded-md hover:bg-accent transition-colors cursor-pointer"><Pencil size={14} /></button>
                <button onClick={() => deleteMut.mutate(s.id)} className="p-1.5 rounded-md hover:bg-red-50 text-destructive transition-colors cursor-pointer"><Trash2 size={14} /></button>
              </div>
            </div>
            {s.interests.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-2">
                {s.interests.map((t) => (
                  <span key={t} className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded-md text-xs">{t}</span>
                ))}
              </div>
            )}
            {s.allergies.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-2">
                {s.allergies.map((t) => (
                  <span key={t} className="px-2 py-0.5 bg-red-50 text-red-700 rounded-md text-xs">⚠️ {t}</span>
                ))}
              </div>
            )}
            {s.parent_name && (
              <p className="text-xs text-muted-foreground mt-2">Parent: {s.parent_name} ({s.parent_email})</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
