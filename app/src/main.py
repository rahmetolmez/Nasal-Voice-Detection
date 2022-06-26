### Speech Therapy Games
### Author: Rahmet Ali Olmez
### November - December 2021

# TODO game initialization takes too long -> loading screen
# TODO model not good on other people
# TODO reduce prediction duration to 0.2s
# DONE stop tongue if no sound below threshold -> noise calibration?
# TODO reset button
# TODO diving game
# TODO hypo and hypernasal

from common import *
from threading import Thread
from cnn_model import *
from item import *
from frog import *
from diver import *
from treasure import *
from fly import *
from ui import button, text, dialog_box, toggle_switch
from crt import *
from frog_main import *
from diver_main import *
import sys

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

pygame.init()
pygame.display.set_caption("Nasalia")
WIN = common.WIN
menu = Menu(common.WIN)

THREAD_QUIT = False

MENU_BG_IMAGE = pygame.image.load(os.path.join('res', 'bg_low_blurred_tint.png')).convert()
MENU_BG_IMAGE_FIT = pygame.transform.scale(MENU_BG_IMAGE, (WIN_WIDTH, WIN_HEIGHT))

def loading_screen():
	text_loading = text.Text(
		x = WIN_WIDTH / 2,
		y = WIN_HEIGHT / 2,
		WIN = common.WIN,
		text = 'Loading...',
		font_path = os.path.join('res', 'liko.ttf'),
		font_size = 15 * BLOCK_SIZE,
		text_color = WHITE,
		text_bg_color = None,
		center_align = True)

	common.WIN.blit(MENU_BG_IMAGE_FIT, (0, 0))
	text_loading.draw()
	pygame.display.update()

loading_screen()


#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
#from tensorflow import keras
from keras.models import load_model

model = load_model(os.path.join('model', 'cnn_model.h5'))

settings_dialog = dialog_box.Dialog_Box(
	x = WIN_WIDTH / 2 - 39 * BLOCK_SIZE,
	y = WIN_HEIGHT / 2 - 39 * BLOCK_SIZE,
	w = 78 * BLOCK_SIZE,
	h = 78 * BLOCK_SIZE,
	WIN = WIN,
	button_count = 1,
	bg_image_path = os.path.join('res', 'dialog_box.png'),
	font_path = os.path.join('res', 'liko.ttf'),
	title_text = 'Settings',
	title_center_align = True,
	title_font_size = 32,
	message_text = 'This is a dialog box.',
	message_font_size = 20,
	title_color = (0, 0, 0),
	message_color = (255, 255, 255))

def goto_menu():
	menu.main_menu = True
	menu.play_frog = False

def exit_app():
	menu.quit = True
	#ctrl.exit_program = True

def main():
	frog = Frog(WIN_WIDTH / 2 - 13 * BLOCK_SIZE, 8 * BLOCK_SIZE, 26 * BLOCK_SIZE, 29 * BLOCK_SIZE, 'frog.png', disable_tongue = True)
	frog_game = Frog_Main(WIN = common.WIN, menu = menu)
	diver_game = Diver_Main(WIN = common.WIN, menu = menu)
	crt = CRT(common.WIN, WIN_WIDTH, WIN_HEIGHT)
	clock = pygame.time.Clock()
	quit = False
	reset = False
	crt_on = False
	fps_on = False

	diver = Diver(WIN_WIDTH, 0, 32 * BLOCK_SIZE, 32 * BLOCK_SIZE, 'diver.png')
	treasure = Treasure(WIN_WIDTH / 2, 300, 47 * BLOCK_SIZE, 51 * BLOCK_SIZE, 'treasure_chest.png')

	#test_accuracy(model, 'em_nasal.wav', 1)

	detector_thread = Thread(target = detect_nasality, args = [model])
	detector_thread.daemon = True
	detector_thread.start()
	#print(model.summary())
	text_fps = text.Text(
		x = BLOCK_SIZE,
		y = BLOCK_SIZE,
		WIN = common.WIN,
		text = 'FPS: ',
		font_path = os.path.join('res', 'liko.ttf'),
		font_size = 6 * BLOCK_SIZE,
		text_color = WHITE,
		text_bg_color = None,
		center_align = False)

	text_title = text.Text(
		x = WIN_WIDTH / 2,
		y = 8 * BLOCK_SIZE + 29 * BLOCK_SIZE,
		WIN = common.WIN,
		text = 'NASALIA',
		font_path = os.path.join('res', 'liko.ttf'),
		font_size = 15 * BLOCK_SIZE,
		text_color = WHITE,
		text_bg_color = None,
		center_align = True)

	button_start = button.Button(
		x = WIN_WIDTH / 2 - 24 * BLOCK_SIZE,
		y = WIN_HEIGHT / 2 - BLOCK_SIZE * 13,
		w = 16 * BLOCK_SIZE * 3,
		h = 8 * BLOCK_SIZE * 3,
		WIN = common.WIN,
		on_image = os.path.join('res', 'button1.png'),
		off_image = os.path.join('res', 'button1_pressed.png'),
		on_click_function = menu.set_play_frog,
		text = 'Frog',
		font_path = os.path.join('res', 'liko.ttf'),
		font_size = 6 * BLOCK_SIZE,
		text_color = (0, 0, 0))


	button_play_diver = button.Button(
		x = WIN_WIDTH / 2 - 24 * BLOCK_SIZE,
		y = button_start.y + button_start.h + 2 * BLOCK_SIZE,
		w = 16 * BLOCK_SIZE * 3,
		h = 8 * BLOCK_SIZE * 3,
		WIN = common.WIN,
		on_image = os.path.join('res', 'button1.png'),
		off_image = os.path.join('res', 'button1_pressed.png'),
		on_click_function = menu.set_play_diver,
		text = 'Diver',
		font_path = os.path.join('res', 'liko.ttf'),
		font_size = 6 * BLOCK_SIZE,
		text_color = (0, 0, 0))

	button_settings = button.Button(
		x = WIN_WIDTH / 2 - 24 * BLOCK_SIZE,
		y = button_play_diver.y + button_play_diver.h + 2 * BLOCK_SIZE,
		w = 16 * BLOCK_SIZE * 3,
		h = 8 * BLOCK_SIZE * 3,
		WIN = common.WIN,
		on_image = os.path.join('res', 'button1.png'),
		off_image = os.path.join('res', 'button1_pressed.png'),
		on_click_function = menu.set_display_settings,
		text = 'Settings',
		font_path = os.path.join('res', 'liko.ttf'),
		font_size = 6 * BLOCK_SIZE,
		text_color = (0, 0, 0))

	button_exit = button.Button(
		x = WIN_WIDTH / 2 - 24 * BLOCK_SIZE,
		y = button_settings.y + button_settings.h + 2 * BLOCK_SIZE,
		w = 16 * BLOCK_SIZE * 3,
		h = 8 * BLOCK_SIZE * 3,
		WIN = common.WIN,
		on_image = os.path.join('res', 'button1.png'),
		off_image = os.path.join('res', 'button1_pressed.png'),
		on_click_function = exit_app,
		text = 'Exit',
		font_path = os.path.join('res', 'liko.ttf'),
		font_size = 6 * BLOCK_SIZE,
		text_color = (0, 0, 0))

	text_toggle_fps = text.Text(
		x = settings_dialog.x + 4 * BLOCK_SIZE,
		y = settings_dialog.y + 20 * BLOCK_SIZE,
		WIN = common.WIN,
		text = 'Show FPS',
		font_path = os.path.join('res', 'liko.ttf'),
		font_size = 5 * BLOCK_SIZE,
		text_color = WHITE,
		text_bg_color = None,
		center_align = False)

	toggle_fps = toggle_switch.Toggle_Switch(
		x = settings_dialog.x + settings_dialog.w - 15 * BLOCK_SIZE,
		y = text_toggle_fps.y,
		WIN = common.WIN,
		w = 11 * BLOCK_SIZE,
		h = 6 * BLOCK_SIZE)

	text_toggle_crt = text.Text(
		x = settings_dialog.x + 4 * BLOCK_SIZE,
		y = toggle_fps.y + 8 * BLOCK_SIZE,
		WIN = common.WIN,
		text = 'Retro Effects',
		font_path = os.path.join('res', 'liko.ttf'),
		font_size = 5 * BLOCK_SIZE,
		text_color = WHITE,
		text_bg_color = None,
		center_align = False)

	toggle_crt = toggle_switch.Toggle_Switch(
		x = settings_dialog.x + settings_dialog.w - 15 * BLOCK_SIZE,
		y = toggle_fps.y + 8 * BLOCK_SIZE,
		WIN = common.WIN,
		w = 11 * BLOCK_SIZE,
		h = 6 * BLOCK_SIZE)

	text_toggle_talk_with_spacebar = text.Text(
		x = settings_dialog.x + 4 * BLOCK_SIZE,
		y = toggle_crt.y + 8 * BLOCK_SIZE,
		WIN = common.WIN,
		text = 'Talk w/ spacebar',
		font_path = os.path.join('res', 'liko.ttf'),
		font_size = 5 * BLOCK_SIZE,
		text_color = WHITE,
		text_bg_color = None,
		center_align = False)

	toggle_talk_with_spacebar = toggle_switch.Toggle_Switch(
		x = settings_dialog.x + settings_dialog.w - 15 * BLOCK_SIZE,
		y = toggle_crt.y + 8 * BLOCK_SIZE,
		WIN = common.WIN,
		w = 11 * BLOCK_SIZE,
		h = 6 * BLOCK_SIZE,
		switch_on = ctrl.talk_with_space)

	while not menu.quit:
		#print(FPS)
		clock.tick(FPS)
		
		#print(clock.get_fps())
		#pygame.time.delay(4)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				menu.quit = True
				#ctrl.exit_program = True
				ctrl.THREAD_QUIT = True
			#if event.type == pygame.VIDEORESIZE:
				#common.WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					menu.quit = True
					ctrl.THREAD_QUIT = True
				if event.key == pygame.K_RETURN:
					menu.play_frog = True
					menu.main_menu = False
				if event.key == pygame.K_SPACE:
					ctrl.space = True
				#if event.key == pygame.K_m:
				#	menu.main_menu = True
				#	menu.play_frog = False
				if event.key == pygame.K_RIGHT:
					ctrl.right_key = True
				if event.key == pygame.K_LEFT:
					ctrl.left_key = True
				if event.key == pygame.K_d:
					ctrl.d_key = True
				if event.key == pygame.K_a:
					ctrl.a_key = True
				#if event.key == pygame.K_r:
				#	ctrl.r_key = True
				if event.key == pygame.K_c:
					ctrl.c_key = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					ctrl.right_key = False
				if event.key == pygame.K_LEFT:
					ctrl.left_key = False
				if event.key == pygame.K_SPACE:
					ctrl.space = False
				if event.key == pygame.K_d:
					ctrl.d_key = False
				if event.key == pygame.K_a:
					ctrl.a_key = False
				#if event.key == pygame.K_r:
					#if ctrl.r_key == True:
					#	reset = True
					#ctrl.r_key = False
				if event.key == pygame.K_c:
					if ctrl.c_key == True:
						if crt_on:
							crt_on = False
						else:
							crt_on = True
					ctrl.c_key = False

		common.WIN.fill((0, 0, 0))
		if reset:
			frog_game_reset()
			reset = False		
		if menu.main_menu == True:
			common.WIN.blit(MENU_BG_IMAGE_FIT, (0, 0))
			frog.draw()
			#diver.draw()
			#treasure.draw()
			text_title.draw()
			button_start.draw()
			button_play_diver.draw()
			button_settings.draw()
			#button_exit.draw()
			if not menu.main_menu_disable:
				button_start.button_pressed()
				button_play_diver.button_pressed()
				button_settings.button_pressed()
				#button_exit.button_pressed()
		if menu.settings == True:
			settings_dialog.draw()
			text_toggle_fps.draw()
			text_toggle_crt.draw()
			text_toggle_talk_with_spacebar.draw()
			toggle_fps.update()
			toggle_crt.update()
			toggle_talk_with_spacebar.update()
			if settings_dialog.check_dialog_collision() is settings_dialog.CLOSE:
				menu.close_settings()
		if menu.play_frog == True:			
			frog_game.draw()
		elif menu.play_diver == True:
			diver_game.draw()

		ctrl.talk_with_space = toggle_talk_with_spacebar.value
		crt_on = toggle_crt.value
		if crt_on:
			crt.draw()

		fps_on = toggle_fps.value
		if fps_on:
			text_fps.set_text('FPS: ' + str(int(clock.get_fps())))
			text_fps.draw()
		pygame.display.update()
	ctrl.THREAD_QUIT = True
	detector_thread.join()
	pygame.display.quit()
	pygame.quit()
	sys.exit(0)

if __name__ == "__main__":
	main()