<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';


const props = defineProps({
    patient: {
        type: {} as PropType<components["schemas"]["PatientRead"]>,
        required: true
    }
})

const patientStore = usePatientStore()
const show = ref(false)

const deletePatient = async () => {
    if(await patientStore.deletePatient(props.patient.patient_id)){
        show.value = false
        navigateTo('/patients')
    }
}
</script>


<template>
    <UModal v-model:open="show" :title="`Видалити пацієнта ${props.patient.first_name} ${props.patient.last_name} ${props.patient.middle_name}`">
        <UButton class="rounded-full hover:cursor-pointer" variant="outline" color="error" icon="i-heroicons-trash" />
        <template #body>
            <div class="flex flex-col gap-2">
                <p class="text-2xl font-bold">Ви впевнені, що хочете видалити пацієнта? <span class="text-error-700">{{patient.last_name}} {{ patient.first_name }} {{ patient.middle_name }} </span></p>
            <p class="text-base font-semibold">Це призведе до видалення всіх його медичних записів.</p>
            <div class="flex items-center gap-2">
                <UButton label="Видалити" color="error" @click="deletePatient"/>
                <UButton label="Скасувати" color="neutral" variant="outline" @click="show = false"/>
            </div>
            </div>
            
        </template>
    </UModal>
</template>
