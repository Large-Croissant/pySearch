import os
import tkinter as tk
from tkinter import filedialog
import threading
import time
import re

def search(path: str, target: str, found: list[str], counter: threading.Event):
    for root, dirs, files in os.walk(path):
        for file in files:
            counter[0] += 1
            regex_search = re.search(target, file)
            if regex_search:
                found.append(os.path.join(root, file))

def update_count(counter: list[int], done: threading.Event, start_time: float):
    # time.sleep(.2)
    while not done.is_set():
        print(f"Searched {counter[0]:,} files in {round(time.perf_counter()-start_time, 1)} seconds", end="\r")
        # time.sleep(.01)

def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    to_search = input("Enter RegEx for search: ")
    print("Beginning search...")

    files_found = []
    counter = [0]
    done = threading.Event()
    start_time = time.perf_counter()
    counter_thread = threading.Thread(target=update_count, args=(counter, done, start_time))
    counter_thread.start()
    search(file_path, to_search, files_found, counter)
    print(f"Searched {counter[0]:,} files in {round(time.perf_counter()-start_time, 1)} seconds", end="\r")
    done.set()
    counter_thread.join()

    print("\nFound:")
    for file in files_found:
        print(f"\t{file}")

if __name__ == "__main__":
    main()