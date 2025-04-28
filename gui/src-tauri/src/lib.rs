#[cfg_attr(mobile, tauri::mobile_entry_point)]

mod model_downloader;
mod transcription;
mod mdns;


extern crate include_dir;

use include_dir::{include_dir, Dir};
use std::fs;

static ASSETS: Dir = include_dir!("$CARGO_MANIFEST_DIR/assets");



fn create_app_dir_and_copy_files() -> Result<(), Box<dyn std::error::Error>> {
  let doc_dir = dirs_next::document_dir().ok_or("Documents not found")?;
  let app_dir = doc_dir.join("MedVoice");

  // Create dir if it doesn't exist
  if !app_dir.exists() {
      fs::create_dir_all(&app_dir)?;
  }

  let models_dir = app_dir.join("models");

  if !models_dir.exists() {
    fs::create_dir_all(&models_dir)?;

    for file in ASSETS.files() {
      let path = models_dir.join(file.path().file_name().unwrap());
      fs::write(path, file.contents())?;
  }
  }

  Ok(())
}

pub fn run() {
  tauri::Builder::default()
    .setup(|app| {
      if cfg!(debug_assertions) {
        app.handle().plugin(
          tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build(),
        )?;
      }
      create_app_dir_and_copy_files().expect("Failed to create dir or copy files");
      // mdns::start_discovering();
      Ok(())
    })
    .manage(transcription::TranscriptionState::new())
    .invoke_handler(tauri::generate_handler![
      model_downloader::check_models,
      model_downloader::download_model,
      transcription::start_transcription,
      transcription::stop_transcription,
      transcription::process_chunk,
      transcription::init_whisper,
      transcription::set_params,
      transcription::process_conversation,
      mdns::discover_services
    ])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
    
}
