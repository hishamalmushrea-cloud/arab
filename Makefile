.PHONY: validate generate check phase0 phase1 phase2 import-tunisia review-tunisia repair

validate:
	python3 scripts/validate.py

generate:
	python3 scripts/generate.py

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

# Phase 2 calls Phase 1, which calls Phase 0; listing all three reruns the same gates.
check: phase2

repair:
	python3 scripts/repair_legacy.py
	python3 scripts/repair_links.py
	python3 scripts/migrate_legacy.py
	python3 scripts/import_tunisia_phase2.py
	python3 scripts/generate.py
