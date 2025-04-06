<template>
  <div class="flex flex-row gap-2 w-full" v-if="status === 'success' && data">
    <UCard class="w-full">
        <div class="flex flex-col gap-2">
                <p class="text-xl">Транскрибований текст</p>
                <pre>{{ data.transcription_text }}</pre>
        </div>
    </UCard>
    <UCard>
        <div class="flex flex-col gap-2">
            <UILabel label="Модель">
                {{ data.asr_model }}
            </UILabel>
            <UILabel label="Мова">
                {{ data.language }}
            </UILabel>
            <USeparator label="Конфігурація" />
            <UILabel :label="param" v-for="param in Object.keys(data.asr_config)">
              {{ data.asr_config[param] }}
            </UILabel>
            
        </div>
    </UCard>
</div>
<div class="w-full h-[300px]" v-else>
  <USkeleton class="w-full h-full" />
</div>
</template>

<script lang="ts" setup>
const props = defineProps({
  id: {
    type: Number,
    required: true
  },
  record_id: {
    type: String,
    required: true
  }
})

const {data, status} = await useBackendData('/api/v1/med-records/{record_id}/transcriptions/{transcription_id}',{
  path: {
    record_id: props.record_id,
    transcription_id: props.id
  }  
})



</script>

<style>

</style>