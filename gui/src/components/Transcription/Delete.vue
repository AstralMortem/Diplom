<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';


const props = defineProps({
    transcription: {
        type: {} as PropType<components["schemas"]["TranscriptionRead"]>,
        required: true
    }
})
const emit = defineEmits(['deleted'])


const show = ref(false)

const deleteTranscription = async () => {
  try{
    await $backend('/api/v1/med-records/{record_id}/transcriptions/{transcription_id}',{
      method: "DELETE",
      path: {
        record_id: props.transcription.record_id,
        transcription_id: props.transcription.transcription_id
      }
    })
    emit('deleted')
    show.value = false
  }catch(error){
    backendError(error)
  }
}
</script>


<template>
    <UModal v-model:open="show" title="Видалити транскрипцію">
        <UButton class="rounded-full hover:cursor-pointer" variant="outline" color="error" icon="i-heroicons-trash" />
        <template #body>
            <div class="flex flex-col gap-2">
                <p class="text-2xl font-bold">Ви впевнені, що хочете видалити транскрипцію?</p>
            <p class="text-base font-semibold">Це призведе до видалення всіх його медичних аудіо файлів.</p>
            <div class="flex items-center gap-2">
                <UButton label="Видалити" color="error" @click="deleteTranscription"/>
                <UButton label="Скасувати" color="neutral" variant="outline" @click="show = false"/>
            </div>
            </div>
            
        </template>
    </UModal>
</template>
