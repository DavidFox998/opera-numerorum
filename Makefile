.PHONY: field_report

# Generate both 1pp and 2pp Field Report variants and record their SHAs in invariants.json.
field_report:
	bash make_field_report.sh
