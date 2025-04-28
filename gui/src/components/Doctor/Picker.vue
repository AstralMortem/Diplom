<script setup lang="ts">

const model = defineModel<string>({default:''})
const authStore = useAuthStore()

model.value = authStore.user?.doctor_id

const search = defineModel<string>('search', {default: ''})

const {data, status} = await useBackend('/api/v1/doctors/',{
    query: {
        page: 1,
        size: 15
    },
    transform: (data) => {
        return { 
            ...data,
            items: data.items.map(item => {
                return {
                    ...item,
                    full_name: `${item.last_name} ${item.first_name} ${item.middle_name}`
                }
        })}
    },
    cache: 'no-cache',
    
})

const {$backend} = useNuxtApp()

if(model.value){
    if(!data.value?.items.find(item => item.doctor_id === model.value)){
        const response = await $backend('/api/v1/doctors/{doctor_id}', {
            path: {
                doctor_id: model.value
            },
            cache: 'no-cache',
            
        })
        data.value?.items.push(response)
    }
}


</script>


<template>
    <UInputMenu v-model="model" v-model:search-term="search" :items="data?.items || []" value-key="doctor_id" label-key="full_name" :loading="status === 'pending'"/>
</template>