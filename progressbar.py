import time

def printProgressBar (progress, total, decimals = 0, length = 100, char = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (progress / float(total)))
    x = int(length * progress // total)
    bar = char * x + '-' * (length - x)

    print('\rProgress: | %s | %s%%' % (bar, percent), end = '\r')

    if (progress == total):
        print('\nLoading completed', end = '\n')