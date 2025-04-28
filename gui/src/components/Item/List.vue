<script setup lang="ts">
import type { paths } from '#open-fetch-schemas/backend'
import { useInfiniteScroll } from '@vueuse/core'


const props = defineProps({
    url:{
        type: String as unknown as keyof paths,
        required: true
    },
    title: {
        type: String,
        required: true
    }
})

const show = ref(false)

const total = ref(0)
const page = ref(1)
const pages = ref(1)
const pageSize = ref(10)

const {data, error, status} = await useBackend(props.url, {
    params: {
        page: page,
        size: pageSize
    },
    
    cache: 'no-cache',
    transform: (item) => {
        total.value = item.total
        page.value = item.page
        pages.value = item.pages
        return item
    }
})


watch(error, ()=>{
    if(error.value){
        backendError(error.value)
    }
})

const listRef = useTemplateRef<HTMLElement>('listRef')

useInfiniteScroll(listRef, async () => {
    page.value += 1
},{
    distance: pageSize.value,
    canLoadMore: () => page.value < pages.value 
})



</script>

<template>
    <UButton class="fixed top-20 right-2 md:hidden rounded-full" :label="props.title" variant="outline" size="lg" @click="show = true"/>
    <UCard class="h-full w-max" :class="[
        'fixed inset-y-0 right-0 w-64 transform transition-transform',
        show ? '-translate-x-0' : 'translate-x-full',
        'md:relative md:translate-x-0'
      ]">
        <template #header>
            <div class="flex items-center justify-between gap-8">
                <span>{{ props.title }} ({{ total }})</span>
                <div class="flex gap-2 items-center">
                    <UButton leading-icon="i-heroicons-magnifying-glass-20-solid" variant="outline" size="lg"/>
                    <UButton leading-icon="i-heroicons-x-mark-20-solid" variant="outline" class="md:hidden" size="lg" @click="show = false"/>
                </div>
            </div>
        </template>
        <div ref="listRef" class="flex flex-col gap-2 h-full min-w-[140px]">
            <slot v-for="(item,idx) in data.items" :key="idx" name="item" :item="item"/>
            <div v-if="data?.items?.length == 0 " class="flex justify-center items-center h-min w-full">
                <p class="text-2xl">Empty :(</p>
            </div>
            <div v-if="status === 'pending'" class="flex flex-col gap-2">
                <USkeleton v-for="i in 10" :key="i" class="h-10 w-full bg-neutral-600 rounded-lg"/>
            </div>
        </div>
    </UCard>
</template>