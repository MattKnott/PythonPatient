import signal
import RPi.GPIO as GPIO

from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto

#Initialise Display

try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


#inky_display.set_rotation(180)
try:
    inky_display.set_border(inky_display.RED)
except NotImplementedError:
    pass

# Figure out scaling for display size

scale_size = 1.0
padding = 0

if inky_display.resolution == (400, 300):
    scale_size = 2.20
    padding = 15

if inky_display.resolution == (600, 448):
    scale_size = 2.20
    padding = 30

# Create a new canvas to draw on

img = Image.new("P", inky_display.resolution, inky_display.WHITE)
draw = ImageDraw.Draw(img)

name = "Matthew Knott"
# Load the fonts

hanken_medbold_font = ImageFont.truetype(HankenGroteskBold, int(12 * scale_size))
hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(16 * scale_size))
hanken_medium_font = ImageFont.truetype(HankenGroteskBold, int(8 * scale_size))

y_top = int(inky_display.height * (5.0 / 10.0))
y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))


# Calculate the positioning and draw the "Hello" text

hello_w, hello_h = hanken_bold_font.getsize("Knott, Matthew A")
hello_x = 5
hello_y = 5
draw.text((hello_x, hello_y), "Knott, Matthew A", inky_display.BLACK, font=hanken_bold_font)

# Calculate the positioning and draw the "my name is" text

mynameis_w, mynameis_h = hanken_medium_font.getsize("DOB: 05/08/1981   AGE: 39   SEX: M")
mynameis_x = 5
mynameis_y = hello_h + 5
draw.text((mynameis_x, mynameis_y), "DOB: 05/08/1981   AGE: 39   SEX: M", inky_display.BLACK, font=hanken_medium_font)

#Add Line
demographics_bottom = (mynameis_y + mynameis_h + 5)
demographics_line_end = (mynameis_y + mynameis_h + 8)

for y in range(demographics_bottom, demographics_line_end):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.RED)


def generatePageTitle(titleText):
    pagetitle_w, pagetitle_h = hanken_medbold_font.getsize(titleText)
    pagetitle_x = 5
    pagetitle_y = demographics_line_end + 5
    draw.text((pagetitle_x, pagetitle_y), titleText, inky_display.BLACK, font=hanken_medbold_font)

def generateIndexItem(indexText, yPos):
    index1_w, index1_h = hanken_medium_font.getsize(indexText)
    index1_x = 5
    index1_y = yPos
    draw.text((index1_x, index1_y), indexText, inky_display.BLACK, font=hanken_medium_font)
    return (yPos+index1_h)

#Create landing page 
generatePageTitle("Patient Summary")

index1Pos = generateIndexItem("1: Admission Details",demographics_line_end + 35)
index2Pos = generateIndexItem("2: Risk Assessments",index1Pos + 5)
index3Pos = generateIndexItem("3: Contact Details",index2Pos + 5)



# Display the completed name badge
inky_display.set_image(img)
inky_display.show()






# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]
LABELS = ['A', 'B', 'C', 'D']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
    if pin == 5:
        show_thing()

    if pin == 6:
        show_thing2()



# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)




def show_thing():
    print("PAGE FORWARDS")
    #Add Line

    for y in range((demographics_line_end + 1), inky_display.height):
        for x in range(0, inky_display.width):
            img.putpixel((x, y), inky_display.WHITE)

    
    generatePageTitle("Admission Details")

    inky_display.set_image(img)
    inky_display.show()

def show_thing2():
    print("PAGE BACKWARDS")
    #Add Line

    for y in range((demographics_line_end + 1), inky_display.height):
        for x in range(0, inky_display.width):
            img.putpixel((x, y), inky_display.WHITE)

    generatePageTitle("Risk Assessments")
    
    inky_display.set_image(img)
    inky_display.show()




# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()