<script setup lang="ts">
const authStore = useAuthStore()

navigateTo('/doctors/' + authStore.user.doctor_id)

</script>