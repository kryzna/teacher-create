import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getMaterials, createMaterial, updateMaterial, recordMaterialUse, deleteMaterial } from "@/api/endpoints";
import { useToast } from "@/components/Toast";
import { Plus, Pencil, Trash2, Play } from "lucide-react";
import type { Material } from "@/types";

const CATEGORIES = ["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science"];
type CreateData = Omit<Material, "id" | "times_used">;
type UpdateData = Omit<Material, "id">;
const emptyForm: CreateData = { name: "", category: "Sensorial", age_range: "3-6", description: "", in_stock: true };

export default function Materials() {
  const qc = useQueryClient();
  const { toast } = useToast();
  const { data: materials = [], isLoading } = useQuery({ queryKey: ["materials"], queryFn: () => getMaterials().then((r) => r.data) });

  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Material | null>(null);
  const [form, setForm] = useState<CreateData>(emptyForm);

  const createMut = useMutation({
    mutationFn: (data: CreateData) => createMaterial(data),
    onSuccess: (_, vars) => { qc.invalidateQueries({ queryKey: ["materials"] }); toast(`Added ${vars.name} successfully!`); resetForm(); },
  });
  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateData }) => updateMaterial(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["materials"] }); toast("Material updated!"); resetForm(); },
  });
  const useMut = useMutation({
    mutationFn: (id: number) => recordMaterialUse(id),
    onSuccess: (_res, id) => { qc.invalidateQueries({ queryKey: ["materials"] }); const m = materials.find((x) => x.id === id); toast(`Recorded use of ${m?.name ?? "material"}`); },
  });
  const deleteMut = useMutation({
    mutationFn: (id: number) => deleteMaterial(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["materials"] }); toast("Material deleted"); },
  });

  function resetForm() { setForm(emptyForm); setShowForm(false); setEditing(null); }

  function startEdit(m: Material) {
    setEditing(m);
    setForm({ name: m.name, category: m.category, age_range: m.age_range, description: m.description, in_stock: m.in_stock });
    setShowForm(true);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.name) return;
    if (editing) {
      updateMut.mutate({ id: editing.id, data: { ...form, times_used: editing.times_used } });
    } else {
      createMut.mutate(form);
    }
  }

  if (isLoading) return <div className="flex justify-center py-20"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" /></div>;

  const categoryColors: Record<string, string> = {
    "Practical Life": "bg-amber-50 text-amber-700",
    "Sensorial": "bg-pink-50 text-pink-700",
    "Language": "bg-blue-50 text-blue-700",
    "Mathematics": "bg-green-50 text-green-700",
    "Art": "bg-purple-50 text-purple-700",
    "Science": "bg-teal-50 text-teal-700",
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">📦 Materials</h1>
          <p className="text-sm text-muted-foreground">{materials.length} materials in inventory</p>
        </div>
        <button onClick={() => { resetForm(); setShowForm(true); }} className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 cursor-pointer">
          <Plus size={16} /> Add Material
        </button>
      </div>

      {showForm && (
        <div className="bg-card border border-border rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4">{editing ? "Edit Material" : "Add Material"}</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Name *</label>
                <input value={form.name} onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="Material name" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Category</label>
                <select value={form.category} onChange={(e) => setForm((f) => ({ ...f, category: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                  {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Age Range</label>
                <input value={form.age_range} onChange={(e) => setForm((f) => ({ ...f, age_range: e.target.value }))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" placeholder="3-6" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Description</label>
              <textarea value={form.description} onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))} rows={3} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary resize-none" placeholder="Describe the material..." />
            </div>
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={form.in_stock} onChange={(e) => setForm((f) => ({ ...f, in_stock: e.target.checked }))} className="rounded" />
              In Stock
            </label>
            <div className="flex gap-3">
              <button type="submit" disabled={createMut.isPending || updateMut.isPending} className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 cursor-pointer">
                {editing ? "Update" : "Add Material"}
              </button>
              <button type="button" onClick={resetForm} className="px-4 py-2 bg-secondary text-secondary-foreground rounded-lg text-sm font-medium hover:bg-accent cursor-pointer">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {materials.map((m) => (
          <div key={m.id} className="bg-card border border-border rounded-xl p-5 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="font-semibold">{m.name}</h3>
                <span className={`inline-block px-2 py-0.5 rounded-md text-xs mt-1 ${categoryColors[m.category] ?? "bg-gray-50 text-gray-700"}`}>{m.category}</span>
              </div>
              <div className="flex gap-1">
                <button onClick={() => useMut.mutate(m.id)} className="p-1.5 rounded-md hover:bg-green-50 text-green-600 cursor-pointer" title="Record use"><Play size={14} /></button>
                <button onClick={() => startEdit(m)} className="p-1.5 rounded-md hover:bg-accent cursor-pointer"><Pencil size={14} /></button>
                <button onClick={() => deleteMut.mutate(m.id)} className="p-1.5 rounded-md hover:bg-red-50 text-destructive cursor-pointer"><Trash2 size={14} /></button>
              </div>
            </div>
            <p className="text-sm text-muted-foreground mb-2">{m.description}</p>
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span>Ages {m.age_range}</span>
              <span>Used {m.times_used}×</span>
              <span className={m.in_stock ? "text-green-600" : "text-red-600"}>{m.in_stock ? "In Stock" : "Out of Stock"}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
