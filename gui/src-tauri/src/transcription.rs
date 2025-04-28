use std::sync::{Arc, Mutex};
use tauri::State;
use tauri::ipc::Channel;
use whisper_rs::{FullParams, SamplingStrategy, WhisperContext, WhisperContextParameters};
use serde::{Deserialize, Serialize};
use ollama_rs::generation::completion::request::GenerationRequest;
use tokio::io::{self, AsyncWriteExt};
use tokio_stream::StreamExt;
use ollama_rs::Ollama;

const SAMPLE_RATE: usize = 16000;
const BUFFER_SIZE: usize = SAMPLE_RATE * 3;

pub struct TranscriptionState<'a, 'b> {
    whisper: Arc<Mutex<Option<WhisperContext>>>,
    buffer: Arc<Mutex<Vec<f32>>>,
    is_recording: Arc<Mutex<bool>>,
    params: Arc<Mutex<FullParams<'a, 'b>>>,
    language: Arc<Mutex<&'a str>>,
}



#[derive(Clone, Serialize)]
pub struct TranscriptedSegment {
    text: String,
    start: i64,
    end: i64,
}

impl<'a, 'b> TranscriptionState<'a, 'b> {
    pub fn new() -> Self {
        TranscriptionState{
            whisper: Arc::new(Mutex::new(None)),
            buffer: Arc::new(Mutex::new(Vec::<f32>::new())),
            is_recording: Arc::new(Mutex::new(false)),
            params: Arc::new(Mutex::new(FullParams::new(SamplingStrategy::Greedy{ best_of: 1 }))),
            language: Arc::new(Mutex::new("uk")),
        }
    }
}

#[tauri::command]
pub fn process_chunk<'a, 'b>(state: State<'_, TranscriptionState<'a, 'b>>, chunk: Vec<f32>) {
    let mut buffer = state.buffer.lock().unwrap();
    buffer.extend(chunk);
}


#[tauri::command]
pub fn start_transcription<'a, 'b>(state: State<'_, TranscriptionState<'a, 'b>>, on_transcript: Channel<TranscriptedSegment> ) -> Result<(), String> {

    let mut recording = state.is_recording.lock().unwrap();
    if *recording {
        return Err("Already recording".to_string());
    }  
    *recording = true;

    let recording_flag = Arc::clone(&state.is_recording);
    let buffer = Arc::clone(&state.buffer);
    let whisper= Arc::clone(&state.whisper);
    let params_lock = Arc::clone(&state.params);
    
    
    std::thread::spawn(move || {
        let whisper = whisper.lock().unwrap();
        let whisper_ctx = whisper.as_ref().expect("Whisper Model not initialized");
        let mut whisper_state = whisper_ctx.create_state().expect("Failed to create whisper state");

        

        while *recording_flag.lock().unwrap() {
            std::thread::sleep(std::time::Duration::from_millis(100));
            let mut audio_buffer = buffer.lock().unwrap();
            if audio_buffer.len() >= BUFFER_SIZE {

                let params = params_lock.lock().unwrap();
                whisper_state.full(params.clone(), &audio_buffer).expect("Failed to process audio");
                let num_segments = whisper_state
                    .full_n_segments()
                    .expect("failed to get number of segments");
                for i in 0..num_segments {
                    let segment = whisper_state
                        .full_get_segment_text(i)
                        .expect("failed to get segment");
                    let start_timestamp = whisper_state
                        .full_get_segment_t0(i)
                        .expect("failed to get segment start timestamp");
                    let end_timestamp = whisper_state
                        .full_get_segment_t1(i)
                        .expect("failed to get segment end timestamp");

                    let result = TranscriptedSegment {
                        text: segment,
                        start: start_timestamp,
                        end: end_timestamp,
                    };
                
                    on_transcript.send(result).unwrap();

                }

                audio_buffer.clear();
            }
        }
    });
    
    Ok(())
}

#[tauri::command]
pub fn stop_transcription<'a, 'b>(state: State<'_, TranscriptionState<'a, 'b>>) -> Result<(), String> {
    let mut recording = state.is_recording.lock().unwrap();
    *recording = false;
    Ok(())
}

#[tauri::command]
pub fn init_whisper<'a, 'b>(state: State<'_, TranscriptionState<'a, 'b>>, model_name: String) -> Result<String, String> {
    let doc_dir = dirs_next::document_dir().ok_or("Documents not found")?;
    let model_path = doc_dir.join("MedVoice").join("models").join(&model_name);

    if !model_path.exists() {
        return Err("Model not found".to_string());
    }

    let mut whisper_ctx = state.whisper.lock().unwrap();
    *whisper_ctx = Some(WhisperContext::new_with_params(model_path.to_str().unwrap(), WhisperContextParameters::default()).unwrap());

    Ok(format!("Model {} initialized", &model_name))
}

#[derive(Clone, Serialize, Deserialize)]
pub struct NewParams {
    language: String,
    num_of_threads: i32,
}

#[tauri::command]
pub fn set_params<'a, 'b>(state: State<'_, TranscriptionState<'a, 'b>>, params: NewParams) -> Result<String, String> {
    let mut current_params = state.params.lock().unwrap();
    
    static ENGLISH: &'static str = "en";
    static UKRAINIAN: &'static str = "uk";

    let lang_ref = match params.language.clone().as_str(){
        "en" => ENGLISH,
        "uk" => UKRAINIAN,
        _ => UKRAINIAN,
    };


    let mut whisper_params = FullParams::new(SamplingStrategy::Greedy{ best_of: 1 });

    whisper_params.set_language(Some(lang_ref));
    whisper_params.set_n_threads(params.num_of_threads);


    *current_params = whisper_params;

    Ok("Parameters updated".to_string())
}

#[tauri::command]
pub async fn process_conversation(conversation: String, on_process: Channel<String>) -> Result<(), String>  {
    let model = "llama3.2".to_string();
    let prompt = format!(
        "Ти — медичний асистент. На основі транскрибованого діалогу між лікарем і пацієнтом, структуруй інформацію у вигляді медичного звіту. Витягни ключову інформацію та запиши її в наступному форматі:
    
    - Скарги: {{основні скарги пацієнта}}
    - Анамнез: {{історія хвороби або симптомів}}
    - Об'єктивні дані: {{вимірювання, спостереження лікаря}}
    - Діагноз (попередній): {{якщо згадано}}
    - Рекомендації: {{лікування, обстеження, поради}}
    
    Текст діалогу:
    \"\"\"{}\"\"\"
    
    Сформуй відповідь у вигляді структурованого звіту українською мовою. Не додавай зайвих пояснень.", conversation);

    let ollama = Ollama::default();
    let mut stream = ollama.generate_stream(GenerationRequest::new(model, prompt)).await.expect("Failed to find Ollama, is it started on this device?");

    while let Some(res) = stream.next().await {
        let responses = res.unwrap();
        for resp in responses{
            on_process.send(resp.response.to_string());
        }
    }

    Ok(())
} 