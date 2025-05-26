import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import shutil


class FontCharacterClassifier:
    def __init__(self, root):
        self.root = root
        self.root.title("Font Character Classifier")
        self.root.geometry("800x600")

        self.image_folder = None
        self.current_image_path = None
        self.current_image = None
        self.image_files = []
        self.current_index = 0
        self.temp_bin_folder = None
        self.output_folder = None
        self.crop_mode = False
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.cropped_images = []
        self.output_to_svg = True

        self.create_widgets()

    def create_widgets(self):
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        top_frame = tk.Frame(main_container)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(
            top_frame, text="Select Image Folder", command=self.select_folder
        ).pack(side=tk.LEFT, padx=5)

        self.image_frame = tk.Frame(main_container, height=400, width=600)
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.image_frame.pack_propagate(False)

        canvas_frame = tk.Frame(self.image_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="gray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = tk.Scrollbar(
            canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = tk.Scrollbar(
            self.image_frame, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.configure(
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        input_frame = tk.Frame(main_container)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(input_frame, text="Character:").pack(side=tk.LEFT, padx=5)
        self.char_entry = tk.Entry(input_frame, width=10)
        self.char_entry.pack(side=tk.LEFT, padx=5)
        self.char_entry.bind("<Return>", self.process_input)

        self.crop_frame = tk.Frame(main_container)
        self.crop_button = tk.Button(
            self.crop_frame, text="Save Crop", command=self.save_crop
        )
        self.crop_button.pack(side=tk.LEFT, padx=5)
        self.cancel_crop_button = tk.Button(
            self.crop_frame, text="Cancel", command=self.cancel_crop
        )
        self.cancel_crop_button.pack(side=tk.LEFT, padx=5)

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        tk.Label(
            self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W
        ).pack(side=tk.BOTTOM, fill=tk.X)

    def select_folder(self):
        folder_path = filedialog.askdirectory(
            title="Select folder with character images"
        )
        if not folder_path:
            return

        self.image_folder = folder_path

        self.temp_bin_folder = os.path.join(os.path.dirname(folder_path), "temp_bin")
        os.makedirs(self.temp_bin_folder, exist_ok=True)

        self.image_files = [
            f
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        if not self.image_files:
            messagebox.showinfo("Info", "No image files found in the selected folder.")
            return

        self.current_index = 0
        self.load_current_image()

    def load_current_image(self):
        if not self.image_files or self.current_index >= len(self.image_files):
            self.status_var.set("All images processed!")
            self.canvas.delete("all")
            return

        filename = self.image_files[self.current_index]
        self.current_image_path = os.path.join(self.image_folder, filename)
        try:
            self.current_image = Image.open(self.current_image_path)
            self.display_image()
            self.status_var.set(
                f"Image {self.current_index+1}/{len(self.image_files)}: {filename}"
            )
            self.char_entry.delete(0, tk.END)
            self.char_entry.focus_set()

        except Exception as e:
            self.status_var.set(f"Error loading image: {str(e)}")
            self.current_index += 1
            self.load_current_image()

    def display_image(self):
        if self.current_image:
            canvas_width = self.canvas.winfo_width() or 600
            canvas_height = self.canvas.winfo_height() or 400

            img_width, img_height = self.current_image.size

            ratio = min(canvas_width / img_width, canvas_height / img_height)

            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)

            self.displayed_image = self.current_image.resize(
                (new_width, new_height), Image.LANCZOS
            )
            self.photo_image = ImageTk.PhotoImage(self.displayed_image)

            self.canvas.delete("all")
            self.canvas.config(scrollregion=(0, 0, new_width, new_height))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

    def process_input(self, event=None):
        if not self.current_image_path:
            return

        char_input = self.char_entry.get().strip()

        if not char_input:
            self.move_to_temp_bin()
        elif len(char_input) == 1:
            self.rename_as_character(char_input)
        else:
            self.enable_crop_mode(char_input)
            return

        self.current_index += 1
        self.load_current_image()

    def move_to_temp_bin(self):
        filename = os.path.basename(self.current_image_path)
        destination = os.path.join(self.temp_bin_folder, filename)

        try:
            shutil.move(self.current_image_path, destination)
            self.status_var.set(f"Moved {filename} to temp_bin folder")
        except Exception as e:
            self.status_var.set(f"Error moving file: {str(e)}")

    def rename_as_character(self, char):
        filename = os.path.basename(self.current_image_path)
        file_ext = os.path.splitext(filename)[1]

        base_name = f"{char}{file_ext}"
        new_path = os.path.join(self.image_folder, base_name)

        iteration = 1
        while os.path.exists(new_path):
            base_name = f"{char}(iteration{iteration}){file_ext}"
            new_path = os.path.join(self.image_folder, base_name)
            iteration += 1

        try:
            shutil.move(self.current_image_path, new_path)
            self.status_var.set(f"Renamed to {base_name}")
            self.image_files[self.current_index] = base_name
        except Exception as e:
            self.status_var.set(f"Error renaming file: {str(e)}")

    def enable_crop_mode(self, chars):
        self.crop_mode = True
        self.crop_chars = chars
        self.crop_frame.pack(fill=tk.X, padx=10, pady=5)
        self.status_var.set("Crop mode enabled. Draw rectangle around character.")

    def on_mouse_down(self, event):
        if not self.crop_mode:
            return

        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if self.rect_id:
            self.canvas.delete(self.rect_id)

        self.rect_id = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            width=2,
        )

    def on_mouse_drag(self, event):
        if not self.crop_mode or not self.rect_id:
            return

        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_mouse_up(self, event):
        pass

    def save_crop(self):
        if not self.rect_id or not self.current_image:
            return

        x1, y1, x2, y2 = self.canvas.coords(self.rect_id)

        canvas_width, canvas_height = self.displayed_image.size
        orig_width, orig_height = self.current_image.size

        x_ratio = orig_width / canvas_width
        y_ratio = orig_height / canvas_height

        orig_x1 = int(min(x1, x2) * x_ratio)
        orig_y1 = int(min(y1, y2) * y_ratio)
        orig_x2 = int(max(x1, x2) * x_ratio)
        orig_y2 = int(max(y1, y2) * y_ratio)

        cropped = self.current_image.crop((orig_x1, orig_y1, orig_x2, orig_y2))

        current_char = self.crop_chars[len(self.cropped_images)]

        file_ext = ".png"
        char_filename = f"{current_char}{file_ext}"
        char_path = os.path.join(self.image_folder, char_filename)

        iteration = 1
        while os.path.exists(char_path):
            char_filename = f"{current_char}(iteration{iteration}){file_ext}"
            char_path = os.path.join(self.image_folder, char_filename)
            iteration += 1

        cropped.save(char_path)
        self.cropped_images.append(char_path)

        if len(self.cropped_images) >= len(self.crop_chars):
            os.remove(self.current_image_path)

            self.cancel_crop()

            self.image_files = [
                os.path.basename(path) for path in self.cropped_images
            ] + self.image_files[self.current_index + 1 :]
            self.cropped_images = []
            self.current_index = 0
            self.load_current_image()
        else:
            self.canvas.delete(self.rect_id)
            self.rect_id = None
            self.status_var.set(
                f"Crop {len(self.cropped_images)}/{len(self.crop_chars)} saved. Select next character."
            )

    def cancel_crop(self):
        self.crop_mode = False
        self.crop_frame.pack_forget()
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None
        self.cropped_images = []
        self.status_var.set("Crop mode cancelled")


if __name__ == "__main__":
    root = tk.Tk()
    app = FontCharacterClassifier(root)
    root.mainloop()
