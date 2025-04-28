<script setup lang="ts">
import type { components } from '#open-fetch-schemas/backend';

const model = defineModel<components["schemas"]["Gender"]>()

const items = ref([
    {
        label: 'Чоловік',
        id: 'male'
    },
    {
        label: 'Жінка',
        id: 'female'
    }
])

</script>


<template>
    <USelectMenu v-model="model" :items="items" value-key="id" placeholder="Стать"  />
</template>