<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';


const props = defineProps({
    medRecord: {
        type: {} as PropType<components["schemas"]["MedRecordRead"]>,
        required: true
    }
})

const show = ref(false)

const deleteMedRecord = async () => {
    try{
        await useBackendData('/api/v1/med-records/{record_id}',{
            method: 'DELETE',
            path: {
                record_id: props.medRecord.record_id
            }
        })
        navigateTo('/medical-records')
        show.value = false


    } catch (error) {
        backendError(error)
    }
}
</script>


<template>
    <UModal v-model:open="show" :title="`Видалити медичний запис за ${new Date(props.medRecord.examination_date).toLocaleString('uk-UA')}`">
        <UButton class="rounded-full hover:cursor-pointer" variant="outline" color="error" icon="i-heroicons-trash" />
        <template #body>
            <div class="flex flex-col gap-2">
                <p class="text-2xl font-bold">Ви впевнені, що хочете видалити медичний запис? <span class="text-error-700">За {{ new Date(props.medRecord.examination_date).toLocaleString('uk-UA') }}</span></p>
            <p class="text-base font-semibold">Це призведе до видалення всіх його транскрипцій та результатів</p>
            <div class="flex items-center gap-2">
                <UButton label="Видалити" color="error" @click="deleteMedRecord"/>
                <UButton label="Скасувати" color="neutral" variant="outline" @click="show = false"/>
            </div>
            </div>
            
        </template>
    </UModal>
</template>
