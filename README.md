# GitHub Actions CI/CD Template für Google Cloud

Ein vollständig parametrisierbares CI/CD-Template für die Bereitstellung von Anwendungen auf Google Cloud Run über GitHub Actions.

## Features

- ✅ **Workload Identity Federation** für sichere Authentifizierung
- ✅ **Vollständig parametrisierbar** ohne hartcodierte Werte
- ✅ **Multi-Stage Docker Builds** für optimierte Images
- ✅ **Automatische Tests und Linting**
- ✅ **Google Cloud Run Deployment**
- ✅ **Google Artifact Registry Integration**

## Verzeichnisstruktur

```
.
├── .github/
│   └── workflows/
│       ├── ci.yml          # Continuous Integration
│       └── cd.yml          # Continuous Deployment
├── backend/
│   └── service-a/
│       ├── index.js        # Express.js Anwendung
│       ├── package.json    # Node.js Dependencies
│       └── Dockerfile      # Multi-Stage Docker Build
└── docs/
    └── quick-start.md      # Setup-Anleitung
```

## Schnellstart

Siehe [docs/quick-start.md](docs/quick-start.md) für eine detaillierte Setup-Anleitung.

## GitHub Secrets

Folgende Secrets müssen in deinem Repository konfiguriert werden:

- `GCP_PROJECT_ID`: Deine Google Cloud Projekt-ID
- `GCP_PROJECT_NUMBER`: Deine Google Cloud Projekt-Nummer  
- `GCP_SA_EMAIL`: Service Account E-Mail-Adresse
- `GCP_WIF_PROVIDER`: Workload Identity Provider URL

## Lizenz

MIT
