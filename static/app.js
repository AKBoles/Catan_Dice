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
    col.innerHTML = '<div class="stat-count" id="sc' + n + '"></div><div class="stat-bar-wrap"><div class="stat-bar' + (n===7?' robber-bar':'') + '" id="sb' + n + '"></div></div><div class="stat-label' + (n===7?' seven':'') + '">' + n + '</div>';
    bar.appendChild(col);
  }
}

function showDie(id, val) {
  const pips = document.getElementById(id).querySelectorAll('.pip');
  const map = PIP_MAP[val];
  pips.forEach(function(p, i) { p.classList.toggle('show', !!map[i]); });
}

function rollDice() {
  if (state.rolling) return;
  state.rolling = true;

  var btn = document.getElementById('rollBtn');
  btn.style.pointerEvents = 'none';

  if (state.vibrate && navigator.vibrate) navigator.vibrate(30);

  var d1 = document.getElementById('die1');
  var d2 = document.getElementById('die2');
  d1.classList.add('rolling');
  d2.classList.add('rolling');

  var flashes = 0;
  var flashInterval = setInterval(function() {
    showDie('die1', Math.ceil(Math.random() * 6));
    showDie('die2', Math.ceil(Math.random() * 6));
    flashes++;
    if (flashes > 6) clearInterval(flashInterval);
  }, 60);

  setTimeout(function() {
    clearInterval(flashInterval);
    d1.classList.remove('rolling');
    d2.classList.remove('rolling');

    var v1 = Math.ceil(Math.random() * 6);
    var v2 = Math.ceil(Math.random() * 6);
    var total = v1 + v2;

    showDie('die1', v1);
    showDie('die2', v2);

    var totalEl = document.getElementById('totalNum');
    totalEl.textContent = total;
    totalEl.classList.toggle('robber', total === 7);

    var alert = document.getElementById('robberAlert');
    alert.classList.remove('show');
    if (total === 7) {
      void alert.offsetWidth;
      alert.classList.add('show');
      if (state.vibrate && navigator.vibrate) navigator.vibrate([50, 50, 100]);
    }

    state.counts[total]++;
    state.rolls.push({ d1: v1, d2: v2, total: total, player: state.currentPlayer });
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
  var max = Math.max(1, Math.max.apply(null, Object.values(state.counts)));
  var maxH = 50;
  var lastTotal = state.rolls.length ? state.rolls[state.rolls.length - 1].total : null;
  for (var n = 2; n <= 12; n++) {
    var bar = document.getElementById('sb' + n);
    var count = document.getElementById('sc' + n);
    var h = state.counts[n] > 0 ? Math.max(4, (state.counts[n] / max) * maxH) : 2;
    bar.style.height = h + 'px';
    bar.classList.toggle('has-rolls', state.counts[n] > 0);
    bar.classList.toggle('highlight', n === lastTotal);
    count.textContent = state.counts[n] > 0 ? state.counts[n] : '';
  }
}

function renderHistory() {
  var el = document.getElementById('history');
  var recent = state.rolls.slice(-20).reverse();
  el.innerHTML = recent.map(function(r, i) {
    return '<div class="hist-chip' + (r.total===7?' seven':'') + '"' + (i===0?' style="animation:chipIn .3s"':'') + '>' + r.total + '</div>';
  }).join('');
}

function renderPlayers() {
  var bar = document.getElementById('playerBar');
  bar.innerHTML = '';
  state.players.forEach(function(c, i) {
    var chip = document.createElement('div');
    chip.className = 'player-chip' + (i === state.currentPlayer ? ' active' : '');
    chip.dataset.color = c;
    chip.textContent = PLAYER_NAMES[PLAYER_COLORS.indexOf(c)];
    chip.onclick = function() { state.currentPlayer = i; renderPlayers(); saveState(); };
    bar.appendChild(chip);
  });
}

function renderPlayerSetup() {
  var el = document.getElementById('playerSetup');
  el.innerHTML = '';
  PLAYER_COLORS.forEach(function(c, i) {
    var active = state.players.includes(c);
    var chip = document.createElement('div');
    chip.className = 'player-chip' + (active ? '' : ' inactive');
    chip.dataset.color = c;
    chip.textContent = PLAYER_NAMES[i];
    chip.onclick = function() {
      if (active) {
        state.players = state.players.filter(function(p) { return p !== c; });
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
  var last = state.rolls.pop();
  state.counts[last.total]--;
  if (state.autoTurn && state.players.length > 0) {
    state.currentPlayer = last.player;
  }
  document.getElementById('rollCount').textContent = state.rolls.length;
  if (state.rolls.length > 0) {
    var prev = state.rolls[state.rolls.length - 1];
    showDie('die1', prev.d1);
    showDie('die2', prev.d2);
    document.getElementById('totalNum').textContent = prev.total;
    document.getElementById('totalNum').classList.toggle('robber', prev.total === 7);
  } else {
    document.getElementById('totalNum').textContent = '\u2013';
    document.getElementById('totalNum').classList.remove('robber');
    ['die1','die2'].forEach(function(id) {
      document.getElementById(id).querySelectorAll('.pip').forEach(function(p) { p.classList.remove('show'); });
    });
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
  document.getElementById('totalNum').textContent = '\u2013';
  document.getElementById('totalNum').classList.remove('robber');
  document.getElementById('robberAlert').classList.remove('show');
  ['die1','die2'].forEach(function(id) {
    document.getElementById(id).querySelectorAll('.pip').forEach(function(p) { p.classList.remove('show'); });
  });
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
    var s = JSON.parse(localStorage.getItem('catan_state'));
    if (s) {
      state.rolls = s.rolls || [];
      state.counts = s.counts || {2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0};
      state.players = s.players || ['red','blue','white','orange'];
      state.currentPlayer = s.currentPlayer || 0;
      state.vibrate = s.vibrate !== undefined ? s.vibrate : true;
      state.autoTurn = s.autoTurn !== undefined ? s.autoTurn : true;
    }
  } catch(e) {}
}

document.addEventListener('keydown', function(e) {
  if (e.code === 'Space' || e.key === 'Enter') { e.preventDefault(); rollDice(); }
});

// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/service-worker.js').catch(function() {});
}

init();
