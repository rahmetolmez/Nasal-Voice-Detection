import pygame
from ui import text, button
from common import *
from item import *
from diver import *
from treasure import *

class Diver_Main:
	def __init__(
		self,
		WIN = common.WIN,
		menu = None):

		#self.last_color_change_time = pygame.time.get_ticks()
		#self.index = 0
		self.WIN = WIN
		self.menu = menu
		self.BG_IMAGE = pygame.image.load(os.path.join('res', 'diver_bg.png')).convert()
		self.BG_IMAGE_FIT = pygame.transform.scale(self.BG_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
		self.BG_IMAGE_BLUR = pygame.image.load(os.path.join('res', 'bg_low_blurred_tint.png')).convert()
		self.BG_IMAGE_BLUR = pygame.transform.scale(self.BG_IMAGE_BLUR, (WIN_WIDTH, WIN_HEIGHT))
		self.last_color_change_time = pygame.time.get_ticks()
		self.index = 0

		self.diver = Diver(WIN_WIDTH / 2 + 23 * BLOCK_SIZE, 1 * BLOCK_SIZE, 26 * BLOCK_SIZE, 29 * BLOCK_SIZE, 'diver.png')
		self.treasure = Treasure(55 * BLOCK_SIZE, 110 * BLOCK_SIZE - 29 * BLOCK_SIZE, 26 * 1.4 * BLOCK_SIZE, 29 * 1.4 * BLOCK_SIZE, 'treasure_chest.png')
		self.treasure_won = Treasure(WIN_WIDTH / 2 - 52 * BLOCK_SIZE, WIN_HEIGHT / 2 - 20 * BLOCK_SIZE, 26 * 4 * BLOCK_SIZE, 29 * 4 * BLOCK_SIZE, 'treasure_chest.png')
		self.game_won = False

		self.text_nasal = text.Text(
			x = WIN_WIDTH - 60 * BLOCK_SIZE,
			y = WIN_HEIGHT - 80 * BLOCK_SIZE,
			WIN = self.WIN,
			text = 'Speech: NASAL',
			font_path = os.path.join('res', 'liko.ttf'),
			font_size = 8 * BLOCK_SIZE,
			text_color = WHITE,
			text_bg_color = RED,
			center_align = True)

		self.text_normal = text.Text(
			x = WIN_WIDTH - 60 * BLOCK_SIZE,
			y = WIN_HEIGHT - 80 * BLOCK_SIZE,
			WIN = self.WIN,
			text = 'Speech: NORMAL',
			font_path = os.path.join('res', 'liko.ttf'),
			font_size = 8 * BLOCK_SIZE,
			text_color = WHITE,
			text_bg_color = GREEN,
			center_align = True)

		self.text_you_win = text.Text(
				x = WIN_WIDTH / 2,
				y = WIN_HEIGHT / 4,
				WIN = self.WIN,
				text = 'YOU WIN!',
				font_path = os.path.join('res', 'liko.ttf'),
				font_size = 32 * BLOCK_SIZE,
				text_color = WHITE,
				text_bg_color = None,
				center_align = True)

		self.text_guide = text.Text(
				x = WIN_WIDTH / 2,
				y = WIN_HEIGHT - 10 * BLOCK_SIZE,
				WIN = self.WIN,
				text = 'Press spacebar while speaking',
				font_path = os.path.join('res', 'liko.ttf'),
				font_size = 8 * BLOCK_SIZE,
				text_color = BLACK,
				text_bg_color = None,
				center_align = True)

		self.button_restart = button.Button(
			x = self.text_normal.x + 14 * 3 * BLOCK_SIZE / 2,
			y = WIN_HEIGHT / 1.5 - 14 * BLOCK_SIZE,
			w = 16 * BLOCK_SIZE * 3,
			h = 8 * BLOCK_SIZE * 3,
			WIN = WIN,
			on_image = os.path.join('res', 'button1.png'),
			off_image = os.path.join('res', 'button1_pressed.png'),
			on_click_function = self.diver_game_reset,
			text = 'Replay',
			font_path = os.path.join('res', 'liko.ttf'),
			font_size = 6 * BLOCK_SIZE,
			text_color = (0, 0, 0))

		self.button_menu = button.Button(
			x = self.text_normal.x + 14 * 3 * BLOCK_SIZE / 2,
			y = self.button_restart.y + self.button_restart.h + BLOCK_SIZE,
			w = 16 * BLOCK_SIZE * 3,
			h = 8 * BLOCK_SIZE * 3,
			WIN = WIN,
			on_image = os.path.join('res', 'button1.png'),
			off_image = os.path.join('res', 'button1_pressed.png'),
			on_click_function = self.diver_game_back_to_menu,
			text = 'Menu',
			font_path = os.path.join('res', 'liko.ttf'),
			font_size = 6 * BLOCK_SIZE,
			text_color = (0, 0, 0))

	def draw(self):
		if not self.game_won:
			self.WIN.blit(self.BG_IMAGE_FIT, (0, 0))
			self.treasure.draw()
			self.diver.draw()
			self.button_menu.draw()
			self.button_menu.button_pressed()

			if ctrl.a_key:
				self.text_nasal.draw()
			else:
				self.text_normal.draw()

			if ctrl.talk_with_space:
				if not ctrl.space:
					self.text_guide.draw()
		
		if self.treasure.check_reached(self.diver):
			self.you_win()

	def you_win(self):
		self.game_won = True
		current_time = pygame.time.get_ticks()

		if current_time - self.last_color_change_time > 300:
			self.text_you_win.set_color(RAINBOW[self.index], None)
			self.index += 1
			self.index = self.index % len(RAINBOW)
			self.last_color_change_time = current_time
		
		self.button_restart.set_pos(WIN_WIDTH / 2 - 24 * BLOCK_SIZE, WIN_HEIGHT / 1.5 - 18 * BLOCK_SIZE)
		self.button_menu.set_pos(WIN_WIDTH / 2 - 24 * BLOCK_SIZE, self.button_restart.y + self.button_restart.h + BLOCK_SIZE)
		self.WIN.blit(self.BG_IMAGE_BLUR, (0, 0))
		self.treasure_won.draw()
		self.text_you_win.draw()
		self.button_restart.draw()
		self.button_restart.button_pressed()
		self.button_menu.draw()
		self.button_menu.button_pressed()

	def diver_game_reset(self):
		self.game_won = False
		self.diver.reset()
		self.treasure.reset()

		self.button_restart.set_pos(self.text_normal.x + 14 * 3 * BLOCK_SIZE / 2, WIN_HEIGHT / 1.5 - 14 * BLOCK_SIZE)
		self.button_menu.set_pos(self.text_normal.x + 14 * 3 * BLOCK_SIZE / 2, self.button_restart.y + self.button_restart.h + BLOCK_SIZE)

	def diver_game_back_to_menu(self):
		self.menu.main_menu = True
		self.menu.play_diver = False
		self.diver_game_reset()

	#def frog_main(self):