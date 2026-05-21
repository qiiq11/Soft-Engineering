import { useState } from 'react'
import GameCanvas from './GameCanvas.jsx'
import { api, startGame } from './api.js'

export default function App() {
  const [sessionId, setSessionId] = useState(null)
  const [player, setPlayer] = useState(null)
  const [room, setRoom] = useState(null)
  const [status, setStatus] = useState(null)
  const [inventory, setInventory] = useState([])
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)
  const [gameOver, setGameOver] = useState(false)
  const [nameInput, setNameInput] = useState('冒险者')

  const pushLog = (msg) => setLogs((prev) => [...prev.slice(-30), msg])

  const refresh = async (sid, client) => {
    const [p, s, r, inv] = await Promise.all([
      client.getPlayer(),
      client.getStatus(),
      client.getRoom(),
      client.getInventory(),
    ])
    setPlayer(p)
    setStatus(s)
    setRoom(r)
    setInventory(inv.items?.map((i) => i.name) || [])
  }

  const handleStart = async () => {
    setLoading(true)
    try {
      const data = await startGame(nameInput)
      setSessionId(data.sessionId)
      setPlayer(data.player)
      setRoom(data.room)
      setGameOver(false)
      pushLog(data.message)
      await refresh(data.sessionId, api(data.sessionId))
    } catch (e) {
      pushLog(`启动失败: ${e.message}`)
    } finally {
      setLoading(false)
    }
  }

  const withClient = async (fn) => {
    if (!sessionId || gameOver) return
    setLoading(true)
    const client = api(sessionId)
    try {
      const res = await fn(client)
      if (res.logs) res.logs.forEach(pushLog)
      else if (res.message) pushLog(String(res.message).split('\n')[0])
      if (res.gameOver) setGameOver(true)
      await refresh(sessionId, client)
    } catch (e) {
      pushLog(`错误: ${e.message}`)
    } finally {
      setLoading(false)
    }
  }

  if (!sessionId) {
    return (
      <div className="app start-screen">
        <h1>MUD 2D Web</h1>
        <p>迭代 5 — 前后端分离图形界面</p>
        <input value={nameInput} onChange={(e) => setNameInput(e.target.value)} placeholder="玩家名" />
        <button onClick={handleStart} disabled={loading}>
          {loading ? '连接中...' : '开始冒险'}
        </button>
      </div>
    )
  }

  return (
    <div className="app">
      <header>
        <h1>MUD 2D</h1>
        <div className="stats">
          <span>{player?.name}</span>
          <span>HP {player?.hp}/{player?.maxHp}</span>
          <span>{status?.status}</span>
          {gameOver && <span className="game-over">游戏结束</span>}
        </div>
      </header>

      <main className="layout">
        <section className="canvas-panel">
          <GameCanvas
            room={room}
            player={player}
            disabled={loading || gameOver}
            onMove={(dir) => withClient((c) => c.move(dir))}
            onPickup={(item) => withClient((c) => c.pickup(item))}
          />
          <div className="dir-pad">
            {['north', 'south', 'east', 'west'].map((d) => (
              <button
                key={d}
                disabled={loading || gameOver || !room?.exits?.includes(d)}
                onClick={() => withClient((c) => c.move(d))}
              >
                {d}
              </button>
            ))}
          </div>
        </section>

        <aside className="side-panel">
          <h3>背包</h3>
          <ul>
            {inventory.length ? inventory.map((i) => (
              <li key={i}>
                {i}
                <button disabled={loading || gameOver} onClick={() => withClient((c) => c.drop(i))}>丢</button>
              </li>
            )) : <li>空</li>}
          </ul>
          <div className="actions">
            <button disabled={loading || gameOver} onClick={() => withClient((c) => c.attack())}>攻击</button>
            <button disabled={loading} onClick={() => withClient((c) => c.look())}>查看</button>
          </div>
          <h3>日志</h3>
          <div className="logs">
            {logs.map((l, i) => (
              <div key={i}>{l}</div>
            ))}
          </div>
        </aside>
      </main>
    </div>
  )
}
