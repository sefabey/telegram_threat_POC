import gradio as gr
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def display_with_overlay(inputs):
    img, text = inputs
    # convert image from numpy array to PIL image
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    # create text overlay
    text = "uploaded by user"
    font = ImageFont.truetype("arial.ttf", 16)
    draw.text((0, 0), text, font=font, fill=(255, 255, 255))
    # convert back to numpy array
    img_arr = np.array(img)
    return img_arr, "user input text: " + text


inputs = [gr.inputs.Image(shape=(256, 256, 3)), gr.inputs.Textbox()]
outputs = [gr.outputs.Image(), gr.outputs.Label()]
iface = gr.Interface(fn=display_with_overlay, inputs=inputs, outputs=outputs, live=True)
iface.launch()
