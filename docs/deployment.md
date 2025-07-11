# Deployment Guide - Phase 1

This guide covers deploying the GCP Cloud Run Blueprint Phase 1 to Google Cloud Platform.

## Prerequisites

1. **Google Cloud SDK**
   ```bash
   # Install Google Cloud SDK
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

2. **Docker**
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Terraform** (optional)
   ```bash
   # Install Terraform
   curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
   sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
   sudo apt-get update && sudo apt-get install terraform
   ```

## Method 1: Quick Deploy with gcloud

### 1. Build and Deploy
```bash
# Build and deploy in one command
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
```

### 2. Verify Deployment
```bash
# Get the service URL
gcloud run services describe cloudrun-blueprint \
  --region us-central1 \
  --format='value(status.url)'

# Test the endpoints
curl https://your-service-url/
curl https://your-service-url/health
curl https://your-service-url/api/info
```

## Method 2: Docker Build and Deploy

### 1. Build Docker Image
```bash
# Build the image
docker build -t gcr.io/PROJECT_ID/cloudrun-blueprint:latest .

# Tag for Container Registry
docker tag cloudrun-blueprint:latest gcr.io/PROJECT_ID/cloudrun-blueprint:latest
```

### 2. Push to Container Registry
```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Push the image
docker push gcr.io/PROJECT_ID/cloudrun-blueprint:latest
```

### 3. Deploy to Cloud Run
```bash
gcloud run deploy cloudrun-blueprint \
  --image gcr.io/PROJECT_ID/cloudrun-blueprint:latest \
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
```

## Method 3: Terraform Deployment

### 1. Configure Terraform
```bash
cd terraform

# Create terraform.tfvars file
cat > terraform.tfvars << EOF
project_id = "your-project-id"
region     = "us-central1"
environment = "production"
app_version = "1.0.0"
EOF
```

### 2. Initialize and Deploy
```bash
# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply the configuration
terraform apply
```

### 3. Get Outputs
```bash
# Get service URL
terraform output service_url

# Get service information
terraform output service_name
terraform output service_location
```

## Method 4: GitHub Actions (CI/CD)

### 1. Set up GitHub Secrets
Add these secrets to your GitHub repository:
- `GCP_PROJECT_ID`: Your GCP project ID
- `GCP_SA_KEY`: Service account key JSON (base64 encoded)

### 2. Create Service Account
```bash
# Create service account
gcloud iam service-accounts create cloudrun-deployer \
  --display-name="Cloud Run Deployer"

# Grant necessary roles
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:cloudrun-deployer@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:cloudrun-deployer@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:cloudrun-deployer@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=cloudrun-deployer@PROJECT_ID.iam.gserviceaccount.com

# Base64 encode for GitHub secret
base64 -i key.json
```

### 3. Push to Trigger Deployment
```bash
# Push to main branch to trigger deployment
git push origin main
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment | `development` |
| `VERSION` | Application version | `1.0.0` |
| `PORT` | Application port | `8080` |

## Health Checks

The application provides several health check endpoints:

- `/health` - General health check
- `/health/live` - Liveness probe
- `/health/ready` - Readiness probe

## Monitoring and Logs

### View Logs
```bash
# View Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=cloudrun-blueprint" \
  --limit=50 \
  --format="table(timestamp,severity,textPayload)"
```

### Monitor Metrics
```bash
# View service metrics
gcloud run services describe cloudrun-blueprint \
  --region us-central1 \
  --format="value(status.conditions)"
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Ensure you have the necessary roles
   gcloud projects add-iam-policy-binding PROJECT_ID \
     --member="user:your-email@domain.com" \
     --role="roles/run.admin"
   ```

2. **Container Build Failures**
   ```bash
   # Test locally first
   docker build -t test-app .
   docker run -p 8080:8080 test-app
   ```

3. **Service Not Starting**
   ```bash
   # Check logs
   gcloud run services logs read cloudrun-blueprint --region us-central1
   ```

### Performance Tuning

- **Memory**: Adjust based on application needs (256Mi - 8Gi)
- **CPU**: Scale from 0.25 to 4.0 vCPUs
- **Concurrency**: Default 80, adjust based on workload
- **Instances**: Min 0-100, Max 1-1000

## Security Considerations

1. **HTTPS Only**: Cloud Run enforces HTTPS
2. **IAM**: Use least privilege principle
3. **Secrets**: Store sensitive data in Secret Manager
4. **Network**: Configure VPC connector if needed

## Cost Optimization

1. **Scale to Zero**: Set min instances to 0
2. **Resource Limits**: Set appropriate CPU/memory limits
3. **Concurrency**: Optimize for your workload
4. **Region**: Choose cost-effective regions

## Next Steps

After successful deployment, consider:

1. **Phase 2**: Add monitoring and observability
2. **Custom Domain**: Configure custom domain
3. **SSL Certificate**: Set up managed SSL
4. **CDN**: Configure Cloud CDN
5. **Backup**: Set up automated backups