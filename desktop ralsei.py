from tkinter import *
import time
from random import randint
from tkinter.font import Font
from object import Textbox, Pet

root = Tk()
# root.geometry("1355x200+0+495")

root.configure(background='green')
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
								   root.winfo_screenheight()))
root.wm_attributes('-transparentcolor', 'green')
root.call('wm', 'attributes', '.', '-topmost', '1')

durations = {
	"idle": 2,
	"dragging": 4,
	"falling": 4,
	"fallingend": 3,
	"walkingright": 4,
	"walkingleft": 4,
	"summon": 3,
	"dance": 10
}

def frame_extract(file, animation):
	return [PhotoImage(file=file, format='gif -index %i' % (i)) for i in range(durations[animation])]

img = PhotoImage(file='face.png')
imgidle = PhotoImage(file='walking.gif')

sprites = {
	"idle": imgidle,
	"walkingright": frame_extract("walking.gif", "walkingright"),
	"walkingleft": frame_extract("walking2.gif", "walkingleft"),
	"dragging": frame_extract("falling2.gif", "dragging"),
	"falling": frame_extract("falling.gif", "falling"),
	"fallingend": frame_extract("falling2.gif", "fallingend"),
	"summon": frame_extract("fallingstart.gif", "summon"),
	"dance": frame_extract("dance.gif", "dance"),
}

image = Label(root, bd=0, highlightthickness=0, bg='green')
pet = Pet(image, root, sprites=(sprites,durations))

box = PhotoImage(file='box.png')
face = PhotoImage(file='Ralsei face.png')
script = open("script.txt").read().split("\n")

canvas = Canvas(width=422, height=119, highlightthickness=0, background='green')
textbox = Textbox(
	canvas,
	root,
	box,
	"hello",
	face,
	script)

pet.textbox = textbox

root.mainloop()
