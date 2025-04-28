import { Channel, invoke } from "@tauri-apps/api/core"

export const useOllama = (conversation: Ref<string>) => {

  
  let saved = ""
  const isSummarizing = useState('summarizing', () => false)
  const isSummarized = useState('summarized', () => false)
  const summarizedFragments = useState('summarizedFragments', () => "")

  const onProcess = new Channel<string>();
  onProcess.onmessage = (response) => {
    summarizedFragments.value += response
  }


  const startSummarize = async () => {
    
    
    try{
      isSummarizing.value = true
      saved = conversation.value
      await invoke('process_conversation', {
        conversation: saved,
        onProcess: onProcess
      })
      isSummarizing.value = false
      isSummarized.value = true
    }catch(error){
      isSummarizing.value = false
      isSummarized.value = false
      useToast().add({
        title: 'Error when summarizing',
        description: error.toString(),
        color: 'error'
      })
    }
  }
  
  const resetSumarizer = () => {
    conversation.value = saved
    saved = ""
    isSummarizing.value = false
    isSummarized.value = false
    summarizedFragments.value = ""
  }

  return {isSummarized, isSummarizing, startSummarize, resetSumarizer, summarizedFragments}



}
