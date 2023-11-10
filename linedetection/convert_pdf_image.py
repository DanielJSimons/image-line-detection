from image_preprocessing import MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS
from pdf2image import convert_from_path
from process_image import process_image
from tkinter import filedialog
import os
import tkinter as tk

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
        print("Currently only PDF page 1 is supported.")
        return file_path, 'pdf'
    else:
        print("Unsupported file type selected.")
        return None, None
    
def process_pdf(pdf_file):
    try:
        images = convert_from_path(pdf_file)
        for img in images:
            img_path = "temp_image.jpg"  # Save the image and get the path
            img.save(img_path, 'JPEG')
            process_image(img_path, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS)
    except Exception as e:
        print(f"Error processing PDF: {e}")