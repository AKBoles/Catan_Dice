from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#2c1810">
<title>Catan Roller</title>
<link rel="manifest" href="/manifest.json">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Alegreya+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{
  --bg:#1a0f0a;--surface:#2c1810;--surface2:#3d2317;--surface3:#4e2e1e;
  --gold:#d4a843;--gold-dim:#8a6d2b;--red:#c0392b;--red-glow:#e74c3c;
  --cream:#f5e6c8;--cream-dim:#bfa87a;--blue:#5b8fb9;--green:#6b9e5a;
  --text:#f5e6c8;--text-dim:#9e8a6a;
  --hex-size:28px;
}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--text);font-family:'Alegreya Sans',sans-serif}
.app{height:100dvh;display:flex;flex-direction:column;max-width:480px;margin:0 auto;position:relative;overflow:hidden}

/* Hex background pattern */
.app::before{
  content:'';position:absolute;inset:0;opacity:.04;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='100'%3E%3Cpath d='M28 66L0 50V16L28 0l28 16v34L28 66zm0 34L0 84V50l28-16 28 16v34L28 100z' fill='none' stroke='%23d4a843' stroke-width='1'/%3E%3C/svg%3E");
  pointer-events:none;z-index:0;
}
.app>*{position:relative;z-index:1}

/* Header */
.header{display:flex;align-items:center;justify-content:space-between;padding:12px 16px 8px;flex-shrink:0}
.logo{font-family:'Cinzel',serif;font-weight:900;font-size:20px;color:var(--gold);letter-spacing:2px;text-transform:uppercase}
.turn-badge{background:var(--surface2);border:1px solid var(--gold-dim);border-radius:20px;padding:4px 14px;font-size:13px;color:var(--cream-dim);font-weight:500}
.turn-badge span{color:var(--gold);font-weight:700}

/* Player bar */
.players{display:flex;gap:6px;padding:4px 16px 10px;flex-shrink:0;overflow-x:auto}
.players::-webkit-scrollbar{display:none}
.player-chip{
  padding:6px 14px;border-radius:20px;font-size:12px;font-weight:700;letter-spacing:.5px;
  border:2px solid transparent;cursor:pointer;transition:all .2s;white-space:nowrap;
  text-transform:uppercase;opacity:.5;flex-shrink:0;
}
.player-chip.active{opacity:1;transform:scale(1.05)}
.player-chip[data-color="red"]{background:#8b1a1a;border-color:#c0392b;color:#f5c6c6}
.player-chip[data-color="blue"]{background:#1a3a5c;border-color:#5b8fb9;color:#c6dff5}
.player-chip[data-color="white"]{background:#4a4a4a;border-color:#aaa;color:#eee}
.player-chip[data-color="orange"]{background:#7a3d00;border-color:#e67e22;color:#fde3c8}
.player-chip[data-color="green"]{background:#1a4a2a;border-color:#6b9e5a;color:#c6f5d0}
.player-chip[data-color="brown"]{background:#3d2010;border-color:#8b6914;color:#e6d5b8}
.player-add{
  padding:6px 12px;border-radius:20px;font-size:14px;font-weight:700;
  background:var(--surface2);border:2px dashed var(--gold-dim);color:var(--gold-dim);
  cursor:pointer;flex-shrink:0;
}

/* Dice area */
.dice-zone{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:0 20px;min-height:0}

.dice-row{display:flex;gap:20px;align-items:center}
.die{
  width:72px;height:72px;background:var(--cream);border-radius:14px;
  display:grid;grid-template:repeat(3,1fr)/repeat(3,1fr);padding:10px;gap:2px;
  box-shadow:0 4px 20px rgba(0,0,0,.4),inset 0 -2px 4px rgba(0,0,0,.1);
  transition:transform .1s;position:relative;
}
.die.rolling{animation:dieShake .4s ease-in-out}
.pip{width:100%;aspect-ratio:1;border-radius:50%;background:var(--bg);opacity:0;transition:opacity .1s}
.pip.show{opacity:1}

/* Total display */
.total-display{text-align:center;margin-top:4px}
.total-num{
  font-family:'Cinzel',serif;font-size:64px;font-weight:900;color:var(--gold);
  line-height:1;text-shadow:0 0 40px rgba(212,168,67,.3);
  transition:transform .2s,color .2s;
}
.total-num.robber{color:var(--red-glow);text-shadow:0 0 40px rgba(231,76,60,.5)}
.total-label{font-size:13px;color:var(--text-dim);letter-spacing:3px;text-transform:uppercase;margin-top:2px}
.robber-alert{
  font-family:'Cinzel',serif;font-size:15px;color:var(--red-glow);letter-spacing:4px;
  text-transform:uppercase;opacity:0;transition:opacity .3s;height:22px;margin-top:2px;
}
.robber-alert.show{opacity:1;animation:robberPulse 1s ease-in-out 2}

/* Roll button */
.roll-btn{
  width:calc(100% - 40px);max-width:400px;padding:18px;border:none;border-radius:16px;
  background:linear-gradient(135deg,var(--gold),#b8912e);color:var(--bg);
  font-family:'Cinzel',serif;font-size:20px;font-weight:900;letter-spacing:4px;
  text-transform:uppercase;cursor:pointer;margin:12px auto 0;
  box-shadow:0 4px 24px rgba(212,168,67,.3);transition:all .15s;flex-shrink:0;
  -webkit-user-select:none;user-select:none;
}
.roll-btn:active{transform:scale(.97);box-shadow:0 2px 12px rgba(212,168,67,.2)}

/* Stats bar */
.stats-bar{
  display:flex;align-items:flex-end;justify-content:center;gap:3px;
  padding:12px 16px 6px;flex-shrink:0;height:100px;
}
.stat-col{display:flex;flex-direction:column;align-items:center;gap:2px;flex:1;max-width:36px}
.stat-bar-wrap{width:100%;display:flex;justify-content:center}
.stat-bar{
  width:16px;border-radius:4px 4px 0 0;background:var(--surface3);
  transition:height .4s cubic-bezier(.34,1.56,.64,1),background .3s;min-height:2px;
}
.stat-bar.has-rolls{background:var(--gold-dim)}
.stat-bar.highlight{background:var(--gold)}
.stat-bar.robber-bar.has-rolls{background:var(--red)}
.stat-count{font-size:9px;color:var(--text-dim);font-weight:700;height:12px}
.stat-label{font-size:10px;color:var(--text-dim);font-weight:700}
.stat-label.seven{color:var(--red)}

/* History */
.history{
  display:flex;gap:6px;padding:6px 16px 6px;flex-shrink:0;overflow-x:auto;
  mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);
}
.history::-webkit-scrollbar{display:none}
.hist-chip{
  flex-shrink:0;width:32px;height:32px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:13px;font-weight:700;background:var(--surface2);color:var(--cream-dim);
  border:1px solid var(--surface3);
}
.hist-chip.seven{background:#5c1a1a;color:var(--red-glow);border-color:var(--red)}
.hist-chip:first-child{animation:chipIn .3s ease-out}

/* Bottom bar */
.bottom-bar{display:flex;gap:8px;padding:8px 16px 16px;flex-shrink:0}
.bottom-bar{padding-bottom:max(16px,env(safe-area-inset-bottom))}
.action-btn{
  flex:1;padding:10px;border:1px solid var(--surface3);border-radius:12px;
  background:var(--surface);color:var(--text-dim);font-size:11px;font-weight:700;
  text-transform:uppercase;letter-spacing:1px;cursor:pointer;text-align:center;
  transition:all .2s;
}
.action-btn:active{background:var(--surface2);color:var(--cream)}
.action-btn .icon{font-size:16px;display:block;margin-bottom:2px}

/* Settings modal */
.modal-overlay{
  position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:100;
  display:none;align-items:flex-end;justify-content:center;
  backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);
}
.modal-overlay.open{display:flex}
.modal{
  background:var(--surface);border-radius:20px 20px 0 0;width:100%;max-width:480px;
  padding:24px 20px;padding-bottom:max(24px,env(safe-area-inset-bottom));
  max-height:70vh;overflow-y:auto;
}
.modal h2{font-family:'Cinzel',serif;color:var(--gold);font-size:18px;margin-bottom:16px;letter-spacing:2px}
.modal-row{display:flex;align-items:center;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--surface2)}
.modal-row label{font-size:14px;color:var(--cream)}
.modal-row .note{font-size:11px;color:var(--text-dim);margin-top:2px}
.toggle{
  width:48px;height:28px;border-radius:14px;background:var(--surface3);
  position:relative;cursor:pointer;transition:background .2s;border:none;flex-shrink:0;
}
.toggle.on{background:var(--gold-dim)}
.toggle::after{
  content:'';position:absolute;top:3px;left:3px;width:22px;height:22px;
  border-radius:50%;background:var(--cream);transition:transform .2s;
}
.toggle.on::after{transform:translateX(20px)}
.modal-close{
  width:100%;padding:14px;border:none;border-radius:12px;margin-top:16px;
  background:var(--surface2);color:var(--gold);font-family:'Cinzel',serif;
  font-size:16px;font-weight:700;cursor:pointer;letter-spacing:2px;
}
.player-setup{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.player-setup .player-chip{opacity:1}
.player-setup .player-chip.inactive{opacity:.3}

/* Animations */
@keyframes dieShake{
  0%{transform:rotate(0) scale(1)}
  20%{transform:rotate(-15deg) scale(1.1)}
  40%{transform:rotate(12deg) scale(.95)}
  60%{transform:rotate(-8deg) scale(1.05)}
  80%{transform:rotate(4deg) scale(.98)}
  100%{transform:rotate(0) scale(1)}
}
@keyframes robberPulse{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes chipIn{from{transform:scale(0);opacity:0}to{transform:scale(1);opacity:1}}
</style>
</head>
<body>
<div class="app">
  <div class="header">
    <div class="logo">Catan</div>
    <div class="turn-badge">Roll <span id="rollCount">0</span></div>
  </div>

  <div class="players" id="playerBar"></div>

  <div class="dice-zone">
    <div class="dice-row">
      <div class="die" id="die1"><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div></div>
      <div class="die" id="die2"><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div><div class="pip"></div></div>
    </div>
    <div class="total-display">
      <div class="total-num" id="totalNum">–</div>
      <div class="robber-alert" id="robberAlert">⚔ Move the Robber ⚔</div>
    </div>
  </div>

  <button class="roll-btn" id="rollBtn" onclick="rollDice()">Roll</button>

  <div class="stats-bar" id="statsBar"></div>
  <div class="history" id="history"></div>

  <div class="bottom-bar">
    <button class="action-btn" onclick="undoRoll()"><span class="icon">↩</span>Undo</button>
    <button class="action-btn" onclick="resetGame()"><span class="icon">↻</span>Reset</button>
    <button class="action-btn" onclick="openSettings()"><span class="icon">⚙</span>Setup</button>
  </div>
</div>

<div class="modal-overlay" id="settingsModal" onclick="closeSettings(event)">
  <div class="modal" onclick="event.stopPropagation()">
    <h2>Game Setup</h2>
    <div style="margin-bottom:12px">
      <label style="font-size:14px;color:var(--cream);display:block;margin-bottom:8px">Players (tap to toggle)</label>
      <div class="player-setup" id="playerSetup"></div>
    </div>
    <div class="modal-row">
      <div>
        <label>Sound & Vibration</label>
        <div class="note">Haptic feedback on roll</div>
      </div>
      <button class="toggle on" id="toggleVibrate" onclick="toggleSetting(this)"></button>
    </div>
    <div class="modal-row">
      <div>
        <label>Auto-advance Turn</label>
        <div class="note">Next player after each roll</div>
      </div>
      <button class="toggle on" id="toggleAutoTurn" onclick="toggleSetting(this)"></button>
    </div>
    <button class="modal-close" onclick="closeSettings()">Done</button>
  </div>
</div>

<script>
const PIP_MAP = {
  1:[0,0,0,0,1,0,0,0,0],
  2:[0,0,1,0,0,0,1,0,0],
  3:[0,0,1,0,1,0,1,0,0],
  4:[1,0,1,0,0,0,1,0,1],
  5:[1,0,1,0,1,0,1,0,1],
  6:[1,0,1,1,0,1,1,0,1]
};

const PLAYER_COLORS = ['red','blue','white','orange','green','brown'];
const PLAYER_NAMES = ['Red','Blue','White','Orange','Green','Brown'];

let state = {
  rolls: [],
  counts: {2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0},
  players: ['red','blue','white','orange'],
  currentPlayer: 0,
  rolling: false,
  vibrate: true,
  autoTurn: true
};

function init() {
  loadState();
  buildStats();
  renderPlayers();
  renderHistory();
  updateStats();
  document.getElementById('rollCount').textContent = state.rolls.length;
  if (state.rolls.length > 0) {
    const last = state.rolls[state.rolls.length - 1];
    showDie('die1', last.d1);
    showDie('die2', last.d2);
    document.getElementById('totalNum').textContent = last.total;
    if (last.total === 7) document.getElementById('totalNum').classList.add('robber');
  }
}

function buildStats() {
  const bar = document.getElementById('statsBar');
  bar.innerHTML = '';
  for (let n = 2; n <= 12; n++) {
    const col = document.createElement('div');
    col.className = 'stat-col';
    col.innerHTML = `<div class="stat-count" id="sc${n}"></div><div class="stat-bar-wrap"><div class="stat-bar${n===7?' robber-bar':''}" id="sb${n}"></div></div><div class="stat-label${n===7?' seven':''}">${n}</div>`;
    bar.appendChild(col);
  }
}

function showDie(id, val) {
  const pips = document.getElementById(id).querySelectorAll('.pip');
  const map = PIP_MAP[val];
  pips.forEach((p, i) => p.classList.toggle('show', !!map[i]));
}

function rollDice() {
  if (state.rolling) return;
  state.rolling = true;

  const btn = document.getElementById('rollBtn');
  btn.style.pointerEvents = 'none';

  if (state.vibrate && navigator.vibrate) navigator.vibrate(30);

  const d1 = document.getElementById('die1');
  const d2 = document.getElementById('die2');
  d1.classList.add('rolling');
  d2.classList.add('rolling');

  // Flash random faces during animation
  let flashes = 0;
  const flashInterval = setInterval(() => {
    showDie('die1', Math.ceil(Math.random() * 6));
    showDie('die2', Math.ceil(Math.random() * 6));
    flashes++;
    if (flashes > 6) clearInterval(flashInterval);
  }, 60);

  setTimeout(() => {
    clearInterval(flashInterval);
    d1.classList.remove('rolling');
    d2.classList.remove('rolling');

    const v1 = Math.ceil(Math.random() * 6);
    const v2 = Math.ceil(Math.random() * 6);
    const total = v1 + v2;

    showDie('die1', v1);
    showDie('die2', v2);

    const totalEl = document.getElementById('totalNum');
    totalEl.textContent = total;
    totalEl.classList.toggle('robber', total === 7);

    const alert = document.getElementById('robberAlert');
    alert.classList.remove('show');
    if (total === 7) {
      void alert.offsetWidth; // reflow
      alert.classList.add('show');
      if (state.vibrate && navigator.vibrate) navigator.vibrate([50, 50, 100]);
    }

    state.counts[total]++;
    state.rolls.push({ d1: v1, d2: v2, total, player: state.currentPlayer });
    document.getElementById('rollCount').textContent = state.rolls.length;

    if (state.autoTurn && state.players.length > 0) {
      state.currentPlayer = (state.currentPlayer + 1) % state.players.length;
      renderPlayers();
    }

    updateStats();
    renderHistory();
    saveState();

    btn.style.pointerEvents = '';
    state.rolling = false;
  }, 420);
}

function updateStats() {
  const max = Math.max(1, ...Object.values(state.counts));
  const maxH = 50;
  const lastTotal = state.rolls.length ? state.rolls[state.rolls.length - 1].total : null;
  for (let n = 2; n <= 12; n++) {
    const bar = document.getElementById('sb' + n);
    const count = document.getElementById('sc' + n);
    const h = state.counts[n] > 0 ? Math.max(4, (state.counts[n] / max) * maxH) : 2;
    bar.style.height = h + 'px';
    bar.classList.toggle('has-rolls', state.counts[n] > 0);
    bar.classList.toggle('highlight', n === lastTotal);
    count.textContent = state.counts[n] > 0 ? state.counts[n] : '';
  }
}

function renderHistory() {
  const el = document.getElementById('history');
  const recent = state.rolls.slice(-20).reverse();
  el.innerHTML = recent.map((r, i) =>
    `<div class="hist-chip${r.total===7?' seven':''}"${i===0?' style="animation:chipIn .3s"':''}>${r.total}</div>`
  ).join('');
}

function renderPlayers() {
  const bar = document.getElementById('playerBar');
  bar.innerHTML = '';
  state.players.forEach((c, i) => {
    const chip = document.createElement('div');
    chip.className = `player-chip${i === state.currentPlayer ? ' active' : ''}`;
    chip.dataset.color = c;
    chip.textContent = PLAYER_NAMES[PLAYER_COLORS.indexOf(c)];
    chip.onclick = () => { state.currentPlayer = i; renderPlayers(); saveState(); };
    bar.appendChild(chip);
  });
}

function renderPlayerSetup() {
  const el = document.getElementById('playerSetup');
  el.innerHTML = '';
  PLAYER_COLORS.forEach((c, i) => {
    const chip = document.createElement('div');
    const active = state.players.includes(c);
    chip.className = `player-chip${active ? '' : ' inactive'}`;
    chip.dataset.color = c;
    chip.textContent = PLAYER_NAMES[i];
    chip.onclick = () => {
      if (active) {
        state.players = state.players.filter(p => p !== c);
      } else {
        state.players.push(c);
      }
      if (state.currentPlayer >= state.players.length) state.currentPlayer = 0;
      renderPlayerSetup();
      renderPlayers();
      saveState();
    };
    el.appendChild(chip);
  });
}

function undoRoll() {
  if (!state.rolls.length) return;
  const last = state.rolls.pop();
  state.counts[last.total]--;
  if (state.autoTurn && state.players.length > 0) {
    state.currentPlayer = last.player;
  }
  document.getElementById('rollCount').textContent = state.rolls.length;
  if (state.rolls.length > 0) {
    const prev = state.rolls[state.rolls.length - 1];
    showDie('die1', prev.d1);
    showDie('die2', prev.d2);
    document.getElementById('totalNum').textContent = prev.total;
    document.getElementById('totalNum').classList.toggle('robber', prev.total === 7);
  } else {
    document.getElementById('totalNum').textContent = '–';
    document.getElementById('totalNum').classList.remove('robber');
    ['die1','die2'].forEach(id => document.getElementById(id).querySelectorAll('.pip').forEach(p => p.classList.remove('show')));
  }
  document.getElementById('robberAlert').classList.remove('show');
  updateStats();
  renderHistory();
  renderPlayers();
  saveState();
  if (navigator.vibrate && state.vibrate) navigator.vibrate(10);
}

function resetGame() {
  if (state.rolls.length === 0) return;
  if (!confirm('Reset all rolls?')) return;
  state.rolls = [];
  state.counts = {2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0};
  state.currentPlayer = 0;
  document.getElementById('rollCount').textContent = 0;
  document.getElementById('totalNum').textContent = '–';
  document.getElementById('totalNum').classList.remove('robber');
  document.getElementById('robberAlert').classList.remove('show');
  ['die1','die2'].forEach(id => document.getElementById(id).querySelectorAll('.pip').forEach(p => p.classList.remove('show')));
  updateStats();
  renderHistory();
  renderPlayers();
  saveState();
}

function openSettings() {
  renderPlayerSetup();
  document.getElementById('toggleVibrate').classList.toggle('on', state.vibrate);
  document.getElementById('toggleAutoTurn').classList.toggle('on', state.autoTurn);
  document.getElementById('settingsModal').classList.add('open');
}

function closeSettings(e) {
  if (e && e.target !== document.getElementById('settingsModal')) return;
  document.getElementById('settingsModal').classList.remove('open');
}

function toggleSetting(el) {
  el.classList.toggle('on');
  if (el.id === 'toggleVibrate') state.vibrate = el.classList.contains('on');
  if (el.id === 'toggleAutoTurn') state.autoTurn = el.classList.contains('on');
  saveState();
}

function saveState() {
  try { localStorage.setItem('catan_state', JSON.stringify(state)); } catch(e) {}
}

function loadState() {
  try {
    const s = JSON.parse(localStorage.getItem('catan_state'));
    if (s) {
      state = { ...state, ...s };
    }
  } catch(e) {}
}

// Keyboard shortcut
document.addEventListener('keydown', e => { if (e.code === 'Space' || e.key === 'Enter') { e.preventDefault(); rollDice(); }});

init();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "Catan Roller",
        "short_name": "Catan",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1a0f0a",
        "theme_color": "#2c1810",
        "description": "Dice roller & stats tracker for Settlers of Catan",
        "icons": [
            {"src": "/icon", "sizes": "192x192", "type": "image/svg+xml"},
            {"src": "/icon", "sizes": "512x512", "type": "image/svg+xml"}
        ]
    })

@app.route('/icon')
def icon():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192">
    <rect width="192" height="192" rx="40" fill="#2c1810"/>
    <text x="96" y="120" text-anchor="middle" font-family="serif" font-weight="900" font-size="100" fill="#d4a843">⚄</text>
    </svg>'''
    return svg, 200, {'Content-Type': 'image/svg+xml'}

if __name__ == '__main__':
    app.run(debug=True)
