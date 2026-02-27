# Fenix VLS - Deploy para Cloud Run

## Pré-Requisitos
- Google Cloud SDK instalado (`gcloud`)
- Projeto GCP com Cloud Run habilitado
- Docker instalado

## 1. Configurar o Projeto GCP
```bash
gcloud config set project SEU_PROJECT_ID
gcloud auth configure-docker
```

## 2. Deploy Simples (direto do código - sem Docker manual)
```bash
cd c:\Users\Mauricio\Desktop\fenix-vls\VLSCommandCenter
gcloud run deploy fenix-vls --source . --region us-central1 --allow-unauthenticated --port 8080
```

## 3. Configurar Variáveis de Ambiente no Cloud Run (Segurança)
```bash
gcloud run services update fenix-vls \
  --region us-central1 \
  --set-env-vars "DJANGO_SECRET_KEY=SUA_CHAVE_SECRETA_AQUI,DEBUG=False,VLS_SECRET_TOKEN=SEU_TOKEN_SECRETO"
```

## 4. Verificar Deployment
```bash
gcloud run services describe fenix-vls --region us-central1
```

## URL Final
Após o deploy, o Google fornece uma URL no formato:
`https://fenix-vls-HASH-uc.a.run.app`

Esta URL é o seu **Sovereign VLS Command Center na Nuvem**.
