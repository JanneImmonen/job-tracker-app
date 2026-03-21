import type { Job, JobFilters, JobFormValues } from "./types";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "http://127.0.0.1:8000";

type ApiValidationDetail = {
  msg?: string;
};

function buildUrl(path: string): string {
  return `${API_BASE_URL}${path}`;
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const payload = (await response.json()) as {
      detail?: string | ApiValidationDetail[];
    };

    if (typeof payload.detail === "string") {
      return payload.detail;
    }

    if (Array.isArray(payload.detail) && payload.detail.length > 0) {
      return payload.detail.map((item) => item.msg ?? "Validation error").join(", ");
    }
  } catch {
    return `${response.status} ${response.statusText}`;
  }

  return `${response.status} ${response.statusText}`;
}

function toPayload(values: JobFormValues): Record<string, string | number | null> {
  return {
    company: values.company.trim(),
    role: values.role.trim(),
    location: values.location.trim() || null,
    salary_min: values.salary_min ? Number(values.salary_min) : null,
    salary_max: values.salary_max ? Number(values.salary_max) : null,
    status: values.status,
    source_url: values.source_url.trim() || null,
    notes: values.notes.trim() || null,
    applied_on: values.applied_on || null,
  };
}

export async function fetchJobs(filters: JobFilters): Promise<Job[]> {
  const params = new URLSearchParams();

  if (filters.status !== "all") {
    params.set("status", filters.status);
  }
  if (filters.company.trim()) {
    params.set("company", filters.company.trim());
  }
  if (filters.q.trim()) {
    params.set("q", filters.q.trim());
  }

  params.set("sort_by", filters.sort_by);
  params.set("order", filters.order);

  const response = await fetch(buildUrl(`/api/jobs?${params.toString()}`));
  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }
  return (await response.json()) as Job[];
}

export async function createJob(values: JobFormValues): Promise<Job> {
  const response = await fetch(buildUrl("/api/jobs"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(toPayload(values)),
  });

  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }

  return (await response.json()) as Job;
}

export async function updateJob(id: number, values: JobFormValues): Promise<Job> {
  const response = await fetch(buildUrl(`/api/jobs/${id}`), {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(toPayload(values)),
  });

  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }

  return (await response.json()) as Job;
}
