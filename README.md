# RasPiMorseCode
Simple script to output text as Morse Code on Raspberry Pi LEDs
* Dot speed = 0.15 seconds, can be changed in `code.py`
    * Dash = 3 dots
    * Space between ticks = 1 dot
    * Space between characters = 3 dots
    * Space (or unrecognized character) 7 dots
* Alternates LEDs on each character
* Restores to default Raspberry Pi LED behavior
* Does not work by default on Raspberry Pi Zero as it only has one LED--delete all references to LED1 for Zero.

## Usage
* `python code.py as much text as you'd like`