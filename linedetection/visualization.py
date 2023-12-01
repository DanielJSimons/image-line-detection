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

import matplotlib.pyplot as plt
import json

def visualize_page_results(page_number):
    with open(f"output/results_page_{page_number}.json", "r") as file:
        results = json.load(file)

    original_image = plt.imread(results["original_image_path"])
    line_data = results["line_data"]
    
    return original_image, line_data


def display_images_in_grid(images_and_lines, grid_dims):
    fig, axes = plt.subplots(*grid_dims)
    axes = axes.flatten()

    for ax, (image, lines) in zip(axes, images_and_lines):
        ax.imshow(image, cmap='gray')
        for x0, y0, x1, y1 in lines:
            ax.plot([x0, x1], [y0, y1], '-r')
        ax.axis('off')

    plt.show()

