import os
import tkinter as tk
from tkinter import filedialog
import threading
import time
import re

def search(path: str, target: str, found: list[str], counter: list[int], search_threads: list[threading.Thread]):
    for root, dirs, files in os.walk(path):
        for file in files:
            counter[0] += 1
            regex_search = re.search(target, file)
            if regex_search:
                found.append(os.path.join(root, file))
        for dir in dirs:
            thread = threading.Thread(target=search, args=(f"{root}/{dir}", target, found, counter, search_threads))
            thread.start()
            search_threads.append(thread)
            os.scandir()

def update_count(counter: list[int], done: threading.Event, start_time: float):
    # time.sleep(.2)
    while not done.is_set():
        print(f"Files searched: {counter[0]:,} in {round(time.perf_counter()-start_time)} seconds",end="\r")
        time.sleep(.1)

def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    to_search = input("Enter RegEx for search: ")
    print("Beginning search...")

    files_found = []
    counter = [0]
    done = threading.Event()
    search_threads: list[threading.Thread] = []

    counter_thread = threading.Thread(target=update_count, args=(counter, done, time.perf_counter()))
    counter_thread.start()

    search(file_path, to_search, files_found, counter, search_threads)
    for thread in search_threads:
        thread.join()

    done.set()
    counter_thread.join()

    print("\n\nFound:")
    for file in files_found:
        print(f"\t{file}")

if __name__ == "__main__":
    main()