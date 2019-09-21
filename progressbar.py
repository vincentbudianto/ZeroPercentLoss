import time

def printProgressBar (progress, total, decimals = 0, char = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (progress / float(total)))
    x = int(progress * 100 // total)
    bar = char * x + '-' * (100 - x)

    print('\rProgress: |%s| %s%%' % (bar, percent), end = '\r')

    if (progress == total):
        print('\nLoading completed', end = '\n')

checksum = list(range(0, 51))
l = len(checksum)

printProgressBar(0, l)
for i, item in enumerate(checksum):
    time.sleep(0.1)
    printProgressBar(i + 1, l)