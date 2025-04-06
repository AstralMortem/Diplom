import { invoke, Channel } from "@tauri-apps/api/core"
import RecordRTC from "recordrtc"

interface TranscriptionFragment {
  text: string,
  start: number,
  end: number
}

interface NewParams {
  language: string,
  num_of_threads: number
}


export const useRecorder = () => {
  const toast = useToast()
  const modelPath = useState<string>("modelPath", () => "")
  const transcriptionFragments = useState<Array<TranscriptionFragment>>("fragments", () => [])
  const transcriptionText = ref()
  const isRecording = useState<boolean>("isRecording", () => false)
  const isInitialized = useState<boolean>("isInitialized", () => false)
  const audioChunks = ref<Float32Array[]>([])
  const params = useState<NewParams>("params", () => ({language: "uk", num_of_threads: 4}))
  const audioURL = useState<string>("audioURL", () => "")
  const audioBlob = useState<Blob | undefined>("audioBlob", () => undefined)

  const formatted = computed({
    get(){
      transcriptionText.value = transcriptionFragments.value.map(fragment => fragment.text).join(" ")
      return transcriptionText.value
    },
    set(value){
      transcriptionText.value = value
    }
  })
  let mediaRecorder: RecordRTC 
  

  const startRecording = async () => {
    if(isInitialized.value){
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    mediaRecorder = new RecordRTC(stream, {
      type: "audio",
      mimeType: "audio/wav",
      recorderType: RecordRTC.StereoAudioRecorder,
      numberOfAudioChannels: 1,
      timeSlice: 1000,
      desiredSampRate: 16000,
      bufferSize: 4096,
      audioBitsPerSecond: 128000,
      ondataavailable: async (blob) => {
        const audioBuffer = await blob.arrayBuffer()
        const audioContext = new AudioContext({sampleRate: 16000})
        const audioData = await audioContext.decodeAudioData(audioBuffer)
        const chunk = new Float32Array(audioData.getChannelData(0))
        audioChunks.value.push(chunk)
        invoke("process_chunk", {chunk: Array.from(chunk)}).catch((error) => {
          toast.add({
            title: "Error while processing chunk",
            description: error.toString(),
            color: "error"
          })
        })
      }
    })

    const onTranscript = new Channel<TranscriptionFragment>()

    onTranscript.onmessage = (fragment) => {
      if (!fragment.text.includes("[BLANK_AUDIO]") || !fragment.text.includes("[музика]")){
        transcriptionFragments.value.push(fragment)
      }
      
    }

    invoke("start_transcription", {onTranscript: onTranscript}).catch((error) => {
      toast.add({
        title: "Error while starting transcription",
        description: error.toString(),
        color: "error"
      })
    })
    mediaRecorder.startRecording();
    isRecording.value = true
    }
    else{
      toast.add({
        title: "Error while starting transcription",
        description: "Model not initialized, select whisper model first",
        color: "error"
      })
    }
  }

  const stopRecording = async () => {
    if (mediaRecorder){
        mediaRecorder.stopRecording(function () {
          const blob = mediaRecorder.getBlob()
          audioBlob.value = blob
          audioURL.value = mediaRecorder.toURL()
        })
        invoke("stop_transcription").catch((error) => {
          toast.add({
            title: "Error while stopping transcription",
            description: error.toString(),
            color: "error"
          })
        })
        isRecording.value = false
    }
  }

  const updateParams = () => {
    invoke<string>("set_params", {params: params.value}).then(res => {
      toast.add({
        title: "Params updated",
        description: res,
        color: "success"
      })
    }).catch((error) => {
      toast.add({
        title: "Error while updating params",
        description: error.toString(),
        color: "error"
      })
    })
  }
  
  const clear = () => {
    transcriptionFragments.value = []
    transcriptionText.value = ""
    audioURL.value = ""
    audioBlob.value = undefined
    audioChunks.value = []
  }

  return { formatted, transcriptionFragments, isRecording, startRecording, stopRecording, updateParams,clear, isInitialized, params, modelPath, audioURL, audioBlob }
}
