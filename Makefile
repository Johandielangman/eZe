.PHONY: run backend frontend

backend:
	@cd backend && ../.venv/Scripts/python main.py --host localhost --port 8081 --reload
