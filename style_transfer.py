import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import threading

def load_img(path_to_img):
    img = plt.imread(path_to_img)
    img = img.astype(np.float32)[np.newaxis, ...] / 255.
    return img

def stylize_image(content_path, style_path):
    # Load the content and style images.
    content_image = load_img(content_path)
    style_image = load_img(style_path)

    # Resize the style image to 256x256.
    style_image = tf.image.resize(style_image, (256, 256))

    # Load the model.
    hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    # Stylize the image.
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0].numpy()

    return stylized_image

def select_image(image_label):
    filename = filedialog.askopenfilename() # show an "Open" dialog box and return the path to the selected file
    if filename: # Check if the filename is not an empty string
        image = Image.open(filename)
        width, height = image.size
        content_ratio = height / width
        max_display_size = 350
        if width > height:
            new_width = max_display_size
            new_height = int(new_width * content_ratio)
        else:
            new_height = max_display_size
            new_width = int(new_height / content_ratio)
        display_image = image.resize((new_width, new_height)) # Resize the image for display only
        photo = ImageTk.PhotoImage(display_image)
        image_label.config(image=photo)
        image_label.image = photo
    return filename

def stylize(content_path, style_path):
    stylized_image = stylize_image(content_path, style_path)
    # Convert the stylized image to a PIL image
    stylized_image = Image.fromarray(np.uint8(stylized_image[0] * 255))

    # Get the original image's size
    original_image = Image.open(content_path)
    original_width, original_height = original_image.size
    content_ratio = original_height / original_width
    max_display_size = 350
    if original_width > original_height:
        new_width = max_display_size
        new_height = int(new_width * content_ratio)
    else:
        new_height = max_display_size
        new_width = int(new_height / content_ratio)

    # Resize the image for display only
    display_image = stylized_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(display_image)
    output_label.config(image=photo)
    output_label.image = photo

def stylize_button_click():
    threading.Thread(target=stylize, args=(content_path.get(), style_path.get())).start()

root = tk.Tk()

content_path = tk.StringVar()
style_path = tk.StringVar()

# Change the font and background color of the buttons
button_font = ("Helvetica", 10)
button_bg = "#e0e0e0"
button_active_bg = "#c0c0c0"

content_button = tk.Button(root, text="Select Content Image", command=lambda: content_path.set(select_image(content_label)), font=button_font, bg=button_bg, activebackground=button_active_bg)
style_button = tk.Button(root, text="Select Style Image", command=lambda: style_path.set(select_image(style_label)), font=button_font, bg=button_bg, activebackground=button_active_bg)
stylize_button = tk.Button(root, text="Stylize", command=stylize_button_click, font=button_font, bg=button_bg, activebackground=button_active_bg)

content_label = tk.Label(root)
content_label.grid(row=0, column=0)
content_button.grid(row=1, column=0)

style_label = tk.Label(root)
style_label.grid(row=0, column=2)
style_button.grid(row=1, column=2)

output_label = tk.Label(root)
output_label.grid(row=0, column=1)
stylize_button.grid(row=1, column=1)

root.mainloop()