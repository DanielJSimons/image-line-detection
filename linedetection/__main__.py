from image_preprocessing import MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS
from input_handling import get_input_with_timeout
from process_image import process_image
from image_test_set import process_test_set
from convert_pdf_image import select_file, process_pdf_multi_thread, processed_images_queue

if __name__ == "__main__":
    choice = get_input_with_timeout("Enter '1' to upload file (image/PDF) or '2' to run test set: ", 15)

    if choice:
        choice = choice.strip()

        if choice == '1':
            print("Option 1 selected: Processing file.")
            file_path, file_type = select_file()
            if file_path:
                if file_type == 'image':
                    process_image(file_path, MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS)
                elif file_type == 'pdf':
                    process_pdf_multi_thread(file_path)
                else:
                    print("Unsupported file type.")
            else:
                print("No file selected.")
        elif choice == '2':
            print("Option 2 selected: Running test set.")
            process_test_set(MIN_LEN, DEG, MAX_R, HOUGH_THRES, HOUGH_POINTS)
            print("Test set processed.")
        else:
            print(f"Invalid selection ('{choice}').")
    else:
        print("Exiting due to no input.")