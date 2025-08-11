<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { calcApi } from '../api/calculateApi'

// --- state ---
const display = ref('0')
const prev = ref(null)          // previous number
const op = ref(null)            // current operator: '+','-','*','/'
const justEvaluated = ref(false)
const history = ref([])
const showHistory = ref(false)

const ops = [
  { label: '÷', val: '/' },
  { label: '×', val: '*' },
  { label: '−', val: '-' },
  { label: '+', val: '+' },
]

// secondary line shows previous + operator
const secondary = computed(() => {
  if (prev.value === null) return ''
  return `${prev.value} ${op.value ?? ''}`.trim()
})

// --- helpers ---
function pressDigit(d) {
  if (display.value === 'Error') display.value = '0'
  if (justEvaluated.value) {
    display.value = (d === '.') ? '0.' : (d === '0' ? '0' : d)
    justEvaluated.value = false
    return
  }
  if (d === '.') {
    if (!display.value.includes('.')) display.value += '.'
    return
  }
  if (display.value === '0') display.value = d
  else display.value += d
}

function backspace() {
  if (justEvaluated.value) return
  if (display.value.length <= 1) display.value = '0'
  else display.value = display.value.slice(0, -1)
}

function toggleSign() {
  if (display.value === '0' || display.value === 'Error') return
  if (display.value.startsWith('-')) display.value = display.value.slice(1)
  else display.value = '-' + display.value
}

function percent() {
  if (display.value === 'Error') return
  const n = Number(display.value)
  if (Number.isFinite(n)) {
    display.value = String(n / 100)
    justEvaluated.value = true
  }
}

function clearAll() {
  display.value = '0'
  prev.value = null
  op.value = null
  justEvaluated.value = false
}

function setOp(nextOp) {
  // if there is a pending op and user already typed a number, compute first
  if (op.value && prev.value !== null && display.value !== '0' && !justEvaluated.value) {
    evaluate().catch(() => {}) // best-effort chain
  } else {
    prev.value = Number(display.value)
    display.value = '0'
  }
  op.value = nextOp
  justEvaluated.value = false
}

async function evaluate() {
  if (op.value == null || prev.value == null) return
  const num1 = prev.value
  const num2 = Number(display.value)

  try {
    let res
    if (op.value === '+') res = await calcApi.add({ num1, num2 })
    if (op.value === '-') res = await calcApi.sub({ num1, num2 })
    if (op.value === '*') res = await calcApi.mul({ num1, num2 })
    if (op.value === '/') res = await calcApi.div({ num1, num2 })

    // Backend returns: { result, expression, timestamp, id, error }
    display.value = String(res.result)
    prev.value = res.result
    op.value = null
    justEvaluated.value = true

    await loadHistory()
  } catch (e) {
    console.error(e)
    display.value = 'Error'
  }
}

async function loadHistory() {
  try {
    history.value = await calcApi.history()
  } catch (e) {
    console.error(e)
  }
}

function formatTime(ts) {
  try { return new Date(ts).toLocaleString() } catch { return ts }
}

// --- keyboard support ---
function onKeydown(e) {
  const k = e.key
  if ((k >= '0' && k <= '9') || k === '.') return pressDigit(k)
  if (k === '+') return setOp('+')
  if (k === '-') return setOp('-')
  if (k === '*') return setOp('*')
  if (k === '/') return setOp('/')
  if (k === 'Enter' || k === '=') return evaluate()
  if (k === 'Backspace') return backspace()
  if (k === 'Escape') return clearAll()
}

onMounted(() => {
  loadHistory()
  window.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div class="min-h-screen bg-black text-white p-4">
    <div class="mx-auto max-w-sm">
      <!-- Display -->
      <div class="pt-8 pb-4 text-right">
        <div class="text-7xl leading-none font-light font-mono tabular-nums select-text">{{ display }}</div>
      </div>

      <!-- Keypad -->
      <div class="grid grid-cols-4 gap-3">
        <!-- Row: AC, +/- , %, ÷ -->
        <button class="h-14 md:h-16 rounded-full bg-neutral-500 text-black text-xl active:opacity-80 focus:outline-none" @click="clearAll" aria-label="All Clear">AC</button>
        <button class="h-14 md:h-16 rounded-full bg-neutral-500 text-black text-xl active:opacity-80 focus:outline-none" @click="toggleSign" aria-label="Toggle sign">+/−</button>
        <button class="h-14 md:h-16 rounded-full bg-neutral-500 text-black text-xl active:opacity-80 focus:outline-none" @click="percent" aria-label="Percent">%</button>
        <button class="h-14 md:h-16 rounded-full bg-orange-500 text-white text-2xl font-semibold active:opacity-90 focus:outline-none" :class="op==='/' ? 'ring-2 ring-white/70' : ''" @click="setOp('/')" aria-label="Divide">÷</button>

        <!-- Row: 7 8 9 × -->
        <button class="h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none" @click="pressDigit('7')">7</button>
        <button class="h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none" @click="pressDigit('8')">8</button>
        <button class="h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none" @click="pressDigit('9')">9</button>
        <button class="h-14 md:h-16 rounded-full bg-orange-500 text-white text-2xl font-semibold active:opacity-90 focus:outline-none" :class="op==='*' ? 'ring-2 ring-white/70' : ''" @click="setOp('*')" aria-label="Multiply">×</button>

        <!-- Row: 4 5 6 − -->
        <button class="h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none" @click="pressDigit('4')">4</button>
        <button class="h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none" @click="pressDigit('5')">5</button>
        <button class="h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none" @click="pressDigit('6')">6</button>
        <button class="h-14 md:h-16 rounded-full bg-orange-500 text-white text-3xl font-semibold active:opacity-90 focus:outline-none" :class="op==='-' ? 'ring-2 ring-white/70' : ''" @click="setOp('-')" aria-label="Minus">−</button>

        <!-- Row: 1 2 3 + -->
        <button class="h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none" @click="pressDigit('1')">1</button>
        <button class="h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none" @click="pressDigit('2')">2</button>
        <button class="h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none" @click="pressDigit('3')">3</button>
        <button class="h-14 md:h-16 rounded-full bg-orange-500 text-white text-3xl font-semibold active:opacity-90 focus:outline-none" :class="op==='+' ? 'ring-2 ring-white/70' : ''" @click="setOp('+')" aria-label="Plus">+</button>

        <!-- Row: 0 (wide) . = -->
        <button class="col-span-2 h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none flex items-center justify-start pl-6" @click="pressDigit('0')">0</button>
        <button class="h-14 md:h-16 rounded-full bg-neutral-700 text-white text-2xl active:opacity-80 focus:outline-none" @click="pressDigit('.')">.</button>
        <button class="h-14 md:h-16 rounded-full bg-orange-500 text-white text-3xl font-semibold active:opacity-90 focus:outline-none" @click="evaluate" aria-label="Equals">=</button>
      </div>

      <!-- Collapsible History (optional) -->
      <div class="mt-6">
        <button class="text-sm text-white/70 underline" @click="showHistory = !showHistory">{{ showHistory ? 'Hide' : 'Show' }} History</button>
        <div v-if="showHistory" class="mt-3 bg-neutral-900 rounded-2xl p-3 border border-white/10">
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-base font-semibold">History</h2>
            <button class="text-sm underline" @click="loadHistory" aria-label="Refresh history">refresh</button>
          </div>
          <ul class="divide-y divide-white/10 max-h-64 overflow-auto">
            <li v-if="!history?.length" class="py-2 text-white/60 text-sm">No history yet.</li>
            <li v-for="(h, i) in history" :key="i" class="py-2 text-sm font-mono flex items-center justify-between">
              <span class="text-white/60 mr-3 shrink-0">{{ formatTime(h.timestamp) }}</span>
              <span class="truncate">{{ h.expression }} = <strong>{{ h.result }}</strong></span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>