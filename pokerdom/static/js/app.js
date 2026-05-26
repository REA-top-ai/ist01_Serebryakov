'use strict';

const DECK_IMG_BASE = 'https://deckofcardsapi.com/static/img';

function cardToApiCode(cardId) {
  const rank = cardId[0].toUpperCase();
  const suit = cardId[1].toUpperCase();
  return (rank === 'T' ? '0' : rank) + suit;
}

function cardImageUrl(cardId) {
  return `${DECK_IMG_BASE}/${cardToApiCode(cardId)}.png`;
}


const state = {
  holeCards:      [],
  communityCards: [],
  mode:           'hole',
};


const $ = id => document.getElementById(id);
function showEl(id) { const el = $(id); if (el) el.classList.remove('d-none'); }
function hideEl(id) { const el = $(id); if (el) el.classList.add('d-none'); }
function setText(id, txt) { const el = $(id); if (el) el.textContent = txt; }

function isCardUsed(cardId) {
  return state.holeCards.includes(cardId) || state.communityCards.includes(cardId);
}

function selectCard(cardId) {
  if (state.holeCards.includes(cardId)) {
    state.holeCards = state.holeCards.filter(c => c !== cardId);
  } else if (state.communityCards.includes(cardId)) {
    state.communityCards = state.communityCards.filter(c => c !== cardId);
  } else if (state.mode === 'hole') {
    if (state.holeCards.length < 2) state.holeCards.push(cardId);
  } else {
    if (state.communityCards.length < 5) state.communityCards.push(cardId);
  }
  updateUI();
}

function clearAll() {
  state.holeCards      = [];
  state.communityCards = [];
  updateUI();
  hideEl('resultPanel');
  hideEl('aiPanel');
  showEl('resultsPlaceholder');
  hideEl('errorAlert');
}


function updateUI() {
  updateCardGrid();
  updateSlots();
  updateHandSummary();
}

function updateCardGrid() {
  document.querySelectorAll('.playing-card-btn').forEach(btn => {
    const cardId = btn.dataset.card;
    btn.classList.remove('selected-hole', 'selected-comm', 'used');
    if (state.holeCards.includes(cardId))      btn.classList.add('selected-hole');
    else if (state.communityCards.includes(cardId)) btn.classList.add('selected-comm');
    else if (!isCardUsed(cardId)) {
      if (state.mode === 'hole'      && state.holeCards.length >= 2)      btn.classList.add('used');
      if (state.mode === 'community' && state.communityCards.length >= 5) btn.classList.add('used');
    }
  });
}

function updateSlots() {
  setText('holeCount', `${state.holeCards.length}/2`);
  for (let i = 0; i < 2; i++) {
    const slot = $(`holeSlot${i}`);
    if (!slot) continue;
    slot.innerHTML = '';
    if (state.holeCards[i]) {
      slot.classList.remove('empty');
      slot.style.position = 'relative';
      const img = document.createElement('img');
      img.src = cardImageUrl(state.holeCards[i]);
      img.alt = state.holeCards[i];
      img.style.cssText = 'width:100%;height:100%;object-fit:cover;border-radius:4px';
      img.onerror = () => { slot.innerHTML = `<span style="font-size:.7rem;font-weight:700;color:#e2e8f0">${state.holeCards[i]}</span>`; };
      const del = makeDelBtn(() => { state.holeCards.splice(i, 1); updateUI(); });
      slot.appendChild(img);
      slot.appendChild(del);
    } else {
      slot.classList.add('empty');
    }
  }

  setText('commCount', `${state.communityCards.length}/5`);
  for (let i = 0; i < 5; i++) {
    const slot = $(`commSlot${i}`);
    if (!slot) continue;
    slot.innerHTML = '';
    if (state.communityCards[i]) {
      slot.classList.remove('empty');
      slot.style.position = 'relative';
      const img = document.createElement('img');
      img.src = cardImageUrl(state.communityCards[i]);
      img.alt = state.communityCards[i];
      img.style.cssText = 'width:100%;height:100%;object-fit:cover;border-radius:4px';
      img.onerror = () => { slot.innerHTML = `<span style="font-size:.65rem;font-weight:700;color:#e2e8f0">${state.communityCards[i]}</span>`; };
      const del = makeDelBtn(() => { state.communityCards.splice(i, 1); updateUI(); });
      slot.appendChild(img);
      slot.appendChild(del);
    } else {
      slot.classList.add('empty');
    }
  }
}

function makeDelBtn(onclick) {
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.innerHTML = '×';
  btn.style.cssText = 'position:absolute;top:1px;right:2px;background:rgba(220,53,69,.8);'
    + 'color:#fff;border:none;border-radius:50%;width:14px;height:14px;font-size:10px;'
    + 'line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;';
  btn.onclick = onclick;
  return btn;
}

function updateHandSummary() {
  const summary = $('handSummary');
  if (!summary) return;
  if (state.holeCards.length >= 1) {
    setText('handSummaryHole', state.holeCards.join(' '));
    setText('handSummaryComm', state.communityCards.join(' ') || 'pre-flop');
    summary.classList.remove('d-none');
  } else {
    summary.classList.add('d-none');
  }
}

async function analyzeHand() {
  if (state.holeCards.length !== 2) {
    showError('Select exactly 2 hole cards before analyzing.');
    return;
  }
  const commLen = state.communityCards.length;
  if (commLen !== 0 && commLen !== 3 && commLen !== 4 && commLen !== 5) {
    showError('Community cards must be 0 (pre-flop), 3 (flop), 4 (turn), or 5 (river).');
    return;
  }

  hideEl('errorAlert');
  setLoading(true);

  const payload = {
    hole_cards: state.holeCards.join(' '),
    board:      state.communityCards.join(' '),
    players:    parseInt($('numPlayers')?.value || 2),
    pot:        parseFloat($('potSize')?.value   || 0),
    bet:        parseFloat($('betToCall')?.value  || 0),
  };

  try {
    const res  = await fetch('/analyze', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();

    if (!res.ok || !data.ok) {
      showError(data.error || 'Analysis failed. Please try again.');
      return;
    }

    renderResults(data.result, data.ai);

  } catch (err) {
    showError('Network error — make sure the server is running.');
    console.error(err);
  } finally {
    setLoading(false);
  }
}

function renderResults(result, ai) {
  hideEl('resultsPlaceholder');

  const resultPanel = $('resultPanel');
  if (resultPanel) { resultPanel.classList.remove('d-none'); resultPanel.classList.add('fade-in'); }

  setText('handNameDisplay', result.hand_name);
  setText('streetDisplay',   result.street.toUpperCase());

  const actionBadge = $('actionBadge');
  if (actionBadge) {
    const action = (ai.action || result.action || 'CALL').toUpperCase();
    actionBadge.textContent = action;
    actionBadge.className = 'badge fs-6 px-3 py-2 ' + actionBadgeClass(action);
  }

  setTimeout(() => {
    setBar('equityWinBar',  result.win  || 0);
    setBar('equityTieBar',  result.tie  || 0);
    setBar('equityLoseBar', result.lose || 0);
    setText('winPct',  `${result.win}%`);
    setText('tiePct',  `${result.tie}%`);
    setText('losePct', `${result.lose}%`);
  }, 50);

  setText('outsDisplay',    result.outs    != null ? result.outs    : '—');
  setText('potOddsDisplay', result.pot_odds != null ? `${result.pot_odds}%` : '—');
  setText('winDisplay',     `${result.win}%`);
  setText('playersDisplay', result.players);
  setText('basicReasoning', result.reason);

  const aiPanel = $('aiPanel');
  if (aiPanel) { aiPanel.classList.remove('d-none'); aiPanel.classList.add('fade-in'); }

  const action = (ai.action || 'CALL').toUpperCase();

  const powBadge  = $('aiPoweredBadge');
  const ruleBadge = $('aiBasicBadge');
  if (powBadge)  powBadge.style.cssText  = ai.ai_powered ? '' : 'display:none!important';
  if (ruleBadge) ruleBadge.style.cssText = ai.ai_powered ? 'display:none!important' : '';

  const actionIcon = $('aiActionIcon');
  if (actionIcon) actionIcon.innerHTML = actionIconHtml(action);

  const actionText = $('aiActionText');
  if (actionText) {
    actionText.textContent = action;
    actionText.className = 'h3 fw-bold mb-0 ' + actionTextClass(action);
  }

  const recText = $('aiRecommendationText');
  if (recText) {
    if (ai.ai_powered && ai.confidence !== undefined) {
      let html = `<strong>${action}</strong> — Confidence: ${ai.confidence}%<br><br>`;
      html += escapeHtml(ai.reasoning || '');
      if (ai.key_insight) html += `<br><br><em class="text-info">💡 ${escapeHtml(ai.key_insight)}</em>`;
      if (ai.bluff_rating !== undefined)
        html += `<br><small class="text-muted">Bluff: ${ai.bluff_rating}/10 · Aggression: ${ai.aggression_rating}/10</small>`;
      recText.innerHTML = html;
    } else {
      recText.textContent = ai.reasoning || result.reason;
    }
  }
}

function setBar(id, pct) {
  const el = $(id);
  if (el) el.style.width = `${Math.max(0, Math.min(100, pct))}%`;
}

function actionBadgeClass(a) {
  if (['RAISE','ALL_IN','BLUFF'].includes(a))         return 'bg-success';
  if (['CALL','CHECK','SLOW_PLAY'].includes(a))        return 'bg-primary';
  return 'bg-danger';
}
function actionTextClass(a) {
  if (['RAISE','ALL_IN','BLUFF'].includes(a))         return 'text-success';
  if (['CALL','CHECK','SLOW_PLAY'].includes(a))        return 'text-primary';
  return 'text-danger';
}
function actionIconHtml(a) {
  const icons = {
    RAISE:     '<i class="bi bi-arrow-up-circle-fill fs-1 text-success"></i>',
    ALL_IN:    '<i class="bi bi-fire fs-1 text-warning"></i>',
    BLUFF:     '<i class="bi bi-mask fs-1 text-warning"></i>',
    CALL:      '<i class="bi bi-check-circle-fill fs-1 text-primary"></i>',
    CHECK:     '<i class="bi bi-dash-circle-fill fs-1 text-info"></i>',
    SLOW_PLAY: '<i class="bi bi-hourglass-split fs-1 text-warning"></i>',
    FOLD:      '<i class="bi bi-x-circle-fill fs-1 text-danger"></i>',
  };
  return icons[a] || '<i class="bi bi-question-circle fs-1 text-secondary"></i>';
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function showError(msg) {
  const el = $('errorAlert'), msgEl = $('errorMessage');
  if (el && msgEl) {
    msgEl.textContent = msg;
    el.classList.remove('d-none');
    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function setLoading(on) {
  const btn = $('analyzeBtn');
  if (!btn) return;
  btn.disabled = on;
  $('analyzeBtnText')?.classList.toggle('d-none', on);
  $('analyzeBtnSpinner')?.classList.toggle('d-none', !on);
}


document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.playing-card-btn').forEach(btn =>
    btn.addEventListener('click', () => selectCard(btn.dataset.card))
  );
  document.querySelectorAll('input[name="cardMode"]').forEach(radio =>
    radio.addEventListener('change', e => { state.mode = e.target.value; updateCardGrid(); })
  );
  $('clearCards')?.addEventListener('click', clearAll);
  $('analyzeBtn')?.addEventListener('click', analyzeHand);
  ['potSize','betToCall','numPlayers','heroStack'].forEach(id =>
    $(id)?.addEventListener('keydown', e => { if (e.key === 'Enter') analyzeHand(); })
  );
  updateUI();
});
