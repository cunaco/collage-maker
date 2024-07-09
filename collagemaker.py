from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import math
from tkinter.ttk import Progressbar

def resize_and_crop(image, target_width, target_height):
    """Resize and crop the image to fill the target dimensions while maintaining aspect ratio."""
    width, height = image.size
    ratio = max(target_width / width, target_height / height)
    new_width, new_height = int(width * ratio), int(height * ratio)
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2
    return resized_image.crop((left, top, right, bottom))

def create_collage(images, collage_width, collage_height, progress_bar):
    num_images = len(images)
    images_per_row = math.ceil(math.sqrt(num_images * collage_width / collage_height))
    images_per_col = math.ceil(num_images / images_per_row)
    
    image_width = collage_width // images_per_row
    image_height = collage_height // images_per_col
    
    collage_image = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))
    
    for index, image in enumerate(images):
        x_offset = (index % images_per_row) * image_width
        y_offset = (index // images_per_row) * image_height
        resized_image = resize_and_crop(image, image_width, image_height)
        collage_image.paste(resized_image, (x_offset, y_offset))
        
        progress_bar['value'] = (index + 1) / num_images * 100
        progress_bar.update_idletasks()

    return collage_image

def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img = Image.open(os.path.join(folder_path, filename))
            images.append(img)
    return images

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        images = load_images_from_folder(folder_path)
        if images:
            try:
                collage_width = int(entry_width.get())
                collage_height = int(entry_height.get())
                
                progress_bar = Progressbar(frame, maximum=100)
                progress_bar.grid(row=3, column=0, columnspan=2, pady=10)
                
                collage_image = create_collage(images, collage_width, collage_height, progress_bar)
                
                save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
                if save_path:
                    collage_image.save(save_path)
                    collage_image.show()
                    messagebox.showinfo("Успех", f"Коллаж создан и сохранен как '{save_path}'.")
                else:
                    messagebox.showwarning("Предупреждение", "Сохранение отменено.")
                    
                progress_bar.destroy()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        else:
            messagebox.showerror("Ошибка", "В выбранной папке нет изображений.")
    else:
        messagebox.showerror("Ошибка", "Папка не выбрана.")

# Создание GUI
root = tk.Tk()
root.title("Создание коллажа")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_width = tk.Label(frame, text="Ширина коллажа:")
label_width.grid(row=0, column=0, padx=5, pady=5)

entry_width = tk.Entry(frame)
entry_width.grid(row=0, column=1, padx=5, pady=5)
entry_width.insert(0, "800")  # Значение по умолчанию

label_height = tk.Label(frame, text="Высота коллажа:")
label_height.grid(row=1, column=0, padx=5, pady=5)

entry_height = tk.Entry(frame)
entry_height.grid(row=1, column=1, padx=5, pady=5)
entry_height.insert(0, "600")  # Значение по умолчанию

button_select_folder = tk.Button(frame, text="Выбрать папку с изображениями", command=select_folder)
button_select_folder.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
