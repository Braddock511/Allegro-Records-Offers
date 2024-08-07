SHELL := /bin/bash

# Variables definitions
# -----------------------------------------------------------------------------

ifeq ($(TIMEOUT),)
TIMEOUT := 60
endif

# Target section and Global definitions
# -----------------------------------------------------------------------------
.PHONY: test install run

backend:
	cd application;\
	PYTHONPATH=application/ poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

frontend:
	cd application;\
	npm run dev
