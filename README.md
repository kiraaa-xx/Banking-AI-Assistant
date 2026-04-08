# 🚀 AI Banking Assistant - Deployment Version

This is a production-ready, lightweight version of the AI Banking Assistant. It includes a React + Vite frontend and a Flask mock backend designed for rapid deployment.

## 📁 Project Structure
- **/frontend**: React application source code.
- **/frontend/dist**: Built version of the website (served by Flask).
- **/backend**: Python Flask logic.
- **/requirements.txt**: Python dependencies for deployment.

## 🛠️ Local Execution (Simple)
To test everything locally with a single command:
1. Open your terminal in the main folder.
2. Run:
   ```bash
   python backend/mock_api.py
   ```
3. Open: [http://localhost:8501](http://localhost:8501)

## 🌐 Cloud Deployment (Render / Heroku)
This project is configured for one-click deployment to **Render.com**.

### **1. Build Settings**
- **Runtime**: `Python`
- **Build Command**: 
  ```bash
  cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt
  ```

### **2. Start Command**
- **Command**:
  ```bash
  gunicorn --chdir backend mock_api:app
  ```

### **3. Environment Variables**
- Add `VITE_BACKEND_URL` with an empty value (so it uses relative paths).

## ✨ Features
- **SPA Routing**: Automatic catch-all route handles `/stats`, `/about`, etc. without 404s.
- **Integrated Serving**: Frontend is served directly through the Flask backend.
- **Cloud Ready**: Automatically detects the environment `PORT` for hosting.
