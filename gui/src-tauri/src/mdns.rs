use mdns_sd::{ServiceDaemon, ServiceEvent, ServiceInfo};
use std::collections::HashMap;
use std::net::IpAddr;
use std::sync::{Arc, Mutex};
use std::time::Duration;

#[tauri::command]
pub async fn discover_services(service_type: String) -> Result<String, String> {
    let mdns = ServiceDaemon::new().expect("Failed to create daemon");
    let receiver = mdns.browse(&service_type).expect("Failed to browse");
    let recived = Arc::new(Mutex::new(String::new()));

    let recived_clone = recived.clone();

    std::thread::spawn(move || {
        let mut local_resolved = recived_clone.lock().unwrap();
        while let Ok(event) = receiver.recv() {
            match event {
                ServiceEvent::ServiceResolved(info) => {
                    println!("Resolved a new service: {}", info.get_fullname());
                    // let mut resolved = local_recived.unwrap();
                    
                    *local_resolved = format!("http://{}:{}", info.get_addresses_v4().iter().collect::<Vec<_>>()[0], info.get_port());
                }
                other_event => {
                    println!("Received other event: {:?}", &other_event);
                }
            }
        }
    });

    std::thread::sleep(std::time::Duration::from_secs(1));
    mdns.shutdown().unwrap();
    return Ok(recived.lock().unwrap().to_string());
    
}