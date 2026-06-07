ARCHITECTURE_MAP = {
	"target_objects": ["advisory", "cve", "asset", "service", "update"],
	"collectors": ["bsi", "nvd", "cisa", "cisco", "github", "microsoft", "entra"],
	"runtime_rules": {
		"deduplicate_by": ["source", "url", "title"],
		"severity_default": "unknown",
		"max_records_per_source": 25,
	},
}

