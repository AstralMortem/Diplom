<template>
  <ItemTable title="Медичні записи" url="/api/v1/med-records/" :columns="columns" :params="$props.query" @selected="onSelect" >
    <template #headerButton>
      <MedRecordAdd/>
    </template>
    <template #actions-cell="{row, refresh}">
      <div class="flex flex-row justify-center items-center gap-2">
        <MedRecordUpdate :record="row.original" @updated="refresh"/>
        <MedRecordDelete :record="row.original" @deleted="refresh"/>
      </div>
    </template>
  </ItemTable>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { TableColumn } from '@nuxt/ui';
import type { PropType } from 'vue';

const props = defineProps({
  query:{
    type: {} as PropType<object>,
    default: {}
  },
  showDoctor: {
    type: Boolean,
    default: true
  },
  showPatient: {
    type: Boolean,
    default: true
  }
})

const columns = ref<TableColumn<components["schemas"]["MedRecordRead"]>[]>([
  {
    header: 'Статус',
    accessorKey: 'status',
    cell: ({row}) => {
      return getRecordStatus(row.getValue('examination_date'))
    }
  },
  {
    header: 'Дата',
    accessorKey: 'examination_date',
    cell: ({ row }) => {
        return new Date(row.getValue('examination_date')).toLocaleString('uk-UA', {
          day: 'numeric',
          month: 'short',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        })
      }
  },{
    header: 'Відділення',
    accessorKey: 'department',
    cell: ({row}) => {
      return h(resolveComponent('DepartmentLink'), {department:row.original.department})
    }
  }
])

if(props.showDoctor){
  columns.value.push({
    header: 'Лікар',
    accessorKey: 'doctor',
    cell: ({row}) => h(resolveComponent('DoctorLink'), {doctor: row.original.doctor})
  })
}

if(props.showPatient){
  columns.value.push({
    header: 'Пацієнт',
    accessorKey: 'patient',
    cell: ({row}) => h(resolveComponent('PatientLink'), {patient: row.original.patient})
  })
}

columns.value.push({
  header: '',
  accessorKey: 'actions'
})

const onSelect = (row: components["schemas"]["MedRecordRead"]) => {
  navigateTo('/records/' + row.record_id)
}

</script>

<style>

</style>