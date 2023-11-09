import sys
from input_handling import get_input_with_timeout
from process_image import process_image, select_image_file
from image_test_set import process_test_set
from image_preprocessing import MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS

if __name__ == "__main__":
    sys.stdout.flush() 
    choice = get_input_with_timeout("Enter '1' to upload image or '2' to run test set: ", 15)

    if choice:
        choice = choice.strip()

        if choice == '1':
            print("Option 1 selected: Processing image.")
            image_file = select_image_file()
            if image_file:
                process_image(image_file, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS)
            else:
                print("No image file selected.")
        elif choice == '2':
            print("Option 2 selected: Running test set.")
            process_test_set(MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS)
            print("Test set processed.")
        else:
            print(f"Invalid selection ('{choice}').")
    else:
        print("Exiting due to no input.")
