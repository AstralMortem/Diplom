
<script setup lang="ts">
import { Channel, invoke } from '@tauri-apps/api/core'

const { modelPath, isInitialized } = useWhisper()


const models = ref([{
  label: 'Base Model',
  value: 'ggml-base.bin',
  isDownloaded: false,
},{
  label: 'Small Model',
  value: 'ggml-small.bin',
  isDownloaded: false
},{
  label: 'Tiny Model',
  value: 'ggml-tiny.bin',
  isDownloaded: false
},{
  label: 'Medium Model',
  value: 'ggml-medium.bin',
  isDownloaded: false
},{
  label: 'Large Model (V1)',
  value: 'ggml-large-v1.bin',
  isDownloaded: false
},{
  label: 'Large Model (V2)',
  value: 'ggml-large-v2.bin',
  isDownloaded: false
},{
  label: 'Large Model (V3)',
  value: 'ggml-large-v3.bin',
  isDownloaded: false
},{
  label: 'Large Model (V3 Turbo)',
  value: "ggml-large-v3-turbo.bin",
  isDownloaded: false
}])

const isDownloading = ref(false)
const downloadProgress = ref(0)

const checkModels = async () => {
  try{
    const modelNames = models.value.map(x => x.value)
    const results = await invoke<boolean[]>('check_models', { models: modelNames })
    return models.value.map((model, index) => ({
      ...model,
      isDownloaded: results[index], // Оновлення isDownloaded
    }));
  }catch(error){
    useToast().add({
      title: 'Failed to check models',
      color: 'error'
    })
    return models.value
  }
}




async function downloadModel(modelName: string) {
  // Create the channel outside the try block so we can close it in the finally block
  const onProgress = new Channel<number>();

  try {
    // Set up the event handler
    onProgress.onmessage = (response) => {
      downloadProgress.value = Number(response)
    };
    
    const result = await invoke<string>("download_model", {
      modelName: modelName,
      onProgress: onProgress
    });
    
    return result;
  } catch (error) {
    useToast().add({
      title: 'Failed to download model',
      description: error.toString(),
      color: 'error'
    });

  }
}


watch(modelPath, async (newPath) => {
  if(newPath){
    const model = models.value.find(x => x.value === newPath)
    if(model && !model.isDownloaded){
      isDownloading.value = true
      downloadProgress.value = 0
      await downloadModel(newPath)
      model.isDownloaded = true
      isDownloading.value = false
      if(model.isDownloaded){
        invoke<string>('init_whisper', {
          modelName: newPath
        }).then(res => {
          useToast().add({title: res, color: 'primary'})
          isInitialized.value = true
      })
        .catch(err => useToast().add({title: err, color: 'error'}))

      }


    }else if(model && model.isDownloaded){
      invoke<string>('init_whisper', {
        modelName: newPath
      }).then(res => {
        useToast().add({title: res, color: 'primary'})
        isInitialized.value = true
      })
      .catch(err => useToast().add({title: err, color: 'error'}))
    }
  }
})

onMounted(async ()=>{
  models.value = await checkModels()
})


</script>

<template>
    <div class="w-full">
      <USelectMenu v-model="modelPath" :items="models" value-key="value" label-key="label" placeholder="Виберіть Whisper модель" class="w-full" :ui="{itemLabel: 'w-full'}" :loading="isDownloading" >
        <template #item-leading="{ item }">
          <UIcon v-if="item.isDownloaded" name="i-heroicons-check-circle" class="text-green-500"/>
          <UIcon v-else name="i-heroicons-arrow-down-tray"/>
        </template>
        <template #item-label="{item}">
          <div class="flex flex-col gap-2 w-full" >
            <p>{{ item.label }}</p>
            <UProgress v-if="isDownloading && item.value === modelPath" v-model="downloadProgress" :max="100" class="w-full" status/>
          </div>
        </template>
      </USelectMenu>
    </div>
</template>
