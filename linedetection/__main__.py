from tkinter.filedialog import askopenfilename
from process_image import select_image_file, process_image

# Import the default values
from image_preprocessing import MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS

if __name__ == "__main__":
    # Ask the user to select an image file
    image_file = select_image_file()
    if image_file:  # Check if a file was selected
        process_image(image_file, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS)
    else:
        print("No image file selected. Exiting.")