# IP-SAKTI — Frontend

React + Vite frontend for IP-SAKTI — AI assistant for Ayurveda IP guidance.

## Setup

```bash
npm install
cp .env.example .env.local
npm run dev
```

Runs at: `http://localhost:5173`

## .env.local

```
VITE_API_URL=http://localhost:8000
```

## Folder Structure

```
src/
├── api/                     # Backend API calls (DO NOT change contracts)
│   ├── axiosInstance.js     # Base axios config
│   ├── chatApi.js           # POST /api/chat
│   └── classifyApi.js       # POST /api/classify
│
├── pages/                   # One file per route
│   ├── HomePage.jsx         # / — landing page
│   ├── ChatPage.jsx         # /chat — main chat interface
│   └── ClassifyPage.jsx     # /classify — formulation wizard
│
├── components/
│   ├── layout/
│   │   └── Navbar.jsx
│   ├── chat/
│   │   ├── ChatWindow.jsx   # Message list
│   │   ├── ChatInput.jsx    # Input box
│   │   ├── SourceCards.jsx  # Citation cards below AI answer
│   │   ├── ConfidenceBadge.jsx
│   │   └── TypingIndicator.jsx
│   ├── classify/
│   │   ├── ClassifyForm.jsx  # Step-by-step wizard
│   │   └── ClassifyResult.jsx
│   └── ui/
│       ├── JurisdictionToggle.jsx
│       └── LanguageToggle.jsx
│
├── App.jsx                  # Routes
├── main.jsx                 # Entry point
└── index.css                # Tailwind imports
```

## API Contracts — Read Before Building

All API request/response shapes are documented inside each file.
**Do not change field names** — backend matches exactly.

### POST /api/chat
See `src/api/chatApi.js` and `src/pages/ChatPage.jsx`

### POST /api/classify
See `src/api/classifyApi.js` and `src/pages/ClassifyPage.jsx`

### GET /api/health
Used in `src/components/layout/Navbar.jsx`
Returns: `{ status: "ok" }`
