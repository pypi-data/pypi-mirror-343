import os
from prompt_hot_reloading.prompt_source.prompt_source import PromptSource
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileSystemSource(PromptSource):
    def __init__(self, prompt_dir: str):
        self.prompt_dir = prompt_dir

    def load_all(self):
        data = {}
        for fname in os.listdir(self.prompt_dir):
            path = os.path.join(self.prompt_dir, fname)
            if os.path.isfile(path):
                name, _ = os.path.splitext(fname)
                data[name] = open(path).read()
        return data

    def watch(self, on_change):
        class H(FileSystemEventHandler):
            def on_modified(self, ev):
                if not ev.is_directory:
                    name, _ = os.path.splitext(os.path.basename(ev.src_path))
                    on_change(name, open(ev.src_path).read())

            on_created = on_modified

        obs = Observer()
        obs.schedule(H(), self.prompt_dir, recursive=False)
        obs.daemon = True
        obs.start()
