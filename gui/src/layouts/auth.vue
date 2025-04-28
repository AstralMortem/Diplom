<template>
  <div class="w-screen h-screen flex flex-col gap-8">
        <div class="w-full h-max p-2">
            <header class="bg-gray-300 dark:bg-gray-800 text-white p-4 flex items-center justify-start w-full rounded-lg">
                <ULink to="/" class="text-2xl font-bold hover:underline">MedVoice</ULink>
            </header>
        </div>
        
        <div class="w-full h-full flex-1 justify-center items-start flex">
            <slot/>
        </div>
    </div>
</template>

<script lang="ts" setup>

</script>

<style>

</style>