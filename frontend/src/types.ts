export const JOB_STATUSES = [
  "saved",
  "applied",
  "interview",
  "offer",
  "rejected",
] as const;

export type JobStatus = (typeof JOB_STATUSES)[number];

export type Job = {
  id: number;
  company: string;
  role: string;
  location: string | null;
  salary_min: number | null;
  salary_max: number | null;
  status: JobStatus;
  source_url: string | null;
  notes: string | null;
  applied_on: string | null;
  created_at: string;
  updated_at: string;
};

export type JobFormValues = {
  company: string;
  role: string;
  location: string;
  salary_min: string;
  salary_max: string;
  status: JobStatus;
  source_url: string;
  notes: string;
  applied_on: string;
};

export type JobFilters = {
  status: JobStatus | "all";
  company: string;
  q: string;
  sort_by: "created_at" | "updated_at" | "company" | "applied_on" | "status";
  order: "asc" | "desc";
};
