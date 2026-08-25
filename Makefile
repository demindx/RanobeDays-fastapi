COMPOSE ?= docker compose
ALEMBIC := $(COMPOSE) run --rm --no-deps backend uv run alembic

.DEFAULT_GOAL := help

.PHONY: help db-up \
	alembic-help alembic-revision alembic-migration alembic-upgrade \
	alembic-downgrade alembic-current alembic-history alembic-heads \
	alembic-branches alembic-show alembic-check alembic-stamp \
	alembic-merge alembic-sql

help:
	@echo "Alembic commands:"
	@echo "  make alembic-migration MESSAGE='add users'  Autogenerate a migration"
	@echo "  make alembic-revision MESSAGE='data fix'    Create an empty migration"
	@echo "  make alembic-upgrade [REV=head]             Upgrade the database"
	@echo "  make alembic-downgrade REV=-1               Downgrade the database"
	@echo "  make alembic-current                         Show current DB revision"
	@echo "  make alembic-history [ARGS='-v']             Show migration history"
	@echo "  make alembic-heads                           Show migration heads"
	@echo "  make alembic-branches                        Show branch points"
	@echo "  make alembic-show [REV=head]                 Show a revision"
	@echo "  make alembic-check                           Check model/migration diff"
	@echo "  make alembic-stamp REV=head                  Stamp without running DDL"
	@echo "  make alembic-merge REVISIONS='a b' MESSAGE='merge heads'"
	@echo "  make alembic-sql [REV=head]                  Print upgrade SQL"
	@echo "  make alembic-help                            Show Alembic CLI help"

db-up:
	$(COMPOSE) up -d db

alembic-help:
	$(ALEMBIC) --help

alembic-revision:
	@test -n "$(MESSAGE)" || (echo "MESSAGE is required" && exit 1)
	$(ALEMBIC) revision -m "$(MESSAGE)"

alembic-migration: db-up
	@test -n "$(MESSAGE)" || (echo "MESSAGE is required" && exit 1)
	$(ALEMBIC) revision --autogenerate -m "$(MESSAGE)"

alembic-upgrade: db-up
	$(ALEMBIC) upgrade "$(if $(REV),$(REV),head)"

alembic-downgrade: db-up
	@test -n "$(REV)" || (echo "REV is required, for example REV=-1" && exit 1)
	$(ALEMBIC) downgrade "$(REV)"

alembic-current: db-up
	$(ALEMBIC) current

alembic-history:
	$(ALEMBIC) history $(ARGS)

alembic-heads:
	$(ALEMBIC) heads

alembic-branches:
	$(ALEMBIC) branches

alembic-show:
	$(ALEMBIC) show "$(if $(REV),$(REV),head)"

alembic-check: db-up
	$(ALEMBIC) check

alembic-stamp: db-up
	@test -n "$(REV)" || (echo "REV is required, for example REV=head" && exit 1)
	$(ALEMBIC) stamp "$(REV)"

alembic-merge:
	@test -n "$(REVISIONS)" || (echo "REVISIONS is required" && exit 1)
	@test -n "$(MESSAGE)" || (echo "MESSAGE is required" && exit 1)
	$(ALEMBIC) merge $(REVISIONS) -m "$(MESSAGE)"

alembic-sql:
	$(ALEMBIC) upgrade "$(if $(REV),$(REV),head)" --sql
