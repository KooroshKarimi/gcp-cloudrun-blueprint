.PHONY: help install test build run deploy clean

# Default target
help:
	@echo "GCP Cloud Run Blueprint - Phase 1"
	@echo ""
	@echo "Available commands:"
	@echo "  install    - Install Python dependencies"
	@echo "  test       - Run tests"
	@echo "  build      - Build Docker image"
	@echo "  run        - Run application locally"
	@echo "  deploy     - Deploy to Cloud Run"
	@echo "  clean      - Clean up build artifacts"
	@echo "  logs       - View Cloud Run logs"
	@echo "  status     - Check service status"

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	python -m pytest tests/ -v --cov=app --cov-report=html

# Build Docker image
build:
	docker build -t cloudrun-blueprint:latest .

# Run locally
run:
	python app.py

# Run with Docker
run-docker:
	docker run -p 8080:8080 cloudrun-blueprint:latest

# Deploy to Cloud Run (requires gcloud auth)
deploy:
	gcloud run deploy cloudrun-blueprint \
		--source . \
		--platform managed \
		--region us-central1 \
		--allow-unauthenticated \
		--memory 512Mi \
		--cpu 1 \
		--max-instances 10 \
		--min-instances 0 \
		--concurrency 80 \
		--timeout 300 \
		--set-env-vars ENVIRONMENT=production,VERSION=1.0.0

# View logs
logs:
	gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=cloudrun-blueprint" \
		--limit=50 \
		--format="table(timestamp,severity,textPayload)"

# Check service status
status:
	gcloud run services describe cloudrun-blueprint \
		--region us-central1 \
		--format="value(status.url)"

# Clean up
clean:
	docker system prune -f
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Terraform commands
tf-init:
	cd terraform && terraform init

tf-plan:
	cd terraform && terraform plan

tf-apply:
	cd terraform && terraform apply

tf-destroy:
	cd terraform && terraform destroy

# Development helpers
dev-install:
	pip install -r requirements.txt
	pip install -e .

format:
	black app.py tests/
	isort app.py tests/

lint:
	flake8 app.py tests/
	black --check app.py tests/
	isort --check-only app.py tests/