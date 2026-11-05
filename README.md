# Local Qwen AI Web Application

A lightweight, modern web interface for running local AI models (`Qwen/Qwen2.5-0.5B-Instruct`) completely offline. Built using FastAPI for the backend and a single-page HTML/CSS/JavaScript web interface.

## Features

- **Instant Server Startup:** Implements lazy model loading so the web interface loads immediately without connection delays.
- **Persistent Chat Storage:** Uses browser `localStorage` to save chat sessions automatically across page reloads and server restarts.
- **Automatic Chat Titling:** Renames new chat threads dynamically based on the first prompt asked.
- **Modern Dark UI:** Responsive ChatGPT/Gemini-style layout featuring individual chat thread isolation and custom session management.
- **Rich Text & Code Formatting:** Parses Markdown syntax (bold, italics, lists, inline code, and dark syntax blocks) in real-time via Marked.js.
- **Custom Cache Pathing:** Keeps model weights localized on a designated storage path (`F:` drive cache) without clogging system primary drives.

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, PyTorch, Hugging Face `transformers`
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Marked.js
- **Model:** `Qwen/Qwen2.5-0.5B-Instruct`

## Prerequisites

- Python 3.10+
- Git

## Installation & Setup

1. **Clone the Repository:**
   ```powershell
   git clone [https://github.com/grishamgauli22-rgb/Qwen-2.5-AI-web-app.git](https://github.com/grishamgauli22-rgb/Qwen-2.5-AI-web-app.git)
   cd Qwen-2.5-AI-web-app

2. **Install Required Python Dependencies:**
```powershell
py -m pip install fastapi uvicorn torch transformers

```


3. **Ensure Local Model Caching Configuration:**
The backend sets `HF_HOME` to cache model weights locally:
```text
F:\Users\grish\Projects\Programming\Python\GPT2\.cache

```


4. **Launch the Server:**
Run the application server using Uvicorn:
```powershell
py -m uvicorn server:app --reload --port 8000

```


*Alternatively, double-click your `run.bat` file if configured.*
5. **Access the App:**
Open your browser and navigate to:
```text
http://localhost:8000

```



## Project Structure

```text
├── .cache/              # Local Hugging Face cache (ignored by Git)
├── .gitignore          # Git exclusion rules
├── index.html          # Web UI layout, CSS styling, and client script
├── server.py           # FastAPI backend server with lazy model loading
├── run.bat             # Quick startup launcher script
├── README.md           # Project documentation
└── LICENSE             # Open-source license terms

```

## License

This project is licensed under the MIT License — see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

```
