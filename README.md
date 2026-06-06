# HumanizeAI — Backend

FastAPI backend for the HumanizeAI app, deployed on Vercel Serverless.

---

## Project Structure

```
humanizer-backend/
├── api/
│   └── index.py        ← FastAPI app (Vercel entry point)
├── vercel.json         ← Vercel deployment config
├── requirements.txt    ← Python dependencies
├── humanizer.html      ← Frontend (deploy separately or open locally)
└── README.md
```

---

## Deploy to Vercel (Step by Step)

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Get your Anthropic API Key
- Go to https://console.anthropic.com
- Click **API Keys → Create Key**
- Copy the key (starts with `sk-ant-...`)

### 3. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/humanizer-backend.git
git push -u origin main
```

### 4. Deploy on Vercel
- Go to https://vercel.com and sign in
- Click **Add New Project → Import** your GitHub repo
- During setup, add this Environment Variable:
  - **Name:** `ANTHROPIC_API_KEY`
  - **Value:** your key from step 2
- Click **Deploy**

### 5. Get your backend URL
After deploy, Vercel gives you a URL like:
```
https://humanizer-backend-xyz.vercel.app
```

### 6. Update the frontend
Open `humanizer.html` and find this line:
```javascript
const BACKEND_URL = "https://try2-web-humanizer.vercel.app";
```
Replace it with your actual Vercel URL.

---

## API Endpoints

| Method | Endpoint        | Description              |
|--------|----------------|--------------------------|
| GET    | `/`            | Status check             |
| GET    | `/api/health`  | Health check             |
| POST   | `/api/humanize`| Humanize text            |

### POST /api/humanize

**Request:**
```json
{ "text": "Your AI-generated text here..." }
```

**Response:**
```json
{ "humanized": "The rewritten human-sounding text..." }
```

---

## Running Locally (optional)

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```

Backend runs at: http://localhost:8000

For local testing, update `humanizer.html`:
```javascript
const BACKEND_URL = "http://localhost:8000";
```
