import { useDeferredValue, useEffect, useState } from "react";

import { createJob, fetchJobs, updateJob } from "./api";
import { JOB_STATUSES, type Job, type JobFilters, type JobFormValues } from "./types";

const EMPTY_FORM: JobFormValues = {
  company: "",
  role: "",
  location: "",
  salary_min: "",
  salary_max: "",
  status: "saved",
  source_url: "",
  notes: "",
  applied_on: "",
};

const INITIAL_FILTERS: JobFilters = {
  status: "all",
  company: "",
  q: "",
  sort_by: "created_at",
  order: "desc",
};

function formatCompensation(job: Job): string {
  if (job.salary_min == null && job.salary_max == null) {
    return "Compensation not provided";
  }
  if (job.salary_min != null && job.salary_max != null) {
    return `${job.salary_min} - ${job.salary_max}`;
  }
  return `${job.salary_min ?? job.salary_max}+`;
}

function formatDate(value: string | null): string {
  if (!value) {
    return "Not set";
  }
  return new Date(value).toLocaleDateString();
}

function toFormValues(job: Job): JobFormValues {
  return {
    company: job.company,
    role: job.role,
    location: job.location ?? "",
    salary_min: job.salary_min?.toString() ?? "",
    salary_max: job.salary_max?.toString() ?? "",
    status: job.status,
    source_url: job.source_url ?? "",
    notes: job.notes ?? "",
    applied_on: job.applied_on ?? "",
  };
}

export default function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [filters, setFilters] = useState<JobFilters>(INITIAL_FILTERS);
  const [formValues, setFormValues] = useState<JobFormValues>(EMPTY_FORM);
  const [editingJobId, setEditingJobId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [saveError, setSaveError] = useState<string | null>(null);
  const deferredSearch = useDeferredValue(filters.q);

  useEffect(() => {
    async function loadJobs() {
      setLoading(true);
      setLoadError(null);

      try {
        const nextJobs = await fetchJobs({
          ...filters,
          q: deferredSearch,
        });
        setJobs(nextJobs);
      } catch (error) {
        setLoadError(
          error instanceof Error ? error.message : "Could not load jobs from the API.",
        );
      } finally {
        setLoading(false);
      }
    }

    void loadJobs();
  }, [
    filters.status,
    filters.company,
    filters.sort_by,
    filters.order,
    deferredSearch,
  ]);

  function resetForm() {
    setFormValues(EMPTY_FORM);
    setEditingJobId(null);
    setSaveError(null);
  }

  async function reloadJobs() {
    setLoading(true);
    setLoadError(null);

    try {
      const nextJobs = await fetchJobs({
        ...filters,
        q: deferredSearch,
      });
      setJobs(nextJobs);
    } catch (error) {
      setLoadError(
        error instanceof Error ? error.message : "Could not refresh jobs from the API.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setSaveError(null);

    if (formValues.status !== "saved" && !formValues.applied_on) {
      setSaving(false);
      setSaveError("Applied date is required when the status is not saved.");
      return;
    }

    try {
      if (editingJobId == null) {
        await createJob(formValues);
      } else {
        await updateJob(editingJobId, formValues);
      }

      resetForm();
      await reloadJobs();
    } catch (error) {
      setSaveError(error instanceof Error ? error.message : "Could not save the job.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="app-shell">
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />

      <main className="layout">
        <section className="hero panel">
          <p className="eyebrow">Job Tracker App</p>
          <div className="hero-grid">
            <div>
              <h1>Track the entire hiring pipeline from one focused dashboard.</h1>
              <p className="hero-copy">
                Save promising roles, update interview progress, and keep your notes close
                to the application itself. The frontend now speaks directly to the FastAPI
                backend you already built.
              </p>
            </div>

            <div className="stats-card">
              <div>
                <span className="stat-label">Visible jobs</span>
                <strong className="stat-value">{jobs.length}</strong>
              </div>
              <div>
                <span className="stat-label">Active filter</span>
                <strong className="stat-value">{filters.status}</strong>
              </div>
              <div>
                <span className="stat-label">Sort order</span>
                <strong className="stat-value">
                  {filters.sort_by} / {filters.order}
                </strong>
              </div>
            </div>
          </div>
        </section>

        <section className="workspace">
          <aside className="panel form-panel">
            <div className="section-heading">
              <div>
                <p className="section-kicker">Create and edit</p>
                <h2>{editingJobId == null ? "Add a new role" : "Update selected role"}</h2>
              </div>
              {editingJobId != null ? (
                <button
                  className="ghost-button"
                  onClick={resetForm}
                  type="button"
                >
                  Cancel edit
                </button>
              ) : null}
            </div>

            <form
              className="job-form"
              onSubmit={handleSubmit}
            >
              <label>
                <span>Company</span>
                <input
                  onChange={(event) =>
                    setFormValues((current) => ({
                      ...current,
                      company: event.target.value,
                    }))
                  }
                  required
                  value={formValues.company}
                />
              </label>

              <label>
                <span>Role</span>
                <input
                  onChange={(event) =>
                    setFormValues((current) => ({
                      ...current,
                      role: event.target.value,
                    }))
                  }
                  required
                  value={formValues.role}
                />
              </label>

              <div className="field-row">
                <label>
                  <span>Location</span>
                  <input
                    onChange={(event) =>
                      setFormValues((current) => ({
                        ...current,
                        location: event.target.value,
                      }))
                    }
                    value={formValues.location}
                  />
                </label>

                <label>
                  <span>Status</span>
                  <select
                    onChange={(event) =>
                      setFormValues((current) => ({
                        ...current,
                        status: event.target.value as JobFormValues["status"],
                      }))
                    }
                    value={formValues.status}
                  >
                    {JOB_STATUSES.map((status) => (
                      <option
                        key={status}
                        value={status}
                      >
                        {status}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <div className="field-row">
                <label>
                  <span>Salary min</span>
                  <input
                    inputMode="numeric"
                    min="0"
                    onChange={(event) =>
                      setFormValues((current) => ({
                        ...current,
                        salary_min: event.target.value,
                      }))
                    }
                    type="number"
                    value={formValues.salary_min}
                  />
                </label>

                <label>
                  <span>Salary max</span>
                  <input
                    inputMode="numeric"
                    min="0"
                    onChange={(event) =>
                      setFormValues((current) => ({
                        ...current,
                        salary_max: event.target.value,
                      }))
                    }
                    type="number"
                    value={formValues.salary_max}
                  />
                </label>
              </div>

              <div className="field-row">
                <label>
                  <span>Source URL</span>
                  <input
                    onChange={(event) =>
                      setFormValues((current) => ({
                        ...current,
                        source_url: event.target.value,
                      }))
                    }
                    placeholder="https://example.com/job"
                    type="url"
                    value={formValues.source_url}
                  />
                </label>

                <label>
                  <span>Applied on</span>
                  <input
                    onChange={(event) =>
                      setFormValues((current) => ({
                        ...current,
                        applied_on: event.target.value,
                      }))
                    }
                    type="date"
                    value={formValues.applied_on}
                  />
                </label>
              </div>

              <label>
                <span>Notes</span>
                <textarea
                  onChange={(event) =>
                    setFormValues((current) => ({
                      ...current,
                      notes: event.target.value,
                    }))
                  }
                  placeholder="Capture recruiter signals, prep ideas, or follow-up notes."
                  rows={5}
                  value={formValues.notes}
                />
              </label>

              {saveError ? <p className="feedback error">{saveError}</p> : null}

              <button
                className="primary-button"
                disabled={saving}
                type="submit"
              >
                {saving
                  ? "Saving..."
                  : editingJobId == null
                    ? "Create job"
                    : "Save changes"}
              </button>
            </form>
          </aside>

          <section className="panel list-panel">
            <div className="section-heading">
              <div>
                <p className="section-kicker">Jobs overview</p>
                <h2>Pipeline board</h2>
              </div>
            </div>

            <div className="filters">
              <label>
                <span>Status</span>
                <select
                  onChange={(event) =>
                    setFilters((current) => ({
                      ...current,
                      status: event.target.value as JobFilters["status"],
                    }))
                  }
                  value={filters.status}
                >
                  <option value="all">all</option>
                  {JOB_STATUSES.map((status) => (
                    <option
                      key={status}
                      value={status}
                    >
                      {status}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                <span>Company</span>
                <input
                  onChange={(event) =>
                    setFilters((current) => ({
                      ...current,
                      company: event.target.value,
                    }))
                  }
                  placeholder="Filter by company"
                  value={filters.company}
                />
              </label>

              <label>
                <span>Search</span>
                <input
                  onChange={(event) =>
                    setFilters((current) => ({
                      ...current,
                      q: event.target.value,
                    }))
                  }
                  placeholder="Search role, location, or notes"
                  value={filters.q}
                />
              </label>

              <label>
                <span>Sort by</span>
                <select
                  onChange={(event) =>
                    setFilters((current) => ({
                      ...current,
                      sort_by: event.target.value as JobFilters["sort_by"],
                    }))
                  }
                  value={filters.sort_by}
                >
                  <option value="created_at">created at</option>
                  <option value="updated_at">updated at</option>
                  <option value="company">company</option>
                  <option value="applied_on">applied on</option>
                  <option value="status">status</option>
                </select>
              </label>

              <label>
                <span>Order</span>
                <select
                  onChange={(event) =>
                    setFilters((current) => ({
                      ...current,
                      order: event.target.value as JobFilters["order"],
                    }))
                  }
                  value={filters.order}
                >
                  <option value="desc">descending</option>
                  <option value="asc">ascending</option>
                </select>
              </label>
            </div>

            {loadError ? <p className="feedback error">{loadError}</p> : null}
            {loading ? <p className="feedback info">Loading jobs from the API...</p> : null}

            {!loading && jobs.length === 0 ? (
              <div className="empty-state">
                <h3>No roles match the current filters.</h3>
                <p>Try clearing a filter or create the first job from the panel on the left.</p>
              </div>
            ) : null}

            <div className="job-grid">
              {jobs.map((job) => (
                <article
                  className="job-card"
                  key={job.id}
                >
                  <div className="job-card-top">
                    <div>
                      <h3>{job.role}</h3>
                      <p className="company-name">{job.company}</p>
                    </div>
                    <span className={`status-badge status-${job.status}`}>{job.status}</span>
                  </div>

                  <dl className="job-meta">
                    <div>
                      <dt>Location</dt>
                      <dd>{job.location ?? "Flexible / not specified"}</dd>
                    </div>
                    <div>
                      <dt>Compensation</dt>
                      <dd>{formatCompensation(job)}</dd>
                    </div>
                    <div>
                      <dt>Applied</dt>
                      <dd>{formatDate(job.applied_on)}</dd>
                    </div>
                    <div>
                      <dt>Updated</dt>
                      <dd>{formatDate(job.updated_at)}</dd>
                    </div>
                  </dl>

                  {job.notes ? <p className="job-notes">{job.notes}</p> : null}

                  <div className="job-card-actions">
                    <button
                      className="ghost-button"
                      onClick={() => {
                        setEditingJobId(job.id);
                        setFormValues(toFormValues(job));
                        setSaveError(null);
                      }}
                      type="button"
                    >
                      Edit
                    </button>

                    {job.source_url ? (
                      <a
                        className="link-button"
                        href={job.source_url}
                        rel="noreferrer"
                        target="_blank"
                      >
                        Open source
                      </a>
                    ) : null}
                  </div>
                </article>
              ))}
            </div>
          </section>
        </section>
      </main>
    </div>
  );
}
