<template>
  <button
    :class="[
      'inline-flex items-center justify-center rounded px-4 py-2 font-medium',
      isOperator ? '!bg-orange-500 hover:!bg-orange-600 !text-white' : 'bg-neutral-700 hover:bg-neutral-600 text-white',
      extraClass,
    ]"
    @click="onClick"
    :aria-label="ariaLabel || label"
    type="button"
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