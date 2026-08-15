.PHONY: validate validate-jordan validate-saudi validate-uae generate generate-uae-report check phase0 phase1 phase2 phase3 phase4 phase5 import-tunisia import-jordan import-saudi import-uae review-tunisia review-jordan review-saudi review-uae test-uae-negative repair

validate:
	python3 scripts/validate.py

validate-jordan:
	python3 scripts/validate_jordan.py

validate-saudi:
	python3 scripts/validate_saudi.py

validate-uae:
	python3 scripts/validate_uae.py

generate:
	python3 scripts/generate.py

generate-uae-report:
	python3 scripts/generate_uae_report.py

phase0:
	python3 scripts/check_phase_gate.py phase0

phase1:
	python3 scripts/check_phase_gate.py phase1

import-tunisia:
	python3 scripts/import_tunisia_phase2.py

review-tunisia:
	python3 scripts/review_tunisia.py

phase2:
	python3 scripts/check_phase_gate.py phase2

import-jordan:
	python3 scripts/import_jordan_phase3.py

review-jordan:
	python3 scripts/review_jordan.py

phase3:
	python3 scripts/check_phase_gate.py phase3

import-saudi:
	python3 scripts/build_saudi_sources.py
	python3 scripts/import_saudi_phase3.py

review-saudi:
	python3 scripts/build_saudi_review_samples.py
	python3 scripts/review_saudi.py

phase4:
	python3 scripts/check_phase_gate.py phase4

import-uae:
	python3 scripts/build_uae_sources.py
	python3 scripts/import_uae_phase5.py

review-uae:
	python3 scripts/build_uae_review_samples.py
	python3 scripts/review_uae.py

test-uae-negative:
	python3 scripts/test_uae_negative.py

phase5:
	python3 scripts/check_phase_gate.py phase5

# UAE Phase 5 calls Saudi Phase 4, Jordan Phase 3, Tunisia Phase 2, Phase 1, and Phase 0.
check: phase5

repair:
	python3 scripts/repair_legacy.py
	python3 scripts/repair_links.py
	python3 scripts/migrate_legacy.py
	python3 scripts/import_tunisia_phase2.py
	python3 scripts/import_jordan_phase3.py
	python3 scripts/build_saudi_sources.py
	python3 scripts/import_saudi_phase3.py
	python3 scripts/build_uae_sources.py
	python3 scripts/import_uae_phase5.py
	python3 scripts/generate.py
