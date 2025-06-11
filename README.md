# Real-time Chat Application with Local LLM

A comprehensive real-time chat application powered by Ollama (local LLM), Socket.IO for real-time messaging, and Streamlit for the frontend interface. The entire system runs in Docker containers for easy deployment.

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

## 🛠️ Quick Start

1. **Clone and navigate to the project:**
   ```bash
   git clone <your-repo-url>
   cd chat-app
   ```

2. **Start the application:**
   ```bash
   docker compose up -d
   ```

3. **Wait for services to initialize:**
   - **LLaMA 3.2 model (2GB) is pre-installed** - no download needed!
   - Backend will connect to Ollama automatically
   - Frontend will start once backend is available

4. **Access the application:**
   - Open your browser and go to `http://localhost:8501`
   - Enter a username and select **llama3.2** as your model
   - Start chatting with the AI!

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │     Ollama      │
│  (Streamlit)    │◄──►│  (Node.js +     │◄──►│   (Local LLM)   │
│   Port: 8501    │    │   Socket.IO)    │    │   Port: 11434   │
└─────────────────┘    │   Port: 3001    │    └─────────────────┘
                       └─────────────────┘
```

## 🤖 Pre-installed Model

Your chat application comes with **LLaMA 3.2 (2GB)** ready to use:

- **Model Size:** 2GB (efficient and fast)
- **Capabilities:** Conversational AI, Q&A, general knowledge
- **Performance:** Optimized for real-time chat responses
- **Status:** ✅ Downloaded and ready

**Model Details:**
- Name: `llama3.2:latest`
- Type: Large Language Model optimized for chat
- Response Time: ~2-5 seconds for typical queries
- Memory Usage: ~2-4GB RAM during inference

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