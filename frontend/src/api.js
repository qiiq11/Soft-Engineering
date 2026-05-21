const API_BASE = import.meta.env.VITE_API_BASE || '/api'

async function request(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

export function startGame(playerName = '玩家') {
  return request('/game/start', {
    method: 'POST',
    body: JSON.stringify({ playerName }),
  })
}

export function api(sessionId) {
  const h = { 'X-Session-Id': sessionId }
  return {
    getPlayer: () => request('/player', { headers: h }),
    getStatus: () => request('/player/status', { headers: h }),
    getRoom: () => request('/room', { headers: h }),
    getInventory: () => request('/inventory', { headers: h }),
    getHelp: () => request('/help', { headers: h }),
    move: (direction) =>
      request('/movement', { method: 'POST', headers: h, body: JSON.stringify({ direction }) }),
    attack: () => request('/combat/attack', { method: 'POST', headers: h }),
    pickup: (item) =>
      request('/item/pickup', { method: 'POST', headers: h, body: JSON.stringify({ item }) }),
    drop: (item) =>
      request('/item/drop', { method: 'POST', headers: h, body: JSON.stringify({ item }) }),
    look: () => request('/game/look', { method: 'POST', headers: h }),
  }
}
