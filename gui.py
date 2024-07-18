import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk


class WatermarkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")

        self.setup_widgets()

    def setup_widgets(self):

        # Frame in which everything else will be placed
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        self.image = Image.open("placeholder.jpg")
        self.tk_image = ImageTk.PhotoImage(Image.open("placeholder.jpg"))
        self.label = tk.Label(frame, image=self.tk_image)
        self.label.grid(row=0, columnspan=3, padx=10, pady=10)

        self.entry = tk.Entry(frame)
        self.entry.grid(row=1, columnspan=3)

        self.load_button = tk.Button(frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=2, column=0, padx=5, pady=10)

        self.apply_button = tk.Button(frame, text="Apply Watermark", command=self.apply_watermark)
        self.apply_button.grid(row=2, column=1, padx=5, pady=10)

        self.save_button = tk.Button(frame, text="Save Image", command=self.save_image)
        self.save_button.grid(row=2, column=2, padx=5, pady=10)

    def load_image(self):
        image_path = filedialog.askopenfilename()
        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(Image.open(image_path))
        self.label.configure(image=self.tk_image)
        self.label.image = self.tk_image

    def apply_watermark(self):
        if self.image.mode != "RGBA":
            self.image = self.image.convert("RGBA")
        watermark_text = self.entry.get()
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.load_default()
        text_width = draw.textlength(watermark_text, font=font)
        text_height = font.size
        x = self.image.width - text_width - 10
        y = self.image.height - text_height - 10
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 64))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.tk_image)
        self.label.image = self.tk_image

    def save_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image is None:
            print("No image to save. Please load an image first.")
            return False

        try:
            self.image.save(save_path)
            print(f"Image saved successfully at {save_path}")
            return True
        except IOError as e:
            print(f"Error saving image to {save_path}: {e}")
            return False
