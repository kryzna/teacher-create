import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getSettings, updateSettings } from "@/api/endpoints";
import { useToast } from "@/components/Toast";
import { useAuth } from "@/context/AuthContext";

const TABS = ["Profile", "Classroom", "Notifications", "Privacy", "Appearance"] as const;
type Tab = typeof TABS[number];

export default function Settings() {
  const { user } = useAuth();
  const qc = useQueryClient();
  const { toast } = useToast();
  const { data, isLoading } = useQuery({ queryKey: ["settings"], queryFn: () => getSettings().then((r) => r.data.settings) });

  const [tab, setTab] = useState<Tab>("Profile");
  const [edits, setEdits] = useState<Record<string, Record<string, unknown>>>({});

  const merged: Record<string, Record<string, unknown>> = {};
  const base = (data as Record<string, Record<string, unknown>> | undefined) ?? {};
  for (const key of new Set([...Object.keys(base), ...Object.keys(edits)])) {
    merged[key] = { ...base[key], ...edits[key] };
  }

  const saveMut = useMutation({
    mutationFn: () => updateSettings(merged),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["settings"] }); setEdits({}); toast(`${tab} settings saved!`); },
  });

  function update(section: string, key: string, value: unknown) {
    setEdits((s) => ({ ...s, [section]: { ...s[section], [key]: value } }));
  }

  if (isLoading) return <div className="flex justify-center py-20"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" /></div>;

  const profile = merged.profile ?? {};
  const classroom = merged.classroom ?? {};
  const notifications = merged.notifications ?? {};
  const privacy = merged.privacy_security ?? {};
  const appearance = merged.appearance ?? {};

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">⚙️ Settings</h1>
        <p className="text-sm text-muted-foreground">Manage your account and preferences</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-muted p-1 rounded-lg w-fit">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer ${tab === t ? "bg-white shadow-sm text-foreground" : "text-muted-foreground hover:text-foreground"}`}
          >
            {t}
          </button>
        ))}
      </div>

      <div className="bg-card border border-border rounded-xl p-6">
        {tab === "Profile" && (
          <div className="space-y-4 max-w-lg">
            <h2 className="text-lg font-semibold">Profile Information</h2>
            <Field label="Name" value={String(profile.name ?? user?.name ?? "")} onChange={(v) => update("profile", "name", v)} />
            <Field label="Email" value={String(profile.email ?? user?.email ?? "")} onChange={(v) => update("profile", "email", v)} />
            <Field label="Phone" value={String(profile.phone ?? "")} onChange={(v) => update("profile", "phone", v)} />
            <div>
              <label className="block text-sm font-medium mb-1">Bio</label>
              <textarea value={String(profile.bio ?? "")} onChange={(e) => update("profile", "bio", e.target.value)} rows={3} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary resize-none" />
            </div>
          </div>
        )}

        {tab === "Classroom" && (
          <div className="space-y-4 max-w-lg">
            <h2 className="text-lg font-semibold">Classroom Settings</h2>
            <Field label="School Name" value={String(classroom.school_name ?? "")} onChange={(v) => update("classroom", "school_name", v)} />
            <Field label="Classroom Name" value={String(classroom.classroom_name ?? "")} onChange={(v) => update("classroom", "classroom_name", v)} />
            <Field label="Academic Year" value={String(classroom.academic_year ?? "")} onChange={(v) => update("classroom", "academic_year", v)} />
            <div>
              <label className="block text-sm font-medium mb-1">Max Students</label>
              <input type="number" value={Number(classroom.student_count ?? 18)} onChange={(e) => update("classroom", "student_count", Number(e.target.value))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
            </div>
          </div>
        )}

        {tab === "Notifications" && (
          <div className="space-y-4 max-w-lg">
            <h2 className="text-lg font-semibold">Notification Preferences</h2>
            <Toggle label="Email for observations" checked={Boolean(notifications.email_observations)} onChange={(v) => update("notifications", "email_observations", v)} />
            <Toggle label="Email for reports" checked={Boolean(notifications.email_reports)} onChange={(v) => update("notifications", "email_reports", v)} />
            <Toggle label="Email for parent communications" checked={Boolean(notifications.email_parent_communications)} onChange={(v) => update("notifications", "email_parent_communications", v)} />
            <Toggle label="Push for activities" checked={Boolean(notifications.push_activities)} onChange={(v) => update("notifications", "push_activities", v)} />
            <Toggle label="Push for schedule changes" checked={Boolean(notifications.push_schedule_changes)} onChange={(v) => update("notifications", "push_schedule_changes", v)} />
            <Toggle label="Weekly digest" checked={Boolean(notifications.weekly_digest)} onChange={(v) => update("notifications", "weekly_digest", v)} />
          </div>
        )}

        {tab === "Privacy" && (
          <div className="space-y-4 max-w-lg">
            <h2 className="text-lg font-semibold">Privacy & Security</h2>
            <Toggle label="Two-factor authentication" checked={Boolean(privacy.two_factor_auth)} onChange={(v) => update("privacy_security", "two_factor_auth", v)} />
            <Toggle label="Share progress with parents" checked={Boolean(privacy.share_progress_with_parents)} onChange={(v) => update("privacy_security", "share_progress_with_parents", v)} />
            <Toggle label="Analytics tracking" checked={Boolean(privacy.analytics_tracking)} onChange={(v) => update("privacy_security", "analytics_tracking", v)} />
            <div>
              <label className="block text-sm font-medium mb-1">Session Timeout (minutes)</label>
              <input type="number" value={Number(privacy.session_timeout ?? 30)} onChange={(e) => update("privacy_security", "session_timeout", Number(e.target.value))} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
            </div>
          </div>
        )}

        {tab === "Appearance" && (
          <div className="space-y-4 max-w-lg">
            <h2 className="text-lg font-semibold">Appearance</h2>
            <div>
              <label className="block text-sm font-medium mb-1">Theme</label>
              <select value={String(appearance.theme ?? "light")} onChange={(e) => update("appearance", "theme", e.target.value)} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                <option value="light">Light</option>
                <option value="dark">Dark</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Accent Color</label>
              <select value={String(appearance.accent_color ?? "Purple")} onChange={(e) => update("appearance", "accent_color", e.target.value)} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                {["Purple", "Blue", "Green", "Orange", "Red"].map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Font Size</label>
              <select value={String(appearance.font_size ?? "Medium")} onChange={(e) => update("appearance", "font_size", e.target.value)} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                {["Small", "Medium", "Large"].map((s) => <option key={s}>{s}</option>)}
              </select>
            </div>
            <Toggle label="Compact mode" checked={Boolean(appearance.compact_mode)} onChange={(v) => update("appearance", "compact_mode", v)} />
          </div>
        )}

        <div className="mt-6">
          <button onClick={() => saveMut.mutate()} disabled={saveMut.isPending} className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 cursor-pointer">
            {saveMut.isPending ? "Saving…" : "Save Settings"}
          </button>
        </div>
      </div>
    </div>
  );
}

function Field({ label, value, onChange }: { label: string; value: string; onChange: (v: string) => void }) {
  return (
    <div>
      <label className="block text-sm font-medium mb-1">{label}</label>
      <input value={value} onChange={(e) => onChange(e.target.value)} className="w-full px-3 py-2 border border-input rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
    </div>
  );
}

function Toggle({ label, checked, onChange }: { label: string; checked: boolean; onChange: (v: boolean) => void }) {
  return (
    <label className="flex items-center justify-between py-2 cursor-pointer">
      <span className="text-sm">{label}</span>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        onClick={() => onChange(!checked)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors cursor-pointer ${checked ? "bg-primary" : "bg-gray-200"}`}
      >
        <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${checked ? "translate-x-6" : "translate-x-1"}`} />
      </button>
    </label>
  );
}
