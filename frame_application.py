import cv2
import numpy as np

def add_complex_frame_to_image(img):
    # Define the colors and thickness of the frames
    frame_colors = [[100, 100, 100], [160, 160, 160], [210, 210, 210], [255, 255, 255], [210, 210, 210], [160, 160, 160], [100, 100, 100], [160, 160, 160], [210, 210, 210], [255, 255, 255], [210, 210, 210], [160, 160, 160], [100, 100, 100]]  # White, Beige, Gray
    frame_thicknesses = [2, 3, 4, 16, 4, 3, 2, 3, 4, 16, 4, 3, 2]

    # Add the frames to the image
    for color, thickness in zip(frame_colors, frame_thicknesses):
        img = cv2.copyMakeBorder(img, thickness, thickness, thickness, thickness, 
                                 cv2.BORDER_CONSTANT, value=color)

    return img