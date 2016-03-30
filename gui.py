import Tkinter as tk
import threading

from drumma import *


class DrumButton(object):
    def __init__(self, win, loop, grid=(0,0)):
        self.win = win
        self.state = False
        self.track = grid[0]
        self.position = grid[1]

        self.loop = loop

        # TODO this logic should be decoupled with application logic
        self.b = tk.Button(win, width=1, height=2, command=self.switch)
        self.b.grid(row=grid[0], column=grid[1])
        self.b.config(bg="white")

    def switch(self):
        if self.state:
            self.state = False
            self.b.config(bg="white")
        else:
            self.state = True
            self.b.config(bg="red")
        self.loop.tracks[self.track].switch(self.position)


if __name__ == "__main__":

    win = tk.Tk()

    snare = Track('samples/Hip-Hop-Snare-1.wav')
    kick  = Track('samples/Dry-Kick.wav')
    hat   = Track('samples/Closed-Hi-Hat-1.wav')
    loop = Loop(time_quant=250, tracks=[snare, kick, hat])
    threading.Thread(target=loop.loop, args=()).start()

    for i in range(3):
        for j in range(16):
            DrumButton(win, loop, grid=(i,j))

    def close():
        loop.stop_loop()
        win.destroy()

    win.protocol('WM_DELETE_WINDOW', close)
    win.mainloop()
