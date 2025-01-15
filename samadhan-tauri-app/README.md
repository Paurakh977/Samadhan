# Tauri + React + Typescript

This template should help get you started developing with Tauri, React and Typescript in Vite.

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Tauri](https://marketplace.visualstudio.com/items?itemName=tauri-apps.tauri-vscode) + [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)

<div align="center">
  <img src="src-tauri/icons/icon.png" alt="Samadhan Logo" width="150"/>

  # ✨ Samadhan Desktop App ✨
  
  <p>A powerful desktop application for managing your daily tasks and schedules with elegance</p>

  [![Tauri](https://img.shields.io/badge/Tauri-2.0-blue.svg)](https://tauri.app/)
  [![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue.svg)](https://www.typescriptlang.org/)
  [![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-blue.svg)](https://tailwindcss.com/)
</div>

## 🌟 About Samadhan

Samadhan is a comprehensive desktop application designed to streamline your daily workflow. Built with modern technologies, it offers a seamless experience across all major desktop platforms.

## 🎯 Key Features

- **📅 Smart Calendar Integration**
  - Efficient schedule management
  - Event reminders and notifications
  - Custom calendar views

- **🔔 Intelligent Notifications**
  - Customizable alert system
  - Priority-based notifications
  - Do not disturb mode

- **👥 User Management**
  - Secure authentication
  - Profile customization
  - Role-based access control

- **⚡ Performance**
  - Lightning-fast operations
  - Minimal resource usage
  - Offline functionality

## 💻 Technology Stack

- **Frontend**
  - React 18 with TypeScript
  - Tailwind CSS for styling
  - Vite for blazing fast development

- **Backend**
  - Tauri 2.0 (Rust)
  - SQLite for local storage
  - Custom Rust APIs

## 🚀 Getting Started

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Node.js (v16 or higher)
# Download from https://nodejs.org/
```

### System Dependencies

<details>
<summary>🐧 Linux</summary>

```bash
sudo apt-get update && sudo apt-get install libwebkit2gtk-4.0-dev \
    build-essential \
    curl \
    wget \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev
```
</details>

<details>
<summary>🍎 macOS</summary>

```bash
xcode-select --install
```
</details>

<details>
<summary>🪟 Windows</summary>

- Install [Microsoft Visual Studio C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Install [WebView2 Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)
</details>

### Installation

```bash
# Clone the repository
git clone https://github.com/Paurakh977/Samadhan.git

# Navigate to project directory
cd samadhan-tauri-app

# Install dependencies
npm install

# Start development server
npm run tauri dev
```

## 🛠️ Development Commands

```bash
# Start development server
npm run tauri dev

# Build for production
npm run tauri build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
samadhan-tauri-app/
├── src/                 # React frontend
│   ├── components/     # UI components
│   ├── pages/         # Application pages
│   └── assets/        # Static assets
├── src-tauri/         # Rust backend
│   ├── src/          # Rust source code
│   └── Cargo.toml    # Rust dependencies
└── public/            # Public assets
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙌 Acknowledgments

- [Tauri](https://tauri.app/) for the amazing framework
- [React](https://reactjs.org/) for the frontend library
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Rust](https://www.rust-lang.org/) for the backend

---

<div align="center">
  <p>Made with ❤️ by Paurakh</p>
  <p>
    <a href="https://github.com/Paurakh977">GitHub</a> •
    <a href="https://github.com/Paurakh977/Samadhan/issues">Report Bug</a> •
    <a href="https://github.com/Paurakh977/Samadhan/issues">Request Feature</a>
  </p>
</div>
