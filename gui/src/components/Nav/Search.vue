<script setup lang="ts">
const show = ref(false)
const groups = ref([
  {
    id: 'apps',
    items: [
      {
        label: 'Calendar',
        icon: 'i-lucide-calendar'
      },
      {
        label: 'Music',
        icon: 'i-lucide-music'
      },
      {
        label: 'Maps',
        icon: 'i-lucide-map'
      }
    ]
  }
])
</script>


<template>
    

    <UModal>
      <UButton
      label="Search ..."
      color="neutral"
      variant="subtle"
      icon="i-lucide-search"
    />
        <template #content>
            <UCommandPalette class="flex-1" :groups="groups"/>
        </template>
    </UModal>



</template>