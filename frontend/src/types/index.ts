export interface User {
  id: number;
  username: string;
  name: string;
  email: string;
  school: string | null;
  classroom: string | null;
}

export interface Student {
  id: number;
  name: string;
  age: number;
  interests: string[];
  allergies: string[];
  parent_name: string;
  parent_email: string;
}

export interface Observation {
  id: number;
  student: string;
  date: string;
  area: string;
  skills: string[];
  notes: string;
}

export interface Schedule {
  id: number;
  day: string;
  time: string;
  activity: string;
  duration: number;
  students: string;
}

export interface Material {
  id: number;
  name: string;
  category: string;
  age_range: string;
  description: string;
  in_stock: boolean;
  times_used: number;
}

export interface DailyEntry {
  id: number;
  student: string;
  date: string;
  subject: string;
  activities: string[];
  skill_level: string;
  notes: string;
}

export interface Settings {
  [key: string]: Record<string, unknown>;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}
