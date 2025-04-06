<template>
      <div 
      :class="[
        'z-20 fixed inset-y-0 left-0 bg-gray-800 text-white w-64 p-4 transform transition-transform',
        isOpen ? 'translate-x-0' : '-translate-x-full',
        'md:relative md:translate-x-0'
      ]"
    >
      <div class="flex justify-between items-center">
        <h2 class="text-xl font-bold">Sidebar</h2>
        <UButton variant="link" @click="isOpen = false" leading-icon="i-heroicons-x-mark" class="md:hidden" color="neutral" />
      </div>
      
      <ul class="mt-4 space-y-2">
        <li v-for="link in links" :key="link.path">
          <ULink :to="link.path" class="block p-2 rounded hover:bg-neutral-700 hover:text-white gap-2 text-neutral-300" active-class="bg-primary-700/20 border-l-2 border-primary-600">
            <div class="flex items-center justify-start font-semibold">
              <UIcon :name="link.icon" v-if="link.icon" />
              <span>{{ link.label }}</span>
            </div>
          </ULink>
        </li>
      </ul>
    </div>
  </template>
  
<script setup>
  
  const isOpen = defineModel({default:false});

  const links = [{
    label: "Головна",
    path: "/",
  },{
    label: "Лікарі",
    path: "/doctors"
  },
  {
    label: "Пацієнти",
    path: "/patients"
  },{
    label: "Медичні записи",
    path: "/medical-records"
  },{
    label: "Відділення",
    path: "/departments"
  }]
  
</script>
  
<style>
  /* Optional: Prevent body scrolling when sidebar is open on mobile */
  body.overflow-hidden {
    overflow: hidden;
  }
</style>
  