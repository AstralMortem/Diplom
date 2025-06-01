<template>
  <UCard :ui="{body: 'flex flex-row justify-start w-full h-full items-start gap-4'}" class="w-full h-full">
    <div class="flex flex-col gap-4 h-full w-full">
      <UILabel label="Документ" class="flex-1 text-base">
        <UCard class="w-full h-full">
          <UTextarea v-model="text" class="w-full h-full"/>
        </UCard>
      </UILabel>
      <UILabel label="Logs">
        <UCard class="w-full">
          <div class="flex flex-col gap-2 items-start justify-start">
            <p v-for="fragment in fragments.slice(-5)" :key="fragment.end + fragment.start + fragment.text" class="text-xs"><span>[{{fragment.start}}] - [{{fragment.end}}] {{fragment.text}}</span></p>
          </div>
        </UCard>
      </UILabel>
    </div>
    <div v-if="text" class="flex flex-col gap-2 items-end">
      <UButton label="Зберегти" class="w-full" @click="saveTranscription"/>
      <UButton v-if="!isSummarized" :loading="isSummarizing" label="Підсумувати" color="warning" class="w-full" @click="startSummarize"/>
      <UButton v-else label="Повернути назад"  color="warning" class="w-full" @click="resetSumarizer"/>
      <UButton label="Очистити" color="error" class="w-full mt-2" @click="resetSumarizer(); resetRecorder(); " />
    </div>
  </UCard>
</template>

<script lang="ts" setup>
const {fragments, resetRecorder, audioBlob} = useAudioRecorder()
const {modelPath, modelParams} = useWhisper()


const text = ref("")
const route = useRoute()

watch(fragments, ()=>{
  text.value = fragments.value.map(t => t.text).join(" ")
},{deep: true, immediate: true})

const {isSummarized, isSummarizing, resetSumarizer, startSummarize, summarizedFragments} = useOllama(text)

watch(summarizedFragments, ()=>{
  text.value = summarizedFragments.value
}, {deep:true, immediate: true})

const {$backend} = useNuxtApp()


const saveTranscription = async () => {
  try{
    
    const file = await fileUpload(audioBlob.value, `records/${route.params.id as string}/`, `${new Date().getTime()}.wav`)
    await $backend('/api/v1/med-records/{record_id}/transcriptions', {
      method: 'POST',
      path:{
        record_id: route.params.id as string
      },
      body: {
        audio_duration: file.duration || 0,
        audio_url: file.file_path,
        asr_model: modelPath.value,
        asr_config: modelParams.value,
        language: modelParams.value.language,
        transcription_text: text.value,
        is_processed: isSummarized.value
      }, 
      
      cache: 'no-cache'
    })
    navigateTo('/records/'+ route.params.id as string)
  }catch(error){
    backendError(error)
  }

}








</script>

<style>

</style>