import sys,os
import curses
import chess
import chess.variant
import numpy as np

curses.initscr()
curses.curs_set(False)

def draw_menu(stdscr):
    k = 0
    delay = 60

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    stdscr.nodelay(True)

    board = chess.variant.HordeBoard()
    #board = chess.Board()

    # Loop where k is the last character pressed
    while (k != ord('q')):
        height, width = stdscr.getmaxyx()

        # Declaration of strings
        title = "Curses example"[:width-1]
        #subtitle = "Written by Clay McLeod"[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        #statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = "No key press detected..."[:width-1]
        if k == ord('s'):
            delay += 10
        if k == ord('f'):
            if delay>0:
                delay -= 10
        curses.delay_output(delay)

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        #start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        #stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        checkmated = board.is_checkmate()
        stalemated = (board.is_stalemate() or
                      board.is_insufficient_material() or
                      board.is_seventyfive_moves() or
                      board.is_fivefold_repetition() or
                      board.can_claim_draw() or
                      board.can_claim_fifty_moves() or
                      board.can_claim_threefold_repetition())

        if k==ord('r') or checkmated or stalemated:
            board = chess.variant.HordeBoard()
            #board = chess.Board()

        # Render the board in the center of the screen
        buffer = int(np.floor(width/4)-4)
        for i,row in enumerate(board.__str__().split('\n')):
            rowtext = row.replace('.',' ')
            rownum = int(np.floor(height/2)-4)+i
            stdscr.addstr(rownum,0,buffer*' ')
            for j,ch in enumerate(rowtext):
                if ch==ch.upper() and ch==ch.lower():
                    pass # Empty square
                elif ch==ch.lower(): # Black piece
                    pass
                elif ch==ch.upper(): # White piece
                    stdscr.attron(curses.A_REVERSE)
                stdscr.addch(rownum,buffer+j,ch)
                stdscr.attroff(curses.A_REVERSE)

        try:
            if board.legal_moves.count()>0:
                n = np.random.randint(0,board.legal_moves.count())
                for i,m in enumerate(board.legal_moves):
                    if i==n:
                        board.push_uci(m.__str__())
            else:
                #stdscr.addstr(10,0,'STALEMATE')
                board = chess.variant.HordeBoard()
                #board = chess.Board()
        except IndexError:
            with open("errors.txt", "a") as text_file:
                text_file.write(repr(board))
                text_file.write('\n\n')
            board = chess.variant.HordeBoard()
            #board = chess.Board
            #print(board)
            break

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
