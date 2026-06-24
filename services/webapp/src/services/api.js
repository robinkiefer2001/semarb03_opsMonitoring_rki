function resolveApiBase() {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }

  if (typeof window !== "undefined") {
    const { protocol, hostname, port } = window.location;
    if (port === "5173") {
      return `${protocol}//${hostname}:8002/api`;
    }
  }

  return "/api";
}

const API_BASE = resolveApiBase();

async function withTimeout(promise, timeoutMs = 12000) {
  let timeoutHandle;
  const timeoutPromise = new Promise((_, reject) => {
    timeoutHandle = setTimeout(() => reject(new Error("Request timeout")), timeoutMs);
  });

  try {
    return await Promise.race([promise, timeoutPromise]);
  } finally {
    clearTimeout(timeoutHandle);
  }
}

async function getJson(path) {
  const response = await withTimeout(fetch(`${API_BASE}${path}`));
  if (!response.ok) {
    throw new Error(`GET ${path} failed: ${response.status}`);
  }
  return response.json();
}

async function postJson(path, body) {
  const response = await withTimeout(
    fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    })
  );
  if (!response.ok) {
    throw new Error(`POST ${path} failed: ${response.status}`);
  }
  return response.json();
}

export function fetchOverview() {
  return getJson("/overview");
}

export function fetchAdvisories(page = 1, pageSize = 10) {
  return getJson(`/advisories?page=${page}&page_size=${pageSize}`);
}

export function fetchCves(page = 1, pageSize = 10) {
  return getJson(`/cves?page=${page}&page_size=${pageSize}`);
}

export function pushDevices(devices) {
  return postJson("/devices/push", { devices });
}

export function fetchDevices(query = "", page = 1, pageSize = 20) {
  const q = encodeURIComponent(query);
  return getJson(`/devices?query=${q}&page=${page}&page_size=${pageSize}`);
}

export function fetchDeviceImpact(deviceId) {
  return getJson(`/impact/device/${encodeURIComponent(deviceId)}`);
}

export function fetchImpactSummary() {
  return getJson("/impact/summary");
}

export function fetchEntraChanges() {
  return getJson("/changes/entra");
}

export function fetchCveIntel(cveId) {
  return getJson(`/cves/${encodeURIComponent(cveId)}/intel`);
}
