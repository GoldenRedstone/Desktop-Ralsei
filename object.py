from tkinter import *
from tkinter.font import Font
from random import randint

fps = 20
h = 610
idle = ["idle", "dance"]

class Object:
	def __init__(self, obj, root, x=0, y=0, delay=10):
		self.obj = obj
		self.obj.pack(padx=50, pady=50)

		self.root = root

		self.x = x
		self.y = y
		self.height = self.obj.winfo_height()
		self.width = self.obj.winfo_width()

		self.delay = delay

		self.dragging = False
		self.make_draggable()
		self.root.after(self.delay, self.update)

	def make_draggable(self):
		self.obj.bind("<Button-1>", self.on_drag_start)
		self.obj.bind("<B1-Motion>", self.on_drag_motion)
		self.obj.bind("<B1-ButtonRelease>", self.on_drag_end)

	def on_drag_start(self, event):
		self._drag_start_x = event.x
		self._drag_start_y = event.y
		self.drag_start = (self.x, self.y)
		self.drag_distance = 0

	def on_drag_end(self, event):
		if self.drag_distance > 10:
			print("dragged")
		else:
			print("clicked")
			self.x, self.y = self.drag_start
			self.obj.place(x=self.x, y=self.y)
			self.on_click()
		self.dragging = False

	def on_drag_motion(self, event):
		self.x = self.x - self._drag_start_x + event.x
		self.y = self.y - self._drag_start_y + event.y
		mx = (self.drag_start[0] - self.x)**2
		my = (self.drag_start[1] - self.y)**2
		self.drag_distance = (mx+my)**0.5
		self.obj.place(x=self.x, y=self.y)
		if self.drag_distance > 10:
			self.dragging = True
		else:
			self.dragging = False

	def update(self):
		self.obj.place(x=self.x, y=self.y)
		self.root.after(self.delay, self.update)

	def on_click(self):
		pass


class Textbox(Object):
	def __init__(self, obj, root, bgimage, text, face, script=None, font=None):
		super().__init__(obj, root, -500, -500, delay=3000)

		self.face = face
		self.bgimage = bgimage
		self.font = Font(family='Fixedsys', size=17)

		self.line = 0

		self.width = 422
		self.height = 119

		self.script = script

		self.shown = False

	def setText(self, text):
		self.obj.itemconfig(self.text, text=text)

	def update(self):
		# self.setText(script[self.line])
		# self.line = (self.line + 1) % 5
		# super().update()
		pass

	def on_click(self):
		self.hide()

	def show(self, text=None, face=None, bgimage=None):

		self.face = face or self.face
		self.bgimage = bgimage or self.bgimage

		if not self.shown:
			self.x = 500
			self.y = 100
			self.obj.place(x=self.x, y=self.y)

		self.bg = self.obj.create_image(0, 0, image=self.bgimage, anchor=NW)
		self.faceimage = self.obj.create_image(25, 23, image=self.face, anchor=NW)
		self.text = self.obj.create_text(100,25, text=text, anchor=NW, fill="white", font=self.font)

		self.shown = True

	def hide(self):
		self.obj.delete(self.bg, self.faceimage, self.text)
		self.x = -500
		self.y = -500
		self.obj.place(x=self.x, y=self.y)

		self.shown = False


class Pet(Object):
	def __init__(self, obj, root, sprites, textbox=None):
		super().__init__(obj, root, 100, -100, delay=10)

		self.xcount = 0
		self.yvel = 0
		# self.dragging = False
		self.grounded = False

		self.idletype = 0
		self.state = "falling"
		self.frame = 0

		self.textbox = textbox

		self.sprites = sprites[0]
		self.durations = sprites[1]

		self.height = 10
		self.width = 10

		self.screenheight = self.root.winfo_screenheight()

	def on_drag_start(self, event):
		# self.dragging = True
		self.grounded = False
		self.yvel = 0
		self.xcount = 0
		super().on_drag_start(event)

	def on_drag_end(self, event):
		# self.dragging = False
		super().on_drag_end(event)

	def update(self):
		if not self.dragging:
			self.y += self.yvel
			if self.xcount != 0:
				self.idletype = 0
			if self.xcount > 0:
				self.x += 0.5
				self.xcount -= 1
			elif self.xcount < 0:
				self.x -= 0.5
				self.xcount += 1

			elif self.xcount == 0:
				if randint(1, 200) == 1:
					self.xcount = randint(-200, 200)
				elif randint(1, 200) == 2:
					self.idletype = randint(0, 1)

			if self.x < 0:
				self.x = 0
				self.xcount = 100
			elif self.x > 1330:
				self.x = 1330
				self.xcount = -100

			self.grounded = False
			# print(self.y, self.textbox.y, self.textbox.height)
			xmatch = self.textbox.x < self.x+38 < self.textbox.x+self.textbox.width
			ymatch = self.textbox.y-self.textbox.height-10 < self.y-self.height < self.textbox.y-(self.textbox.height/2)
			if xmatch and ymatch and (self.textbox is not None):
				self.y = self.textbox.y-self.textbox.height+self.height
				self.grounded = True
				self.bounce()
			elif self.y > h - 1:
				self.y = h
				self.grounded = True
				self.bounce()

			if not self.grounded:
				self.yvel += 0.2

			self.obj.place(x=self.x, y=self.y)

		self.selectState()
		self.selectImage()

		super().update()

	def bounce(self):
		if self.yvel >= 5:
			self.yvel = self.yvel * -0.5
		elif self.yvel < 5:
			self.yvel = 0

	def selectState(self):
		# self.desired = self.state
		if self.dragging:
			self.state = "dragging"
		elif not self.grounded:
			if self.y < h*0.7:
				self.state = "falling"
			else:
				self.state = "fallingend"
		elif self.xcount > 0 and self.yvel == 0:
			self.state = "walkingright"
		elif self.xcount < 0 and self.yvel == 0:
			self.state = "walkingleft"

		elif self.yvel == 0:
			self.state = idle[self.idletype]

		self.frame += 1
		if self.frame >= self.durations[self.state]*fps:
			# self.state = self.desired
			self.frame = 0

	def selectImage(self):
		if self.state in self.sprites:
			if type(self.sprites[self.state]) is list:
				self.obj.configure(
					image=self.sprites[self.state][self.frame//fps])
			else:
				self.obj.configure(image=self.sprites[self.state])
		else:
			self.obj.configure(image=img)

	def on_click(self):
		if self.textbox.script is None:
			self.textbox.show(str(randint(1,100)))
		else:
			self.textbox.show(self.textbox.script[self.textbox.line])
			self.textbox.line = (self.textbox.line + 1)%len(self.textbox.script)

