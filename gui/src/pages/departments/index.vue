<template>
  <ItemTable title="Відділення" url="/api/v1/departments/" :columns="columns" @selected="onSelect">
    <template #headerButton="{refresh}">
      <DepartmentAdd @added="refresh"/>
    </template>
    <template #actions-cell="{row, refresh}">
      <div class="flex flex-row justify-start items-center gap-2">
        <DepartmentUpdate :department="row.original" @updated="refresh"/>
        <DepartmentDelete :department="row.original" @deleted="refresh"/> 
      </div>
    </template>
  </ItemTable>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { TableColumn } from '@nuxt/ui';

const columns: TableColumn<components['schemas']['DepartmentRead']>[] = [{
  header: '#',
  accessorKey: 'department_id'
},{
  header: 'Назва',
  accessorKey: 'name',
},
{
  header: 'Опис',
  accessorKey: 'description'
},
{
  header: 'Контактний телефон',
  accessorKey: 'contact_phone'
},
{
  header: '',
  accessorKey: 'actions'
}]

const onSelect = (row: components["schemas"]["DepartmentRead"]) => {
  navigateTo(`/departments/${row.department_id}`)
}

useBackButton().value = false


definePageMeta({
  resourece: "departments"
})

</script>

<style>

</style>