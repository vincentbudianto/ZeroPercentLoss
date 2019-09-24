import time
import sys

class ProgressBar:
    def __init__(self, bar_length):
        self.bar_length = bar_length

    def display_progress_bar(self, caption, progress, total):
        percent = 100.0*i/total
        current_bar_num = int(i / total * self.bar_length)

        sys.stdout.write('\r') #prevent output from being appended at the end

        sys.stdout.write("{} : [{:<{}}] {:<3}%"
                        .format(caption, '='*current_bar_num,
                                self.bar_length, int(percent)))
        sys.stdout.flush()

if __name__ == "__main__":
    total = 1000
    progressBar = ProgressBar(30)

    for i in range(total+1):
        caption = "File_1"
        progressBar.display_progress_bar(caption, i, total)
        time.sleep(0.002)
    print()