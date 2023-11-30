from matplotlib import pyplot as plt

def show_images(images, titles, figsize=(24,12)):

    if len(images) != len(titles):
        raise ValueError("The number of images must match the number of titles.")

    plt.figure(figsize=figsize)
    for i, (image, title) in enumerate(zip(images, titles)):
        plt.subplot(1, len(images), i + 1)
        plt.imshow(image, cmap='gray')
        plt.title(title)
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout()
    plt.show()

def plot_detected_lines(ax, x0, y0, x1, y1, color='-r'):

    ax.plot((x0, x1), (y0, y1), color)

import json
import matplotlib.pyplot as plt

def visualize_page_results(page_number):
    # Load the processed data
    print(f"Visualizing page {page_number}")
    json_path = f"results_page_{page_number}.json"
    print(f"Reading JSON: {json_path}")

    with open(f"results_page_{page_number}.json", "r") as file:
        results = json.load(file)

    img_path = results["original_image_path"]
    print(f"Loading image: {img_path}")

    # Load original image
    original_image = plt.imread(results["original_image_path"])

    # Create a plot
    plt.figure(figsize=(8, 6))
    plt.imshow(original_image, cmap='gray')
    plt.title(f"Processed Page {page_number}")

    # Draw lines based on the processed data
    for x0, y0, x1, y1 in results["line_data"]:
        plt.plot([x0, x1], [y0, y1], '-r')

    # Save or show the plot
    plt.savefig(f"visualization_page_{page_number}.png")
    print(f"Visualization saved for page {page_number}")
    plt.close()