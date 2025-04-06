<script setup lang="ts">

const {params, updateParams} = useRecorder()

const languages = [{
    label: 'Українська',
    value: 'uk'
}, {
    label: 'Англійська',
    value: 'en'
}, {
    label: 'Російська',
    value: 'ru'
},{
    label: 'Авто',
    value: 'auto'
}]



watch(params, (newVal) => {
    updateParams()
},{deep:true})

</script>

<template>
    <div class="flex flex-col gap-2">
        <UILabel label="Модель">
            <TranscriptionModelDownloader/>
        </UILabel>
        <UILabel label="Мова">
            <USelectMenu v-model="params.language" :items="languages" value-key="value" label-key="label" placeholder="Виберіть мову"/>
        </UILabel>
        <UILabel label="Кількість потоків">
            <USelectMenu v-model.number="params.num_of_threads" :items="[1,2,3,4,5,6,7,8]" placeholder="Виберіть кількість потоків"/>
        </UILabel>
    </div>
</template>
