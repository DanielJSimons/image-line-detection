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
        print("Output PDF")
        return file_path, 'pdf'
    else:
        print("Unsupported file type selected.")
        return None, None
    
def process_pdf(pdf_file):
    try:
        # Convert each page of the PDF to an image
        images = convert_from_path(pdf_file)

        for i, img in enumerate(images):
            # Create a unique temporary file name for each image
            temp_img_path = f"temp_image_page_{i+1}.jpg"

            # Save the image
            img.save(temp_img_path, 'JPEG')
            print(f"Page {i+1}")
            # Process the image
            process_image(temp_img_path, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS)

            # Optionally, delete the temporary file after processing
            os.remove(temp_img_path)

    except Exception as e:
        print(f"Error processing PDF: {e}")