<script setup lang="ts">
const authStore = useAuthStore()

const model = defineModel<number>()

if(!model.value){
    model.value = authStore.user?.department?.department_id
}


const {data, status, error} = await useBackend('/api/v1/departments/', {
    query:{
        page: 1,
        size: 50
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
    <USelectMenu v-model="model" :items="data?.items" :loading="status === 'pending'" value-key="department_id" label-key="name" placeholder="Відділ" />

</template>