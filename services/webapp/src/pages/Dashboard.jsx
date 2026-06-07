import React from "react";
import { useEffect, useState } from "react";

import AdvisoryTable from "../components/AdvisoryTable";
import InfoModal from "../components/InfoModal";
import StatCard from "../components/StatCard";
import {
  fetchAdvisories,
  fetchCveIntel,
  fetchCves,
  fetchDeviceImpact,
  fetchDevices,
  fetchEntraChanges,
  fetchImpactSummary,
  fetchOverview,
  pushDevices,
} from "../services/api";

const SAMPLE_DEVICES = [
  {
    device_id: "dev-win-01",
    hostname: "dc-core-01",
    device_type: "windows-server",
    platform: "windows server 2022",
    vendor: "microsoft",
    product: "active directory",
    version: "2022",
    business_unit: "identity",
    owner: "infra-team",
    identity_provider: "entra",
    tags: ["windows", "domain-controller", "entra", "critical"],
  },
  {
    device_id: "dev-net-01",
    hostname: "switch-core-01",
    device_type: "switch",
    platform: "ios-xe",
    vendor: "cisco",
    product: "catalyst",
    version: "17.x",
    business_unit: "network",
    owner: "network-team",
    identity_provider: "entra",
    tags: ["switch", "network", "edge"],
  },
  {
    device_id: "dev-linux-01",
    hostname: "app-linux-01",
    device_type: "linux-server",
    platform: "ubuntu",
    vendor: "canonical",
    product: "nginx",
    version: "24.04",
    business_unit: "apps",
    owner: "platform-team",
    identity_provider: "entra",
    tags: ["linux", "web", "production"],
  },
];

export default function Dashboard() {
  const [overview, setOverview] = useState({ stats: {} });
  const [advisories, setAdvisories] = useState([]);
  const [cves, setCves] = useState([]);
  const [devices, setDevices] = useState([]);
  const [impactSummary, setImpactSummary] = useState({ items: [] });
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [selectedDeviceImpact, setSelectedDeviceImpact] = useState(null);
  const [deviceWindowOpen, setDeviceWindowOpen] = useState(false);
  const [cveWindowOpen, setCveWindowOpen] = useState(false);
  const [selectedCveIntel, setSelectedCveIntel] = useState(null);
  const [entraChanges, setEntraChanges] = useState({ items: [] });
  const [selectedAdvisory, setSelectedAdvisory] = useState(null);
  const [selectedCve, setSelectedCve] = useState(null);
  const [sourceFilter, setSourceFilter] = useState("all");
  const [severityFilter, setSeverityFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [deviceQuery, setDeviceQuery] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        await pushDevices(SAMPLE_DEVICES);

        const [overviewData, advisoryData, cveData, devicesData, impactData, entraData] = await Promise.all([
          fetchOverview(),
          fetchAdvisories(1, 12),
          fetchCves(1, 12),
          fetchDevices("", 1, 50),
          fetchImpactSummary(),
          fetchEntraChanges(),
        ]);

        setOverview(overviewData);
        setAdvisories(advisoryData.items || []);
        setCves(cveData.items || []);
        setDevices(devicesData.items || []);
        setImpactSummary(impactData || { items: [] });
        setEntraChanges(entraData || { items: [] });

        const initialDevice = (devicesData.items || [])[0] || null;
        setSelectedDevice(initialDevice);

        if (initialDevice) {
          const initialImpact = await fetchDeviceImpact(initialDevice.device_id);
          setSelectedDeviceImpact(initialImpact);
        }

        setSelectedAdvisory((advisoryData.items || [])[0] || null);
        setSelectedCve((cveData.items || [])[0] || null);
      } catch (err) {
        setError("Konnte API-Daten nicht laden. Bitte pruefe, ob api-service laeuft.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  async function runDeviceSearch() {
    try {
      const result = await fetchDevices(deviceQuery, 1, 50);
      setDevices(result.items || []);
      if ((result.items || []).length > 0) {
        setSelectedDevice(result.items[0]);
        const impact = await fetchDeviceImpact(result.items[0].device_id);
        setSelectedDeviceImpact(impact);
      } else {
        setSelectedDevice(null);
        setSelectedDeviceImpact(null);
      }
    } catch (err) {
      setError("Device-Suche fehlgeschlagen.");
    }
  }

  async function selectDevice(device) {
    setSelectedDevice(device);
    try {
      const impact = await fetchDeviceImpact(device.device_id);
      setSelectedDeviceImpact(impact);
    } catch (err) {
      setError("Impact-Analyse fuer Device fehlgeschlagen.");
    }
  }

  async function openCveWindow(cveId) {
    try {
      const intel = await fetchCveIntel(cveId);
      setSelectedCveIntel(intel);
      setCveWindowOpen(true);
    } catch (err) {
      setError("CVE-Intel konnte nicht geladen werden.");
    }
  }

  const sources = Array.from(new Set([...advisories.map((a) => a.source), ...cves.map((c) => c.source)])).sort();
  const severities = Array.from(
    new Set([...advisories.map((a) => a.severity), ...cves.map((c) => c.severity)].filter(Boolean))
  ).sort();

  const normalizedSearch = searchTerm.trim().toLowerCase();

  const filteredAdvisories = advisories.filter((advisory) => {
    const sourceOk = sourceFilter === "all" || advisory.source === sourceFilter;
    const severityOk = severityFilter === "all" || advisory.severity === severityFilter;
    const searchOk =
      normalizedSearch.length === 0 ||
      advisory.title?.toLowerCase().includes(normalizedSearch) ||
      advisory.summary?.toLowerCase().includes(normalizedSearch) ||
      (advisory.cves || []).join(" ").toLowerCase().includes(normalizedSearch);
    return sourceOk && severityOk && searchOk;
  });

  const filteredCves = cves.filter((cve) => {
    const sourceOk = sourceFilter === "all" || cve.source === sourceFilter;
    const severityOk = severityFilter === "all" || cve.severity === severityFilter;
    const searchOk =
      normalizedSearch.length === 0 ||
      cve.cve_id?.toLowerCase().includes(normalizedSearch) ||
      (cve.vendors || []).join(" ").toLowerCase().includes(normalizedSearch);
    return sourceOk && severityOk && searchOk;
  });

  const selectedAdvisoryCves = selectedAdvisory
    ? cves.filter((cve) => (selectedAdvisory.cves || []).includes(cve.cve_id))
    : [];

  const selectedCveAdvisories = selectedCve
    ? advisories.filter((advisory) => (advisory.cves || []).includes(selectedCve.cve_id))
    : [];

  return (
    <main className="dashboard">
      <header className="hero hero-grid">
        <div>
          <p className="eyebrow">Ops Monitoring Command Center</p>
          <h1>Threat Exposure Cockpit</h1>
          <p className="subtitle">
            Suche nach Windows Server, Switches und Services und bewerte in Echtzeit, ob aktuelle CVEs,
            Advisories oder Entra-Aenderungen dein Inventar betreffen.
          </p>
        </div>
        <div className="hero-badge">
          <span>Risk Pulse</span>
          <strong>{impactSummary.critical || 0} Critical Devices</strong>
          <small>{overview.generated_at ? `Snapshot: ${overview.generated_at}` : "Snapshot wird geladen"}</small>
        </div>
      </header>

      {error && <p className="error-box">{error}</p>}

      <section className="stats-grid">
        <StatCard label="Advisories" value={overview.stats.advisory_count ?? "-"} />
        <StatCard label="CVEs" value={overview.stats.cve_count ?? "-"} />
        <StatCard label="Quellen" value={(overview.stats.sources || []).join(", ") || "-"} />
        <StatCard label="Devices" value={devices.length} />
        <StatCard label="Critical Exposure" value={impactSummary.critical ?? 0} />
        <StatCard label="High Exposure" value={impactSummary.high ?? 0} />
      </section>

      <section className="panel">
        <h2>Inventory Search und Push API Ready</h2>
        <div className="device-search-row">
          <input
            value={deviceQuery}
            onChange={(event) => setDeviceQuery(event.target.value)}
            placeholder="Suche: windows server, switch, entra, cisco ..."
          />
          <button type="button" onClick={runDeviceSearch}>
            Devices suchen
          </button>
        </div>
        <p className="hint-text">
          API zum Pushen deiner echten Devices ist aktiv unter POST /api/devices/push.
        </p>
      </section>

      <section className="detail-grid">
        <article className="panel detail-card">
          <h2>Device Inventory</h2>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Hostname</th>
                  <th>Typ</th>
                  <th>Version</th>
                  <th>Vendor</th>
                  <th>Produkt</th>
                </tr>
              </thead>
              <tbody>
                {devices.length === 0 ? (
                  <tr>
                    <td colSpan={5}>Keine Devices gefunden</td>
                  </tr>
                ) : (
                  devices.map((device) => (
                    <tr
                      key={device.device_id}
                      className={`clickable-row ${selectedDevice?.device_id === device.device_id ? "active" : ""}`}
                      onClick={() => selectDevice(device)}
                    >
                      <td>{device.hostname}</td>
                      <td>{device.device_type}</td>
                      <td>{device.version || "-"}</td>
                      <td>{device.vendor || "-"}</td>
                      <td>{device.product || "-"}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </article>

        <article className="panel detail-card">
          <h2>Was betrifft mich konkret?</h2>
          {selectedDeviceImpact ? (
            <>
              <p>
                <strong>{selectedDeviceImpact.device.hostname}</strong> ({selectedDeviceImpact.device.device_type})
              </p>
              <p>
                Version: <strong>{selectedDeviceImpact.device.version || "unbekannt"}</strong> | Platform: {selectedDeviceImpact.device.platform || "-"}
              </p>
              <p>
                Risk Score: <strong>{selectedDeviceImpact.risk_score}</strong> | Level: <strong>{selectedDeviceImpact.risk_level}</strong>
              </p>
              <p>
                Matches: {selectedDeviceImpact.advisory_count} Advisories, {selectedDeviceImpact.cve_count} CVEs
              </p>
              <p>Top CVEs:</p>
              <div className="chip-wrap">
                {(selectedDeviceImpact.matched_cves || []).slice(0, 6).map((item) => (
                  <button
                    type="button"
                    key={item.cve_id}
                    className="chip"
                    onClick={() => {
                      const target = cves.find((cve) => cve.cve_id === item.cve_id) || item;
                      setSelectedCve(target);
                      openCveWindow(item.cve_id);
                    }}
                  >
                    {item.cve_id}
                  </button>
                ))}
              </div>
              <div className="device-actions">
                <button type="button" onClick={() => setDeviceWindowOpen(true)}>
                  Device Fenster oeffnen
                </button>
              </div>
            </>
          ) : (
            <p className="hint-text">Waehle links ein Device aus.</p>
          )}
        </article>
      </section>

      <section className="panel">
        <h2>Entra Change Feed</h2>
        <p className="hint-text">Aenderungen, die Identity-/Policy-Kontext betreffen koennen.</p>
        <div className="chip-wrap">
          {(entraChanges.items || []).length === 0 && <span className="hint-text">Keine Entra-Changes vorhanden</span>}
          {(entraChanges.items || []).map((change) => (
            <button
              type="button"
              key={`${change.source}-${change.title}`}
              className="chip"
              onClick={() => setSelectedAdvisory(change)}
            >
              {change.title}
            </button>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>Drilldown und Filter</h2>
        <div className="controls-grid">
          <label className="control">
            Quelle
            <select value={sourceFilter} onChange={(event) => setSourceFilter(event.target.value)}>
              <option value="all">Alle</option>
              {sources.map((source) => (
                <option key={source} value={source}>
                  {source}
                </option>
              ))}
            </select>
          </label>

          <label className="control">
            Severity
            <select value={severityFilter} onChange={(event) => setSeverityFilter(event.target.value)}>
              <option value="all">Alle</option>
              {severities.map((severity) => (
                <option key={severity} value={severity}>
                  {severity}
                </option>
              ))}
            </select>
          </label>

          <label className="control">
            Suche
            <input
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder="Titel, CVE, Vendor..."
            />
          </label>
        </div>
      </section>

      {loading ? (
        <p className="loading">Lade Daten...</p>
      ) : (
        <>
          <AdvisoryTable
            title="Aktuelle Advisories"
            rows={filteredAdvisories}
            columns={[
              { key: "source", label: "Quelle" },
              { key: "title", label: "Titel" },
              { key: "severity", label: "Severity" },
              { key: "published_at", label: "Published" },
            ]}
            rowKey="title"
            selectedRowKey={selectedAdvisory?.title || ""}
            onRowClick={(row) => setSelectedAdvisory(row)}
          />
          <AdvisoryTable
            title="Aktuelle CVEs"
            rows={filteredCves}
            columns={[
              { key: "cve_id", label: "CVE" },
              { key: "source", label: "Quelle" },
              { key: "severity", label: "Severity" },
            ]}
            rowKey="cve_id"
            selectedRowKey={selectedCve?.cve_id || ""}
            onRowClick={(row) => {
              setSelectedCve(row);
              openCveWindow(row.cve_id);
            }}
          />

          <section className="detail-grid">
            <article className="panel detail-card">
              <h2>Advisory Detail</h2>
              {selectedAdvisory ? (
                <>
                  <p>
                    <strong>{selectedAdvisory.title}</strong>
                  </p>
                  <p>{selectedAdvisory.summary || "Keine Summary vorhanden."}</p>
                  <p>
                    Quelle: {selectedAdvisory.source} | Severity: {selectedAdvisory.severity || "unknown"}
                  </p>
                  <p>Betroffene CVEs:</p>
                  <div className="chip-wrap">
                    {(selectedAdvisory.cves || []).length === 0 && <span className="hint-text">Keine CVEs verknuepft</span>}
                    {(selectedAdvisory.cves || []).map((cveId) => (
                      <button
                        type="button"
                        key={cveId}
                        className="chip"
                        onClick={() => {
                          const target = cves.find((item) => item.cve_id === cveId);
                          if (target) {
                            setSelectedCve(target);
                          }
                        }}
                      >
                        {cveId}
                      </button>
                    ))}
                  </div>
                </>
              ) : (
                <p className="hint-text">Waehle eine Advisory-Zeile fuer Details.</p>
              )}
            </article>

            <article className="panel detail-card">
              <h2>CVE Detail</h2>
              {selectedCve ? (
                <>
                  <p>
                    <strong>{selectedCve.cve_id}</strong>
                  </p>
                  <p>
                    Quelle: {selectedCve.source} | Severity: {selectedCve.severity || "unknown"}
                  </p>
                  <p>
                    Vendors: {(selectedCve.vendors || []).length > 0 ? selectedCve.vendors.join(", ") : "keine Angabe"}
                  </p>
                  <p>Verknuepfte Advisories:</p>
                  <div className="chip-wrap">
                    {selectedCveAdvisories.length === 0 && <span className="hint-text">Keine Advisory verknuepft</span>}
                    {selectedCveAdvisories.map((advisory) => (
                      <button
                        type="button"
                        key={`${selectedCve.cve_id}-${advisory.title}`}
                        className="chip"
                        onClick={() => setSelectedAdvisory(advisory)}
                      >
                        {advisory.title}
                      </button>
                    ))}
                  </div>
                </>
              ) : (
                <p className="hint-text">Waehle eine CVE-Zeile fuer Details.</p>
              )}
            </article>
          </section>

          <section className="panel">
            <h2>Beziehungsvorschau</h2>
            {selectedAdvisory ? (
              <p>
                Die Advisory <strong>{selectedAdvisory.title}</strong> betrifft {selectedAdvisoryCves.length} CVE(s).
              </p>
            ) : (
              <p className="hint-text">Keine Advisory ausgewaehlt.</p>
            )}
            {selectedCve ? (
              <p>
                Die CVE <strong>{selectedCve.cve_id}</strong> taucht in {selectedCveAdvisories.length} Advisory(s) auf.
              </p>
            ) : (
              <p className="hint-text">Keine CVE ausgewaehlt.</p>
            )}
          </section>

          <section className="panel">
            <h2>Exposure Ranking</h2>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Device</th>
                    <th>Risk</th>
                    <th>Advisories</th>
                    <th>CVEs</th>
                  </tr>
                </thead>
                <tbody>
                  {(impactSummary.items || []).length === 0 ? (
                    <tr>
                      <td colSpan={4}>Keine Exposure-Daten</td>
                    </tr>
                  ) : (
                    (impactSummary.items || []).map((item) => (
                      <tr
                        key={item.device.device_id}
                        className="clickable-row"
                        onClick={() => {
                          setSelectedDevice(item.device);
                          setSelectedDeviceImpact(item);
                        }}
                      >
                        <td>{item.device.hostname}</td>
                        <td>{item.risk_level} ({item.risk_score})</td>
                        <td>{item.advisory_count}</td>
                        <td>{item.cve_count}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}

      <InfoModal
        open={deviceWindowOpen && !!selectedDeviceImpact}
        title="Device Detail Fenster"
        subtitle={selectedDeviceImpact ? `${selectedDeviceImpact.device.hostname} | ${selectedDeviceImpact.device.device_id}` : ""}
        onClose={() => setDeviceWindowOpen(false)}
      >
        {selectedDeviceImpact && (
          <div className="intel-grid">
            <p>
              <strong>Version:</strong> {selectedDeviceImpact.device.version || "unbekannt"}
            </p>
            <p>
              <strong>Platform:</strong> {selectedDeviceImpact.device.platform || "-"}
            </p>
            <p>
              <strong>Vendor / Produkt:</strong> {selectedDeviceImpact.device.vendor || "-"} / {selectedDeviceImpact.device.product || "-"}
            </p>
            <p>
              <strong>Owner:</strong> {selectedDeviceImpact.device.owner || "-"} | <strong>Business Unit:</strong> {selectedDeviceImpact.device.business_unit || "-"}
            </p>
            <p>
              <strong>Identity Provider:</strong> {selectedDeviceImpact.device.identity_provider || "-"}
            </p>
            <p>
              <strong>Risk:</strong> {selectedDeviceImpact.risk_level} ({selectedDeviceImpact.risk_score})
            </p>
            <p>
              <strong>Matches:</strong> {selectedDeviceImpact.advisory_count} Advisories, {selectedDeviceImpact.cve_count} CVEs
            </p>
            <p>
              <strong>Tags:</strong> {(selectedDeviceImpact.device.tags || []).join(", ") || "-"}
            </p>
          </div>
        )}
      </InfoModal>

      <InfoModal
        open={cveWindowOpen && !!selectedCveIntel}
        title="CVE Intel Fenster"
        subtitle={selectedCveIntel?.cve?.cve_id || ""}
        onClose={() => setCveWindowOpen(false)}
      >
        {selectedCveIntel && (
          <>
            <p>
              <strong>Severity:</strong> {selectedCveIntel.cve.severity || "unknown"} | <strong>Source:</strong> {selectedCveIntel.cve.source || "-"}
            </p>
            <p>
              <strong>Beschreibung:</strong> {selectedCveIntel.cve.description || "Keine Detailbeschreibung vorhanden."}
            </p>
            <p>
              <strong>Vendors:</strong> {(selectedCveIntel.cve.vendors || []).join(", ") || "-"}
            </p>

            <h4>Betroffene Devices (mit Version)</h4>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Hostname</th>
                    <th>Version</th>
                    <th>Risk</th>
                    <th>Match-Grund</th>
                  </tr>
                </thead>
                <tbody>
                  {(selectedCveIntel.impacted_devices || []).length === 0 ? (
                    <tr>
                      <td colSpan={4}>Keine betroffenen Devices gefunden</td>
                    </tr>
                  ) : (
                    (selectedCveIntel.impacted_devices || []).map((item) => (
                      <tr key={`${selectedCveIntel.cve.cve_id}-${item.device.device_id}`}>
                        <td>{item.device.hostname}</td>
                        <td>{item.device.version || "-"}</td>
                        <td>{item.risk_level} ({item.risk_score})</td>
                        <td>{(item.reasons || []).join(", ") || "linked-via-advisory"}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            <h4>Verknuepfte Advisories</h4>
            <div className="chip-wrap">
              {(selectedCveIntel.related_advisories || []).length === 0 && <span className="hint-text">Keine Advisory verknuepft</span>}
              {(selectedCveIntel.related_advisories || []).map((advisory) => (
                <button
                  type="button"
                  className="chip"
                  key={`${selectedCveIntel.cve.cve_id}-${advisory.title}`}
                  onClick={() => setSelectedAdvisory(advisory)}
                >
                  {advisory.title}
                </button>
              ))}
            </div>
          </>
        )}
      </InfoModal>
    </main>
  );
}
