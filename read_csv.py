
import sys
import csv
from tkinter.messagebox import NO

def ReadCSV_out_performance_accuracy(fn):
    names = []
    performances = []
    accuray = []

    with open(fn, newline='') as f:
        reader = csv.reader(f)
        idx = -1
        try:
            for row in reader:
                idx += 1

                # print(row)
                if idx == 0:
                    print("Ignore title of CSV.")
                else:
                    names.append(row[0])
                    performances.append(row[6])
                    accuray.append(row[16])
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(fn, reader.line_num, e))
    
    return names, performances, accuray