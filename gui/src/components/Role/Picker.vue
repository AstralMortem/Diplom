<script setup lang="ts">

const model = defineModel<number>({default: null})

const {data, status, error} = await useBackend('/api/v1/roles/',{
  query:{
    size:50,
    page: 1
  },
  
  cache: 'no-cache'
})

watch(error, ()=>{
  if(error.value){
    backendError(error.value)
  }
})

</script>


<template>
<USelectMenu v-model="model" :items="data?.items" :loading="status === 'pending'" value-key="role_id" label-key="name" placeholder="Роль" />
</template>