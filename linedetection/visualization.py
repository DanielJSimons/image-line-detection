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
