# Banking Assistant Frontend

A clean, minimalist React frontend for the Banking Assistant System (Final Year Project) — LLM + RAG Banking AI with 91% accuracy.

## Features

- **Chat Interface** — Natural language banking assistant with quick prompt shortcuts
- **Statistics Dashboard** — Dataset analytics, category/intent distribution charts, model accuracy metrics
- **About Page** — System architecture, tech stack, backend scripts, and full setup guide
- **Dark Mode** — Toggle between light and dark themes with persistence
- **Font Awesome Icons** — Professional iconography throughout
- **Responsive Design** — Works on desktop and mobile

## Setup (Standalone)

### 1. Install dependencies

```bash
# Rename package.standalone.json to package.json
cp package.standalone.json package.json
npm install
# or: yarn / pnpm install
```

### 2. Configure environment variables (optional)

Create a `.env` file in the root:

```env
# URL of your Python backend (if running)
VITE_BACKEND_URL=http://localhost:8501
```

If `VITE_BACKEND_URL` is not set, the frontend operates in **demo mode** with intelligent mock responses.

### 3. Start development server

```bash
npm run dev
```

Open http://localhost:3000 in your browser.

### 4. Build for production

```bash
npm run build
```

The production build will be in the `dist/` directory. Deploy it to any static hosting service (Vercel, Netlify, GitHub Pages, etc.).

## Connecting to the Python Backend

The frontend communicates with your Python backend via a REST API. Add a `/chat` endpoint to your Python backend:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from banking_assistant import BankingAssistant

app = Flask(__name__)
CORS(app)
assistant = BankingAssistant()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    result = assistant.process_query(query)
    return jsonify({
        'response': result['response'],
        'intent': result['intent'],
        'category': result['category'],
        'confidence': result['confidence'],
        'masked_pii': result.get('masked_pii', False)
    })

if __name__ == '__main__':
    app.run(port=8501)
```

Install Flask: `pip install flask flask-cors`

Then set `VITE_BACKEND_URL=http://localhost:8501` in your `.env`.

## Project Structure

```
banking-assistant-frontend/
├── src/
│   ├── components/
│   │   ├── Sidebar.tsx          # Navigation sidebar with dark mode toggle
│   │   └── MarkdownRenderer.tsx # Renders bot responses as formatted markdown
│   ├── lib/
│   │   └── api.ts               # Backend API calls and mock data
│   ├── pages/
│   │   ├── Chat.tsx             # Main chat interface
│   │   ├── Stats.tsx            # Statistics dashboard with charts
│   │   └── About.tsx            # System info and setup guide
│   ├── App.tsx                  # Root component with routing
│   ├── index.css                # Theme variables and global styles
│   └── main.tsx                 # Entry point
├── index.html
├── vite.config.standalone.ts    # Standalone Vite config (use this)
├── package.standalone.json      # Standalone package.json (rename to package.json)
└── tsconfig.json
```

## Technology Stack

| Technology | Purpose |
|---|---|
| React 19 | UI framework |
| TypeScript | Type safety |
| Vite | Build tool |
| Tailwind CSS v4 | Styling |
| Font Awesome | Icons |
| Recharts | Charts and data visualization |
| Wouter | Client-side routing |
| Framer Motion | Animations |
| TanStack Query | Server state management |
