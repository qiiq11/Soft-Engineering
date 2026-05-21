import { useEffect, useRef } from 'react'

const EXIT_POS = {
  north: { x: 200, y: 40, label: '北' },
  south: { x: 200, y: 260, label: '南' },
  east: { x: 340, y: 150, label: '东' },
  west: { x: 60, y: 150, label: '西' },
}

export default function GameCanvas({ room, player, onMove, onPickup, disabled }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas || !room) return
    const ctx = canvas.getContext('2d')
    const w = canvas.width
    const h = canvas.height

    ctx.fillStyle = '#1a1f2e'
    ctx.fillRect(0, 0, w, h)

    ctx.fillStyle = '#2d3a52'
    ctx.fillRect(80, 70, 240, 160)
    ctx.strokeStyle = '#6ee7b7'
    ctx.lineWidth = 2
    ctx.strokeRect(80, 70, 240, 160)

    ctx.fillStyle = '#e2e8f0'
    ctx.font = 'bold 16px sans-serif'
    ctx.fillText(room.name, 100, 95)
    ctx.font = '12px sans-serif'
    wrapText(ctx, room.description, 100, 115, 200, 16)

    if (room.isSafe) {
      ctx.fillStyle = '#6ee7b7'
      ctx.fillText('安全区', 100, 200)
    }

    room.exits?.forEach((dir) => {
      const pos = EXIT_POS[dir]
      if (!pos) return
      ctx.beginPath()
      ctx.arc(pos.x, pos.y, 22, 0, Math.PI * 2)
      ctx.fillStyle = disabled ? '#475569' : '#0ea5e9'
      ctx.fill()
      ctx.fillStyle = '#fff'
      ctx.font = 'bold 14px sans-serif'
      ctx.textAlign = 'center'
      ctx.fillText(pos.label, pos.x, pos.y + 5)
      ctx.textAlign = 'left'
    })

    room.items?.forEach((item, i) => {
      const x = 110 + (i % 3) * 70
      const y = 210 + Math.floor(i / 3) * 24
      ctx.fillStyle = '#fbbf24'
      ctx.fillRect(x, y, 60, 20)
      ctx.fillStyle = '#1a1f2e'
      ctx.font = '11px sans-serif'
      ctx.fillText(item.slice(0, 4), x + 6, y + 14)
    })

    if (room.enemy) {
      ctx.fillStyle = '#ef4444'
      ctx.beginPath()
      ctx.arc(280, 180, 28, 0, Math.PI * 2)
      ctx.fill()
      ctx.fillStyle = '#fff'
      ctx.font = '12px sans-serif'
      ctx.fillText(room.enemy.name, 248, 185)
      ctx.fillText(`HP ${room.enemy.hp}`, 252, 200)
    }

    if (player) {
      ctx.fillStyle = '#38bdf8'
      ctx.beginPath()
      ctx.arc(150, 180, 20, 0, Math.PI * 2)
      ctx.fill()
      ctx.fillStyle = '#fff'
      ctx.font = '11px sans-serif'
      ctx.fillText(player.name?.slice(0, 4) || '玩家', 132, 184)
    }
  }, [room, player, disabled])

  const handleClick = (e) => {
    if (disabled || !room) return
    const rect = canvasRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    for (const [dir, pos] of Object.entries(EXIT_POS)) {
      const dx = x - pos.x
      const dy = y - pos.y
      if (dx * dx + dy * dy <= 22 * 22 && room.exits?.includes(dir)) {
        onMove?.(dir)
        return
      }
    }

    room.items?.forEach((item, i) => {
      const ix = 110 + (i % 3) * 70
      const iy = 210 + Math.floor(i / 3) * 24
      if (x >= ix && x <= ix + 60 && y >= iy && y <= iy + 20) {
        onPickup?.(item)
      }
    })
  }

  return (
    <canvas
      ref={canvasRef}
      width={400}
      height={300}
      className="game-canvas"
      onClick={handleClick}
      title="点击出口移动，点击物品拾取"
    />
  )
}

function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
  const words = text.split('')
  let line = ''
  let cy = y
  for (const ch of words) {
    const test = line + ch
    if (ctx.measureText(test).width > maxWidth) {
      ctx.fillText(line, x, cy)
      line = ch
      cy += lineHeight
    } else {
      line = test
    }
  }
  if (line) ctx.fillText(line, x, cy)
}
