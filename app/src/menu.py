import pygame
import os

pygame.init()

class Menu():
	WIN_WIDTH, WIN_HEIGHT = 1920 / 2, 1080 / 2
	WIN = None
	
	BG_IMAGE = pygame.image.load(os.path.join("res", "bg_low.png")) #.convert()
	BG_IMAGE_FIT = pygame.transform.scale(BG_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
	HEADING = pygame.image.load(os.path.join("res", "nasalia_text.png")) #.convert()
	HEADING_FIT = pygame.transform.scale(HEADING, (33 * 8, 5 * 8))
	play_frog = False
	play_diver = False
	main_menu = True

	def __init__(self, win):
		self.WIN = win
		self.quit = False
		self.settings = False
		self.main_menu_disable = False

	def display(self):
		self.WIN.blit(self.BG_IMAGE_FIT, (0, 0))
		self.WIN.blit(self.HEADING_FIT, (self.WIN_WIDTH / 2 - 33/2*8, 100))

	def execute(self):
		self.display()

	def set_play_frog(self):
		self.play_frog = True
		self.main_menu = False

	def set_play_diver(self):
		self.play_diver = True
		self.main_menu = False

	def set_display_settings(self):
		self.settings = True
		self.main_menu = True
		self.main_menu_disable = True
		self.play_frog = False

	def close_settings(self):
		self.settings = False
		self.main_menu = True
		self.main_menu_disable = False
		self.play_frog = False

	def goto_menu(self):
		self.main_menu = True
		self.play_frog = False