<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
const patientStore = useMedRecordStore()


const formState = ref<components["schemas"]["MedRecordCreate"]>({})

const createMedRecord = async (e: any) => {
    try{
        const response = await $backend('/api/v1/med-records/',{
            method: 'POST',
            body: e.data
        })
        emit('add', response)
        navigateTo('/medical-records/' + response.record_id)
        clean()
    }catch(error){
        backendError(error)
    }
    
}

const clean = () => {
    show.value = false
    formState.value = {} as components["schemas"]["MedRecordCreate"]
}

const show = ref(false)
const form = useTemplateRef<HTMLFormElement>('form')
const emit = defineEmits(['add'])




</script>


<template>

    <UModal v-model:open="show" title="Додати прийом">
        <UButton label="Додати запис" color="primary" icon="i-heroicons-plus-20-solid"/>
        <template #body>
            <UForm :state="formState" @submit.prevent="createMedRecord" class="space-y-4" ref="form">
                <UFormField label="Пацієнт" name="patient_id">
                    <FormPatients v-model="formState.patient_id" class="w-full"/>
                </UFormField>
                <UFormField label="Лікар" name="doctor_id">
                    <FormDoctors v-model="formState.doctor_id" class="w-full"/>
                </UFormField>
                <UFormField label="Відділення" name="department_id">
                    <FormDepartments v-model="formState.department_id" class="w-full"/>
                </UFormField>
                <UFormField label="Дата прийому" name="examination_date">
                    <DateTimePicker v-model="formState.examination_date" class="w-full"/>
                    <!-- <div class="flex flex-row justify-start items-center gap-2">
                        <DatePicker v-model="formState.examination_date" class="w-full"/>
                        <TimePicker class="w-full"/>
                    </div> -->
                    
                </UFormField>


            </UForm>
        </template>
        <template #footer>
            <div class="flex items-center gap-2">
                <UButton label="Save" color="primary" @click="form?.submit()"/>
                <UButton label="Cancel" color="neutral" variant="outline" @click="clean"/>
            </div>
        </template>
    </UModal>
</template>