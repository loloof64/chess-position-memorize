from tkinter import *
from tkinter.filedialog import *

class MainWindow(Tk):

	PICTURES_SIZE = 40

	def __init__(self):
		Tk.__init__(self)
		self.winfo_toplevel().title("Chess Position Memorize")
		self._create_pictures()
		self._add_widgets()
		self._playing_mode = False
		self._error_mode = False

		self._load_position("d8h4", "  rk /  pp /     /     /B Q R")
		self._clear_errors()

		self._update_board()

	def _load_position(self, corner_cells, pieces):
		self._pieces = pieces
		self._corner_cells = corner_cells
		self._pieces_codes = list(map(lambda x: list(x), self._pieces.split("/")))
		self._clear_errors()
		self._update_board()

	def _open_file(self):
		file_path = askopenfilename(title="Open a file",filetypes=[('all text files','*')])
		if file_path != () and file_path != '' :
			self._load_position_from_file(file_path)

	def _load_position_from_file(self, file_path):
		with open(file_path, 'r') as file :
			file_data = file.read().split("\n")
			self._playing_mode = False
			self._error_mode = False
			self._clear_errors()
			self._load_position(file_data[0], file_data[1])

	def _clear_errors(self):
		self._errors = [[False for cell in line] for line in self._pieces_codes]

	def _update_widgets(self):
		if self._playing_mode :
			self._white_pieces_buttons.pack()
			self._black_pieces_buttons.pack()
			self._bin_button.pack()
			self._ready_button['text'] = "Submit"
		else :
			self._white_pieces_buttons.pack_forget()
			self._black_pieces_buttons.pack_forget()
			self._bin_button.pack_forget()
			self._ready_button['text'] = "I'm ready"

	def _add_widgets(self):
		top_paned_window = PanedWindow(self, orient=HORIZONTAL)
		top_paned_window.pack(side=TOP)

		self._load_button = Button(self, text="Load position", command=lambda: self._open_file())
		top_paned_window.add(self._load_button)

		self._ready_button = Button(self, text="I'm ready", command=lambda: self._toggle_playing_state())
		top_paned_window.add(self._ready_button)

		self._bin_image = PhotoImage(file = "bin.png")
		self._bin_button = Button(self, image = self._bin_image)
		self._bin_button.pack(side=BOTTOM)

		self._black_pieces_buttons = PanedWindow(self, orient=HORIZONTAL)
		self._black_pieces_buttons.pack(side=BOTTOM)

		self._black_pawn_button = Button(self, image = self._pieces_images_list["BlackPawn"])
		self._black_pieces_buttons.add(self._black_pawn_button)
		self._black_knight_button = Button(self, image = self._pieces_images_list["BlackKnight"])
		self._black_pieces_buttons.add(self._black_knight_button)
		self._black_bishop_button = Button(self, image = self._pieces_images_list["BlackBishop"])
		self._black_pieces_buttons.add(self._black_bishop_button)
		self._black_rook_button = Button(self, image = self._pieces_images_list["BlackRook"])
		self._black_pieces_buttons.add(self._black_rook_button)
		self._black_queen_button = Button(self, image = self._pieces_images_list["BlackQueen"])
		self._black_pieces_buttons.add(self._black_queen_button)
		self._black_king_button = Button(self, image = self._pieces_images_list["BlackKing"])
		self._black_pieces_buttons.add(self._black_king_button)

		self._white_pieces_buttons = PanedWindow(self, orient=HORIZONTAL)
		self._white_pieces_buttons.pack(side=BOTTOM)

		self._white_pawn_button = Button(self, image = self._pieces_images_list["WhitePawn"])
		self._white_pieces_buttons.add(self._white_pawn_button)
		self._white_knight_button = Button(self, image = self._pieces_images_list["WhiteKnight"])
		self._white_pieces_buttons.add(self._white_knight_button)
		self._white_bishop_button = Button(self, image = self._pieces_images_list["WhiteBishop"])
		self._white_pieces_buttons.add(self._white_bishop_button)
		self._white_rook_button = Button(self, image = self._pieces_images_list["WhiteRook"])
		self._white_pieces_buttons.add(self._white_rook_button)
		self._white_queen_button = Button(self, image = self._pieces_images_list["WhiteQueen"])
		self._white_pieces_buttons.add(self._white_queen_button)
		self._white_king_button = Button(self, image = self._pieces_images_list["WhiteKing"])
		self._white_pieces_buttons.add(self._white_king_button)

		self._bin_button.config(command=lambda: self._set_editing_piece(""))
		self._black_pawn_button.config(command=lambda: self._set_editing_piece("BlackPawn"))
		self._black_knight_button.config(command=lambda: self._set_editing_piece("BlackKnight"))
		self._black_bishop_button.config(command=lambda: self._set_editing_piece("BlackBishop"))
		self._black_rook_button.config(command=lambda: self._set_editing_piece("BlackRook"))
		self._black_queen_button.config(command=lambda: self._set_editing_piece("BlackQueen"))
		self._black_king_button.config(command=lambda: self._set_editing_piece("BlackKing"))
		self._white_pawn_button.config(command=lambda: self._set_editing_piece("WhitePawn"))
		self._white_knight_button.config(command=lambda: self._set_editing_piece("WhiteKnight"))
		self._white_bishop_button.config(command=lambda: self._set_editing_piece("WhiteBishop"))
		self._white_rook_button.config(command=lambda: self._set_editing_piece("WhiteRook"))
		self._white_queen_button.config(command=lambda: self._set_editing_piece("WhiteQueen"))
		self._white_king_button.config(command=lambda: self._set_editing_piece("WhiteKing"))

		self._canvas = Canvas(self,
			width=MainWindow.PICTURES_SIZE*9,
			height=MainWindow.PICTURES_SIZE*9,
			bg = '#128812'
		)
		self._canvas.pack(side=BOTTOM)
		self._canvas.bind("<Button-1>", self._update_canvas_on_click)

		self._white_pieces_buttons.pack_forget()
		self._black_pieces_buttons.pack_forget()
		self._bin_button.pack_forget()

	def _update_canvas_on_click(self, event):
		if self._playing_mode :
			event_in_bounds = (
				event.x >= MainWindow.PICTURES_SIZE * 0.5 and
				event.x <= MainWindow.PICTURES_SIZE * (0.5+ self._board_size[0]) and
				event.y >= MainWindow.PICTURES_SIZE * 0.5 and
				event.y <= MainWindow.PICTURES_SIZE * (0.5+ self._board_size[1])
				)

			if event_in_bounds:
				cell_x = int((event.x - MainWindow.PICTURES_SIZE*0.5) / MainWindow.PICTURES_SIZE)
				cell_y = int((event.y - MainWindow.PICTURES_SIZE*0.5) / MainWindow.PICTURES_SIZE)

				self._update_piece_at_relative_coords(cell_x, cell_y)

	def _update_piece_at_relative_coords(self, cell_x, cell_y):
		new_piece_code = self._get_editing_piece_code()
		old_piece_code = self._pieces_codes[cell_y][cell_x]
		self._pieces_codes[cell_y][cell_x] = new_piece_code if (old_piece_code != new_piece_code) else ""
		self._update_board()

	def _get_editing_piece_code(self):
		if self._editing_piece == "" :
			return ""
		if self._editing_piece == "WhitePawn" :
			return 'P'
		if self._editing_piece == "WhiteKnight" :
			return 'N'
		if self._editing_piece == "WhiteBishop" :
			return 'B'
		if self._editing_piece == "WhiteRook" :
			return 'R'
		if self._editing_piece == "WhiteQueen" :
			return 'Q'
		if self._editing_piece == "WhiteKing" :
			return 'K'
		if self._editing_piece == "BlackPawn" :
			return 'p'
		if self._editing_piece == "BlackKnight" :
			return 'n'
		if self._editing_piece == "BlackBishop" :
			return 'b'
		if self._editing_piece == "BlackRook" :
			return 'r'
		if self._editing_piece == "BlackQueen" :
			return 'q'
		if self._editing_piece == "BlackKing" :
			return 'k'

	def _toggle_playing_state(self):
		if self._playing_mode :
			self._update_errors()
			self._pieces_codes =  list(map(lambda x: list(x), self._expected_position.split("/")))
			self._update_board()
			self._playing_mode = False
			errors_count = sum(map(lambda line: sum(line), [[1 if error else 0 for error in line] for line in self._errors]))
			self._error_mode = errors_count > 0
			self._ready_button['text'] = "Understood" if self._error_mode else "I'm ready"
			if not self._error_mode:
				self._load_position(self._corner_cells, self._expected_position)
				self._update_widgets()
			else:
				self._update_board()
		else :
			if self._error_mode:
				self._error_mode = False
				self._ready_button['text'] = "I'm ready"
				self._load_position(self._corner_cells, self._expected_position)
				self._update_board()
			else:
				self._expected_position = self._pieces
				self._clear_board()
				self._set_editing_piece("")
				self._playing_mode = True
				self._update_widgets()

	def _update_errors(self):
		expected_pieces = list(map(lambda x: list(x), self._expected_position.split("/")))
		for cell_y in range(len(self._pieces_codes)) :
			for cell_x in range(len(self._pieces_codes[cell_y])) :
				self._errors[cell_y][cell_x] = expected_pieces[cell_y][cell_x] != self._pieces_codes[cell_y][cell_x]
		self._update_board()

	def _set_editing_piece(self, piece):
		self._editing_piece = piece
		self._update_pieces_buttons()

	def _update_pieces_buttons(self):
		self._bin_button.config(relief="sunken" if self._editing_piece == "" else "groove",
		bg="red" if self._editing_piece == "" else "gray")
		self._white_pawn_button.config(relief="sunken" if self._editing_piece == "WhitePawn" else "groove",
		bg="red" if self._editing_piece == "WhitePawn" else "gray")
		self._white_knight_button.config(relief="sunken" if self._editing_piece == "WhiteKnight" else "groove",
		bg="red" if self._editing_piece == "WhiteKnight" else "gray")
		self._white_bishop_button.config(relief="sunken" if self._editing_piece == "WhiteBishop" else "groove",
		bg="red" if self._editing_piece == "WhiteBishop" else "gray")
		self._white_rook_button.config(relief="sunken" if self._editing_piece == "WhiteRook" else "groove",
		bg="red" if self._editing_piece == "WhiteRook" else "gray")
		self._white_queen_button.config(relief="sunken" if self._editing_piece == "WhiteQueen" else "groove",
		bg="red" if self._editing_piece == "WhiteQueen" else "gray")
		self._white_king_button.config(relief="sunken" if self._editing_piece == "WhiteKing" else "groove",
		bg="red" if self._editing_piece == "WhiteKing" else "gray")
		self._black_pawn_button.config(relief="sunken" if self._editing_piece == "BlackPawn" else "groove",
		bg="red" if self._editing_piece == "BlackPawn" else "gray")
		self._black_knight_button.config(relief="sunken" if self._editing_piece == "BlackKnight" else "groove",
		bg="red" if self._editing_piece == "BlackKnight" else "gray")
		self._black_bishop_button.config(relief="sunken" if self._editing_piece == "BlackBishop" else "groove",
		bg="red" if self._editing_piece == "BlackBishop" else "gray")
		self._black_rook_button.config(relief="sunken" if self._editing_piece == "BlackRook" else "groove",
		bg="red" if self._editing_piece == "BlackRook" else "gray")
		self._black_queen_button.config(relief="sunken" if self._editing_piece == "BlackQueen" else "groove",
		bg="red" if self._editing_piece == "BlackQueen" else "gray")
		self._black_king_button.config(relief="sunken" if self._editing_piece == "BlackKing" else "groove",
		bg="red" if self._editing_piece == "BlackKing" else "gray")


	def _clear_board(self):
		new_position = "/".join(["".join([" " for i in range(self._board_size[1])]) for j in range(self._board_size[0])])
		self._load_position(self._corner_cells, new_position)

	def _update_board(self):
		self._canvas.delete("all")
		self._compute_board_size()
		self._compute_top_left_cell_absolute_coords()
		self._canvas.config(
			width = (self._board_size[0]+1) * MainWindow.PICTURES_SIZE,
			height = (self._board_size[1]+1) * MainWindow.PICTURES_SIZE
		)

		for cell_y in range(0, len(self._pieces_codes)):
			for cell_x in range(0, len(self._pieces_codes[cell_y])):
				self._draw_single_cell((cell_y, cell_x))

		self._create_piece_images()
		self._draw_cells_coordinates()

	def _compute_board_size(self):
		corner_cells_num = list(map(ord, self._corner_cells))
		width = corner_cells_num[2] - corner_cells_num[0] + 1
		height = corner_cells_num[1] - corner_cells_num[3] + 1
		self._board_size = (width, height)

	def _compute_top_left_cell_absolute_coords(self):
		corner_cells_num = list(map(ord, self._corner_cells))
		self._top_left_cell_absolute_coords = (
			corner_cells_num[1] - ord('1'),
			corner_cells_num[0] - ord('a')
		)

	def _draw_single_cell(self, cell_coord):
		absolute_coord = (
			cell_coord[1] - self._top_left_cell_absolute_coords[1],
			cell_coord[0] - self._top_left_cell_absolute_coords[0],
		)

		is_white_cell = (absolute_coord[0] + absolute_coord[1]) %2 != 0
		bg_color = 'red' if self._errors[cell_coord[0]][cell_coord[1]] else '#f5f6ce' if is_white_cell else '#CD853F'

		square_y = (cell_coord[0] + 0.5) * MainWindow.PICTURES_SIZE
		square_x = (cell_coord[1] + 0.5) * MainWindow.PICTURES_SIZE

		self._canvas.create_rectangle(
			square_x,
			square_y,
			square_x + MainWindow.PICTURES_SIZE,
			square_y + MainWindow.PICTURES_SIZE,
			fill = bg_color
		)

	def caesar_char(c, step):
		return chr(ord(c) + step)

	def _create_pictures(self):
		self._pieces_images_list = {}
		pictures_to_build = [
			"WhitePawn",
			"WhiteKnight",
			"WhiteBishop",
			"WhiteRook",
			"WhiteQueen",
			"WhiteKing",
			"BlackPawn",
			"BlackKnight",
			"BlackBishop",
			"BlackRook",
			"BlackQueen",
			"BlackKing"
		]
		for picture_name in pictures_to_build :
			picture = PhotoImage(file = picture_name + ".png")
			picture = picture.subsample(int(80 / MainWindow.PICTURES_SIZE))
			self._pieces_images_list[picture_name] = picture

	def _create_piece_images(self):
		for cell_y in range(0, len(self._pieces_codes)):
			for cell_x in range(0, len(self._pieces_codes[cell_y])):
				piece = self._pieces_codes[cell_y][cell_x]
				piece_image = self._piece_image_from_code(piece)

				if piece_image != "":
					picture = self._pieces_images_list[piece_image]
					square_y = (cell_y + 0.5) * MainWindow.PICTURES_SIZE
					square_x = (cell_x + 0.5) * MainWindow.PICTURES_SIZE
					self._canvas.create_image(square_x, square_y, image=picture, anchor = 'nw')

	def _draw_cells_coordinates(self):
		font = 'Arial 9 bold'
		letters_coll = [MainWindow.caesar_char(self._corner_cells[0], step).upper() for step in range(self._board_size[0])]
		for letter_index, letter in enumerate(letters_coll) :
			x = MainWindow.PICTURES_SIZE * (0.9 + letter_index)
			y1 = MainWindow.PICTURES_SIZE * 0.15
			y2 = MainWindow.PICTURES_SIZE * (0.65 + self._board_size[1])
			self._canvas.create_text(x,y1, text = letter, anchor='nw', font=font)
			self._canvas.create_text(x,y2, text = letter, anchor='nw', font=font)

		letters_coll = [MainWindow.caesar_char(self._corner_cells[3], step).upper() for step in range(self._board_size[1])]
		for letter_index, letter in enumerate(list(reversed(letters_coll))) :
			x1 = MainWindow.PICTURES_SIZE * 0.12
			x2 = MainWindow.PICTURES_SIZE * (0.62 + self._board_size[0])
			y = MainWindow.PICTURES_SIZE * (0.9 + letter_index)
			self._canvas.create_text(x1,y, text = letter, anchor='nw', font=font)
			self._canvas.create_text(x2,y, text = letter, anchor='nw', font=font)

	def _piece_image_from_code(self, piece):
		if piece == 'P':
			return "WhitePawn"
		if piece == 'N' :
			return "WhiteKnight"
		if piece == 'B' :
			return "WhiteBishop"
		if piece == 'R' :
			return "WhiteRook"
		if piece == 'Q' :
			return "WhiteQueen"
		if piece == 'K' :
			return "WhiteKing"
		if piece == 'p' :
			return "BlackPawn"
		if piece == 'n' :
			return "BlackKnight"
		if piece == 'b' :
			return "BlackBishop"
		if piece == 'r' :
			return "BlackRook"
		if piece == 'q' :
			return "BlackQueen"
		if piece == 'k' :
			return "BlackKing"
		return ""

if __name__ == "__main__":
	MainWindow().mainloop()
