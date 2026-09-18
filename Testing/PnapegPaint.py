import tkinter as tk
from tkinter import messagebox, colorchooser
import struct
from PIL import Image, ImageDraw

MAGIC_NUMBER = b'PNAP'
HEADER_FORMAT = '>HIII'

class PnapegPaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PNAPEG Paint Studio")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f0f0")
        
        self.width = 800
        self.height = 500
        self.current_color = "#000000"
        self.brush_size = 5
        self.last_x = None
        self.last_y = None
        
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)
        
        self.setup_ui()

    def setup_ui(self):
        toolbar = tk.Frame(self.root, bg="#dcdcdc", height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        color_btn = tk.Button(toolbar, text="Choose Color", command=self.choose_color, bg="#ffffff")
        color_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        size_label = tk.Label(toolbar, text="Size:", bg="#dcdcdc")
        size_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.size_slider = tk.Scale(toolbar, from_=1, to=20, orient=tk.HORIZONTAL, command=self.update_brush_size)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side=tk.LEFT, padx=5, pady=5)
        
        clear_btn = tk.Button(toolbar, text="Clear Canvas", command=self.clear_canvas, bg="#ffcccc")
        clear_btn.pack(side=tk.LEFT, padx=20, pady=5)
        
        save_btn = tk.Button(toolbar, text="💾 Save to .pnapeg", command=self.save_pnapeg, bg="#ccffcc", font=("Arial", 10, "bold"))
        save_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white", cursor="pencil")
        self.canvas.pack(side=tk.TOP, pady=20)
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_coordinates)

    def choose_color(self):
        color = colorchooser.askcolor(color=self.current_color)
        if color:
            self.current_color = color[1]

    def update_brush_size(self, val):
        self.brush_size = int(val)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, self.width, self.height], fill="white")

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, 
                                    fill=self.current_color, width=self.brush_size, 
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            
            self.draw.line([self.last_x, self.last_y, event.x, event.y], 
                           fill=self.current_color, width=self.brush_size, joint="round")
            
        self.last_x = event.x
        self.last_y = event.y

    def reset_coordinates(self, event):
        self.last_x = None
        self.last_y = None

    def save_pnapeg(self):
        filename = "canvas_artwork.pnapeg"
        raw_pixels = self.image.tobytes()
        version = 1
        
        try:
            with open(filename, 'wb') as f:
                f.write(MAGIC_NUMBER)
                header = struct.pack(HEADER_FORMAT, version, self.width, self.height, len(raw_pixels))
                f.write(header)
                f.write(raw_pixels)
                
            messagebox.showinfo("Success", f"Artwork saved successfully as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{str(e)}")

if __name__ == "__main__":
    window = tk.Tk()
    app = PnapegPaintApp(window)
    window.mainloop()
