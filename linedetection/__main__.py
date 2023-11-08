from process_image import process_image, select_image_file
from image_test_set import process_test_set
import sys

# Importing default values
from image_preprocessing import MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS

if __name__ == "__main__":
    sys.stdout.flush()  # Force flushing the stdout buffer
    choice = input("Enter '1' to upload image or '2' to run test set: ").strip()

    if choice == '1':
        print("Option 1 selected: Uploading an image.")
        image_file = select_image_file()
        if image_file:
            process_image(image_file, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS)
        else:
            print("No image file selected. Exiting.")
    elif choice == '2':
        print("Option 2 selected: Running test set.")
        try:
            process_test_set(MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS)
            print("Test set processed.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Invalid selection ('{choice}'). Exiting.")
