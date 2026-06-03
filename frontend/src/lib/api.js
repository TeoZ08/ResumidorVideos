const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = "Ocorreu um erro inesperado.";

    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      message = response.statusText || message;
    }

    throw new Error(message);
  }

  return response.json();
}

export async function summarizeVideo({ url, force }) {
  return request("/api/summarize", {
    method: "POST",
    body: JSON.stringify({ url, force }),
  });
}

export async function getHistory() {
  return request("/api/history");
}

export async function getHistoryItem(videoId) {
  return request(`/api/history/${videoId}`);
}

export function getExportUrl(videoId) {
  return `${API_BASE_URL}/api/export/${videoId}`;
}
