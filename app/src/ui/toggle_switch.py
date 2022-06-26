import pygame
import os

class Toggle_Switch:

	default_base_image_path = os.path.join(os.path.dirname(__file__), 'assets', 'toggle_base.png')
	default_base_green_image_path = os.path.join(os.path.dirname(__file__), 'assets', 'toggle_base_green.png')
	default_knob_image_path = os.path.join(os.path.dirname(__file__), 'assets', 'toggle_knob.png')
	RELEASED = 0
	CLICKED = 1

	KNOB_STILL = 0
	KNOB_SLIDING_R = 1
	KNOB_SLIDING_L = 2

	def __init__(
		self,
		x,
		y,
		WIN,
		w = 11 * 4,
		h = 6 * 4,
		base_image_path = None,
		base_green_image_path = None,
		knob_image_path = None,
		on_click_function = None,
		switch_on = False):

		self.x, self.y = x, y
		self.w, self.h = w, h
		self.WIN = WIN
		self.value = switch_on

		self.knob_x, self.knob_y = self.x, self.y
		self.knob_w = self.h

		self.last_switch_time = pygame.time.get_ticks()

		if not base_image_path:
			self.base_image_path = self.default_base_image_path
			self.base_green_image_path = self.default_base_green_image_path
			self.knob_image_path = self.default_knob_image_path
		else:
			self.base_image_path = base_image_path
			self.base_green_image_path = base_green_image_path
			self.knob_image_path = knob_image_path

		self.base_image = pygame.image.load(self.base_image_path).convert_alpha()
		self.base_image = pygame.transform.scale(self.base_image, (self.w, self.h))
		self.base_green_image = pygame.image.load(self.base_green_image_path).convert_alpha()
		self.base_green_image = pygame.transform.scale(self.base_green_image, (self.w, self.h))
		self.knob_image = pygame.image.load(self.knob_image_path).convert_alpha()
		self.knob_image = pygame.transform.scale(self.knob_image, (self.w * 6 / 11, self.h))

		self.current_base_image = self.base_image
		self.state = self.RELEASED
		self.knob_state = self.KNOB_STILL

		if self.value is True:
			self.current_base_image = self.base_green_image
			self.knob_x = self.x + self.w - self.knob_w

	def draw(self):
		self.WIN.blit(self.current_base_image, (self.x, self.y))
		self.WIN.blit(self.knob_image, (self.knob_x, self.knob_y))

	def update(self):
		self.check_pressed()
		self.draw()

	def check_pressed(self):
		#current_time = pygame.time.get_ticks()
		#if current_time - self.last_switch_time > 400:
		mouse_buttons = pygame.mouse.get_pressed()

		if mouse_buttons[0] is not True and self.state is self.CLICKED:
			self.switch()
			self.state = self.RELEASED

		x, y = pygame.mouse.get_pos()
		if (x >= self.x) and (x <= self.x + self.w) and (y >= self.y) and (y <= self.y + self.h):
			if mouse_buttons[0]:
				self.state = self.CLICKED
		else:
			self.state = self.RELEASED
			

	def switch(self):
		if self.value is True:
			self.value = False
			self.knob_x = self.x
			self.current_base_image = self.base_image
		else:
			self.value = True
			self.knob_x = self.x + self.w - self.knob_w
			self.current_base_image = self.base_green_image