import { invoke } from "@tauri-apps/api/core"

export const useMDNS = async () => {
    const url = useState('url', () => "")
    if(!url.value){
        try{
            url.value = await invoke<string>('discover_services', {serviceType: '_myapp._tcp.local.'});
        }catch(error){
            useToast().add({title: 'Error discover service', description: err.toString(), color: 'error'})
        }
    }
    return url
    
}
