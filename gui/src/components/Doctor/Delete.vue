<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';


const props = defineProps({
    doctor: {
        type: {} as PropType<components["schemas"]["DoctorRead"]>,
        required: true
    }
})

const doctorStore = useDoctorStore()
const show = ref(false)

const deleteDoctor = async () => {
    if(await doctorStore.deleteDoctor(props.doctor.doctor_id)){
        show.value = false
        navigateTo('/doctors')
    }
}
</script>


<template>
    <UModal v-model:open="show" :title="`Видалити лікаря ${props.doctor.first_name} ${props.doctor.last_name} ${props.doctor.middle_name}`">
        <UButton class="rounded-full hover:cursor-pointer" variant="outline" color="error" icon="i-heroicons-trash" />
        <template #body>
            <div class="flex flex-col gap-2">
                <p class="text-2xl font-bold">Ви впевнені, що хочете видалити лікаря? <span class="text-error-700">{{doctor.last_name}} {{ doctor.first_name }} {{ doctor.middle_name }} </span></p>
            <p class="text-base font-semibold">Це призведе до видалення всіх його медичних записів.</p>
            <div class="flex items-center gap-2">
                <UButton label="Видалити" color="error" @click="deleteDoctor"/>
                <UButton label="Скасувати" color="neutral" variant="outline" @click="show = false"/>
            </div>
            </div>
            
        </template>
    </UModal>
</template>
