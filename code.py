from sys import argv
from json import load
from subprocess import Popen, call, PIPE
from time import sleep
from os.path import dirname, realpath

JSON_FILE_PATH = dirname(realpath(__file__)) + "/code.json"
LED_PATH = "/sys/class/leds/led"
DOT_SPEED = 0.15


def write_to_file(val, file):
    devnull = open("/dev/null", 'w')
    tmp = Popen(["echo", val], stdout = PIPE)
    call(["sudo", "tee", file], stdin = tmp.stdout, stdout = devnull)
    return

if len(argv) <= 1 or argv[1] == "-h" or argv[1] == "--help":
    
    print "This script converts text to morse code that is blinked out by the LEDs on your Raspberry Pi."
    print "The LED will switch with each character."
    print "Enter some text after the filename!"
    
else:
    
    # set LEDs to gpio mode and turn off for a space's length
    write_to_file("gpio", LED_PATH + "0" + "/trigger")
    write_to_file("0", LED_PATH + "0" + "/brightness")
    write_to_file("gpio", LED_PATH + "1" + "/trigger")
    write_to_file("0", LED_PATH + "1" + "/brightness")
    sleep(DOT_SPEED * 7)
    
    i = 1
    text = ""
    
    # combine all argv into one string
    while i < len(argv):
        text += argv[i] + " "
        i += 1
        
    # parse charcters as Morse
    led = "0"
    code = load(open(JSON_FILE_PATH))
    for x in text:
        try:
            for y in code[x.lower()]:
                write_to_file("1", LED_PATH + led + "/brightness")
                if y == ".":
                    sleep(DOT_SPEED)
                else:
                    sleep(DOT_SPEED * 3)
                # silence for one tick between characters
                write_to_file("0", LED_PATH + led + "/brightness")
                sleep(DOT_SPEED)
            if led == "0":
                led = "1"
            else:
                led = "0"
        except:
            # char not found, insert a space
            # silence for 7 ticks total (4 + 1 from char before + 2 for between chars)
            write_to_file("0", LED_PATH + led + "/brightness")
            sleep(DOT_SPEED * 4)
        # silence for three ticks between characters (2 + 1 from after character)
        write_to_file("0", LED_PATH + led + "/brightness")
        sleep(DOT_SPEED * 2)
            
# reset to default LED behavior
write_to_file("mmc0", LED_PATH + "0" + "/trigger")
write_to_file("input", LED_PATH + "1" + "/trigger")