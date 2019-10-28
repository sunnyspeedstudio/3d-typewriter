import config
import requests
import readchar
import subprocess
import json


# global
# start point of the pen
pen_x = config.paper['start_x'] + config.paper['margin']
pen_y = config.paper['start_y'] - config.paper['margin']
# find the most right and most bottom of a char, so that the pen can move to the next position
ch_most_right = pen_x
ch_most_bottom = pen_y
# end point of the pen
max_x = config.paper['start_x'] + config.paper['width'] - config.paper['margin']
max_y = config.paper['start_y'] - config.paper['height'] + config.paper['margin']
# TODO: handle when pen reaches to the bottom of the page


def print_char(ch):
    #1. convert char to gcode using "hf2gcode"
    # thanks to https://github.com/Andy1978/hf2gcode
    post_json_data = char_to_gcode(ch)

    #2. send gcode to machine, and print using "octoprint"
    # thanks to https://github.com/foosel/OctoPrint
    post_url = 'http://' + config.octoprint['link_ip'] + ':' + str(config.octoprint['link_port']) + '/api/printer/command'
    post_headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': config.octoprint['api_key']
    }

    result = requests.post(post_url, json = post_json_data, headers = post_headers)

    if config.setting['debug']:
        print("post response = " + result.text)


def char_to_gcode(ch):
    global pen_x
    global pen_y
    global ch_most_right
    global ch_most_bottom
    global max_x
    global max_y

    # get the gcode from user input
    if ch == '\r':
        # when press ENTER
        # new line
        pen_x = config.paper['start_x']
        pen_y = ch_most_bottom - config.paper['line_spacing']
        # reset
        ch_most_right = pen_x
        ch_most_bottom = pen_y
        gcode = '{"commands": ["G0 X' + str(pen_x) + ' Y' + str(pen_y) + '"]}'
    elif ch == ' ':
        # when press SPACE
        if pen_x >= max_x:    # handle the pen reaches to the right side of the paper
            # new line
            pen_x = config.paper['start_x']
            pen_y = ch_most_bottom - config.paper['line_spacing']
            # reset
            ch_most_right = pen_x
            ch_most_bottom = pen_y
        else:
            # move a space forward
            pen_x += config.paper['word_spacing']
        gcode = '{"commands": ["G0 X' + str(pen_x) + ' Y' + str(pen_y) + '"]}'
    else:
        # when press other keys
        # calling hf2gcode
        result = subprocess.run([
                config.setting['hf2gcode_path'],
                ch,
                "--xoffset=" + str(pen_x),
                "--yoffset= " + str(pen_y),
                "--scale=" + str(config.paper['font_size']),
                "--min-gcode",
                "--z-down=-" + str(config.paper['pen_lift']),
                "--z-up=" + str(config.paper['pen_lift']),
                "--font=" + config.paper['font']
            ],
            universal_newlines = True, stdout = subprocess.PIPE)

        if config.setting['debug']:
            print("hf2gcode stdout = " + str(result.stdout))

        # format the gcode result to json, so that we can make api call to octoprint
        lines = result.stdout.splitlines()
        gcode = '{"commands": ['
        for line in lines:
            if line.startswith('G'):
                gcode += '"' + line + ' F' + str(config.paper['speed']) + '", '
        gcode += '""]}'

        # find ch_most_right and ch_most_bottom
        find_ch_most_position(lines)

        # move the pen to the next position
        pen_x = ch_most_right + config.paper['ch_spacing']
        if pen_x >= max_x:
            # new line
            pen_x = config.paper['start_x']
            pen_y = ch_most_bottom - config.paper['line_spacing']
            # reset
            ch_most_right = pen_x
            ch_most_bottom = pen_y
            gcode = '{"commands": ["G0 X' + str(pen_x) + ' Y' + str(pen_y) + '"]}'

    if config.setting['debug']:
        print("hf2gcode = " + gcode)

    # convert string to json
    gcode_json = json.loads(gcode)

    return gcode_json


def find_ch_most_position(lines):
    global ch_most_right
    global ch_most_bottom
    x = 0.0
    y = 0.0

    for line in lines:
        i_x = line.find('X') + 1
        i_y = line.find('Y') + 1
        if i_x > 0 and i_y > 0:
            # both X and Y
            i_y -= 2
            x = float(line[i_x:i_y])
            i_y += 2
            y = float(line[i_y:])
            if ch_most_right < x:
                ch_most_right = x
            if ch_most_bottom > y:
                ch_most_bottom = y
        elif i_x > 0:
            # only X
            x = float(line[i_x:])
            if ch_most_right < x:
                ch_most_right = x
        elif i_y > 0:
            # only Y
            y = float(line[i_y:])
            if ch_most_bottom > y:
                ch_most_bottom = y
        if config.setting['debug']:
            print("x  = " + str(x) + " y = " + str(y))
    if config.setting['debug']:
        print("ch_most_right  = " + str(ch_most_right) + " ch_most_bottom = " + str(ch_most_bottom))


print("Start typing")

while True:
    ch = readchar.readchar()

    if config.setting['debug']:
        print("you pressed = " + ch)

    # quit it when press Esc
    if ch == '\x1b':
        quit()

    print_char(ch)
