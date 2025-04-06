<script setup lang="ts">

const { startRecording, stopRecording, isInitialized, isRecording, audioURL } = useRecorder()

</script>


<template>
    <div class="flex flex-col gap-2">
        <div class="flex flex-row gap-2" v-if="isInitialized">
            <UButton @click="stopRecording" v-if="isRecording" color="error">Stop Recording</UButton>
            <UButton @click="startRecording"  v-else>Start Recording</UButton>
        </div>
        <div class="flex flex-row gap-2" v-if="audioURL">
            <audio :src="audioURL" controls/>
        </div>
    </div>
    
</template>