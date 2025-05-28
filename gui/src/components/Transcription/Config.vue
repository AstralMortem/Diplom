<template>
  <UCard>
    <div class="flex flex-col gap-3">
      <USeparator label="Recorder"/>
      <div class="flex flex-col gap-2">
        <UButton v-if="isRecording" variant="subtle" color="error"  label="Зупинити запис" @click="stopRecording"/>
        <UButton v-else variant="subtle" label="Почати запис" :disabled="!isInitialized" @click="startRecording"/>
        <audio v-if="audioURL" :src="audioURL" controls/>
      </div>
      <USeparator label="Whisper"/>
      <div class="flex flex-col gap-2">
        <UILabel label="Модель">
          <TranscriptionModelDownloader/>
        </UILabel>
        <UILabel label="Мова">
          <USelectMenu v-model="modelParams.language" :items="[{label: 'Українська', value: 'uk'}]" value-key="value"  />
        </UILabel>
        <UILabel label="К-ть потоків">
          <USelectMenu v-model="modelParams.num_of_threads" :items="[4,6,8,10,12,14,16]" value-key="value"  />
        </UILabel>
      </div>
    </div>
  </UCard>
</template>

<script lang="ts" setup>
const {modelParams, isInitialized} = useWhisper()
const {isRecording, initRecorder, startRecording, stopRecording, audioURL} = useAudioRecorder()

try{
  await initRecorder()
}catch(e){
  abortNavigation()
}



</script>

<style>

</style>