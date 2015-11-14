import curses
import time
import random
import locale
import os
import argparse


def lamentOnTheNatureOfMondaysAndLasagne(msg=None):
    # Set locale - solves unicode issues
    locale.setlocale(locale.LC_ALL, "")

    with CursesDrawer() as drawer:
        drawGarfieldImage(drawer)

        # Now for the text bubble overlay...
        overlay = getSnarkyBubbleText(msg)
        drawTextOverlay(drawer, overlay)
        
        # Now wait
        os.system('read -s -n 1')
    
    
def getSnarkyBubbleText(msg=None):
    quotes = [
        "Good times are ahead!\nOr behind.\nBecause they sure aren't here.",
        "I hate Mondays.",
        "If you want to appear smarter,\nhang around someone stupider.",
        "Would you be willing to lead a \nparade in celebration of the lazy life?\nIf the answer is yes...\nyou're all wrong for lazy week.",
        "His I.Q. is so low you can't test it.\nYou have to dig for it."
    ]

    if msg is None:
        msg = random.choice(quotes)

    msg_lines = msg.split("\n")
    longest_line = max([len(i) for i in msg_lines])


    bubble = r" /" + (u"\xaf" * (longest_line + 10)) + "\ " + "\n"

    # Add all lines but the last
    for line in msg_lines[:-1]:
        len_diff = longest_line - len(line)
        bubble += " |     " + line + (" " * len_diff) + "     |" + "\n"

    # Add the last line
    len_diff = longest_line - len(msg_lines[-1])
    bubble += " |     " + msg_lines[-1] + (" " * len_diff) + "     |" + "\n"

    bubble += "/______" + ("_" * longest_line) + "_____/"

    return bubble
    

def drawGarfieldImage(drawer):
    # Get our Garfield ascii image and draw it
    with open("garfield.txt") as garfieldFile:
        strimg = garfieldFile.read()

    drawer.drawStr(strimg, {'x': 4, 'y': 0})


def drawTextOverlay(drawer, overlay):
    screenHeight, screenWidth = drawer.getScreenHeightWidth()

    # Where the overlay should be positioned so the bottom left of the bubble lines
    #  up with Garfield's mouth
    overlay_ords = { 'x': 64, 'y': 18 }
    
    # The default overlay ords assume there is exactly 3 lines, if there's more then move the message up
    overlay_lines = len(overlay.split("\n")) 
    if overlay_lines > 3:
        overlay_ords['y'] -= overlay_lines - 3 
    
    # If the msg is clipping off to the right, move it to the left
    longest_line_length = len(max(overlay.split("\n"), key=len))
    if longest_line_length + overlay_ords['x'] > screenWidth:
        overlay_ords['x'] -= overlay_ords['x'] + longest_line_length - screenWidth
    
    # If we've pushed it too far to the left, just sit it at x=0
    if overlay_ords['x'] < 0:
        overlay_ords['x'] = 0
    
    # If the msg will is too far up, move it down
    if overlay_ords['y'] < 0:
        overlay_ords['y'] = 0
    
    drawer.drawStr(overlay, overlay_ords, curses.color_pair(2))

            

# This is just a simple wrapper to manage creating and destroying
# the curses window stuff. Best to call it using the `with` syntax. 
class CursesDrawer:
    def __init__(self):
        self.stdscr = curses.initscr()

        try:
            curses.noecho()

            curses.curs_set(0)

            curses.start_color()
            curses.use_default_colors()

            for i in range(0, curses.COLORS):
                curses.init_pair(i + 1, i, -1)

        except:
            self.finish();

    def finish(self):
        curses.echo()
        curses.endwin() 
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.finish();    
        
    def drawStr(self, txt, start_ords={'x':0,'y':0}, color=None):
        screenHeight, screenWidth = self.getScreenHeightWidth()

        imgLines = txt.split("\n")

        imageHeight = len(imgLines)
        imageWidth = max([len(i) for i in imgLines])

        # Ensure we don't print more lines than we can fit in the terminal
        for i in range(min(imageHeight + start_ords['y'], screenHeight) - start_ords['y']):
            line = imgLines[i]
            
            # Only get enough of the line so we don't draw past the edge
            line = line[:(screenWidth - start_ords['x'])].encode('utf-8')

            if color is not None:
                self.stdscr.addstr(i + start_ords['y'], start_ords['x'], line, color)
            else:
                self.stdscr.addstr(i + start_ords['y'], start_ords['x'], line)
        
        self.stdscr.refresh()
        
    def getScreenHeightWidth(self):
        return self.stdscr.getmaxyx()
        
        
        
if __name__ == "__main__":
    # Read in arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", help="message to be shown")
    args = parser.parse_args()

    # Do the showing of the message
    lamentOnTheNatureOfMondaysAndLasagne(args.message)
