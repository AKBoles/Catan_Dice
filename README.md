# Catan Roller

Mobile-first dice roller & stats companion for Settlers of Catan.

## Features
- **Animated dice** with haptic feedback
- **Roll distribution chart** — see if the dice are "fair"
- **Robber alert** — flash + vibrate on 7s
- **Player turn tracking** — auto-advances, supports 2-6 players
- **Undo & Reset** — fix mis-rolls
- **Installable PWA** — add to home screen, works offline
- **Persistent state** — resume your game after closing

## Deploy to Render (Free)
1. Push this folder to a GitHub repo
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your repo
4. Render auto-detects `render.yaml` — click Deploy
5. Share the URL with your Catan group

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000 on your phone (same Wi-Fi).
