# GCP Cloud Run Blueprint

A comprehensive blueprint for deploying applications on Google Cloud Run with best practices and automation.

## Phase 1: Foundation Setup

Phase 1 establishes the foundational components for a Cloud Run application:

### Components
- **Web Application**: Basic Flask application with health checks
- **Containerization**: Dockerfile for building container images
- **Deployment**: Cloud Run service configuration
- **Infrastructure**: Terraform configuration for GCP resources
- **CI/CD**: GitHub Actions workflow for automated deployment
- **Monitoring**: Basic logging and monitoring setup

### Features
- ✅ Containerized web application
- ✅ Health check endpoints
- ✅ Environment variable configuration
- ✅ Auto-scaling configuration
- ✅ HTTPS enforcement
- ✅ Cloud Run service deployment
- ✅ Infrastructure as Code (Terraform)
- ✅ Automated CI/CD pipeline

## Quick Start

1. **Prerequisites**
   - Google Cloud SDK installed
   - Docker installed
   - Terraform installed (optional)

2. **Local Development**
   ```bash
   # Run locally
   python app.py
   
   # Build and run with Docker
   docker build -t cloudrun-app .
   docker run -p 8080:8080 cloudrun-app
   ```

3. **Deploy to Cloud Run**
   ```bash
   # Deploy using gcloud
   gcloud run deploy cloudrun-app \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. **Deploy with Terraform**
   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```

## Project Structure

```
├── app.py                 # Main Flask application
├── Dockerfile             # Container configuration
├── requirements.txt       # Python dependencies
├── .dockerignore         # Docker ignore file
├── terraform/            # Infrastructure as Code
│   ├── main.tf          # Main Terraform configuration
│   ├── variables.tf     # Variable definitions
│   └── outputs.tf       # Output values
├── .github/              # GitHub Actions workflows
│   └── workflows/
│       └── deploy.yml   # CI/CD pipeline
└── docs/                 # Documentation
    └── deployment.md    # Deployment guide
```

## Next Phases

- **Phase 2**: Advanced monitoring and observability
- **Phase 3**: Multi-region deployment and CDN
- **Phase 4**: Security hardening and compliance
- **Phase 5**: Performance optimization and scaling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details
