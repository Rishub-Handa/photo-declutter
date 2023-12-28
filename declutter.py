'''
Description: 
- A simple script to help declutter your images.

TODO: 
- Make sure all filenames are unique even in different directories
'''

import os
import glob
import shutil
import tkinter as tk
from tkinter import Frame, Canvas, Scrollbar
from PIL import Image, ImageTk



class Declutter:

    def __init__(self, source_dir, target_dir): 
        if not os.path.isdir(source_dir):
            raise Exception("Source directory not found")
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
        self.source_dir = source_dir
        self.target_dir = target_dir

        # Recursively get all image files from the source directory
        self.image_files = []
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')):
                    self.image_files.append(os.path.join(root, file))
        if not self.image_files:
            raise Exception("No images found in the directory")
        
        self.curr_image_idx = 0

        # Setting up the Tkinter window
        self.setup_ui()

    def setup_ui(self):
        # ... existing setup ...
        self.root = tk.Tk()
        self.root.title("Image Viewer")
        self.image_label = tk.Label(self.root)
        self.image_label.pack(side="left")
        self.index_label = tk.Label(self.root, text="")
        self.index_label.pack()

        # Create a scrollable frame for thumbnails
        self.thumbnail_frame = Frame(self.root)
        self.thumbnail_canvas = Canvas(self.thumbnail_frame)
        self.scrollbar = Scrollbar(self.thumbnail_frame, orient="vertical", command=self.thumbnail_canvas.yview)
        self.scrollable_frame = Frame(self.thumbnail_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.thumbnail_canvas.configure(
                scrollregion=self.thumbnail_canvas.bbox("all")
            )
        )

        self.thumbnail_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.thumbnail_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.thumbnail_frame.pack(side="right", fill="y")
        self.thumbnail_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind the key press event
        self.root.bind('<Right>', self.handle_key_press)
        self.root.bind('<Down>', self.handle_key_press)
        self.root.bind('<Up>', self.handle_key_press)
        self.root.bind('<Left>', self.handle_key_press)

    def refresh_thumbnails(self):
        # Clear current thumbnails
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Load and display updated thumbnails
        self.load_thumbnails()

    def load_thumbnails(self):
        # Load and display thumbnails for each image in the target directory
        for image_path in os.listdir(self.target_dir):
            if image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')):
                img = Image.open(os.path.join(self.target_dir, image_path))
                img.thumbnail((100, 100))  # Resize to thumbnail size
                photo = ImageTk.PhotoImage(img)
                label = tk.Label(self.scrollable_frame, image=photo)
                label.image = photo  # Keep a reference!
                label.pack()

    def run(self):
        # Display the first image
        self.update_image(0)
        self.load_thumbnails()

        # Start the Tkinter event loop
        self.root.mainloop()

    def update_window(self, image_idx): 
        self.update_image(image_idx)
        self.refresh_thumbnails()

    def update_image(self, image_idx):
        image_path = os.path.join(self.source_dir, self.image_files[image_idx])
        img = Image.open(image_path)

        # Resize the image
        screen_width = self.root.winfo_screenwidth()  # Get screen width
        screen_height = self.root.winfo_screenheight()  # Get screen height
        max_size = (screen_width // 2, screen_height // 2)  # Define max size (half of screen size)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img

        dest = os.path.join(self.target_dir, os.path.basename(self.image_files[self.curr_image_idx]))
        checkmark = " ✅" if os.path.isfile(dest) else ""

        index_text = f"Image {image_idx + 1} of {len(self.image_files)}" + checkmark
        self.index_label.config(text=index_text)

    def handle_key_press(self, event):
        if event.keysym == 'Right':
            self.curr_image_idx = min(self.curr_image_idx + 1, len(self.image_files) - 1)
        elif event.keysym == 'Down':
            src = self.image_files[self.curr_image_idx]
            dst = os.path.join(self.target_dir, os.path.basename(self.image_files[self.curr_image_idx]))
            shutil.copy(src, dst)
            print(f"Copied: {self.image_files[self.curr_image_idx]}")
            self.refresh_thumbnails()
        elif event.keysym == 'Up':
            src = os.path.join(self.target_dir, os.path.basename(self.image_files[self.curr_image_idx]))
            if os.path.isfile(src):
                os.remove(src)
                print(f"Removed: {src}")
                self.refresh_thumbnails()
            else:
                print(f"File not found: {src}")
        elif event.keysym == 'Left':
            self.curr_image_idx = max(self.curr_image_idx - 1, 0)


        self.update_image(self.curr_image_idx)




if __name__ == "__main__":
    source_dir = "/Users/rishubhanda/Desktop/Gia 2"
    target_dir = "./target1"
    # display_images(source_dir, target_dir)
    declutter = Declutter(source_dir, target_dir)
    declutter.run()
    print("Done. ")