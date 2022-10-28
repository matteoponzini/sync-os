#!/usr/bin/python3
import time
from watchdog.observers import Observer
from HelperWatcher import MonitorFolder

if __name__ == "__main__":
    configPath = "./install.yaml"
    event_handler = MonitorFolder('install')
    observerConfig = Observer()
    observerConfig.schedule(event_handler, configPath, recursive=True)
    observerConfig.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observerConfig.stop()
    observerConfig.join()