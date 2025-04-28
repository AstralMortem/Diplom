export default async(file: Blob, filePath: string, fileName: string) => {
  console.log(file)
  const formData = new FormData()
  formData.append("file", file, fileName)

  const {$backend} = useNuxtApp()
  
  try{
    const response = await $backend('/api/v1/files/upload', {
      method: "POST",
      query: {
        file_path: filePath,
        file_name: fileName
      },
      body: formData,
      
      cache: 'no-cache'
    })
    return response
  }catch(error){
    throw error
  }
}
