<template>
  <ItemDeleteModal url="/api/v1/med-records/{record_id}" :path="{record_id:$props.record.record_id}" resource="medical_records" :title="'Видалити запис за ' + data" @deleted="$emit('deleted')">
    <template #body>
      <p class="font-semibold text-2xl">Ви впевнені що хочете видалити медичний запиз за  <span class="text-error-500">{{ data }}</span>?</p>
    </template>
  </ItemDeleteModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';

defineEmits(['deleted'])

const props = defineProps({
  record: {
    type: {} as PropType<components["schemas"]["MedRecordRead"]>,
    required: true
  }
})

const data = computed(()=> new Date(props.record.examination_date).toLocaleString('uk-UA', {
          day: 'numeric',
          month: 'short',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        }))

</script>

<style>

</style>