import tkinter as tk
import numpy as np
from predictor import Predictor
from PIL import ImageGrab
import os
import cv2

BASE_DIR = os.path.dirname(__file__)
IMAGE_FOLDER = os.path.join(BASE_DIR, 'temp')


class MainWindow(tk.Frame):
    def __init__(self, master):
        super(MainWindow, self).__init__(master)
        self.pack()
        self.master.title("Character Recognizer")
        self.aspect_ratio = self.calculate_aspect_ratio()
        self.drawing_canvas = tk.Canvas(self, width=320,
                                        height=180, bg='black')
        self.drawing_canvas.pack()
        self.drawing_canvas.bind('<B1-Motion>', self.move)
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(side='bottom', padx=15, pady=15)
        self.button = tk.Button(self.bottom_frame, text="Process")
        self.button.pack(side='left', padx=15, pady=15)
        self.button.bind('<Button-1>', self.make_prediction)
        self.clear_button = tk.Button(self.bottom_frame, text="Clear")
        self.clear_button.pack(side='left', padx=15, pady=15)
        self.clear_button.bind('<Button-1>', self.clear_canvas)
        self.result = tk.Label(self.bottom_frame, text="Result")
        self.result.pack(side='left', padx=15, pady=15)
        self.prev = None
        self.image_id = 0
        self.get_predictor()

    def calculate_aspect_ratio(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        aspect_ratio = (screen_width * 1.0) / screen_height
        print("Width: {}, Height: {}, Aspect Ratio: {}".format(screen_width, screen_height, aspect_ratio))
        return aspect_ratio

    def get_predictor(self):
        self.predictor = Predictor()

    def clear_canvas(self, event):
        self.drawing_canvas.delete('all')

    def extract_digit(self, img):
        row_vals, col_vals = np.where(img == 255)
        min_row = np.min(row_vals)
        max_row = np.max(row_vals)
        min_col = np.min(col_vals)
        max_col = np.max(col_vals)
        cropped_image = img[min_row - 10: max_row + 10,
                            min_col - 20: max_col + 20]
        return cropped_image

    def make_prediction(self, event):
        self.image_id += 1
        image_path = os.path.join(IMAGE_FOLDER,
                                  'img' + str(self.image_id) + '.png')
        x = self.master.winfo_rootx() + self.drawing_canvas.winfo_x()
        y = self.master.winfo_rooty() + self.drawing_canvas.winfo_y()
        x1 = x + self.drawing_canvas.winfo_width()
        y1 = y + self.drawing_canvas.winfo_height()
        img = ImageGrab.grab().crop((x, y, x1, y1)).convert("RGB")
        image = np.array(img)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = self.extract_digit(image)
        #image = cv2.resize(image, (image.shape[1], int(image.shape[1] / self.aspect_ratio)))
        cv2.imwrite(image_path, image)
        print("Numpy array shape is: {}".format(image.shape))
        prediction = self.predictor.predict(image)
        self.result.config(text=str(prediction))

    def move(self, event):
        buffer_width = 5
        x1, y1 = event.x - buffer_width, event.y - buffer_width
        x2, y2 = event.x + buffer_width, event.y + buffer_width
        self.drawing_canvas.create_oval(x1, y1, x2, y2,
                                        outline='white', fill='white')

    def perform_cleanup(self):
        self.predictor.close_session()
        self.delete_temporary_files()

    def delete_temporary_files(self):
        for image in os.listdir(IMAGE_FOLDER):
            image_path = os.path.join(IMAGE_FOLDER, image)
            if os.path.isfile(image_path):
                os.unlink(image_path)


if __name__ == '__main__':
    main = None
    try:
        root = tk.Tk()
        main = MainWindow(root)
        root.mainloop()
    finally:
        if main:
            main.perform_cleanup()
