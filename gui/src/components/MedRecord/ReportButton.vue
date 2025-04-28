<script setup lang="ts">
import { ReportRecord } from '#components';
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';

const {setParams, generate} = usePDF()

const props = defineProps({
    record: {
        type: {} as PropType<components["schemas"]["MedRecordDetailRead"]>,
        required: true
    },
})

onMounted(()=>{
    setParams(ReportRecord, {record:props.record})
})

</script>

<template>
    <UButton label="Друкувати звіт" color="secondary" @click="generate(`${props.record.examination_date}_${props.record.patient.last_name}_${props.record.patient.first_name}_${props.record.patient.middle_name}`)"/>
</template>