from flask import Flask, render_template, redirect, request
import string
import signal
import sys
from threading import Thread

import control

app = Flask(__name__)

current_function = None
controller = control.Control()
control_thread = None


@app.route('/')
def index():
    return render_template('index.html', function=current_function)


@app.route('/white', methods=['GET'])
def white():

    # Set function
    global current_function
    current_function = "White"

    # Execute function
    global control_thread
    if control_thread:
        controller.running = False
        control_thread.join(0.1)
        controller.running = True

    control_thread = Thread(target=controller.color, args=(255, 255, 255))
    control_thread.start()

    return redirect('/', code=302)


@app.route('/color_temp', methods=['GET'])
def color_temp():

    # Get and parse data
    temp = str(request.args['color_temp'])
    if temp.isdigit() and 500 <= int(temp) <= 20000:
        temp = int(temp)
    else:
        temp = 5500

    # Set function
    global current_function
    current_function = "Color Temperature {}".format(temp)

    # Execute function
    global control_thread
    if control_thread:
        controller.running = False
        control_thread.join(0.1)
        controller.running = True

    control_thread = Thread(target=controller.color_temp, args=(temp,))
    control_thread.start()

    return redirect('/', code=302)


@app.route('/color', methods=['GET'])
def color():

    # Get and parse data
    rgb = str(request.args['color']).lstrip('#')

    if len(rgb) == 6 and all(c in string.hexdigits for c in rgb):
        rgb = tuple(int(rgb[i:i + 2], 16) for i in (0, 2, 4))
    else:
        rgb = (255, 255, 255)

    # Set function
    global current_function
    current_function = "RGB Color ({}, {}, {})".format(*rgb)

    # Execute function
    global control_thread
    if control_thread:
        controller.running = False
        control_thread.join(0.1)
        controller.running = True

    control_thread = Thread(target=controller.color, args=rgb)
    control_thread.start()

    return redirect('/', code=302)


@app.route('/rainbow', methods=['GET'])
def rainbow():

    # Set function
    global current_function
    current_function = "Rainbow"

    # Execute function
    global control_thread
    if control_thread:
        controller.running = False
        control_thread.join(0.1)
        controller.running = True

    control_thread = Thread(target=controller.rainbow)
    control_thread.start()

    return redirect('/', code=302)


@app.route('/rainbow_onecolor', methods=['GET'])
def rainbow_onecolor():

    # Set function
    global current_function
    current_function = "Rainbow with single color"

    # Execute function
    global control_thread
    if control_thread:
        controller.running = False
        control_thread.join(0.1)
        controller.running = True

    control_thread = Thread(target=controller.rainbow_onecolor)
    control_thread.start()

    return redirect('/', code=302)


def signal_handler(signal, frame):
    print('Exiting...')
    if control_thread:
        controller.running = False
        control_thread.join(0.1)

    sys.exit(0)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)

    app.debug = False
    app.run(host='0.0.0.0', port=80)



