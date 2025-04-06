
<script setup lang="ts">
const { transcriptionFragments, formatted, isRecording, audioBlob, modelPath, clear, params  } = useRecorder()
const route = useRoute()

const save = async () => {

  try{
    const fileName  = `${Date.now()}.wav`
    const file = await uploadFile(audioBlob.value, `transcriptions/${route.params.id}`, fileName )
    await $backend('/api/v1/med-records/{record_id}/transcriptions',{
      method: "POST",
      path: {
        record_id: route.params.id as string
      },
      body: {
        audio_url: file.file_path,
        audio_duration: file.duration || 0,
        transcription_text: formatted.value,
        asr_model: modelPath.value,
        asr_config: params.value,
        language: params.value.language
      }
    })
    navigateTo(`/medical-records/${route.params.id}`)
    clear()
    
  }catch(error){
    console.error(error)
    backendError(error)
  }

}

</script>


<template>
  <UCard class="w-full h-full">
    <div class="flex flex-col gap-2 h-full w-full">
      <UTextarea v-model="formatted" class="w-full h-full" :ui="{base: 'h-full'}"/>
      <div class="flex flex-row gap-4 items-center justify-between">
        <UILabel label="Logs" class="w-full">
        <UCard class="w-full">
          <ul>
            <li v-for="log in transcriptionFragments.slice(-5)" :key="log.text" class="text-sm">
              <span>[{{log.start}}] - [{{log.end}}] {{log.text}}</span>
            </li>
          </ul>
        </UCard>
      </UILabel>
        <div class="flex flex-col gap-2">
          <UButton size="lg" label="Зберегти" color="primary" class="w-fit" @click="save" :disabled="isRecording"/>
          <UButton size="lg" label="Очистити" color="warning" class="w-fit" @click="clear"/>
        </div>
      </div>
      
    </div>
  </UCard>

  
</template>
