import pygame
import colors
import tkinter as tk
import sys
from pathlib import Path
import os
import winsound


class Grid:
	selected_color = colors.earth_green

	def __init__(self, cell_size):
		self.cell_size = cell_size
		self.cell_size_temp = cell_size
		self.rows = SCREENHEIGHT // self.cell_size
		self.cols = SCREENWIDTH // self.cell_size
		self.cell_data = {}
		self.cell_data_temp = {}
		self.background = colors.white
		self.background_temp = colors.white

	def reset_grid_size(self, cell_size):
		self.cell_size = cell_size
		self.rows = SCREENHEIGHT // self.cell_size
		self.cols = SCREENWIDTH // self.cell_size
		self.cell_data = {}

	def draw(self, surface, color):
		# drawing columns
		for col in range(0, self.cols + 1):
			pygame.draw.line(surface, color, (0 + self.cell_size * col, 0), (0 + self.cell_size * col, SCREENHEIGHT))

		# drawing rows
		for row in range(0, self.rows):
			pygame.draw.line(surface, color, (0, 0 + self.cell_size * row), (SCREENWIDTH, 0 + self.cell_size * row))

	def _fill(self, surface, row, col, color):
		surface.fill(color, (0 + self.cell_size * col, 0 + self.cell_size * row, self.cell_size + 1, self.cell_size + 1))

	def draw_cells(self, surface):
		global current_file_name
		try:
			for CELL in self.cell_data:
				self._fill(game_display, CELL[0], CELL[1], self.cell_data[CELL])
		except Exception as e:
			winsound.PlaySound("*", winsound.SND_ASYNC)
			corrupted_file_dialog(e)
			current_file_name = file_name_temp
			set_title()
			self.cell_size = self.cell_size_temp
			self.cell_data = self.cell_data_temp
			self.background = self.background_temp

	def clear_cells(self):
		self.cell_data.clear()

	def grid_events(self, surface):
		mouse_click = pygame.mouse.get_pressed()
		key_press = pygame.key.get_pressed()
		selected_col = selected_row = None
		mouse_pos = pygame.mouse.get_pos()
		if(mouse_pos[0] <= SCREENWIDTH and mouse_pos[1] < SCREENHEIGHT):
			# finding column
			for col in range(1, self.cols + 2):
				if(col * self.cell_size < mouse_pos[0]):
					continue
				else:
					selected_col = col - 1
					break

			# finding row
			for row in range(1, self.rows + 2):
				if(row * self.cell_size < mouse_pos[1]):
					continue
				else:
					selected_row = row - 1
					break

			if(mouse_click[0] == 1 or key_press[pygame.K_d]):
				self.cell_data[(selected_row, selected_col)] = Grid.selected_color
			elif(mouse_click[1] == 1 or key_press[pygame.K_f]):
				cell_color = None
				delta_row = delta_col = 0
				working_row = cell_row = selected_row
				working_col = cell_col = selected_col
				try:
					if(self.cell_data[(selected_row, selected_col)] != Grid.selected_color):
						cell_color = self.cell_data[(selected_row, selected_col)]
				except KeyError:
					cell_color = colors.white
				delta_row = -1
				delta_col = -1
				for i in range(0, 2):
					while True:
						try:
							if(self.cell_data[(working_row, working_col)] != cell_color or (working_row > grid.rows - 1 or working_row < 0)):
								delta_row *= -1
								working_row = cell_row + 1
								break
						except KeyError:
							if(colors.white != cell_color or (working_row > grid.rows - 1 or working_row < 0)):
								delta_row *= -1
								working_row = cell_row + 1
								break
						for j in range(0, 2):
							while True:
								try:
									if(self.cell_data[(working_row, working_col)] != cell_color or (working_col > grid.cols - 1 or working_col < 0)):
										delta_col *= -1
										working_col = cell_col + 1
										break
								except KeyError:
									if(colors.white != cell_color or (working_col > grid.cols - 1 or working_col < 0)):
										delta_col *= -1
										working_col = cell_col + 1
										break

								# fill
								self.cell_data[(working_row, working_col)] = Grid.selected_color

								working_col += delta_col

						working_row += delta_row
						working_col = cell_col
			elif(mouse_click[2] == 1 or key_press[pygame.K_e]):
				self.cell_data.pop((selected_row, selected_col), None)

	@classmethod
	def set_color(cls, color):
		cls.selected_color = color


class Tool:
	def __init__(self, cmds_list, alter_cmds_list, x, y, width, height, color=colors.white, caption="", border=0, caption_size=None):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.cmds_list = cmds_list
		self.alter_cmds_list = alter_cmds_list
		self.color = color
		self.caption = caption
		self.border = border
		if(self.caption != ""):
			if(caption_size is None):
				text_surface_temp = BASIC_FONT.render(self.caption, True, colors.black)
				self.caption_size = (text_surface_temp.get_width(), text_surface_temp.get_height())
			else:
				self.caption_size = caption_size
			self.text_surface = pygame.transform.scale(BASIC_FONT.render(self.caption, True, colors.black), self.caption_size)
		else:
			self.text_surface = None

	def execute(self):
		for CMD in self.cmds_list:
			eval(CMD)

	def alter_execute(self):
		for CMD in self.alter_cmds_list:
			eval(CMD)

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), self.border)
		if(self.text_surface is not None):
			surface.blit(self.text_surface, (self.x + self.width // 2 - self.text_surface.get_width() // 2, self.y + self.height // 2 - self.text_surface.get_height() // 2))

	def tool_events(self):
		mouse_click = pygame.mouse.get_pressed()
		if(mouse_click[0] == 1):
			mouse_pos = pygame.mouse.get_pos()
			if(mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width and mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height):
				self.execute()
		elif(mouse_click[2] == 1):
			mouse_pos = pygame.mouse.get_pos()
			if(mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width and mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height):
				self.alter_execute()


def QUIT():
	pygame.quit()
	sys.exit()


def get_screen_size(tk_root):
	width = tk_root.winfo_screenwidth()
	height = tk_root.winfo_screenheight()
	return width, height


def corrupted_file_dialog(e):
	root = tk.Tk()
	root.resizable(False, False)
	root.title("Corrupted File Detected!")
	screen_size = get_screen_size(root)
	root.geometry(f"600x100+{screen_size[0] // 2 - 300}+{screen_size[1] // 2 - 50}")

	label_corrupted_info = tk.Label(root, text="Sorry, the file you're looking for seems bad/corrupted in some way!")
	label_corrupted_info.pack()

	label_corrupted_exception = tk.Label(root, text="EXCEPTION : " + str(e), fg="red")
	label_corrupted_exception.pack()

	button_ok = tk.Button(root, text="OK", command=root.destroy)
	button_ok.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


def update_color_text(text_surface):
	global color_text
	color_text = text_surface


def load():
	def load_project():
		global current_file_name, file_name_temp
		cvp_path = os.path.join(entry_file_path.get(), entry_file_name.get() + ".cvp")
		try:
			with open(os.path.join(cvp_path), 'r') as f:
				grid.cell_data_temp = grid.cell_data
				grid.cell_size_temp = grid.cell_size
				grid.background_temp = grid.background
				file_name_temp = current_file_name
				try:
					load_data = eval(f.read())            # (10, {}, (255, 255, 255))
					grid_size = load_data[0]
					cell_data = load_data[1]
					if(type(load_data[2]) is str):
						background = pygame.transform.scale(pygame.image.load(load_data[2]), (SCREENWIDTH, SCREENHEIGHT))
					elif(type(load_data[2] is tuple)):
						background = load_data[2]
					grid.reset_grid_size(grid_size)
					grid.cell_data = cell_data
					grid.background = background
					current_file_name = entry_file_name.get()
					set_title()
				except Exception as e:
					winsound.PlaySound("*", winsound.SND_ASYNC)
					corrupted_file_dialog(e)

				root.destroy()
		except Exception:
			winsound.PlaySound("*", winsound.SND_ASYNC)

	root = tk.Tk()
	root.resizable(False, False)
	screen_size = get_screen_size(root)
	root.geometry(f"400x200+{screen_size[0] // 2 - 200}+{screen_size[1] // 2 - 100}")
	root.title("Load Project...")

	label_file_path = tk.Label(root, text="File Path : ")
	label_file_path.pack()

	entry_file_path = tk.Entry(root)
	entry_file_path.insert(0, canvas_projects_path)
	entry_file_path.pack()

	label_file_name = tk.Label(root, text="File Name : ")
	label_file_name.pack()

	entry_file_name = tk.Entry(root)
	entry_file_name.pack()

	button_load = tk.Button(root, text="Load .CVP (Canvas Project)", command=load_project)
	button_load.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


def save():
	def save_project():
		global current_file_name
		cvp_path = os.path.join(entry_file_path.get(), entry_file_name.get() + ".cvp")
		try:
			with open(os.path.join(cvp_path), 'w') as f:
				if(background_path is not None):
					f.write(repr((grid.cell_size, grid.cell_data, background_path)))
				else:
					f.write(repr((grid.cell_size, grid.cell_data, grid.background)))
				current_file_name = entry_file_name.get()
				set_title()

			root.destroy()
		except Exception:
			winsound.PlaySound("*", winsound.SND_ASYNC)

	root = tk.Tk()
	root.resizable(False, False)
	screen_size = get_screen_size(root)
	root.geometry(f"400x200+{screen_size[0] // 2 - 200}+{screen_size[1] // 2 - 100}")
	root.title("Save Project...")

	label_file_path = tk.Label(root, text="File Path : ")
	label_file_path.pack()

	entry_file_path = tk.Entry(root)
	entry_file_path.insert(0, canvas_projects_path)
	entry_file_path.pack()

	label_file_name = tk.Label(root, text="File Name : ")
	label_file_name.pack()

	entry_file_name = tk.Entry(root)
	entry_file_name.pack()
	entry_file_name.insert(0, current_file_name)

	button_save = tk.Button(root, text="Save .CVP (Canvas Project)", command=save_project)
	button_save.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


def export():
	def export_png():
		png_path = os.path.join(entry_file_path.get(), entry_file_name.get() + ".png")
		sub_surface = game_display.subsurface((0, 0, SCREENWIDTH, SCREENHEIGHT))
		try:
			pygame.image.save(sub_surface, png_path)
			root.destroy()
		except Exception:
			winsound.PlaySound("*", winsound.SND_ASYNC)

	root = tk.Tk()
	root.resizable(False, False)
	screen_size = get_screen_size(root)
	root.geometry(f"400x200+{screen_size[0] // 2 - 200}+{screen_size[1] // 2 - 100}")
	root.title("Export .PNG...")

	label_file_path = tk.Label(root, text="File Path : ")
	label_file_path.pack()

	entry_file_path = tk.Entry(root)
	entry_file_path.insert(0, canvas_path)
	entry_file_path.pack()

	label_file_name = tk.Label(root, text="File Name : ")
	label_file_name.pack()

	entry_file_name = tk.Entry(root)
	entry_file_name.pack()

	button_export = tk.Button(root, text="Export .PNG", command=export_png)
	button_export.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


def change_bg():
	def apply_bg():
		global background_path
		try:
			background_path = entry_bg_path.get()
			bg_img = pygame.image.load(background_path)
			grid.background = pygame.transform.scale(bg_img, (SCREENWIDTH, SCREENHEIGHT))
			root.destroy()
		except Exception:
			winsound.PlaySound("*", winsound.SND_ASYNC)

	root = tk.Tk()
	root.resizable(False, False)
	screen_size = get_screen_size(root)
	root.geometry(f"400x200+{screen_size[0] // 2 - 200}+{screen_size[1] // 2 - 100}")
	root.title("Set Background")

	label_bg_color = tk.Label(root, text="\nTo set a color background, do right-click\non a color instead of left-clicking it!")
	label_bg_color.pack()

	label_bg_image = tk.Label(root, text="\n Set an image background (Enter path below) :")
	label_bg_image.pack()

	entry_bg_path = tk.Entry(root)
	entry_bg_path.pack()

	button_set_bg = tk.Button(root, text="Apply", command=apply_bg)
	button_set_bg.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


def change_bg_color(color):
	global background_path
	grid.background = color
	background_path = None


def modify_grid_size():
	def apply_grid_size():
		try:
			grid_size_value = int(entry_grid_size.get())
			if(grid_size_value in range(10, 41)):
				grid.reset_grid_size(grid_size_value)
				root.destroy()
			else:
				raise Exception
		except Exception:
			winsound.PlaySound("*", winsound.SND_ASYNC)

	root = tk.Tk()
	root.resizable(False, False)
	screen_size = get_screen_size(root)
	root.geometry(f"600x100+{screen_size[0] // 2 - 300}+{screen_size[1] // 2 - 50}")
	root.title("Change Grid Size")

	label_grid_size = tk.Label(root, text="Enter the Grid Size between 10 & 40 (both included) :")
	label_grid_size.pack()

	label_warning = tk.Label(root, text="Warning : ALL DATA of the current working file will be lost if grid size is changed!", fg="IndianRed4")
	label_warning.pack()

	entry_grid_size = tk.Entry(root)
	entry_grid_size.pack()

	button_apply = tk.Button(root, text="Apply", command=apply_grid_size)
	button_apply.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


def how_to_use():
	root = tk.Tk()
	root.resizable(False, False)
	screen_size = get_screen_size(root)
	root.geometry(f"500x400+{screen_size[0] // 2 - 250}+{screen_size[1] // 2 - 200}")
	root.title("How to Use Canvas")

	label_how_to_use_title = tk.Label(root, text="\nHow to Use Canvas\n")
	label_how_to_use_title.pack()

	label_how_to_use_info = tk.Label(root, text='''
Left Click/Keyboard D --> Draw
Right Click/Keyboard E --> Erase
Middle Click/Keyboard F --> Fill
Move Mouse --> Move tools around the screen
Keyboard C --> Clear
Export --> Use to export a PNG file of your creation
Save --> Save the Canvas project (.CVP) you made so\nthat you can open it later
Open --> Open/Load a Canvas project file (.CVP)
Background --> Set a background
Keyboard R --> Reset background to white
Grid Size --> Change the grid cell size (or brush size in other words)\nyou are working in
		''')
	label_how_to_use_info.pack()

	button_ok = tk.Button(root, text="OK, Got it!", command=root.destroy)
	button_ok.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


def credits():
	root = tk.Tk()
	root.resizable(False, False)
	screen_size = get_screen_size(root)
	root.geometry(f"400x320+{screen_size[0] // 2 - 200}+{screen_size[1] // 2 - 160}")
	root.title("Credits")

	label_developed = tk.Label(root, text="\nSoftware (Version 1.4) Developed by :\nVaibhav Kumar")
	label_developed.pack()

	label_tools = tk.Label(root, text="\nPencil, Eraser and Fill Tool Icons from :\nfindicons.com\n")
	label_tools.pack()

	label_icon = tk.Label(root, text="\nApplication Icon by :\nfindicons.com\n")
	label_icon.pack()

	button_ok = tk.Button(root, text="OK", command=root.destroy)
	button_ok.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


pygame.init()

# constants
SCREENWIDTH = 1080
SCREENHEIGHT = 600
FPS = 120
CLOCK = pygame.time.Clock()
BASIC_FONT = pygame.font.SysFont("comicsans", 40)

# making the game display surface and setting up the icon
game_display = pygame.display.set_mode((SCREENWIDTH + 300, SCREENHEIGHT))
pygame.display.set_icon(pygame.transform.scale(pygame.image.load("icon.ico"), (32, 32)))

# file name variable(s)
current_file_name = "New Canvas Project"
file_name_temp = None

# setting the title
set_title = lambda: pygame.display.set_caption(f"{current_file_name} - Canvas")
set_title()

# creating the empty grid of size 20 ppc (px. per cell)
grid = Grid(20)

# loading drawing pointer images
pencil_surface = pygame.image.load("pencil.png").convert_alpha()
eraser_surface = pygame.transform.scale(pygame.image.load("eraser.png").convert_alpha(), (48, 48))
fill_bucket_surface = pygame.transform.scale(pygame.image.load("fill.png").convert_alpha(), (48, 48))

# creating tools
# colors
color_red = Tool(["Grid.set_color(colors.really_red)", "update_color_text(BASIC_FONT.render('Red', True, colors.black))"], ["change_bg_color(self.color)"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 1, 50, 50, colors.really_red)
color_green = Tool(["Grid.set_color(colors.earth_green)", "update_color_text(BASIC_FONT.render('Green', True, colors.black))"], ["change_bg_color(self.color)"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 1, 50, 50, colors.earth_green)
color_blue = Tool(["Grid.set_color(colors.really_blue)", "update_color_text(BASIC_FONT.render('Blue', True, colors.black))"], ["change_bg_color(self.color)"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 3, 50, 50, colors.really_blue)
color_pink = Tool(["Grid.set_color(colors.bright_pink)", "update_color_text(BASIC_FONT.render('Pink', True, colors.black))"], ["change_bg_color(self.color)"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 3, 50, 50, colors.bright_pink)
color_purple = Tool(["Grid.set_color(colors.purple)", "update_color_text(BASIC_FONT.render('Purple', True, colors.black))"], ["change_bg_color(self.color)"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 5, 50, 50, colors.purple)
color_yellow = Tool(["Grid.set_color(colors.bright_yellow)", "update_color_text(BASIC_FONT.render('Yellow', True, colors.black))"], ["change_bg_color(self.color)"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 5, 50, 50, colors.bright_yellow)
color_toothpaste = Tool(["Grid.set_color(colors.toothpaste)", "update_color_text(BASIC_FONT.render('Toothpaste', True, colors.black))"], ["change_bg_color(self.color)"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 7, 50, 50, colors.toothpaste)
color_cream = Tool(["Grid.set_color(colors.cream)", "update_color_text(BASIC_FONT.render('Cream', True, colors.black))"], ["change_bg_color(self.color)"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 7, 50, 50, colors.cream)
# other tools
save_project = Tool(["save()"], [], SCREENWIDTH + 25 * 2, 0 + 50 * 9 - 25, 100, 35, colors.really_blue, "Save", 2)
open_project = Tool(["load()"], [], SCREENWIDTH + 25 * 2, 0 + 50 * 10 - 25, 100, 35, colors.really_blue, "Open", 2)
export_image = Tool(["export()"], [], SCREENWIDTH + 25 * 2, 0 + 50 * 11 - 25, 100, 35, colors.bright_pink, "Export", 2)
add_background = Tool(["change_bg()"], [], SCREENWIDTH + 25 * 3 + 100, 0 + 50 * 9 - 25, 100, 35, colors.purple, "Background", 2, (85, 25))
change_grid_size = Tool(["modify_grid_size()"], [], SCREENWIDTH + 25 * 3 + 100, 0 + 50 * 10 - 25, 100, 35, colors.really_blue, "Grid Size", 2, (90, 25))
show_how_to_use = Tool(["how_to_use()"], [], SCREENWIDTH + 25 * 3 + 100, 0 + 50 * 11 - 25, 100, 35, colors.shady_red, "HOW TO USE", 2, (90, 25))
show_credits = Tool(["credits()"], [], SCREENWIDTH + 50 * 2, 0 + 50 * 12 - 35, 120, 30, colors.bright_yellow, "Credits", 2)

colors_tuple = (color_red, color_green, color_blue, color_pink, color_purple, color_yellow, color_toothpaste, color_cream)
other_tools_tuple = (save_project, open_project, export_image, add_background, change_grid_size, show_how_to_use, show_credits)

color_text = BASIC_FONT.render("Green", True, colors.black)

# making directories and related variables
home_dir = str(Path.home())
canvas_path = os.path.join(home_dir, "Pictures", "Canvas")
canvas_projects_path = os.path.join(home_dir, "Documents", "Canvas Projects")
background_path = None
print(os.path.isdir(canvas_path), canvas_path)
# Canvas directory
if(os.path.isdir(canvas_path)):
	pass
else:
	os.makedirs(canvas_path)
# Canvas projects directory
if(os.path.isdir(canvas_projects_path)):
	pass
else:
	os.makedirs(canvas_projects_path)

run = True
while run:
	# event section start
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			QUIT()
		elif(event.type == pygame.KEYUP):
			if(event.key == pygame.K_c):
				grid.clear_cells()
			elif(event.key == pygame.K_r):
				change_bg_color(colors.white)
	# event section end

	game_display.fill(colors.white)

	sub_surface = game_display.subsurface((0, 0, SCREENWIDTH, SCREENHEIGHT))
	if(type(grid.background) is tuple):
		sub_surface.fill(grid.background)
	elif(type(grid.background) is pygame.Surface):
		sub_surface.blit(grid.background, (0, 0))

	grid.grid_events(game_display)
	# if(type(grid.background) is tuple):
	# 	grid.draw(game_display, grid.background)
	grid.draw_cells(game_display)

	pygame.draw.line(game_display, colors.black, (SCREENWIDTH + 25, 0 + 25), (SCREENWIDTH + 25, SCREENHEIGHT - 25))

	# colors tuple iteration
	for COLOR_BUTTON in colors_tuple:
		COLOR_BUTTON.draw(game_display)
		COLOR_BUTTON.tool_events()

	# other tools iteration
	for OTHER_BUTTON in other_tools_tuple:
		OTHER_BUTTON.draw(game_display)
		OTHER_BUTTON.tool_events()

	# blitting text(s)
	game_display.blit(color_text, (SCREENWIDTH + 25 + 100, 0 + 25 - color_text.get_height() // 2))

	mouse_pos = pygame.mouse.get_pos()
	if(mouse_pos[0] <= SCREENWIDTH):
		pygame.mouse.set_visible(False)
		mouse_click = pygame.mouse.get_pressed()
		key_press = pygame.key.get_pressed()
		if(mouse_click[0] == 1 or key_press[pygame.K_d]):
			game_display.blit(pencil_surface, (mouse_pos[0], mouse_pos[1] - pencil_surface.get_height()))
		elif(mouse_click[1] == 1 or key_press[pygame.K_f]):
			game_display.blit(fill_bucket_surface, (mouse_pos[0], mouse_pos[1] - fill_bucket_surface.get_height()))
		elif(mouse_click[2] == 1 or key_press[pygame.K_e]):
			game_display.blit(eraser_surface, (mouse_pos[0], mouse_pos[1] - eraser_surface.get_height()))
		else:
			game_display.blit(pencil_surface, (mouse_pos[0], mouse_pos[1] - pencil_surface.get_height()))
	else:
		pygame.mouse.set_visible(True)

	pygame.display.update()
	CLOCK.tick(FPS)

pygame.quit()
quit()
