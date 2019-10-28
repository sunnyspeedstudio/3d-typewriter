octoprint = {
    'api_key': '84B7FCF8A62B4D7F90D6F3FCCDE7FC94',    # api key can be found in OctoPrint API setting page
    'link_ip': '192.168.1.135',                       # the ip to OctoPrint
    'link_port': 80
}

setting = {
    'debug': False,                                         # print debug info or not
    'hf2gcode_path': '/home/pi/dev/hf2gcode/src/hf2gcode'   # full path to installed hf2gcode
}

# all unit is in mm
paper = {
    'width': 185,         # writing area
    'height': 110,
    'start_x': -21,       # start point, from the top left of the paper
    'start_y': 191,
    'margin': 10,         # the paper margin, 4 sides (top, bottom, left and right)
    'ch_spacing': 0.1,    # the space between character in a world
    'line_spacing': 5,    # the space between lines
    'word_spacing': 4,    # the space between words, ie, when you press the SPACE key
    'font_size': 0.3,     # font size
    'pen_lift': 2,        # how high the pen lift
    'font': 'rowmans',    # possible selections from hf2gcode: cursive, futural, futuram, gothgbt, gothgrt, gothiceng, gothicger, gothicita, gothitt, greekc, greek, greeks, rowmand, rowmans, rowmant, scriptc, scripts, symbolic, timesg, timesib, timesi, timesrb, timesr
    'speed': 6000
}