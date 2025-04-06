<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';

const props = defineProps({
    medRecord: {
        type: {} as PropType<components["schemas"]["MedRecordRead"]>,
        required: true
    }
})

const formState = ref<components["schemas"]["MedRecordUpdate"]>(JSON.parse(JSON.stringify(props.medRecord)))

const changedData = computed(() => {
  const changes = {};
  for (const key in formState.value) {
    if (formState.value[key] !== props.medRecord[key]) {
      changes[key] = formState.value[key];
    }
  }
  return changes
});

const updateMedRecord = async (e: any) => {
    if(Object.keys(changedData.value).length > 0){
        try{
            const response =await useBackendData('/api/v1/med-records/{record_id}',{
                method: 'PATCH',
                path: {
                    record_id: props.medRecord.record_id
                },
                body: changedData.value
            })
            show.value = false
            emit('updated', response)
        } catch (error) {
            backendError(error)
        }
    }
    
}

const form = useTemplateRef<HTMLFormElement>('form')
const show = ref(false)
const emit = defineEmits(['updated'])

</script>


<template>
<UModal v-model:open="show" :title="`Редагувати медичний запис за ${new Date(props.medRecord.examination_date).toLocaleString('uk-UA')}`">
    <UButton class="rounded-full hover:cursor-pointer" variant="outline" color="warning" icon="i-heroicons-pencil-square" />
    <template #body>
        <UForm :state="formState" @submit.prevent="updateMedRecord" class="space-y-4" ref="form">
                <UFormField label="Пацієнт" name="patient_id">
                    <FormPatients v-model="formState.patient_id" class="w-full"/>
                </UFormField>
                <UFormField label="Відділення" name="department_id">
                    <FormDepartments v-model="formState.department_id" class="w-full"/>
                </UFormField>
                <UFormField label="Дата прийому" name="examination_date">
                    <DateTimePicker v-model="formState.examination_date" class="w-full"/>
                </UFormField>
            </UForm>
    </template>

    <template #footer>
            <div class="flex items-center gap-2">
                <UButton label="Save" color="primary" @click="form?.submit()"/>
                <UButton label="Cancel" color="neutral" variant="outline" @click="show = false"/>
            </div>
        </template>
</UModal>
</template>