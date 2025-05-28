<script setup lang="ts">

const model = defineModel<string>({default:''})
const search = defineModel<string>('search', {default: ''})

const {data, status} = await useBackend('/api/v1/patients/',{
    query: {
        page: 1,
        size: 15
    },
    transform: (data) => {
        console.log(data)
        return { 
            ...data,
            items: data.items.map(item => {
                return {
                    ...item,
                    full_name: `${item.first_name} ${item.last_name} ${item.middle_name}`
                }
        })}
    },
    cache: 'no-cache',
    // credentials: 'include'
})

const {$backend} = useNuxtApp()

if(model.value){
    if(!data.value?.items.find(item => item.patient_id === model.value)){
        const response = await $backend('/api/v1/patients/{patient_id}', {
            path: {
                patient_id: model.value
            },
            
            cache: 'no-cache'
        })
        data.value?.items.push(response)
        data.value.total = (data.value!.total || 0) + 1
    }
}


</script>


<template>
    <UInputMenu v-model="model" v-model:search-term="search" :items="data?.items || []" value-key="patient_id"  label-key="full_name" :loading="status === 'pending'"/>
</template>