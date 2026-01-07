# Smart Bus Tracking (Node.js + Next.js)

A real-time bus tracking system built with a **Node.js Socket Server** and a **Next.js Frontend**.

## 🚀 Architecture
- **Socket Server (`/socket-server`)**: 
  - Runs on Port `4000`.
  - Handles real-time websocket connections from drivers and users.
  - Broadcasts GPS updates instantenously.
- **Frontend (`/web`)**: 
  - Runs on Port `3000`.
  - Built with **Next.js 14** (App Router).
  - Premium Glassmorphism UI.

## 🛠️ How to Run
**Option 1: One-Click (Windows)**
Double-click `start_app.bat`.

**Option 2: Manual**
1. **Start Backend**:
   ```bash
   cd socket-server
   npm install
   npm run dev
   ```
2. **Start Frontend**:
   ```bash
   cd web
   npm install
   npm run dev
   ```

## 📱 Usage
- **Passenger Dashboard**: Open `http://localhost:3000`. You will see live moving bus markers.
- **Driver App**: Open `http://localhost:3000/driver`. Login and click "Start Tracking" to become a live bus on the map.
