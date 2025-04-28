<script setup lang="ts">

const model = defineModel<string>({default: new Date().toISOString()})


const date = computed({
    get(){
        return model.value.split('T')[0]
    },set(value){
        model.value = `${value}T${time.value}`
    }
})

const time = computed({
    get(){
        return model.value.split('T')[1]
    },set(value){
        model.value = `${date.value}T${value}`
    }
})



</script>

<template>
    <div class="flex flex-row gap-2 items-center">
        <UIDatePicker v-model="date" class="w-full"/>
        <UITimePicker v-model="time" class="w-full"/>
    </div>
</template>