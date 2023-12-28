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
        self.root = tk.Tk()
        self.root.title("Image Viewer")
        self.label = tk.Label(self.root)
        self.label.pack()
        self.index_label = tk.Label(self.root, text="")
        self.index_label.pack()

        # Bind the key press event
        self.root.bind('<Right>', self.handle_key_press)
        self.root.bind('<Down>', self.handle_key_press)
        self.root.bind('<Up>', self.handle_key_press)
        self.root.bind('<Left>', self.handle_key_press)

    def run(self):
        # Display the first image
        self.update_image(0)

        # Start the Tkinter event loop
        self.root.mainloop()

    def update_image(self, image_idx):
        image_path = os.path.join(self.source_dir, self.image_files[image_idx])
        img = Image.open(image_path)

        # Resize the image
        screen_width = self.root.winfo_screenwidth()  # Get screen width
        screen_height = self.root.winfo_screenheight()  # Get screen height
        max_size = (screen_width // 2, screen_height // 2)  # Define max size (half of screen size)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        img = ImageTk.PhotoImage(img)
        self.label.config(image=img)
        self.label.image = img

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
        elif event.keysym == 'Up':
            src = os.path.join(self.target_dir, os.path.basename(self.image_files[self.curr_image_idx]))
            if os.path.isfile(src):
                os.remove(src)
                print(f"Removed: {src}")
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