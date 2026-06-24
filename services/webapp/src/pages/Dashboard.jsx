import React, { useCallback, useEffect, useMemo, useState } from "react";

import AdvisoryTable from "../components/AdvisoryTable";
import InfoModal from "../components/InfoModal";
import StatCard from "../components/StatCard";
import {
  fetchAdvisories,
  fetchCveIntel,
  fetchCves,
  fetchDeviceImpact,
  fetchDevices,
  fetchImpactSummary,
  fetchOverview,
} from "../services/api";

const NAV = [
  { id: "cves", label: "CVEs" },
  { id: "advisories", label: "Advisories" },
  { id: "overview", label: "Overview" },
  { id: "assets", label: "Assets" },
];

const RISK_ORDER = {
  low: 1,
  medium: 2,
  high: 3,
  critical: 4,
};

function atLeastRisk(actual, minRisk) {
  if (minRisk === "all") {
    return true;
  }
  return (RISK_ORDER[actual] || 0) >= (RISK_ORDER[minRisk] || 0);
}

function normalizeText(value) {
  return String(value || "").trim().toLowerCase();
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("cves");
  const [overview, setOverview] = useState({ stats: {} });
  const [advisories, setAdvisories] = useState([]);
  const [cves, setCves] = useState([]);
  const [devices, setDevices] = useState([]);
  const [impactSummary, setImpactSummary] = useState({ items: [] });

  const [selectedDeviceImpact, setSelectedDeviceImpact] = useState(null);
  const [selectedCveIntel, setSelectedCveIntel] = useState(null);
  const [selectedAdvisory, setSelectedAdvisory] = useState(null);

  const [cveWindowOpen, setCveWindowOpen] = useState(false);
  const [advisoryWindowOpen, setAdvisoryWindowOpen] = useState(false);

  const [infoQuery, setInfoQuery] = useState("");
  const [assetFilterQuery, setAssetFilterQuery] = useState("");
  const [assetSearchQuery, setAssetSearchQuery] = useState("");
  const [severityFilter, setSeverityFilter] = useState("all");
  const [sourceFilter, setSourceFilter] = useState("all");
  const [impactRiskFilter, setImpactRiskFilter] = useState("all");
  const [onlyImpacted, setOnlyImpacted] = useState(false);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError("");

    const jobs = await Promise.allSettled([
      fetchOverview(),
      fetchAdvisories(1, 100),
      fetchCves(1, 100),
      fetchDevices("", 1, 100),
      fetchImpactSummary(),
    ]);

    const failures = [];

    if (jobs[0].status === "fulfilled") {
      setOverview(jobs[0].value || { stats: {} });
    } else {
      failures.push("overview");
    }

    if (jobs[1].status === "fulfilled") {
      setAdvisories(jobs[1].value?.items || []);
    } else {
      failures.push("advisories");
    }

    if (jobs[2].status === "fulfilled") {
      setCves(jobs[2].value?.items || []);
    } else {
      failures.push("cves");
    }

    if (jobs[3].status === "fulfilled") {
      setDevices(jobs[3].value?.items || []);
    } else {
      failures.push("assets");
    }

    if (jobs[4].status === "fulfilled") {
      setImpactSummary(jobs[4].value || { items: [] });
    } else {
      failures.push("impact");
    }

    if (failures.length > 0) {
      setError(`Partial data loaded. Missing: ${failures.join(", ")}.`);
    }

    setLoading(false);
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const normalizedInfoQuery = normalizeText(infoQuery);
  const normalizedAssetFilterQuery = normalizeText(assetFilterQuery);

  const sources = useMemo(
    () =>
      Array.from(
        new Set([...advisories.map((item) => item.source), ...cves.map((item) => item.source)].filter(Boolean))
      ).sort(),
    [advisories, cves]
  );

  const cveToAssets = useMemo(() => {
    const map = new Map();
    for (const impact of impactSummary.items || []) {
      const asset = impact.device || {};
      for (const cve of impact.matched_cves || []) {
        const key = cve.cve_id;
        if (!key) {
          continue;
        }
        const current = map.get(key) || [];
        current.push({
          asset,
          risk_level: impact.risk_level || "low",
          risk_score: impact.risk_score || 0,
        });
        map.set(key, current);
      }
    }
    return map;
  }, [impactSummary]);

  const advisoryToAssets = useMemo(() => {
    const map = new Map();
    for (const impact of impactSummary.items || []) {
      const asset = impact.device || {};
      for (const advisory of impact.matched_advisories || []) {
        const key = advisory.title;
        if (!key) {
          continue;
        }
        const current = map.get(key) || [];
        current.push({
          asset,
          risk_level: impact.risk_level || "low",
          risk_score: impact.risk_score || 0,
        });
        map.set(key, current);
      }
    }
    return map;
  }, [impactSummary]);

  function filterImpactedAssets(rows) {
    const seen = new Set();
    return (rows || []).filter((item) => {
      const device = item.asset || item.device || {};
      const host = normalizeText(device.hostname);
      const vendor = normalizeText(device.vendor);
      const platform = normalizeText(device.platform);
      const text = `${host} ${vendor} ${platform}`;
      const queryOk = !normalizedAssetFilterQuery || text.includes(normalizedAssetFilterQuery);
      const riskOk = atLeastRisk(item.risk_level, impactRiskFilter);
      const id = device.device_id || `${host}-${item.risk_score}`;
      if (!queryOk || !riskOk || seen.has(id)) {
        return false;
      }
      seen.add(id);
      return true;
    });
  }

  const filteredCves = useMemo(() => {
    return cves.filter((item) => {
      const sourceOk = sourceFilter === "all" || item.source === sourceFilter;
      const severityOk = severityFilter === "all" || item.severity === severityFilter;
      const text = `${item.cve_id || ""} ${(item.vendors || []).join(" ")} ${item.description || ""}`.toLowerCase();
      const queryOk = !normalizedInfoQuery || text.includes(normalizedInfoQuery);

      const impactedAssets = filterImpactedAssets(cveToAssets.get(item.cve_id));
      const impactOk = !onlyImpacted || impactedAssets.length > 0;

      return sourceOk && severityOk && queryOk && impactOk;
    });
  }, [
    cves,
    sourceFilter,
    severityFilter,
    normalizedInfoQuery,
    onlyImpacted,
    cveToAssets,
    normalizedAssetFilterQuery,
    impactRiskFilter,
  ]);

  const filteredAdvisories = useMemo(() => {
    return advisories.filter((item) => {
      const sourceOk = sourceFilter === "all" || item.source === sourceFilter;
      const severityOk = severityFilter === "all" || item.severity === severityFilter;
      const text = `${item.title || ""} ${item.summary || ""} ${(item.cves || []).join(" ")}`.toLowerCase();
      const queryOk = !normalizedInfoQuery || text.includes(normalizedInfoQuery);

      const impactedAssets = filterImpactedAssets(advisoryToAssets.get(item.title));
      const impactOk = !onlyImpacted || impactedAssets.length > 0;

      return sourceOk && severityOk && queryOk && impactOk;
    });
  }, [
    advisories,
    sourceFilter,
    severityFilter,
    normalizedInfoQuery,
    onlyImpacted,
    advisoryToAssets,
    normalizedAssetFilterQuery,
    impactRiskFilter,
  ]);

  async function searchAssets() {
    try {
      const result = await fetchDevices(assetSearchQuery, 1, 100);
      setDevices(result.items || []);
    } catch (searchError) {
      setError("Asset search failed.");
    }
  }

  async function showAssetImpact(deviceId) {
    try {
      const impact = await fetchDeviceImpact(deviceId);
      setSelectedDeviceImpact(impact);
    } catch (impactError) {
      setError("Could not load asset impact details.");
    }
  }

  async function openCveIntel(cveId) {
    try {
      const intel = await fetchCveIntel(cveId);
      setSelectedCveIntel(intel);
      setCveWindowOpen(true);
    } catch (intelError) {
      setError("Could not load CVE intelligence details.");
    }
  }

  function openAdvisoryDrilldown(advisory) {
    setSelectedAdvisory(advisory);
    setAdvisoryWindowOpen(true);
  }

  return (
    <main className="dashboard">
      <header className="hero">
        <div className="hero-copy">
          <p className="kicker">Ops Monitoring</p>
          <h1>Information-First Threat Intelligence</h1>
          <p>
            Start with all CVEs and Advisories. Filter impacted assets only as an inspect layer for operational
            relevance.
          </p>
        </div>
        <div className="hero-pulse">
          <strong>{impactSummary.critical || 0} critical assets</strong>
          <span>{overview.generated_at ? `Snapshot: ${overview.generated_at}` : "No snapshot timestamp"}</span>
        </div>
      </header>

      <nav className="top-nav">
        {NAV.map((item) => (
          <button
            key={item.id}
            type="button"
            className={activeTab === item.id ? "nav-btn active" : "nav-btn"}
            onClick={() => setActiveTab(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      {error && <p className="error-box">{error}</p>}
      {loading && <p className="loading">Loading data...</p>}

      <section className="stats-grid">
        <StatCard label="Advisories" value={overview.stats.advisory_count ?? advisories.length} />
        <StatCard label="CVEs" value={overview.stats.cve_count ?? cves.length} />
        <StatCard label="Data Sources" value={(overview.stats.sources || []).join(", ") || "-"} />
        <StatCard label="Assets" value={devices.length} />
        <StatCard label="Critical" value={impactSummary.critical ?? 0} />
        <StatCard label="High" value={impactSummary.high ?? 0} />
      </section>

      <section className="panel filter-panel">
        <h2>Global Information Filters</h2>
        <div className="filters filters-wide">
          <input
            value={infoQuery}
            onChange={(event) => setInfoQuery(event.target.value)}
            placeholder="Search in CVEs and Advisories"
          />
          <select value={sourceFilter} onChange={(event) => setSourceFilter(event.target.value)}>
            <option value="all">All sources</option>
            {sources.map((source) => (
              <option key={source} value={source}>
                {source}
              </option>
            ))}
          </select>
          <select value={severityFilter} onChange={(event) => setSeverityFilter(event.target.value)}>
            <option value="all">All severities</option>
            <option value="critical">critical</option>
            <option value="high">high</option>
            <option value="medium">medium</option>
            <option value="low">low</option>
            <option value="unknown">unknown</option>
          </select>
          <input
            value={assetFilterQuery}
            onChange={(event) => setAssetFilterQuery(event.target.value)}
            placeholder="Impacted asset filter (hostname/vendor/platform)"
          />
          <select value={impactRiskFilter} onChange={(event) => setImpactRiskFilter(event.target.value)}>
            <option value="all">All impact levels</option>
            <option value="critical">critical and above</option>
            <option value="high">high and above</option>
            <option value="medium">medium and above</option>
            <option value="low">low and above</option>
          </select>
          <label className="toggle-inline">
            <input
              type="checkbox"
              checked={onlyImpacted}
              onChange={(event) => setOnlyImpacted(event.target.checked)}
            />
            Only show entries with impacted assets
          </label>
          <button type="button" onClick={loadData}>
            Refresh data
          </button>
        </div>
      </section>

      {activeTab === "cves" && (
        <section className="panel">
          <h2>All CVEs</h2>
          <p className="hint-text">Primary intelligence list. Inspect related advisories and impacted assets.</p>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>CVE</th>
                  <th>Severity</th>
                  <th>Source</th>
                  <th>Vendors</th>
                  <th>Impacted assets</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredCves.map((item) => {
                  const impactedAssets = filterImpactedAssets(cveToAssets.get(item.cve_id));
                  return (
                    <tr key={item.cve_id}>
                      <td>{item.cve_id}</td>
                      <td>{item.severity || "unknown"}</td>
                      <td>{item.source || "-"}</td>
                      <td>{(item.vendors || []).join(", ") || "-"}</td>
                      <td>{impactedAssets.length}</td>
                      <td>
                        <button type="button" onClick={() => openCveIntel(item.cve_id)}>
                          Inspect
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {activeTab === "advisories" && (
        <section className="panel">
          <h2>All Advisories</h2>
          <p className="hint-text">Primary advisory intelligence list with impacted-asset filtering and inspect actions.</p>
          <AdvisoryTable
            title="Advisory feed"
            rowKey="title"
            rows={filteredAdvisories.map((advisory) => ({
              ...advisory,
              impacted_assets: filterImpactedAssets(advisoryToAssets.get(advisory.title)).length,
            }))}
            columns={[
              { key: "source", label: "Source" },
              { key: "severity", label: "Severity" },
              { key: "title", label: "Title" },
              { key: "impacted_assets", label: "Impacted assets" },
            ]}
            onRowClick={openAdvisoryDrilldown}
          />
        </section>
      )}

      {activeTab === "overview" && (
        <section className="detail-grid">
          <article className="panel">
            <h2>Top impacted assets</h2>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Asset</th>
                    <th>Risk</th>
                    <th>Advisories</th>
                    <th>CVEs</th>
                  </tr>
                </thead>
                <tbody>
                  {filterImpactedAssets(impactSummary.items || [])
                    .slice(0, 15)
                    .map((item) => (
                      <tr key={item.device?.device_id || item.device?.hostname}>
                        <td>{item.device?.hostname || "-"}</td>
                        <td>{item.risk_level}</td>
                        <td>{item.advisory_count}</td>
                        <td>{item.cve_count}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </article>

          <article className="panel">
            <h2>Platform spread</h2>
            <div className="chip-wrap">
              {Array.from(new Set(devices.map((item) => item.platform).filter(Boolean))).map((platform) => (
                <span key={platform} className="chip">
                  {platform}
                </span>
              ))}
            </div>
          </article>
        </section>
      )}

      {activeTab === "assets" && (
        <section className="detail-grid">
          <article className="panel">
            <h2>Asset inventory</h2>
            <div className="asset-search-row">
              <input
                value={assetSearchQuery}
                onChange={(event) => setAssetSearchQuery(event.target.value)}
                placeholder="Search assets by hostname, vendor, product"
              />
              <button type="button" onClick={searchAssets}>
                Search assets
              </button>
            </div>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Hostname</th>
                    <th>Type</th>
                    <th>Platform</th>
                    <th>Vendor</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {devices.map((device) => (
                    <tr key={device.device_id}>
                      <td>{device.hostname}</td>
                      <td>{device.device_type}</td>
                      <td>{device.platform}</td>
                      <td>{device.vendor}</td>
                      <td>
                        <button type="button" onClick={() => showAssetImpact(device.device_id)}>
                          Show impact
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </article>

          <article className="panel">
            <h2>Selected asset impact</h2>
            {!selectedDeviceImpact && <p className="hint-text">Select an asset and click Show impact.</p>}
            {selectedDeviceImpact && (
              <>
                <p>
                  <strong>Asset:</strong> {selectedDeviceImpact.device?.hostname}
                </p>
                <p>
                  <strong>Risk:</strong> {selectedDeviceImpact.risk_level} ({selectedDeviceImpact.risk_score})
                </p>
                <p>
                  <strong>Linked advisories:</strong> {selectedDeviceImpact.advisory_count}
                </p>
                <p>
                  <strong>Linked CVEs:</strong> {selectedDeviceImpact.cve_count}
                </p>
              </>
            )}
          </article>
        </section>
      )}

      <InfoModal
        open={cveWindowOpen}
        title={selectedCveIntel?.cve?.cve_id || "CVE details"}
        subtitle="Related advisories and impacted assets"
        onClose={() => setCveWindowOpen(false)}
      >
        <p>
          <strong>Severity:</strong> {selectedCveIntel?.cve?.severity || "unknown"}
        </p>
        <p>
          <strong>Vendors:</strong> {(selectedCveIntel?.cve?.vendors || []).join(", ") || "-"}
        </p>

        <h4>Related advisories</h4>
        <ul>
          {(selectedCveIntel?.related_advisories || []).map((item, idx) => (
            <li key={`${item.title}-${idx}`}>{item.title}</li>
          ))}
        </ul>

        <h4>Impacted assets</h4>
        <ul>
          {filterImpactedAssets(selectedCveIntel?.impacted_devices || []).map((item) => (
            <li key={item.asset?.device_id || item.device?.device_id}>
              {(item.asset?.hostname || item.device?.hostname) || "unknown"} ({item.risk_level}, score {item.risk_score})
            </li>
          ))}
        </ul>
      </InfoModal>

      <InfoModal
        open={advisoryWindowOpen}
        title={selectedAdvisory?.title || "Advisory details"}
        subtitle={`${selectedAdvisory?.source || ""} ${selectedAdvisory?.severity || ""}`.trim()}
        onClose={() => setAdvisoryWindowOpen(false)}
      >
        <p>
          <strong>Summary:</strong> {selectedAdvisory?.summary || "-"}
        </p>
        <p>
          <strong>Linked CVEs:</strong> {(selectedAdvisory?.cves || []).length}
        </p>
        <div className="chip-wrap">
          {(selectedAdvisory?.cves || []).map((cveId) => (
            <button key={cveId} type="button" className="chip" onClick={() => openCveIntel(cveId)}>
              {cveId}
            </button>
          ))}
        </div>

        <h4>Impacted assets</h4>
        <ul>
          {filterImpactedAssets(advisoryToAssets.get(selectedAdvisory?.title) || []).map((item) => (
            <li key={item.asset?.device_id || item.asset?.hostname}>
              {item.asset?.hostname || "unknown"} ({item.risk_level}, score {item.risk_score})
            </li>
          ))}
        </ul>
      </InfoModal>
    </main>
  );
}
