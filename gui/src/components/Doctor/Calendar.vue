<script setup lang="ts">
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'

const calendarOptions = ref({
  plugins: [dayGridPlugin, timeGridPlugin],
  initialView: 'timeGridWeek',
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },
  events: [],
  eventClick(info) {
    const id = info.event.extendedProps.record_id
    navigateTo('/records/' + id)
  }
})

const {$backend} = useNuxtApp()
const authStore = useAuthStore()

onMounted(async ()=>{
    try{
        const response = await $backend('/api/v1/med-records/',{
            query:{
                doctor_id: authStore.user.doctor_id,
                page:1,
                size: 10
            },
            
            cache: 'no-cache'
        })

        if(response.items.length > 0){
            calendarOptions.value.events = response.items.map((i)=>{
                return {
                    title: `${i.patient.last_name} ${i.patient.first_name} ${i.patient.middle_name}`,
                    start: new Date(i.examination_date),
                    end:  new Date(i.examination_date),
                    extendedProps: {
                        record_id: i.record_id
                    }
                }
            })
        }

    }catch(error){
        backendError(error)
    }
})

</script>


<template>
<UCard class="w-full h-[80vh] overflow-auto">
    <FullCalendar :options="calendarOptions"/>
</UCard>


</template>