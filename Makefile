.PHONY: schema-migration-test malformed-json-test validate validate-jordan validate-saudi validate-uae validate-bahrain generate generate-uae-report check phase0 phase1 phase2 phase3 phase4 phase5 bahrain import-tunisia import-jordan import-saudi import-uae import-bahrain review-tunisia review-jordan review-saudi review-uae review-bahrain test-uae-negative test-bahrain-negative repair

schema-migration-test:
	python3 scripts/test_schema_migration.py

malformed-json-test:
	python3 scripts/test_malformed_json.py

validate:
	python3 scripts/validate.py

validate-jordan:
	python3 scripts/validate_jordan.py

validate-saudi:
	python3 scripts/validate_saudi.py

validate-uae:
	python3 scripts/validate_uae.py

validate-bahrain:
	python3 scripts/validate_bahrain.py

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

import-bahrain:
	python3 scripts/build_bahrain_sources.py
	python3 scripts/import_bahrain_production.py

review-bahrain:
	python3 scripts/build_bahrain_review_samples.py
	python3 scripts/review_bahrain.py

test-bahrain-negative:
	python3 scripts/test_bahrain_negative.py

bahrain:
	python3 scripts/check_bahrain_gate.py

# Phase 5 calls all accepted pilot gates; Bahrain is the first production gate layered after it.
import-kuwait:
	python3 scripts/build_kuwait_sources.py
	python3 scripts/import_kuwait_production.py

review-kuwait:
	python3 scripts/build_kuwait_review_samples.py
	python3 scripts/review_kuwait.py

test-kuwait-negative:
	python3 scripts/test_kuwait_negative.py

validate-kuwait:
	python3 scripts/validate_kuwait.py

kuwait:
	python3 scripts/check_kuwait_gate.py

qatar:
	python3 scripts/check_qatar_gate.py

oman:
	python3 scripts/check_oman_gate.py

djibouti:
	python3 scripts/check_djibouti_gate.py

morocco:
	python3 scripts/check_morocco_gate.py

algeria:
	python3 scripts/check_algeria_gate.py

egypt:
	python3 scripts/check_egypt_gate.py

mauritania:
	python3 scripts/check_mauritania_gate.py

lebanon:
	python3 scripts/check_lebanon_gate.py

comoros:
	python3 scripts/check_comoros_gate.py

palestine:
	python3 scripts/check_palestine_gate.py

check: phase5 bahrain kuwait qatar oman djibouti morocco algeria egypt mauritania lebanon comoros palestine

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
	python3 scripts/build_bahrain_sources.py
	python3 scripts/import_bahrain_production.py
	python3 scripts/build_kuwait_sources.py
	python3 scripts/import_kuwait_production.py
	python3 scripts/import_qatar_production.py
	python3 scripts/import_oman_production.py
	python3 scripts/import_djibouti_production.py
	python3 scripts/import_morocco_production.py
	python3 scripts/import_algeria_production.py
	python3 scripts/import_egypt_production.py
	python3 scripts/import_mauritania_production.py
	python3 scripts/import_lebanon_production.py
	python3 scripts/import_comoros_production.py
	python3 scripts/import_palestine_production.py
	python3 scripts/generate.py
