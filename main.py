# import statements
import chess
import pygame

# chess variable initialisations
instructions = "\nWelcome to Ghost Chess!\nA game where pawns are pumpkins and ghosts and all of the rules of chess apply except for pawn promotion. Now you must battle harder to keep more pieces!\nBring a friend and have a game of ghost chess!\nTo maximise your experience, go into fullscreen (f11) and maximise the output window. For this to work, the output window must be horizontally parallel to the console tab (you can add tabs by clicking the + button!) If you do not have the necessary settings, change them and rerun the program.\nGood luck!\n"
print(instructions)
color = int(input("Which side would you like to play? Enter 0 for white and 1 for black : "))
selected_piece = ""
pos_x, pos_y, prev_piece_column, piece_column, piece_row = 0, 0, 0, 0, 0
previous_column, previous_row, opponent_turn = 0, 0, True if color == 1 else False

# pygame variable initialisations
pygame.init()
background_color = (0, 0, 0)
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Ghost chess")
pygame.display.set_icon(pygame.image.load("ghost.png"))

# class for handling conversions between different units and notations
class Conversions:
    def __init__(self):
        self.board = chess.Board()
        self.moves = []

    def coordinates_to_grid(self, pos):
        global piece_column, piece_row
        x, y = pos
        for i in range(0, 641, 80):
            piece_column += 1
            if i <= x <= i + 80:
                break
        for i in range(0, 641, 80):
            piece_row += 1
            if i <= y <= i + 80:
                break

    def mouse_to_grid(self, pos):
        global piece_column, piece_row, pos_x, pos_y
        x, y = pos
        for i in range(0, 641, 80):
            pos_x += 80
            piece_column += 1
            if i <= x <= i + 80:
                break
        for i in range(0, 641, 80):
            piece_row += 1
            pos_y += 80
            if i <= y <= i + 80:
                break

    def convert_to_chess_notation(self, capture, moved_piece):
        position = ""
        new_column = 0
        new_row = 0
        if moved_piece[1] == 'P':
            moved_piece = ''
        else:
            moved_piece = moved_piece[1]
        position += moved_piece
        if capture:
            position += 'x'
        if color == 0:
            new_row = 9-piece_row
            new_column = chr(96+piece_column)
        else:
            new_row = piece_row
            new_column = chr(105-piece_column)
        position += new_column+str(new_row)
        return position

    def move(self):
        from_column, from_row, to_column, to_row = 0, 0, 0, 0
        if color == 0:
            from_row = 57-previous_row
            to_row = 57-piece_row
            from_column = 96+previous_column
            to_column = 96+piece_column
        else:
            from_row = previous_row+48
            to_row = piece_row+48
            from_column = 105-previous_column
            to_column = 105-piece_column
        return chr(from_column)+chr(from_row)+chr(to_column)+chr(to_row)

# class for handling gui
class GUI:
    def __init__(self):
        # hash map for black and white pieces, with mapping between image name and pygame Surface.
        if color == 0:
            self.white_pieces = {'wR1': '', 'wN1': '', 'wB1': '', 'wQ': '', 'wK': '', 'wB2': '', 'wN2': '', 'wR2': ''}
            self.black_pieces = {'bR1': '', 'bN1': '', 'bB1': '', 'bQ': '', 'bK': '', 'bB2': '', 'bN2': '', 'bR2': ''}
        else:
            self.white_pieces = {'wR1': '', 'wN1': '', 'wB1': '', 'wK': '', 'wQ': '', 'wB2': '', 'wN2': '', 'wR2': ''}
            self.black_pieces = {'bR1': '', 'bN1': '', 'bB1': '', 'bK': '', 'bQ': '', 'bB2': '', 'bN2': '', 'bR2': ''}
        # hash map for black and white pawns, with mapping between image name and pygame Surface.
        self.white_pawns = {'wP1': '', 'wP2': '', 'wP3': '', 'wP4': '', 'wP5': '', 'wP6': '', 'wP7': '', 'wP8': ''}
        self.black_pawns = {'bP1': '', 'bP2': '', 'bP3': '', 'bP4': '', 'bP5': '', 'bP6': '', 'bP7': '', 'bP8': ''}
        # hash map with mapping between piece (column, row) pair and pygame Surface.
        self.position = {}
        # hash map with mapping between piece coordinate and pygame Surface
        self.coordinates = {}
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.reset()

    def reset(self):
        self.draw_board()
        self.initialise_white_pieces()
        self.initialise_black_pieces()
        pygame.display.update()

    def draw_board(self):
        global color
        # local variables for board labels and square color
        if color == 1:
            start = 0
            increment = -1
            char = 73
        else:
            start = 9
            increment = 1
            char = 64
        square_color = (255, 255, 255)
        for i in range(0, 640, 80):
            char += increment
            start += -1*increment
            screen.blit(self.font.render('   '+chr(char), True, (255, 255, 255), (0, 0, 0)), (i, 640))
            screen.blit(self.font.render('   '+str(start), True, (255, 255, 255), (0, 0, 0)), (640, i+30))
            for j in range(0, 640, 80):
                pygame.draw.rect(screen, square_color, pygame.Rect(j, i, 80, 80))
                if j != 560:
                    if square_color == (255, 255, 255):
                        square_color = (0, 97, 0)
                    else:
                        square_color = (255, 255, 255)

    def initialise_white_pieces(self):
        global pos_x, pos_y, piece_column, piece_row
        if color == 1:
            piece_column, piece_row = 0, 1
            pos_x, pos_y = 0, 0
        else:
            piece_column, piece_row = 0, 8
            pos_x, pos_y = 0, 560
        for pieces in self.white_pieces:
            piece_column += 1
            self.white_pieces[pieces] = pygame.image.load('white_img/'+pieces+'.png')
            self.position[(piece_column, piece_row)] = self.white_pieces[pieces]
            self.coordinates[(pos_x, pos_y)] = self.white_pieces[pieces]
            screen.blit(self.white_pieces[pieces], (pos_x, pos_y))
            pos_x += 80
        if color == 1:
            piece_column, piece_row = 0, 2
            pos_x, pos_y = 0, 80
        else:
            piece_column, piece_row = 0, 7
            pos_x, pos_y = 0, 480
        for pawns in self.white_pawns:
            piece_column += 1
            self.white_pawns[pawns] = pygame.image.load('white_img/'+pawns+'.png')
            self.position[(piece_column, piece_row)] = self.white_pawns[pawns]
            self.coordinates[(pos_x, pos_y)] = self.white_pawns[pawns]
            screen.blit(self.white_pawns[pawns], (pos_x, pos_y))
            pos_x += 80

    def initialise_black_pieces(self):
        global pos_x, pos_y, piece_column, piece_row
        if color == 1:
            piece_column, piece_row = 0, 8
            pos_x, pos_y = 0, 560
        else:
            piece_column, piece_row = 0, 1
            pos_x, pos_y = 0, 0
        for pieces in self.black_pieces:
            piece_column += 1
            self.black_pieces[pieces] = pygame.image.load('black_img/'+pieces+'.png')
            self.position[(piece_column, piece_row)] = self.black_pieces[pieces]
            self.coordinates[(pos_x, pos_y)] = self.black_pieces[pieces]
            screen.blit(self.black_pieces[pieces], (pos_x, pos_y))
            pos_x += 80
        if color == 1:
            piece_column, piece_row = 0, 7
            pos_x, pos_y = 0, 480
        else:
            piece_column, piece_row = 0, 2
            pos_x, pos_y = 0, 80
        for pawns in self.black_pawns:
            piece_column += 1
            self.black_pawns[pawns] = pygame.image.load('black_img/'+pawns+'.png')
            self.position[(piece_column, piece_row)] = self.black_pawns[pawns]
            self.coordinates[(pos_x, pos_y)] = self.black_pawns[pawns]
            screen.blit(self.black_pawns[pawns], (pos_x, pos_y))
            pos_x += 80

    def handle_piece_location(self, x, y):
        # set new coordinates and position of piece.
        self.coordinates[(x, y)] = selected_piece
        self.position[(piece_column, piece_row)] = selected_piece
        # push new move to board from uci format.
        conversions.board.push(chess.Move.from_uci(move))
        
    def handle_screen(self):
        # place pieces at new coordinates and update screen.
        global piece_column, piece_row
        self.draw_board()
        for coordinates in self.coordinates.keys():
            screen.blit(self.coordinates[coordinates], coordinates)
        pygame.display.update()
        piece_column, piece_row = 0, 0

    def handle_kingside_castling(self):
        if color == 0:
            # setting king position
            self.coordinates[(480, 560)] = selected_piece
            self.position[(7, 8)] = selected_piece

            # setting rook position
            self.coordinates[(400, 560)] = self.white_pieces['wR2']
            self.position[(6, 8)] = self.white_pieces['wR2']

            # remove old king position
            self.coordinates.pop((previous_column * 80 - 80, previous_row * 80 - 80))
            self.position.pop((previous_column, previous_row))

            # remove old rook position
            self.coordinates.pop((560, 560))
            self.position.pop((8, 8))

        else:
            # setting king position
            self.coordinates[(80, 560)] = selected_piece
            self.position[(2, 8)] = selected_piece

            # setting rook position
            self.coordinates[(160, 560)] = self.black_pieces['bR1']
            self.position[(3, 8)] = self.black_pieces['bR1']

            # remove old king position
            self.coordinates.pop((previous_column * 80 - 80, previous_row * 80 - 80))
            self.position.pop((previous_column, previous_row))

            # remove old rook position
            self.coordinates.pop((0, 560))
            self.position.pop((1, 8))
        conversions.board.push(chess.Move.from_uci(move))

    def handle_queenside_castling(self):
        if color == 0:
            # setting king position
            self.coordinates[(160, 560)] = selected_piece
            self.position[(3, 8)] = selected_piece

            # setting rook position
            self.coordinates[(240, 560)] = self.white_pieces['wR1']
            self.position[(4, 8)] = self.white_pieces['wR1']

            # remove old king position
            self.coordinates.pop((previous_column*80-80, previous_row*80-80))
            self.position.pop((previous_column, previous_row))

            # remove old rook position
            self.coordinates.pop((0, 560))
            self.position.pop((1, 8))

        else:
            # setting king position
            self.coordinates[(400, 560)] = selected_piece
            self.position[(4, 8)] = selected_piece

            # setting rook position
            self.coordinates[(320, 560)] = self.black_pieces['bR2']
            self.position[(5, 8)] = self.black_pieces['bR2']

            # remove old king position
            self.coordinates.pop((previous_column*80-80, previous_row*80-80))
            self.position.pop((previous_column, previous_row))

            # remove old rook position
            self.coordinates.pop((560, 560))
            self.position.pop((8, 8))
        conversions.board.push(chess.Move.from_uci(move))

    def handle_en_passant(self):
        # set new coordinates and position of pawn
        self.coordinates[(pos_x - 80, pos_y - 80)] = selected_piece
        self.position[(piece_column, piece_row)] = selected_piece
        # remove old position of capturing pawn and captured pawn.
        # since the pawns are parallel, the row remains the same but the column changes.
        if color == 0:
            self.coordinates.pop((80*(ord(move[0])-97), 80*(56-ord(move[1]))))
            self.coordinates.pop((80*(ord(move[2])-97), 80*(56-ord(move[1]))))
        else:
            self.coordinates.pop((80*(104-ord(move[0])), 80*(55-ord(move[1]))))
            self.coordinates.pop((80*(104-ord(move[2])), 80*(55-ord(move[1]))))

    def handle_opponent_kingside_castling(self):
        if color == 1:
            # setting king position
            self.coordinates[(80, 0)] = selected_piece
            self.position[(2, 1)] = selected_piece

            # setting rook position
            self.coordinates[(160, 0)] = self.white_pieces['wR1']
            self.position[(3, 1)] = self.white_pieces['wR1']

            # remove old king position
            self.coordinates.pop((previous_column * 80 - 80, previous_row * 80 - 80))
            self.position.pop((previous_column, previous_row))

            # remove old rook position
            self.coordinates.pop((0, 0))

        else:
            # setting king position
            self.coordinates[(480, 0)] = selected_piece
            self.position[(7, 1)] = selected_piece

            # setting rook position
            self.coordinates[(400, 0)] = self.black_pieces['bR2']
            self.position[(6, 1)] = self.black_pieces['bR2']

            # remove old king position
            self.coordinates.pop((previous_column * 80 - 80, previous_row * 80 - 80))
            self.position.pop((previous_column, previous_row))

            # remove old rook position
            self.coordinates.pop((560, 0))
        conversions.board.push(chess.Move.from_uci(move))

    def handle_opponent_queenside_castling(self):
        if color == 1:
            # setting king position
            self.coordinates[(400, 0)] = selected_piece
            self.position[(6, 1)] = selected_piece

            # setting rook position
            self.coordinates[(320, 0)] = self.white_pieces['wR2']
            self.position[(5, 1)] = self.white_pieces['wR2']

            # remove old king position
            self.coordinates.pop((previous_column * 80 - 80, previous_row * 80 - 80))
            self.position.pop((previous_column, previous_row))

            # remove old rook position
            self.coordinates.pop((560, 0))

        else:
            # setting king position
            self.coordinates[(160, 0)] = selected_piece
            self.position[(2, 1)] = selected_piece

            # setting rook position
            self.coordinates[(240, 0)] = self.black_pieces['bR1']
            self.position[(4, 1)] = self.black_pieces['bR1']

            # remove old king position
            self.coordinates.pop((previous_column * 80 - 80, previous_row * 80 - 80))
            self.position.pop((previous_column, previous_row))

            # remove old rook position
            self.coordinates.pop((0, 0))
        conversions.board.push(chess.Move.from_uci(move))

    def handle_opponent_en_passant(self):
        # set new coordinates and position of pawn
        self.coordinates[(pos_x - 80, pos_y - 80)] = selected_piece
        self.position[(piece_column, piece_row)] = selected_piece
        # remove old position of capturing pawn and captured pawn.
        # since the pawns are parallel, the row remains the same but the column changes.
        if color == 0:
            self.coordinates.pop((80*(ord(move[0])-97), 80*(56-ord(move[1]))))
            self.coordinates.pop((80*(ord(move[2])-97), 80*(ord(move[1])-55)))
        else:
            print(move)
            self.coordinates.pop((80*(104-ord(move[0])), 80*(57-ord(move[1]))))
            self.coordinates.pop((80*(104-ord(move[2])), 80*(57-ord(move[1]))))

    def checkmate(self):
        screen.fill(background_color)
        if opponent_turn:
            if color == 0:
                screen.blit(self.font.render("Black wins!", True, (255, 255, 255), (0, 0, 0)), (400, 400))
            else:
                screen.blit(self.font.render("White wins!", True, (255, 255, 255), (0, 0, 0)), (400, 400))
        else:
            if color == 0:
                screen.blit(self.font.render("White wins!", True, (255, 255, 255), (0, 0, 0)), (400, 400))
            else:
                screen.blit(self.font.render("Black wins!", True, (255, 255, 255), (0, 0, 0)), (400, 400))
        pygame.display.update()

    def draw(self):
        screen.fill(background_color)
        screen.blit(self.font.render("Draw!", True, (255, 255, 255), (0, 0, 0)), (400, 400))
        pygame.display.update()

# object initialisations
gui = GUI()
conversions = Conversions()

# pygame event listener
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game moves in uci format are", conversions.moves)
            print("Game fen is", conversions.board.fen())
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            piece_column, piece_row = 0, 0
            conversions.coordinates_to_grid(pygame.mouse.get_pos())
            previous_column, previous_row = piece_column, piece_row
            if (piece_column, piece_row) in gui.position.keys():
                selected_piece = gui.position[(piece_column, piece_row)]

        elif event.type == pygame.MOUSEBUTTONUP:
            piece_column, piece_row, pos_x, pos_y = 0, 0, 0, 0
            conversions.mouse_to_grid(pygame.mouse.get_pos())
            move = conversions.move()
            conversions.moves.append(move)
            # verifies that the position of the mouse is within the board.
            # verifies that a piece was not placed in the same square.
            if pos_x-80 < 561 and pos_y-80 < 561 and move[0]+move[1] != move[2]+move[3]:
                if conversions.board.is_legal(chess.Move.from_uci(move)):
                    if conversions.board.is_kingside_castling(chess.Move.from_uci(move)):
                        if opponent_turn:
                            gui.handle_opponent_kingside_castling()
                        else:
                            gui.handle_kingside_castling()
                    elif conversions.board.is_queenside_castling(chess.Move.from_uci(move)):
                        if opponent_turn:
                            gui.handle_opponent_queenside_castling()
                        else:
                            gui.handle_queenside_castling()
                    elif conversions.board.is_en_passant(chess.Move.from_uci(move)):
                        if opponent_turn:
                            gui.handle_opponent_en_passant()
                        else:
                            gui.handle_en_passant()
                    else:
                        for coordinates in gui.coordinates.keys():
                            if gui.coordinates[coordinates] == selected_piece:
                                gui.coordinates.pop(coordinates, None)
                                break
                        gui.handle_piece_location(pos_x-80, pos_y-80)
                    gui.handle_screen()
                    if conversions.board.is_checkmate():
                        gui.checkmate()
                    if conversions.board.can_claim_draw():
                        gui.draw()
                    opponent_turn = False if opponent_turn else True