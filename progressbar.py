import random
import sys
import time

class ProgressBar:
    def __init__(self, max_length):
        self.max_length = max_length
        self.total = None
        self.start_time = None
        self.finish_time = None

    def set_total(self, total):
        self.total = total

    def printProgressBar (self, progress, filename, decimals = 0, char = '█'):
        if (not self.start_time):
            self.start_time = time.time()
        current_time = time.time() - self.start_time

        remaining_time = current_time * ((self.total/progress)-1)

        percent = ("{0:." + str(decimals) + "f}").format(100 * (progress / float(self.total)))
        x = int(progress * 50 // self.total)
        bar = char * x + '-' * (50 - x)

        print('\rProgress: |{}| {:>3}% Remaining time: {:>5.1f}s'.format(bar, percent, remaining_time), end="\r")

        if (progress == self.total):
            self.finish_time = time.time()
            print('\nElapsed time: {}s\n'.format(self.finish_time-self.start_time))
            print('<<<     %s completed     >>>\n' % filename)
            self.start_time = None

    def print_progress_bar (self, progress, filename, decimals = 0, char = '█'):
        if (not self.start_time) :
            self.start_time = time.time()
        current_time = time.time() - self.start_time

        remaining_time = current_time * ((100/progress)-1)

        percent = ("{0:." + str(decimals) + "f}").format(progress)

        x = int(progress/100 * 50)
        bar = char * x + '-' * (50 - x)

        print ('{y:<{x}} : |{}| {:>3}% Remaining time: {:>5.1f}s'.format(bar, percent, remaining_time, y=filename, x=self.max_length))

        if (progress == self.total):
            self.finish_time = time.time()
            print('\nElapsed time: {}s\n'.format(self.finish_time-self.start_time))
            print('<<<     %s completed     >>>\n' % filename)
            self.start_time = None