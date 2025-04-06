<script setup lang="ts">
useBackButton().value = true

</script>

<template>
    <div class="flex flex-col-reverse md:flex-row gap-4 w-full">
        <TranscriptionArea class="w-full h-full"/>
        <UCard class="w-auto">
            <div class="flex flex-col gap-6 w-max ">
                <TranscriptionRecorder/>
                <TranscriptionParamsList/>
            </div>
        </UCard>
    </div>
</template>


