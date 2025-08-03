# Vertex AI Chatbot with Gemini

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

## 🔑 Step 1: Enable Required Services

Run the following commands to enable necessary Google Cloud APIs:

```bash
gcloud services enable \
  aiplatform.googleapis.com \
  cloudfunctions.googleapis.com \
  artifactregistry.googleapis.com \
  iamcredentials.googleapis.com \
  storage.googleapis.com
```

👤 Step 2: Create Service Account for Cloud Function
```bash
# Create a service account
gcloud iam service-accounts create vertex-chatbot-sa \
  --display-name "Vertex Chatbot Service Account"

# Grant necessary roles
gcloud projects add-iam-policy-binding <YOUR_PROJECT_ID> \
  --member="serviceAccount:vertex-chatbot-sa@<YOUR_PROJECT_ID>.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding <YOUR_PROJECT_ID> \
  --member="serviceAccount:vertex-chatbot-sa@<YOUR_PROJECT_ID>.iam.gserviceaccount.com" \
  --role="roles/storage.viewer"
```
Replace <YOUR_PROJECT_ID> with your actual GCP project ID.

🧠 Step 3: Prepare Your Python Cloud Function
```python
from flask import Request, jsonify
import vertexai
from vertexai.preview.generative_models import GenerativeModel

def chatbot(request: Request):
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "Prompt is missing"}), 400

        vertexai.init(project="gcp-learning-01-463711", location="us-central1")

        model = GenerativeModel("gemini-1.5-flash-002")
        response = model.generate_content(prompt)

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

```requirements.txt
google-cloud-aiplatform==1.48.0
flask
```

☁️ Step 4: Deploy to Google Cloud
```bash
gcloud functions deploy palmChatbot \
  --runtime python311 \
  --trigger-http \
  --entry-point chatbot \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account vertex-chatbot-sa@<YOUR_PROJECT_ID>.iam.gserviceaccount.com
```

🌐 Step 5: Frontend
Use this index.html for local testing:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Gemini Chatbot</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 2rem;
      max-width: 700px;
      margin: auto;
      background: #f8f9fa;
    }
    textarea {
      width: 100%;
      height: 100px;
      padding: 10px;
    }
    button {
      margin-top: 10px;
      padding: 10px 20px;
    }
    #response {
      margin-top: 30px;
      background: #fff;
      padding: 20px;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <h1>Ask Gemini</h1>
  <textarea id="prompt" placeholder="Ask a question..."></textarea><br />
  <button onclick="sendPrompt()">Ask</button>
  <div id="response"></div>

  <script>
    async function sendPrompt() {
      const prompt = document.getElementById('prompt').value;
      const responseDiv = document.getElementById('response');
      responseDiv.innerHTML = '⏳ Waiting for response...';

      try {
        const res = await fetch("https://<region>-<project_id>.cloudfunctions.net/<function_name>", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt }),
        });

        const data = await res.json();
        if (data.response) {
          responseDiv.innerHTML = marked.parse(data.response);
        } else {
          responseDiv.innerHTML = "❌ Error: " + JSON.stringify(data);
        }
      } catch (err) {
        responseDiv.innerHTML = "❌ Network error: " + err.message;
      }
    }
  </script>
</body>
</html>
```
✅ Open index.html locally or host it via GitHub Pages, Firebase Hosting, or any static server.


### Deploy:
```
gcloud functions deploy palmChatbot \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point chatbot \
  --region us-central1
```

### Run Curl or Frontend index.html file to verify
```
curl -X POST https://<region>-<project_id>.cloudfunctions.net/<function_name> \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is DevOps in simple words?"}'
```

🧪 Example Prompt
```json
{
  "prompt": "What is MLOps in simple words?"
}
```

🙌 Credits
    Google Cloud Vertex AI team
    Gemini Model (gemini-1.5-flash-002)
    marked.js open-source project

## Reference Link
- Goodle Models including versions: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions