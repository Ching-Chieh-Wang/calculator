<template>
  <button
    :class="[
      'h-14 md:h-16 rounded-full text-2xl active:opacity-80 focus:outline-none',
      isOperator ? 'bg-orange-500 text-white font-semibold active:opacity-90' : 'bg-neutral-700 text-white',
      extraClass || ''
    ]"
    @click="onClick"
    :aria-label="ariaLabel || label"
  >
    {{ label }}
  </button>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    required: true
  },
  onClick: {
    type: Function,
    required: true
  },
  isOperator: {
    type: Boolean,
    default: false
  },
  ariaLabel: String,
  extraClass: String
});
</script>