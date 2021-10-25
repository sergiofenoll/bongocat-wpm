import pyglet
import pyglet.gl as gl
import time
from queue import Queue
from threading import Thread
from pynput import keyboard

window = pyglet.window.Window(1200, 1200)
gl.glClearColor(1, 1, 1, 1)
bongo_cat_up = pyglet.resource.image("assets/bongo_cat.png")
bongo_cat_down = pyglet.resource.image("assets/bongo_cat_down.png")
label = pyglet.text.Label(
    f"WPM: {0:03d}",
    x=window.width // 2,
    y=(window.height - bongo_cat_up.height) // 2,
    anchor_x="center",
    anchor_y="center",
    color=(0, 0, 0, 255),
)

start = time.time()
last_time = start
count = 0
wpm = 0
draw_up = True

def calculate_wpm():
    global wpm
    global count
    elapsed = time.time() - start
    wpm = ((count / 5) / elapsed) * 60

    global draw_up
    draw_up = False
    def set_draw_up_true(dt=None):
        global draw_up
        draw_up = True
    pyglet.clock.schedule_once(set_draw_up_true, 1 / 10.0)

def write_wpm(dt):
    label.text = f"WPM: {round(wpm):03d}"


pyglet.clock.schedule_interval(write_wpm, 1 / 30.0)


def on_press(key):
    if isinstance(key, keyboard.KeyCode):
        print(key)
        global count
        global last_time
        now = time.time()
        last_time = now
        if now >= last_time + 10:
            count = 0
            start = now

        count += 1
        calculate_wpm()


@window.event
def on_draw():
    window.clear()
    if (draw_up):
        bongo_cat_up.blit((window.width - bongo_cat_up.width) // 2, (window.height - bongo_cat_up.height) // 2)
    else:
        bongo_cat_down.blit((window.width - bongo_cat_up.width) // 2, (window.height - bongo_cat_up.height) // 2) 
    label.draw()


@window.event
def on_close():
    listener.stop()


listener = keyboard.Listener(on_press=on_press)
listener.start()
pyglet.app.run()
