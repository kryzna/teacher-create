import client from "./client";
import type {
  User,
  Student,
  Observation,
  Schedule,
  Material,
  DailyEntry,
  Settings,
} from "@/types";

// Auth
export const login = (username: string, password: string) =>
  client.post<{ access_token: string; token_type: string }>("/api/auth/login", { username, password });

export const getMe = () => client.get<User>("/api/auth/me");

// Students
export const getStudents = () => client.get<Student[]>("/api/students");
export const createStudent = (data: Omit<Student, "id">) =>
  client.post<Student>("/api/students", data);
export const updateStudent = (id: number, data: Omit<Student, "id">) =>
  client.put<Student>(`/api/students/${id}`, data);
export const deleteStudent = (id: number) =>
  client.delete(`/api/students/${id}`);

// Observations
export const getObservations = () => client.get<Observation[]>("/api/observations");
export const createObservation = (data: Omit<Observation, "id">) =>
  client.post<Observation>("/api/observations", data);
export const updateObservation = (id: number, data: Omit<Observation, "id">) =>
  client.put<Observation>(`/api/observations/${id}`, data);
export const deleteObservation = (id: number) =>
  client.delete(`/api/observations/${id}`);

// Schedule
export const getSchedules = () => client.get<Schedule[]>("/api/schedule");
export const createSchedule = (data: Omit<Schedule, "id">) =>
  client.post<Schedule>("/api/schedule", data);
export const updateSchedule = (id: number, data: Omit<Schedule, "id">) =>
  client.put<Schedule>(`/api/schedule/${id}`, data);
export const deleteSchedule = (id: number) =>
  client.delete(`/api/schedule/${id}`);

// Materials
export const getMaterials = () => client.get<Material[]>("/api/materials");
export const createMaterial = (data: Omit<Material, "id" | "times_used">) =>
  client.post<Material>("/api/materials", data);
export const updateMaterial = (id: number, data: Omit<Material, "id">) =>
  client.put<Material>(`/api/materials/${id}`, data);
export const recordMaterialUse = (id: number) =>
  client.post<Material>(`/api/materials/${id}/use`);
export const deleteMaterial = (id: number) =>
  client.delete(`/api/materials/${id}`);

// Daily Entries
export const getDailyEntries = () => client.get<DailyEntry[]>("/api/daily-entries");
export const createDailyEntry = (data: Omit<DailyEntry, "id">) =>
  client.post<DailyEntry>("/api/daily-entries", data);
export const updateDailyEntry = (id: number, data: Omit<DailyEntry, "id">) =>
  client.put<DailyEntry>(`/api/daily-entries/${id}`, data);
export const deleteDailyEntry = (id: number) =>
  client.delete(`/api/daily-entries/${id}`);

// Settings
export const getSettings = () => client.get<{ settings: Settings }>("/api/settings");
export const updateSettings = (settings: Settings) =>
  client.put<{ settings: Settings }>("/api/settings", { settings });

// Chat
export const sendChat = (message: string) =>
  client.post<{ response: string }>("/api/chat", { message });
