# input_handling.py

import threading
import queue
import sys

# Function to run in the thread
def input_with_timeout(prompt, output_queue):
    print(prompt, end='') 
    sys.stdout.flush() 
    output_queue.put(input())

# Function to get input with timeout using a thread
def get_input_with_timeout(prompt, timeout=30):
    output_queue = queue.Queue()
    input_thread = threading.Thread(target=input_with_timeout, args=(prompt, output_queue))
    input_thread.start()
    input_thread.join(timeout)
    if input_thread.is_alive():
        print("\nTimeout occurred - no input received.")
        return None
    else:
        return output_queue.get()