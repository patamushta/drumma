import pygame

pygame.mixer.pre_init(44100, -16, 2, 256)  # adjust last parameter(buffer) if needed
pygame.init()

class Track(object):
    """
    One track object. 
    Contains filename of wav sample, sequence of play/noplay time quants,
    volume etc
    """
    def __init__(self, filename, sequence=[]):
        self.set_filename(filename)

        self.sequence = sequence 

    def set_filename(self, filename):
        self._filename = filename
        self.sound = pygame.mixer.Sound(filename) # TODO what if no such file,
                                                  # log & error message in GUI

    def set_volume(self, volume):
        """ Volume lies in [0..1], 1 by default """
        self.sound.set_volume(volume)

    def switch(self, position):
        self.sequence[position] = int(not self.sequence[position])


class Loop(object):
    def __init__(self, time_quant=1000, num_beats=16, tracks=[]):
        # TODO use beats per minute to calculate time_quant
        self.tracks = tracks 
        self.time_quant = time_quant
        self.num_beats = num_beats
        # align track sequences to num_beats: 
        for track in self.tracks:
            track.sequence += [0] * num_beats
            track.sequence = track.sequence[:num_beats]

        self.play = True

    def stop_loop(self):
        self.play = False



    def loop(self):
        while True:
            for i in range(self.num_beats):
                for track in self.tracks:
                    if track.sequence[i]:
                        track.sound.play()

                if not self.play:
                    return

                pygame.time.delay(self.time_quant)
    # TODO clock events to synchronize different loops, gui ets
    # ala clock = pygame.time.Clock()


if __name__ == '__main__':
    # test
    snare = Track('samples/Hip-Hop-Snare-1.wav')
    snare.sequence = [0,0,1,0] * 4

    kick  = Track('samples/Dry-Kick.wav')
    kick.sequence = [1,0,0,0,0,1,0,0] + [1,0,0,1] + [0, 1, 0, 0] # * 2# + [1,1,0,0]

    hat   = Track('samples/Closed-Hi-Hat-1.wav')
    hat.sequence = [0,1] * 6 + [1] * 4 

    time_quant = 250

    loop = Loop(time_quant=time_quant, tracks=[snare, kick, hat])
    loop.loop()

