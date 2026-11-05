/**
 * Thin API client – wraps fetch calls to the FastAPI backend.
 * All paths are relative so the Vite dev proxy forwards them correctly.
 */

const BASE = "/api/v1";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  health: () => request<{ status: string }>("/health"),
  datasets: {
    list: () => request<unknown[]>("/datasets/"),
  },
  backtests: {
    list: () => request<unknown[]>("/backtests/"),
    create: (payload: { name: string; description?: string }) =>
      request<{ id: string; name: string }>("/backtests/", {
        method: "POST",
        body: JSON.stringify(payload),
      }),
    get: (id: string) => request<unknown>(`/backtests/${id}`),
  },
};
