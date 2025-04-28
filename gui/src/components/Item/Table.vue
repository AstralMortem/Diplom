<script setup lang="ts">
import type { TableColumn, TableRow } from '@nuxt/ui'
import type { Component, ConcreteComponent, PropType } from 'vue'
import type { components, paths } from '#open-fetch-schemas/backend'


const page = ref(1)
const pageSize = ref(10)
const total = ref(0)


const props = defineProps({
    title: {
        type: String,
        required: true
    },
    url:{
        type: String as PropType<keyof paths>,
        required: true
    },
    columns:{
        type: Array<object>,
        default: [{header:"#", accessorKey: "id"}]
    },
    pageSizes: {
        type: Array<number>,
        default: [5,10,15,25,50]
    },
    params: {
        type: {} as PropType<object>,
        default: {}
    }
    
})


const {data, error, status, refresh} = await useBackend(props.url, {
    params: {
        page: page,
        size: pageSize,
        ...props.params
    },
    
    lazy: true,
    cache: 'no-store'
})


watch(data, ()=> {
    page.value = data.value?.page || 1
    total.value = data.value?.total || 1
})

watch(error, () => {
    if(error.value){
        backendError(error.value)
    }
})

const emit = defineEmits(["selected"])

const onSelect = (row: TableRow<typeof data.value.items>, e?: Event) => {
    emit('selected', row.original)
}

</script>

<template>
<UCard class="w-full" :ui="{body: 'overflow-y-scroll max-h-[70vh]'}">
    <template #header>
        <slot name="header">
            <div class="flex flex-row justify-between items-center">
                <p>{{props.title}} ({{ total }})</p>
                <slot name="headerButton" :refresh="refresh"/>
            </div>
        </slot>
    </template>
    <slot name="body">
        <UTable :loading="status === 'pending'" :data="data?.items || []" :columns="props.columns as TableColumn<typeof data>[]" @select="onSelect">
            <template v-for="(slotProps, name) in $slots" #[name]="slotProps">
                <slot :name="name" v-bind="slotProps || {}" :refresh="refresh"/>
            </template>
        </UTable>
    </slot>
    <template #footer>
        <slot name="footer">
            <div class="flex flex-row justify-between items-center">
                <div class="flex flex-row justify-start items-center gap-2">
                    <UButton variant="subtle" color="neutral" leading-icon="i-heroicons-arrow-path" @click="refresh"/>
                    <USelectMenu v-model="pageSize" :items="props.pageSizes"/>
                </div>
                <UPagination v-model:page="page" :page-size="pageSize" :total="total"/>
            </div>
        </slot>
    </template>
</UCard>
</template>