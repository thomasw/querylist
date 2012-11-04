"""Automatically runs tests and pep8 checker on .py file update."""
from datetime import datetime
import time
import os
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def run_tests():
    "Run tests with nosetests and pep8 conformance checker."
    os.chdir(BASE_DIR)

    print "Running unit tests at %s" % datetime.now()
    subprocess.call('nosetests')

    print "Checking PEP 8 compliance...\n"
    subprocess.call(['pep8', 'querylist/'])
    print "\n"

    print "Finished running tests at %s!\n" % datetime.now()


class ChangeHandler(FileSystemEventHandler):
    """Runs the project's tests if .py files are changed."""
    def on_any_event(self, event):
        if event.src_path.rpartition('.')[-1] == 'py':
            run_tests()

if __name__ == '__main__':
    run_tests()

    observer = Observer()
    observer.schedule(ChangeHandler(), BASE_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
