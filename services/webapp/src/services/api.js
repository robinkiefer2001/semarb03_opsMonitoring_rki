const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8002";

async function getJson(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

async function postJson(path, body) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

export function fetchOverview() {
  return getJson("/api/overview");
}

export function fetchAdvisories(page = 1, pageSize = 10) {
  return getJson(`/api/advisories?page=${page}&page_size=${pageSize}`);
}

export function fetchCves(page = 1, pageSize = 10) {
  return getJson(`/api/cves?page=${page}&page_size=${pageSize}`);
}

export function pushDevices(devices) {
  return postJson("/api/devices/push", { devices });
}

export function fetchDevices(query = "", page = 1, pageSize = 20) {
  const q = encodeURIComponent(query);
  return getJson(`/api/devices?query=${q}&page=${page}&page_size=${pageSize}`);
}

export function fetchDeviceImpact(deviceId) {
  return getJson(`/api/impact/device/${encodeURIComponent(deviceId)}`);
}

export function fetchImpactSummary() {
  return getJson("/api/impact/summary");
}

export function fetchEntraChanges() {
  return getJson("/api/changes/entra");
}

export function fetchCveIntel(cveId) {
  return getJson(`/api/cves/${encodeURIComponent(cveId)}/intel`);
}
