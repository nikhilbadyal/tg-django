"""Restart on code changes."""

import os
import subprocess
import sys
import time
from typing import Any

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class MyHandler(FileSystemEventHandler):  # type: ignore[misc]
    def __init__(self, excluded_dir: list[str]) -> None:
        """Initialize the handler and start the main script process.

        Args:
            excluded_dir: A list of excluded directory names.
        """
        self.process: subprocess.Popen[Any] | None = None
        self.excluded_directories = excluded_dir
        self.start_process()

    def on_modified(self, event: FileSystemEvent) -> None:
        """Called when a file is modified in the watched directory.

        Args:
            event: An event object representing the file system event.
        """
        path_components = os.path.normpath(event.src_path).split(os.path.sep)

        # Check if the modified file is not in the excluded directories and has a .py extension
        if all(directory not in path_components for directory in self.excluded_directories) and event.src_path.endswith(
            ".py",
        ):
            self.restart_process()

    def start_process(self) -> None:
        """Start the main script process."""
        self.process = subprocess.Popen([sys.executable, "main.py"])

    def restart_process(self) -> None:
        """Terminate the main script process and start it again."""
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.start_process()


if __name__ == "__main__":
    included_directories: str = "."
    excluded_directories = ["migrations"]

    # Initialize the event handler with the excluded_directories list
    event_handler = MyHandler(excluded_directories)

    # Start the Observer to watch for changes in the included_directories
    observer = Observer()
    observer.schedule(event_handler, included_directories, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
