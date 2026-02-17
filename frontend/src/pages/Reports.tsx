import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getStudents, getObservations, getDailyEntries } from "@/api/endpoints";
import { formatDate } from "@/lib/utils";

export default function Reports() {
  const { data: students = [] } = useQuery({ queryKey: ["students"], queryFn: () => getStudents().then((r) => r.data) });
  const { data: observations = [] } = useQuery({ queryKey: ["observations"], queryFn: () => getObservations().then((r) => r.data) });
  const { data: entries = [] } = useQuery({ queryKey: ["daily-entries"], queryFn: () => getDailyEntries().then((r) => r.data) });

  const [selectedId, setSelectedId] = useState<number | null>(null);
  const selected = students.find((s) => s.id === selectedId);

  const studentObs = selected ? observations.filter((o) => o.student === selected.name) : [];
  const studentEntries = selected ? entries.filter((e) => e.student === selected.name) : [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">📊 Student Reports</h1>
        <p className="text-sm text-muted-foreground">Select a student to view their progress report</p>
      </div>

      <div className="grid grid-cols-4 gap-6">
        {/* Student List */}
        <div className="col-span-1 space-y-2">
          {students.map((s) => (
            <button
              key={s.id}
              onClick={() => setSelectedId(s.id)}
              className={`w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-colors cursor-pointer ${
                selectedId === s.id ? "bg-primary text-primary-foreground" : "bg-card border border-border hover:bg-accent"
              }`}
            >
              {s.name}
              <span className="block text-xs opacity-70">Age {s.age}</span>
            </button>
          ))}
        </div>

        {/* Report */}
        <div className="col-span-3">
          {!selected ? (
            <div className="bg-card border border-border rounded-xl p-10 text-center text-muted-foreground">
              <p className="text-lg">Select a student to view their report</p>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Student Header */}
              <div className="bg-card border border-border rounded-xl p-6">
                <h2 className="text-xl font-bold">{selected.name}</h2>
                <div className="grid grid-cols-3 gap-4 mt-3 text-sm">
                  <div><span className="text-muted-foreground">Age:</span> {selected.age}</div>
                  <div><span className="text-muted-foreground">Parent:</span> {selected.parent_name}</div>
                  <div><span className="text-muted-foreground">Email:</span> {selected.parent_email}</div>
                </div>
                {selected.interests.length > 0 && (
                  <div className="flex gap-1 mt-3">
                    {selected.interests.map((i) => <span key={i} className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded-md text-xs">{i}</span>)}
                  </div>
                )}
                {selected.allergies.length > 0 && (
                  <div className="flex gap-1 mt-2">
                    {selected.allergies.map((a) => <span key={a} className="px-2 py-0.5 bg-red-50 text-red-700 rounded-md text-xs">⚠️ {a}</span>)}
                  </div>
                )}
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-card border border-border rounded-xl p-4 text-center">
                  <p className="text-2xl font-bold">{studentObs.length}</p>
                  <p className="text-sm text-muted-foreground">Observations</p>
                </div>
                <div className="bg-card border border-border rounded-xl p-4 text-center">
                  <p className="text-2xl font-bold">{studentEntries.length}</p>
                  <p className="text-sm text-muted-foreground">Daily Entries</p>
                </div>
                <div className="bg-card border border-border rounded-xl p-4 text-center">
                  <p className="text-2xl font-bold">{new Set(studentObs.map((o) => o.area)).size}</p>
                  <p className="text-sm text-muted-foreground">Areas Covered</p>
                </div>
              </div>

              {/* Observations */}
              <div className="bg-card border border-border rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-3">Observations</h3>
                {studentObs.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No observations recorded yet.</p>
                ) : (
                  <div className="space-y-3">
                    {studentObs.map((o) => (
                      <div key={o.id} className="border-b border-border pb-3 last:border-0">
                        <div className="flex justify-between text-sm">
                          <span className="font-medium">{o.area}</span>
                          <span className="text-muted-foreground">{formatDate(o.date)}</span>
                        </div>
                        {o.skills.length > 0 && (
                          <div className="flex gap-1 mt-1">
                            {o.skills.map((s) => <span key={s} className="px-2 py-0.5 bg-green-50 text-green-700 rounded-md text-xs">{s}</span>)}
                          </div>
                        )}
                        <p className="text-sm text-muted-foreground mt-1">{o.notes}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Daily Entries */}
              <div className="bg-card border border-border rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-3">Daily Entries</h3>
                {studentEntries.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No daily entries recorded yet.</p>
                ) : (
                  <div className="space-y-3">
                    {studentEntries.map((e) => (
                      <div key={e.id} className="border-b border-border pb-3 last:border-0">
                        <div className="flex justify-between text-sm">
                          <span className="font-medium">{e.subject}</span>
                          <span className="text-muted-foreground">{formatDate(e.date)}</span>
                        </div>
                        <div className="flex gap-1 mt-1">
                          <span className="px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded-md text-xs">{e.skill_level}</span>
                          {e.activities.map((a) => <span key={a} className="px-2 py-0.5 bg-gray-100 text-gray-700 rounded-md text-xs">{a}</span>)}
                        </div>
                        {e.notes && <p className="text-sm text-muted-foreground mt-1">{e.notes}</p>}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
