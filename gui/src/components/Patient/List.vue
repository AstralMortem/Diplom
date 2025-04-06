<script setup lang="ts">
import { useInfiniteScroll } from '@vueuse/core'

const patientStore = usePatientStore()
const {patients, isPending, size, page, pages, total} = storeToRefs(patientStore)


const listRef = useTemplateRef<HTMLElement>('listRef')

const {reset} = useInfiniteScroll(listRef, async () => {
    await patientStore.fetchPatients()
},{
    distance: size.value,
    canLoadMore: () => page.value < pages.value 
})

const show = ref(false)

onMounted(async () =>{
    await patientStore.fetchPatients()
})



</script>

<template>
    <UButton class="fixed top-20 right-2 md:hidden rounded-full" label="Patients" variant="outline" size="lg" @click="show = true"/>
    <UCard class="h-full w-max" :class="[
        'fixed inset-y-0 right-0 w-64 transform transition-transform',
        show ? '-translate-x-0' : 'translate-x-full',
        'md:relative md:translate-x-0'
      ]">
        <template #header>
            <div class="flex items-center justify-between gap-8">
                <span>Patients ({{ total }})</span>
                <div class="flex gap-2 items-center">
                    <UButton leading-icon="i-heroicons-magnifying-glass-20-solid" variant="outline" size="lg"/>
                    <UButton leading-icon="i-heroicons-x-mark-20-solid" variant="outline" class="md:hidden" size="lg" @click="show = false"/>
                </div>
            </div>
        </template>
        <div class="flex flex-col gap-2 h-full min-w-[140px]" ref="listRef">
            <PatientListItem v-for="patient in patients" :key="patient.patient_id" :patient="patient" />
            <div class="flex justify-center items-center h-min w-full" v-if="patients.length === 0">
                <p class="text-2xl">Empty :(</p>
            </div>
            <div class="flex flex-col gap-2" v-if="isPending">
                <USkeleton class="h-10 w-full bg-neutral-600 rounded-lg" v-for="i in 10" :key="i"/>
            </div>
        </div>
    
    </UCard>

    
</template>
