import { jsPDF } from "jspdf"
import { render, type Component, type ConcreteComponent } from "vue";
import { RobotoBase64 } from "~/assets/RobotoBase64";

export const usePDF = () => {

    
    const componentInstance = shallowRef<Component>()
    const componentProps = ref<object>({})

    const setParams = (component: Component, componentParams: object) => {
        componentInstance.value = component
        componentProps.value = componentParams
    }

    const generate = (filename: string) => {
        const doc = new jsPDF('p', 'pt', 'a4')
        if(componentInstance.value){
            const content = h(componentInstance.value, componentProps.value)
            const el = document.createElement('div')
            el.classList.add("w-full", "h-full")
            el.style.fontFamily = "Roboto"
            render(content, el)
            console.log(el)
            
            doc.html(el, {
                callback: (file) => {
                    file.save(`${filename}.pdf`)
                },
                width: 580,
                windowWidth: 580,
                margin: 4,
                fontFaces: [{
                    family: 'Roboto',
                    style: 'normal',
                    weight: 400,
                    src: [{
                        url: URL.createObjectURL(new Blob([RobotoBase64])),
                        format: 'truetype'
                    }]
                }]
            })
            }else{
                useToast().add({
                    title: 'You need set component name first', 
                    color: 'error'
                })
        }
    }

    return {generate, setParams}

}