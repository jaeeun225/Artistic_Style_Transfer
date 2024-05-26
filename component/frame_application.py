import cv2
import numpy as np

def add_complex_frame_to_image(img):
    # Define the colors and thickness of the frames
    frame_colors = [[50, 60, 70], [100, 110, 120], [150, 160, 170], [255, 255, 255], [150, 160, 170], [100, 110, 120], [50, 60, 70], [255, 255, 255], [150, 160, 170], [100, 110, 120], [50, 60, 70], [255, 255, 255], [150, 160, 170], [100, 110, 120], [50, 60, 70]]  # White, Beige, Gray
    frame_thicknesses = [1, 1, 2, 6, 2, 1, 1, 12, 2, 1, 1, 6, 2, 1, 1]

    # Add the frames to the image
    for color, thickness in zip(frame_colors, frame_thicknesses):
        img = cv2.copyMakeBorder(img, thickness, thickness, thickness, thickness, 
                                 cv2.BORDER_CONSTANT, value=color)

    return img