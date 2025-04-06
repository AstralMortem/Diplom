<script setup lang="ts">
defineProps(["label"])
</script>

<template>
<div class="flex flex-col gap-1 text-xl font-bold items-start ">
  <p class="text-neutral-500 text-sm font-normal">{{label}}</p>
  <slot/>
</div>
</template>

<style scoped>

</style>