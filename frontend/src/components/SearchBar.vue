<!-- frontend/src/components/SearchBar.vue -->

<script setup>
const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: 'Search' },
  maxWidth: { type: String, default: '320px' }
})

const emit = defineEmits(['update:modelValue'])

function onInput(event) {
  emit('update:modelValue', event.target.value)
}
</script>

<template>
  <input
    :value="props.modelValue"
    @input="onInput"
    class="form-control"
    :style="{ maxWidth: props.maxWidth }"
    :placeholder="props.placeholder"
  >
</template>
