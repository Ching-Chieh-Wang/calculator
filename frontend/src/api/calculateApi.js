const BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

async function req(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json()
}

// four ops — call backend for each operation
export const calcApi = {
  add: ({ num1, num2 }) => req('/add', { method: 'POST', body: JSON.stringify({ num1, num2 }) }),
  sub: ({ num1, num2 }) => req('/subtract', { method: 'POST', body: JSON.stringify({ num1, num2 }) }),
  mul: ({ num1, num2 }) => req('/multiply', { method: 'POST', body: JSON.stringify({ num1, num2 }) }),
  div: ({ num1, num2 }) => req('/divide', { method: 'POST', body: JSON.stringify({ num1, num2 }) }),
  history: () => req('/history', { method: 'GET' }),
}