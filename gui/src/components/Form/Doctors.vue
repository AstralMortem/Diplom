<script setup lang="ts">

const model = defineModel({default:''})
const authStore = useAuthStore()

model.value = authStore.user?.doctor_id

const search = ref('')

const {data, status} = await useBackendData('/api/v1/doctors/',{
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
    lazy: true,
    cache: false
})


if(model.value){
    if(!data.value?.items.find(item => item.doctor_id === model.value)){
        const response = await $backend('/api/v1/doctors/{doctor_id}', {
            path: {
                doctor_id: model.value
            }
        })
        data.value?.items.push(response)
    }
}


</script>


<template>
    <UInputMenu v-model="model" :items="data?.items || []" value-key="doctor_id" label-key="full_name" :loading="status === 'pending'" v-model:search-term="search"/>
</template>