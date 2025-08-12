<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { calcApi } from '../api/calculateApi'
import CalculateButton from '../components/CalculateButton.vue'

// --- state ---
const display = ref('0')
const prev = ref(null)          // previous number
const op = ref(null)            // current operator: '+','-','*','/'
const justEvaluated = ref(false)
const history = ref([])
const showHistory = ref(false)


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
  }
  op.value = nextOp
  justEvaluated.value = true
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
        <CalculateButton label="AC" :on-click="clearAll" :is-operator=false aria-label="All Clear" />
        <CalculateButton label="+/−" :on-click="toggleSign" :is-operator=false aria-label="Toggle sign" />
        <CalculateButton label="%" :on-click="percent" :is-operator=false aria-label="Percent" />
        <CalculateButton label="÷" :on-click="() => setOp('/')" :is-operator=true :extra-class="op==='/' ? 'ring-2 ring-white/70' : ''" aria-label="Divide" />

        <!-- Row: 7 8 9 × -->
        <CalculateButton label="7" :on-click="() => pressDigit('7')" :is-operator=false />
        <CalculateButton label="8" :on-click="() => pressDigit('8')" :is-operator=false />
        <CalculateButton label="9" :on-click="() => pressDigit('9')" :is-operator=false />
        <CalculateButton label="×" :on-click="() => setOp('*')" :is-operator=true :extra-class="op==='*' ? 'ring-2 ring-white/70' : ''" aria-label="Multiply" />

        <!-- Row: 4 5 6 − -->
        <CalculateButton label="4" :on-click="() => pressDigit('4')" :is-operator=false />
        <CalculateButton label="5" :on-click="() => pressDigit('5')" :is-operator=false />
        <CalculateButton label="6" :on-click="() => pressDigit('6')" :is-operator=false />
        <CalculateButton label="−" :on-click="() => setOp('-')" :is-operator=true :extra-class="op==='-' ? 'ring-2 ring-white/70' : ''" aria-label="Minus" />

        <!-- Row: 1 2 3 + -->
        <CalculateButton label="1" :on-click="() => pressDigit('1')" :is-operator=false />
        <CalculateButton label="2" :on-click="() => pressDigit('2')" :is-operator=false />
        <CalculateButton label="3" :on-click="() => pressDigit('3')" :is-operator=false />
        <CalculateButton label="+" :on-click="() => setOp('+')" :is-operator=true :extra-class="op==='+' ? 'ring-2 ring-white/70' : ''" aria-label="Plus" />

        <!-- Row: 0 (wide) . = -->
        <CalculateButton label="0" :on-click="() => pressDigit('0')" :is-operator=false :extra-class="'col-span-2 flex items-center justify-start pl-6'" />
        <CalculateButton label="." :on-click="() => pressDigit('.')" :is-operator=false />
        <CalculateButton label="=" :on-click="evaluate" :is-operator=true aria-label="Equals" />
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