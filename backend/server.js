const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3001;
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434';

// Store active users and chat history
const activeUsers = new Map();
const chatHistory = [];

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Get chat history endpoint
app.get('/api/history', (req, res) => {
  res.json(chatHistory.slice(-50)); // Return last 50 messages
});

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.id}`);

  // Handle user joining
  socket.on('join', (userData) => {
    const user = {
      id: socket.id,
      username: userData.username || `User_${Math.random().toString(36).substr(2, 6)}`,
      joinedAt: new Date().toISOString()
    };
    
    activeUsers.set(socket.id, user);
    
    // Send current user info
    socket.emit('user_info', user);
    
    // Broadcast user joined
    socket.broadcast.emit('user_joined', {
      username: user.username,
      timestamp: new Date().toISOString()
    });
    
    // Send updated user list
    io.emit('users_update', Array.from(activeUsers.values()));
    
    // Send chat history to new user
    socket.emit('chat_history', chatHistory.slice(-50));
    
    console.log(`User ${user.username} joined the chat`);
  });

  // Handle regular chat messages
  socket.on('message', async (data) => {
    const user = activeUsers.get(socket.id);
    if (!user) return;

    const message = {
      id: `${Date.now()}_${socket.id}`,
      username: user.username,
      content: data.content,
      timestamp: new Date().toISOString(),
      type: 'user'
    };

    chatHistory.push(message);
    
    // Broadcast message to all clients
    io.emit('message', message);
    
    console.log(`Message from ${user.username}: ${data.content}`);
  });

  // Handle LLM chat requests
  socket.on('llm_message', async (data) => {
    const user = activeUsers.get(socket.id);
    if (!user) return;

    const userMessage = {
      id: `${Date.now()}_${socket.id}`,
      username: user.username,
      content: data.content,
      timestamp: new Date().toISOString(),
      type: 'user'
    };

    chatHistory.push(userMessage);
    io.emit('message', userMessage);

    try {
      // Send typing indicator
      io.emit('llm_typing', { isTyping: true });

      // Get response from Ollama
      const response = await axios.post(`${OLLAMA_URL}/api/generate`, {
        model: data.model || 'llama3.2',
        prompt: data.content,
        stream: false,
        options: {
          temperature: 0.7,
          max_tokens: 500
        }
      }, {
        timeout: 30000
      });

      const llmMessage = {
        id: `${Date.now()}_llm`,
        username: `🤖 ${data.model || 'LLaMA'}`,
        content: response.data.response,
        timestamp: new Date().toISOString(),
        type: 'llm'
      };

      chatHistory.push(llmMessage);
      
      // Stop typing indicator and send LLM response
      io.emit('llm_typing', { isTyping: false });
      io.emit('message', llmMessage);

      console.log(`LLM response generated for ${user.username}`);

    } catch (error) {
      console.error('Error calling Ollama:', error.message);
      
      io.emit('llm_typing', { isTyping: false });
      
      const errorMessage = {
        id: `${Date.now()}_error`,
        username: '⚠️ System',
        content: `Error: Unable to get response from LLM. ${error.message}`,
        timestamp: new Date().toISOString(),
        type: 'error'
      };
      
      chatHistory.push(errorMessage);
      io.emit('message', errorMessage);
    }
  });

  // Handle user disconnect
  socket.on('disconnect', () => {
    const user = activeUsers.get(socket.id);
    if (user) {
      activeUsers.delete(socket.id);
      
      // Broadcast user left
      socket.broadcast.emit('user_left', {
        username: user.username,
        timestamp: new Date().toISOString()
      });
      
      // Send updated user list
      io.emit('users_update', Array.from(activeUsers.values()));
      
      console.log(`User ${user.username} disconnected`);
    }
  });
});

// Start server
server.listen(PORT, () => {
  console.log(`Chat backend server running on port ${PORT}`);
  console.log(`Ollama URL: ${OLLAMA_URL}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});