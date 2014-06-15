"""reads integers from two different files and provides statitical analysis"""

import sys
import os.path
import fileinput
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

def boxplot(sample1, sample2, filename="boxplot.png"):
    """creates a boxplot from 2 samples"""

    vect1 = robjects.IntVector(sample1)
    vect2 = robjects.IntVector(sample2)

    grdevices = importr('grDevices')
    grdevices.png(file=filename)

    rboxplot = robjects.r['boxplot']

    rboxplot(vect1, vect2, main="Boxplot", names=["Sample 1", "Sample 2"])

    grdevices.dev_off()

    print("image saved to '{}'".format(filename))

def correlation(sample1, sample2, filename="correlation.png"):
    """plots the correlation between two samples"""

    vect1 = robjects.IntVector(sample1)
    vect2 = robjects.IntVector(sample2)

    grdevices = importr('grDevices')
    grdevices.png(file=filename)

    rcor = robjects.r['cor']
    rplot = robjects.r['plot']
    rabline = robjects.r['abline']
    rlm = robjects.r['lm']

    robjects.globalenv["vect1"] = vect1
    robjects.globalenv["vect2"] = vect2

    cor = str(rcor(vect1, vect2)[0])

    rplot(vect1, vect2, main="Correlation: " + cor, xlab="Sample 1", ylab="Sample 2")
    rabline(rlm("vect2 ~ vect1"), col="red", lwd=2)

    grdevices.dev_off()

    print("image saved to '{}'".format(filename))

def sample_test():
    print("sample_test")

def deciles():
    print("deciles")

def differences(sample1, sample2, filename="differences.png"):
    """creates a boxplot of the differences between two samples"""

    if len(sample1) != len(sample2):
        print("samples are not of same length")
        return

    diff = []
    for i in range(0, len(sample1)):
        diff.append(sample1[i] - sample2[i])

    vect = robjects.IntVector(diff)

    grdevices = importr('grDevices')
    grdevices.png(file=filename)

    rboxplot = robjects.r['boxplot']

    rboxplot(vect, main="Differences")

    grdevices.dev_off()

    print("image saved to '{}'".format(filename))

options = {
    1: boxplot,
    2: correlation,
    3: sample_test,
    4: deciles,
    5: differences
}

def choose_option():
    for number, func in options.items():
        print("{}: {}".format(number, func.__name__))

    print("0: exit")

    try:
        option = int(input())
        return option
    except ValueError:
        print("invalid character")
        print()
        return choose_option()

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: statistics.py file1 file2")

    if not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
        sys.exit("Not a valid file")

    sample1 = []
    sample2 = []

    with fileinput.input(sys.argv[1]) as file1:
        for line in file1:
            sample1.append(int(line))

    with fileinput.input(sys.argv[2]) as file2:
        for line in file2:
            sample2.append(int(line))

    print("2 samples read")
    print("sample 1: {} values".format(len(sample1)))
    print("sample 2: {} values".format(len(sample2)))
    print()

    print("please choose:")

    option = choose_option()

    while option != 0:
        try:
            options[option](sample1, sample2)
        except KeyError:
            print("invalid option")

        print()
        option = choose_option()

if __name__ == '__main__':
    main()
