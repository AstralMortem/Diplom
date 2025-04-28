import Badge from "@nuxt/ui/runtime/components/Badge.vue"

export default (date: string) => {

    const currentDate = new Date()
    const examinationDate = new Date(date)
    if (examinationDate < currentDate) {
        return h(Badge, {
            label: "Завершено",
            color: "success",
            variant: "subtle"
        })
        
    }else if (examinationDate > currentDate) {
        return h(Badge, {
            label: "Заплановано",
            color: "warning",
            variant: "subtle"
        })
    }else {
        return h(Badge, {
            label: "Прямо зараз",
            color: "error",
            variant: "subtle"
        })
    }
}

