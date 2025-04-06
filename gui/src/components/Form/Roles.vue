<script setup lang="ts">

const model = defineModel<number>({default: null})

const {data, status} = await useBackendData('/api/v1/roles/')

</script>


<template>
<USelectMenu v-model="model" :items="data?.items" :loading="status === 'pending'" value-key="role_id" label-key="name" placeholder="Роль" />
</template>