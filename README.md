# Vertex AI Gemini Chatbot on Google Cloud

![Cloud Function Deploy](https://github.com/engr-usman/vertex-ai-chatbot-gemini/actions/workflows/list-cloud-functions/badge.svg)
![Lint & Docs](https://github.com/engr-usman/vertex-ai-chatbot-gemini/actions/workflows/test-and-deploy/badge.svg)

A serverless chatbot powered by **Gemini 1.5** on **Google Cloud Vertex AI**, deployed using **Cloud Functions**, and presented through a Markdown-friendly frontend using `marked.js`.

---

## 🚀 Features

- 💡 Uses `gemini-1.5-flash-002` (latest supported model) from Vertex AI
- ⚙️ Built as a Google Cloud Function with Python
- 🌐 Simple frontend interface with Markdown formatting
- 🛡️ Secured via IAM roles and Vertex AI user permissions

---

## 📋 Prerequisites

Make sure you have:

- A Google Cloud Project (Billing Enabled)
- Google Cloud SDK installed and authenticated (`gcloud auth login`)
- Python 3.11+ installed
- Billing linked to your project

---

## 📆 Part 1: Backend Setup (Cloud Function)

### ✅ Prerequisites

* A Google Cloud Project (e.g., `gcp-learning-01-463711`)
* Billing enabled
* Vertex AI & Cloud Functions APIs enabled

### 🔌 Enable Required APIs

```bash
gcloud services enable \
  aiplatform.googleapis.com \
  cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com \
  iam.googleapis.com
```

### 👤 Create Service Account for GitHub Actions

```bash
export PROJECT_ID=gcp-learning-01-463711
export SA_NAME=vertex-sa

gcloud iam service-accounts create $SA_NAME \
  --description="Service Account for Vertex AI Chatbot" \
  --display-name="Vertex AI Chatbot SA"
```

#### 🔐 Grant Roles

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.developer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding gcp-learning-01-463711 \
  --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"
```

### 🔑 Create and Download Service Account Key

```bash
gcloud iam service-accounts keys create sa-key.json \
  --iam-account=$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com
```

Then base64 encode and store in GitHub secrets:
```bash
base64 sa-key.json > sa-key.b64
```
FOR Linux/Mac
```bash
base64 -i sa-key.json -o sa-key.txt
```

### ✨ Deploy Cloud Function

```bash
gcloud functions deploy palmChatbot \
  --region=us-central1 \
  --runtime=python310 \
  --trigger-http \
  --entry-point=chatbot \
  --memory=512MB \
  --allow-unauthenticated \
  --source=.
```

### 🧲 Test with `curl`

```bash
curl -X POST https://REGION-PROJECT_ID.cloudfunctions.net/palmChatbot \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Kubernetes?"}'
```

---

## 🌐 Part 2: Frontend with HTML (index.html)

Use the provided `docs/index.html` to create a simple chatbot UI with:

* Prompt input
* Response display
* Loading animation
* Clear chat button

### ▶️ Local Deployment

Just open `docs/index.html` in your browser or deploy with GitHub Pages (set `docs/` as your Pages root).

---

## ⚙️ Part 3: GitHub Workflows

### ✅ list-cloud-functions.yml

Lists deployed functions on push to `main`.

```yaml
name: List Cloud Functions
on:
  push:
    branches: ["main"]

jobs:
  list:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: google-github-actions/auth@v1
        with:
          credentials_json: "${{ secrets.GCP_SA_KEY }}"
      - uses: google-github-actions/setup-gcloud@v1
        with:
          project_id: gcp-learning-01-463711
      - run: gcloud functions list
```

### ✅ test-and-deploy.yml

Formats code, deploys to Cloud Functions.

```yaml
name: Test and Deploy Cloud Function
on:
  push:
    branches: ["main"]

jobs:
  test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python3 -m pip install -r requirements.txt
          python3 -m pip install black

      - name: Lint
        run: black --check .

      - uses: google-github-actions/auth@v1
        with:
          credentials_json: "${{ secrets.GCP_SA_KEY }}"

      - uses: google-github-actions/setup-gcloud@v1
        with:
          project_id: gcp-learning-01-463711

      - name: Deploy
        run: |
          gcloud functions deploy palmChatbot \
            --region=us-central1 \
            --runtime=python310 \
            --trigger-http \
            --entry-point=chatbot \
            --memory=512MB \
            --allow-unauthenticated \
            --source=.
```

### 🧲 Testing Deployment

Update `main.py`, push to `main`, and GitHub Action will:

* Lint code
* Deploy updated function

---

## 🧹 Part 4: Delete All Resources (Optional Cleanup)

### 1. Delete Cloud Function

```bash
gcloud functions delete palmChatbot --region=us-central1 --quiet
```

### 2. Delete Service Account

```bash
gcloud iam service-accounts list
# Replace with your actual SA email
gcloud iam service-accounts delete vertex-sa@gcp-learning-01-463711.iam.gserviceaccount.com --quiet
```

### 3. Disable APIs

```bash
gcloud services disable aiplatform.googleapis.com

gcloud services disable cloudfunctions.googleapis.com

gcloud services disable cloudbuild.googleapis.com

gcloud services disable iam.googleapis.com
```

### 4. Delete Buckets (Optional)

```bash
gcloud storage buckets list
gcloud storage buckets delete gs://your-bucket-name
```

### 5. Remove GitHub Secrets (Optional)

Go to `Repo → Settings → Secrets → Actions → Delete GCP_SA_KEY` if needed.

---

You're now ready to redeploy or share this project! ✨

## Reference Link
- Goodle Model versions and lifecycle: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions