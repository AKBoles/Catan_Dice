# Catan Roller

Mobile-first dice roller & stats companion for Settlers of Catan.

## Features
- Animated dice with haptic feedback
- Roll distribution chart
- Robber alert on 7s
- Player turn tracking (2-6 players)
- Undo & Reset
- Installable PWA
- Persistent state via localStorage

## Deploy to Render
1. Push to GitHub
2. Render → New → Web Service → connect repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```
