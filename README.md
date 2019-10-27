# 3D Typewriter
Making a real typewriter with an old 3D printer!

## Special Thanks
OctoPrint: https://github.com/foosel/OctoPrint

hf2gcode: https://github.com/Andy1978/hf2gcode

## Demo Video

## Quick Guide
1. Setup 3D printer, Raspberry Pi and OctoPrint. 
  * Enable CORS in the API sction in OctoPrint
  * The 3D printer HAS to be connected first in OctoPrint
  * A keyboard is needed, and connected to Raspberry Pi
  * A monitor is nice to have, and connected to Raspberry Pi. The other option is having a computer SSH to Raspberry Pi.

2. Setup hf2gcode (https://github.com/Andy1978/hf2gcode) in the same Raspberry Pi
  * Should be able to run it by entering the command `./hf2gcode a`
  
3. Convert 3D printer to writing machine, video:

4. **Edit the config.py in this project**

5. Run the code `python3 3d_typewriter.py`
