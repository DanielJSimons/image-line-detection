from image_preprocessing import MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS
from pdf2image import convert_from_path
from process_image import process_image, process_image_pdf
from tkinter import filedialog
import os
import tkinter as tk
from threading import Thread
from queue import Queue
import json
from visualization import visualize_page_results


processed_images_queue = Queue()

def select_file():
    # Preventing Tkinter window from appearing.
    root = tk.Tk()
    root.withdraw()

    # Show an "Open" dialog box and return the path to the selected file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"),
                                                      ("PDF files", "*.pdf")])
    if not file_path:  # User cancelled the dialog
        return None, None

    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']:
        return file_path, 'image'
    elif file_extension == '.pdf':
        print("Output PDF")
        return file_path, 'pdf'
    else:
        print("Unsupported file type selected.")
        return None, None
    
import json
import matplotlib.pyplot as plt
    
def process_pdf_multi_thread(pdf_file):
    try:
        images = convert_from_path(pdf_file)
        threads = []

        for i, img in enumerate(images):
            thread = Thread(target=process_and_show_page, args=(img, i+1, True))  # Pass a flag to not delete
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print("printing images")
        total_number_of_pages = len(images)
        for i in range(1, total_number_of_pages + 1):
            visualize_page_results(i)

        # Delete temp images after visualization
        for i in range(1, total_number_of_pages + 1):
            os.remove(f"temp_image_page_{i}.jpg")

    except Exception as e:
        print(f"Error processing PDF: {e}")


def process_and_show_page(img, page_number, keep_image=False):
    try:
        temp_img_path = f"temp_image_page_{page_number}.jpg"
        img.save(temp_img_path, 'JPEG')

        # Perform image processing and save results
        results = process_image_pdf(temp_img_path, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS)
        with open(f"results_page_{page_number}.json", "w") as file:
            json.dump(results, file)

        if not keep_image:
            os.remove(temp_img_path)

    except Exception as e:
        print(f"Error processing page {page_number}: {e}")



