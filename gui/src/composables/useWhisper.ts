import { invoke } from "@tauri-apps/api/core"

export const useWhisper = () => {
  const toast = useToast()
  const isInitialized = useState('initialized', () => false)
  const modelPath = useState('modelPath', () => '')
  const modelParams = ref({
    language: 'uk',
    num_of_threads: 4
  })


  watch(modelParams, ()=>{
    invoke<string>("set_params", {params: modelParams.value }).then(res => {
      toast.add({
        title: "Params updated",
        description: res,
        color: "success"
      })
    }).catch((error) => {
      isInitialized.value = false
      toast.add({
        title: "Error while updating params",
        description: error.toString(),
        color: "error"
      })
    })
  },{deep:true})


  return {isInitialized, modelParams, modelPath}
}
