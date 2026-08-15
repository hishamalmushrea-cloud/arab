.PHONY: validate generate check phase0 phase1 repair

validate:
	python3 scripts/validate.py

generate:
	python3 scripts/generate.py

phase0:
	python3 scripts/check_phase_gate.py phase0

phase1:
	python3 scripts/check_phase_gate.py phase1

check: phase0 phase1

repair:
	python3 scripts/repair_legacy.py
	python3 scripts/repair_links.py
	python3 scripts/migrate_legacy.py
	python3 scripts/generate.py
