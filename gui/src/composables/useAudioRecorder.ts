import { Channel, invoke } from "@tauri-apps/api/core"
import RecordRTC from "recordrtc"

interface TranscriptionFragment {
  text: string,
  start: number,
  end: number
}


export const useAudioRecorder = () => {
  const toast = useToast()
  const isRecording = useState('isRecording', ()=> false)
  const onTranscript = new Channel<TranscriptionFragment>()
  const fragments = useState("fragments", () => [] as Array<TranscriptionFragment>)
  const audioBlob = useState("audioBlob", ()=> undefined)
  const audioURL = ref<string>()

  let mediaRecorder: RecordRTC 

  onTranscript.onmessage = (fragment) => {
    if (!fragment.text.includes("[BLANK_AUDIO]") || !fragment.text.includes("[музика]")){
      fragments.value.push(fragment)
    }
  }

  const isSuppoertWEBRTC = () => {
    const hasWebRTC = !!(
    window.RTCPeerConnection ||
    window.webkitRTCPeerConnection ||
    window.mozRTCPeerConnection
    );
  
    const hasGetUserMedia = !!(
      navigator.mediaDevices &&
      navigator.mediaDevices.getUserMedia
    );
    
    return hasWebRTC && hasGetUserMedia;
  }

  const checkWebRTC = () => {
    if (!isSuppoertWEBRTC()) {
      toast.add({
        title: "WebRTC is not supported",
        description: "Please use a modern browser that supports WebRTC.",
        color: "error"
      })
      throw new Error("WebRTC is not supported")
    }
  }

  const initRecorder = async () => {
    checkWebRTC()
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
        invoke("process_chunk", {chunk: Array.from(chunk)}).catch((error) => {
          useToast().add({
            title: "Error while processing chunk",
            description: error.toString(),
            color: "error"
          })
        })
      }
    })

    console.log('Recorder inited')
  }

  const startRecording = async () => {
    if(!mediaRecorder){
      toast.add({
        title: "Audio recorder not initialized",
        color: 'error'
      })
    }else{
      invoke("start_transcription", {onTranscript: onTranscript})
      .then(()=>{
        mediaRecorder.startRecording()
        isRecording.value = true
      })
      .catch((error) => {
        toast.add({
          title: "Error while starting transcription",
          description: error.toString(),
          color: "error"
        })
      })
    }
    
  }

  const stopRecording = async () => {
    if(isRecording){
      mediaRecorder.stopRecording(function () {
        const blob = mediaRecorder.getBlob()
        audioBlob.value = blob
        audioURL.value = mediaRecorder.toURL()
      })
      invoke('stop_transcription').then(()=>{
        isRecording.value = false
      }).catch(error =>{
        isRecording.value = false
        toast.add({
          title: 'Error when stop recording',
          description: error.toString(),
          color: 'error'
        })
      })
    }
  }
  
  const resetRecorder = () => {
    audioBlob.value = undefined as Blob | undefined
    audioURL.value = undefined as string | undefined
    fragments.value = []
  }

  return {initRecorder, startRecording, stopRecording, resetRecorder, audioBlob, audioURL, isRecording, fragments}

}
