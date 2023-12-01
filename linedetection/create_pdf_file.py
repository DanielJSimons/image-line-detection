from PIL import Image
import os

def create_combined_pdf(image_paths, output_pdf_path):
    output_pdf_path = f"output/{output_pdf_path}"
    image_list = [Image.open(img_path).convert('RGB') for img_path in image_paths]
    first_image = image_list.pop(0)
    first_image.save(output_pdf_path, save_all=True, append_images=image_list)
    print("Saving first image.")


    for img_path in image_paths:
        os.remove(img_path)
