# Real-time Chat Application with Local LLM

[![GitHub Repository](https://img.shields.io/badge/GitHub-Dockerized--Chat--Application-blue?style=for-the-badge&logo=github)](https://github.com/shyamkaarthikeyan/Dockerized-chat-application)

A comprehensive real-time chat application powered by **Ollama LLaMA 3.2**, Socket.IO for real-time messaging, and Streamlit for the frontend interface. The entire system runs in Docker containers for easy deployment.

## 🔗 **Repository**
**GitHub:** https://github.com/shyamkaarthikeyan/Dockerized-chat-application

## 🚀 Features

- **Real-time messaging** with Socket.IO
- **Local LLM integration** using Ollama (LLaMA 3, Mistral, CodeLlama, etc.)
- **Multi-user support** with user presence indicators
- **Beautiful web interface** built with Streamlit
- **Fully containerized** with Docker Compose
- **Chat history** persistence
- **Typing indicators** for LLM responses
- **Multiple LLM models** support

## 📋 Prerequisites

- Docker and Docker Compose installed
- At least 8GB of RAM (for running LLM models)
- Internet connection for initial model downloads

## 🛠️ Quick Start - Copy & Paste Commands

**Step 1: Clone the repository**
```bash
git clone https://github.com/shyamkaarthikeyan/Dockerized-chat-application.git
cd Dockerized-chat-application
```

**Step 2: Start the application (one command)**
```bash
docker compose up -d
```

**Step 3: Access your chat application**
- **Frontend URL:** http://localhost:8501
- **Model to select:** `llama3.2` (pre-installed, 2GB)
- **Ready to chat!** ✅

### ⚡ **One-Line Setup (Copy & Paste)**
```bash
git clone https://github.com/shyamkaarthikeyan/Dockerized-chat-application.git && cd Dockerized-chat-application && docker compose up -d
```

### 🎯 **What Happens Next:**
1. **Ollama starts** with LLaMA 3.2 model (pre-installed)
2. **Backend initializes** on port 3001
3. **Frontend launches** on port 8501
4. **Chat ready** in ~30 seconds

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │     Ollama      │
│  (Streamlit)    │◄──►│  (Node.js +     │◄──►│   (Local LLM)   │
│   Port: 8501    │    │   Socket.IO)    │    │   Port: 11434   │
└─────────────────┘    │   Port: 3001    │    └─────────────────┘
                       └─────────────────┘
```

## 🤖 Pre-installed Model - LLaMA 3.2 Implementation

Your chat application comes with **LLaMA 3.2 (2GB)** ready to use:

### 📊 **Model Specifications**
- **Model Name:** `llama3.2:latest`
- **Size:** 2GB (efficient and fast)
- **Type:** Large Language Model optimized for chat
- **Capabilities:** Conversational AI, Q&A, general knowledge, code assistance
- **Performance:** Optimized for real-time chat responses
- **Status:** ✅ Pre-installed and ready to use

### ⚡ **Performance Metrics**
- **Response Time:** ~2-5 seconds for typical queries
- **Memory Usage:** ~2-4GB RAM during inference
- **Concurrent Users:** Supports multiple users simultaneously
- **Model Loading:** ~10-15 seconds on first startup

### 🔧 **Implementation Details**
The LLaMA 3.2 model is integrated through:
- **Ollama API** endpoint: `http://localhost:11434`
- **Backend integration** via Socket.IO for real-time responses
- **Streamlit frontend** with model selection dropdown
- **Docker containerization** for easy deployment

### 💡 **Copy-Paste Model Usage**
```javascript
// Backend API call to LLaMA 3.2
const response = await axios.post(`${OLLAMA_URL}/api/generate`, {
  model: 'llama3.2',
  prompt: userMessage,
  stream: false,
  options: {
    temperature: 0.7,
    max_tokens: 500
  }
});
```

### 🎯 **Quick Model Test**
After starting the application, test the LLaMA 3.2 model:
1. Go to http://localhost:8501
2. Enter username: `testuser`
3. Select model: `llama3.2`
4. Ask: `"Hello, can you help me with coding questions?"`
5. Get AI response in ~3 seconds! ✅

## 📁 Project Structure

```
chat-app/
├── docker-compose.yml          # Orchestrates all services
├── README.md                   # This file
├── backend/                    # Node.js Socket.IO server
│   ├── Dockerfile
│   ├── package.json
│   └── server.js
└── frontend/                   # Streamlit web interface
    ├── Dockerfile
    ├── requirements.txt
    └── app.py
```

## 🔧 Configuration

### Environment Variables

- **Backend:**
  - `OLLAMA_URL`: URL to Ollama service (default: `http://ollama:11434`)
  - `NODE_ENV`: Environment mode (default: `production`)

- **Frontend:**
  - `BACKEND_URL`: URL to backend service (default: `http://backend:3001`)

### LLM Models

The application supports multiple Ollama models:
- `llama3.2` (default, 2GB - **currently installed and ready**)
- `mistral` (4GB)
- `codellama`
- `neural-chat`

**Current Setup:**
- ✅ **LLaMA 3.2 (2GB)** - Pre-installed and configured
- This model provides excellent performance for chat applications
- Optimized for conversational AI with good speed and accuracy

To add more models, edit the `available_models` list in `frontend/app.py`.

## 📖 Usage

1. **Connect to Chat:**
   - Enter your username in the sidebar
   - Select your preferred LLM model
   - Click "Connect to Chat"

2. **Send Messages:**
   - Type in the message area
   - Click "💬 Send to Chat" for regular messages
   - Click "🤖 Ask LLM" to get AI responses

3. **Features:**
   - See online users in the sidebar
   - View chat history when you join
   - Real-time typing indicators
   - Different message styles for users, LLM, and system messages

## 🚀 Development

### Running in Development Mode

1. **Start Ollama separately:**
   ```bash
   docker run -d -p 11434:11434 --name ollama ollama/ollama
   ```

2. **Install and run backend:**
   ```bash
   cd backend
   npm install
   npm run dev
   ```

3. **Install and run frontend:**
   ```bash
   cd frontend
   pip install -r requirements.txt
   streamlit run app.py
   ```

### Adding New LLM Models

1. **Pull the model in Ollama:**
   ```bash
   docker exec ollama ollama pull <model-name>
   ```

2. **Add to the frontend model list:**
   Edit `frontend/app.py` and add the model name to `available_models`.

## 🐛 Troubleshooting

### Common Issues

1. **Ollama model download fails:**
   - Check internet connection
   - Ensure sufficient disk space
   - Try pulling the model manually: `docker exec ollama ollama pull llama3.2`

2. **Frontend can't connect to backend:**
   - Check if backend service is running: `docker-compose logs backend`
   - Verify port 3001 is not blocked

3. **LLM responses are slow:**
   - This is normal for the first request (model loading)
   - Ensure sufficient RAM is available
   - Consider using smaller models like `neural-chat`

### Health Checks

- **Backend health:** `http://localhost:3001/health`
- **Ollama health:** `http://localhost:11434/api/tags`
- **Frontend:** Available through the web interface

## 🔍 Monitoring

### View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f ollama
```

### Check service status:
```bash
docker-compose ps
```

## 🛑 Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clears chat history and models)
docker-compose down -v
```

## 🔒 Security Considerations

- The application is configured for local development
- For production deployment, consider:
  - Adding authentication
  - Using HTTPS
  - Implementing rate limiting
  - Securing WebSocket connections
  - Adding input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM hosting
- [Socket.IO](https://socket.io/) for real-time communication
- [Streamlit](https://streamlit.io/) for the beautiful web interface
- [Docker](https://docker.com/) for containerization

---

**Built with ❤️ using modern technologies for seamless real-time AI-powered conversations.**
