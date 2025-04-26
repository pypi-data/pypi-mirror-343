# 🛡️ VirtueRed Web UI

**VirtueRed** is a red teaming evaluation interface built for AI safety auditing at scale.  
This Web UI allows you to interactively view model performance, risk categories, and failure cases, connected to any backend instance of VirtueRed.

---

## 🚀 Features

- ⚡ Fast, lightweight Web UI with zero setup required
- 🔌 Connects to any locally or remotely hosted VirtueRed backend
- 🧪 Evaluate model scans, dashboards, charts, and PDFs
- 🔐 Built for privacy, works entirely client-side once deployed

---

## 🧪 Quick Start

```bash
pip install virtuered-webui
```

Launch the UI with default settings:

```bash
virtuered-webui serve
```

By default, this will:

- Open the Web UI at: `http://localhost:3000`
- Connect to the backend at: `http://localhost:4401`

You can customize both using the CLI flags:
```bash
virtuered-webui serve --backend-url=http://your-server:4418 --port=3001
```


---


## ⚙️ CLI Options

| Option           | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `--backend-url`  | The full base URL of your VirtueRed backend (default: `http://localhost:4401`) |
| `--port`         | The port number to host the Web UI (default: `3000`)                        |


---


## 🧠 Developer Note

- You must have a running instance of the VirtueRed backend at the URL you specify via `--backend-url`.
- This tool dynamically injects the backend URL at runtime, so no rebuild is necessary for different environments.

---

## 📄 License

MIT License. See [LICENSE](./LICENSE) for details.  
© 2025 VirtueAI. All rights reserved.

