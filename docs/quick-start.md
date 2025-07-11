# Quick Start Guide

Dieses Repository dient als Blaupause für CI/CD-Pipelines von GitHub nach Google Cloud und ist vollständig parametrisierbar ohne hartcodierte Werte.

## Voraussetzungen

- Ein Google Cloud Projekt
- GitHub Repository (erstellt über "Use this template")
- GCP CLI (optional, für lokale Tests)

## Setup-Schritte

### 1. Repository erstellen

1. Klicke auf "Use this template" in diesem Repository
2. Erstelle ein neues Repository mit deinem gewünschten Namen
3. Clone das neue Repository lokal

### 2. Google Cloud APIs aktivieren

Aktiviere die folgenden APIs in deinem GCP-Projekt:

```bash
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable iamcredentials.googleapis.com
```

### 3. Workload Identity Federation konfigurieren

Erstelle einen Workload Identity Pool und Provider:

```bash
# Pool erstellen
gcloud iam workload-identity-pools create "github-actions-pool" \
  --project="${GCP_PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Actions Pool"

# Provider erstellen
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="${GCP_PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --display-name="GitHub provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

### 4. Service Account erstellen und konfigurieren

```bash
# Service Account erstellen
gcloud iam service-accounts create "github-actions-sa" \
  --project="${GCP_PROJECT_ID}" \
  --display-name="GitHub Actions Service Account"

# Berechtigungen zuweisen
gcloud projects add-iam-policy-binding "${GCP_PROJECT_ID}" \
  --member="serviceAccount:github-actions-sa@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding "${GCP_PROJECT_ID}" \
  --member="serviceAccount:github-actions-sa@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding "${GCP_PROJECT_ID}" \
  --member="serviceAccount:github-actions-sa@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Workload Identity Binding
gcloud iam service-accounts add-iam-policy-binding "github-actions-sa@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${GCP_PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${GCP_PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/${GITHUB_REPOSITORY}"
```

### 5. Artifact Registry Repository erstellen

```bash
gcloud artifacts repositories create "my-artifacts" \
  --project="${GCP_PROJECT_ID}" \
  --repository-format="docker" \
  --location="europe-west3" \
  --description="Docker repository for Cloud Run deployments"
```

### 6. GitHub Secrets konfigurieren

Füge die folgenden Secrets in deinem GitHub Repository hinzu:

- `GCP_PROJECT_ID`: Deine GCP Projekt-ID
- `GCP_PROJECT_NUMBER`: Deine GCP Projekt-Nummer
- `GCP_SA_EMAIL`: `github-actions-sa@${GCP_PROJECT_ID}.iam.gserviceaccount.com`
- `GCP_WIF_PROVIDER`: `projects/${GCP_PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider`

### 7. Deployment starten

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

Das erste Deployment wird automatisch gestartet und deine Anwendung wird auf Google Cloud Run bereitgestellt.

## Anpassungen

### Region ändern

Ändere die `GCP_REGION` und `GAR_LOCATION` Variablen in `.github/workflows/cd.yml`:

```yaml
env:
  GCP_REGION: us-central1
  GAR_LOCATION: us-central1
```

### Repository-Name ändern

Ändere die `REPOSITORY` Variable in `.github/workflows/cd.yml`:

```yaml
env:
  REPOSITORY: dein-repository-name
```

### Service-Name ändern

Ändere den Service-Namen im Deploy-Schritt in `.github/workflows/cd.yml`:

```yaml
gcloud run deploy dein-service-name \
```

## Überprüfung

Nach dem Deployment kannst du deine Anwendung unter der URL erreichen, die in den GitHub Actions Logs angezeigt wird. Die Anwendung sollte "Hello World from Cloud Run!" zurückgeben.

## Troubleshooting

- **Authentifizierungsfehler**: Überprüfe die Workload Identity Federation Konfiguration
- **Build-Fehler**: Stelle sicher, dass das Artifact Registry Repository existiert
- **Deployment-Fehler**: Überprüfe die Service Account Berechtigungen