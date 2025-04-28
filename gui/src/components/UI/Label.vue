<script setup lang="ts">
defineProps({
  label: {
    type: String,
    required: true
  }
})
</script>

<template>
<div class="flex flex-col gap-1 text-base font-semibold items-start ">
  <p class="text-neutral-500 text-sm font-normal">{{label}}</p>
  <slot/>
</div>
</template>

<style scoped>

</style>