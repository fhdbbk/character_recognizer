from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line, Color, Rectangle
from predictor import Predictor
from functools import partial
import os
import random

IMAGE_FOLDER = 'temp'

class DrawInput(Widget):
	def __init__(self, **kwargs):
		super(DrawInput, self).__init__(**kwargs)
		self.image_id = 1
		self.predictor = Predictor()
		with self.canvas.before:
			Color(1, 1, 1, mode='rgb')
			Rectangle(pos=self.pos, size=self.pos)
		with self.canvas:
			Color(0, 1, 0, mode='rgb')

	def on_touch_down(self, touch):
		with self.canvas:
			touch.ud["line"] = Line(points=(touch.x, touch.y), width=5.0)

	def on_touch_move(self, touch):
		touch.ud["line"].points += (touch.x, touch.y)

	def save_image(self, *args):
		print("Button pressed")
		self.image_id += 1
		image_path = os.path.join(IMAGE_FOLDER, 'img' + str(self.image_id) + '.png')
		self.export_to_png(image_path)
		result = self.predictor.predict(image_path)
		print("Final result: {}".format(result))
		print(type(args[0]))
		args[0].text = result
		#text_box.text = result



class ScatterTextWidget(BoxLayout):
	pass


class TextReader(App):
	# def __init__(self, **kwargs):
	# 	super(TextReader, self).__init__(**kwargs)
	# 	self.predictor = Predictor()
		 
	def build(self):
		main_widget = ScatterTextWidget(orientation='vertical')
		painter = DrawInput()
		bottom_part = BoxLayout(orientation='horizontal')
		b = Button(id='processor', font_size=100, size_hint_y=None,
				   height=150, text='Process')#, on_press=painter.save_image)
		text_box = TextInput(id='result', font_size=100,
							 size_hint_y=None, height=150)

		#b.bind(on_press=painter.save_image)
		bottom_part.add_widget(b)
		bottom_part.add_widget(text_box)
		main_widget.add_widget(painter)
		main_widget.add_widget(bottom_part)
		button_callback = partial(painter.save_image, text_box)
		b.bind(on_press=button_callback)
		return main_widget
 		

if __name__ == '__main__':
	obj = TextReader()
	obj.run()