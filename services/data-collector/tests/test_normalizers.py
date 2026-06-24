from app.mapping.advisory_mapping import map_advisory
from app.mapping.cve_mapping import map_cve
from app.normalizers.advisory_normalizer import normalize_advisory
from app.normalizers.cve_normalizer import normalize_cve


def test_advisory_normalizer_extracts_cves_and_normalizes_fields():
    advisory = map_advisory(
        {
            "source": "NVD ",
            "vendor": " ExampleVendor ",
            "title": "Important fix for CVE-2026-12345",
            "summary": "This also references cve-2025-9999.",
            "severity": "Important",
            "cves": [],
        }
    )

    normalized = normalize_advisory(advisory)

    assert normalized.source == "nvd"
    assert normalized.vendor.name == "ExampleVendor"
    assert normalized.severity == "high"
    assert normalized.cves == ["CVE-2025-9999", "CVE-2026-12345"]


def test_cve_normalizer_rejects_invalid_cve_id():
    cve = map_cve(cve_id="not-a-cve", source="NVD", severity="HIGH", vendor_name="Vendor")
    normalized = normalize_cve(cve)

    assert normalized.cve_id == ""
    assert normalized.source == "nvd"
    assert normalized.severity == "high"
