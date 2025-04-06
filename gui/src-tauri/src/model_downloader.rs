use futures_util::StreamExt;
use tauri::ipc::Channel;





#[tauri::command]
pub fn check_models(models: Vec<String>) -> Result<Vec<bool>, String> {
  let doc_dir = dirs_next::document_dir().ok_or("Documents not found")?;
  let models_dir = doc_dir.join("MedVoice").join("models");
  let result = models.iter().map(|model| {
        models_dir.join(model).exists() // Перевірка, чи існує файл
    }).collect();

  Ok(result)
}


#[tauri::command]
pub async fn download_model(model_name: String, on_progress: Channel<u8>) -> Result<String, String> {
  let url = format!("https://huggingface.co/ggerganov/whisper.cpp/resolve/main/{}", model_name);
  let doc_dir = dirs_next::document_dir().ok_or("Documents not found")?;
  let models_dir = doc_dir.join("MedVoice").join("models");
  let save_path = models_dir.join(model_name).to_str().unwrap().to_string();

  let response = reqwest::get(&url).await.map_err(|e| e.to_string())?;
  let total_size = response.content_length().ok_or("Failed to get content length")?;

  let mut stream = response.bytes_stream();

  let mut file = std::fs::File::create(&save_path).map_err(|e| format!("File create error: {}", e))?;

  let mut downloaded: u64 = 0;

  while let Some(chunk) = stream.next().await {
    let data = chunk.map_err(|e| format!("Stream error: {}", e))?;
    std::io::copy(&mut data.as_ref(), &mut file)
            .map_err(|e| format!("Write error: {}", e))?;
    downloaded += data.len() as u64;
    let progress = (downloaded as f64 / total_size as f64) * 100.0;
    
    on_progress.send(progress as u8).unwrap();
  }

  return Ok("File Downloaded".to_string());
}