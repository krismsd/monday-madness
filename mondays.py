import curses
import time
import random
import locale


def lamentOnTheNatureOfMondaysAndLasagne():
    pass
    

def drawGarfieldImage():
    pass
    

def drawTextBubble():
    pass


def drawStr(stdscr, txt, start_ords={'x':0,'y':0}, color=None):
    screenHeight, screenWidth = stdscr.getmaxyx()

    imgLines = txt.split("\n")

    imageHeight = len(imgLines)
    imageWidth = max([len(i) for i in imgLines])

    # Ensure we don't print more lines than we can fit in the terminal
    for i in range(min(imageHeight + start_ords['y'], screenHeight) - start_ords['y']):
        line = imgLines[i]
        
        # Only get enough of the line so we don't draw past the edge
        line = line[:(screenWidth - start_ords['x'])].encode('utf-8')

        if color is not None:
            stdscr.addstr(i + start_ords['y'], start_ords['x'], line, color)
        else:
            stdscr.addstr(i + start_ords['y'], start_ords['x'], line)
            



# Set locale - solves unicode issues
locale.setlocale(locale.LC_ALL,"")


# Get our Garfield ascii image
with open("garfield.txt") as garfieldFile:
    strimg = garfieldFile.read()


# Where the overlay should be positioned so the bottom left of the bubble lines
#  up with Garfield's mouth
base_overlay_ords = { 'x': 64, 'y': 18 }

quotes = [
    "MOAR LASAGNE!",
    "*sigh* mondays...",
    "sfgtdsegfuasrhgisudfghsiodufg\nhsyud\n\n\n\n\n\nfgasuydgfausydfgsuadyfgusadyghauhefiuhfiuehfwieufhwiuehfwfuadergergertg erg erge rge rg\n\ne rger ger g ergergergsfgusadfgsiaufgs,\n\n\n\n\n\n\nfuswagdfiuysgafusyfdgydf saghudsfhg sudyfhg sduifhgs iudfg\n sufigashgdiufasdf",
    "Mondays monkey works\nfor the weekends"
]

msg = random.choice(quotes)
# msg = quotes[2]

msg_lines = msg.split("\n")
longest_line = max([len(i) for i in msg_lines])


bubble = r" /" + (u"\xaf" * (longest_line + 10)) + "\ " + "\n"

# Add all lines but the last
for line in msg_lines[:-1]:
    len_diff = longest_line - len(line)
    bubble += " |     " + line + (" " * len_diff) + "     |" + "\n"
    
    # Each line pushes the bottom of the bubble down so move it up
    base_overlay_ords['y'] -= 1

# Add the last line
len_diff = longest_line - len(msg_lines[-1])
bubble += " |     " + msg_lines[-1] + (" " * len_diff) + "     |" + "\n"

bubble += "/______" + ("_" * longest_line) + "_____/"


overlay = bubble











stdscr = curses.initscr()
try:
    curses.noecho()

    curses.start_color()
    curses.use_default_colors()


    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    screenHeight, screenWidth = stdscr.getmaxyx()

    # Draw the Garfield image
    drawStr(stdscr, strimg, {'x': 4, 'y': 0})

    # Now for the text bubble overlay...
    # Calc the coordinates of where we should display it
    overlay_ords = base_overlay_ords;
    
    # If the msg is clipping off to the right, move it to the left
    longest_line_length = len(max(overlay.split("\n"), key=len))
    if longest_line_length + overlay_ords['x'] > screenWidth:
        overlay_ords['x'] -= overlay_ords['x'] + longest_line_length - screenWidth
    
    # If we've pushed it too far to the left, just sit it at x=0
    if overlay_ords['x'] < 0:
        overlay_ords['x'] = 0
        # exit("Couldn't fit message in terminal, no lasagne for u :(")
    
    # If the msg will is too far up, move it down
    if overlay_ords['y'] < 0:
        overlay_ords['y'] = 0
    
    # and draw it
    drawStr(stdscr, overlay, overlay_ords, curses.color_pair(2))

    stdscr.refresh()

    time.sleep(25)

finally:
    curses.echo()
    curses.endwin()
