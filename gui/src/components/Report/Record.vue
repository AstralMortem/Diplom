<template>
    <div class="flex flex-col gap-4 report w-full h-full font-['Roboto']">
    <p class="font-bold self-center">Медичний звіт за {{ new Date(props.record.examination_date).toLocaleString() }}</p>
    <div class="border-2 border-neutral-500 p-4 rounded-lg">
      <UILabel class="font-normal" label="Відділення">
        {{ props.record.department.name }}
      </UILabel>
    </div>
    <div class="flex flex-row justify-between items-start gap-2 h-fit">
      <div class="flex flex-col gap-2 border-2 border-neutral-500 p-4 rounded-lg h-max">
        <p class="font-bold self-center">Лікар</p>
        <USeparator/>
        <UILabel class="font-normal" label="ПІБ">{{ props.record.doctor.last_name }} {{ props.record.doctor.first_name }} {{ props.record.doctor.middle_name }}</UILabel>
        <UILabel label="Посада">
          {{ props.record.doctor.specialization }}
        </UILabel>
        <UILabel class="font-normal" label="Контакти">
          <div class="flex flex-col gap-1">
            <p>Телефон: {{ props.record.doctor.phone_number }}</p>
            <p>Email: {{ props.record.doctor.email }}</p>
          </div>
        </UILabel >
      </div>
      <div class="flex flex-col gap-2 border-2 border-neutral-500 p-4 rounded-lg h-max">
        <p class="font-bold self-center">Пацієнт</p>
        <USeparator/>
        <UILabel class="font-normal" label="ПІБ">{{ props.record.patient.last_name }} {{ props.record.patient.first_name }} {{ props.record.patient.middle_name }}</UILabel>
        <UILabel class="font-normal" label="Дата народження">{{ new Date(props.record.patient.birth_data).toLocaleDateString() }} ({{ getAge(props.record.patient.birth_data) }})</UILabel>
        <UILabel class="font-normal" label="Контакти">
          <div class="flex flex-col gap-1">
            <p>Телефон: {{ props.record.patient.phone_number }}</p>
            <p>Email: {{ props.record.patient.email }}</p>
          </div>
        </UILabel>
      </div>
    </div>
    <div class="border-2 border-neutral-500 p-4 rounded-lg">
      <p class="font-bold">Транскрипції</p>
      <div class="flex flex-col gap-1" v-for="transcription in props.record?.transcriptions || []" :key="transcription.transcription_id">
        <div class="flex flex-row items-center">
          <p>Запис #{{ transcription.transcription_id }}</p>
        </div>
        <USeparator/>
        <p class="whitespace-pre-line">{{ transcription.transcription_text }}</p>
      </div>

    </div>
    
  </div>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';


const props = defineProps({
    record: {
        type: {} as PropType<components["schemas"]["MedRecordDetailRead"]>,
        required: true
    }
})


</script>