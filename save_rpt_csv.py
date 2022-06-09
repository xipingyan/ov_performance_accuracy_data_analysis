
import sys
import csv
from tkinter.messagebox import NO

# Save analysis result
# sv_fn: save name
# names, performances, accuracys: Read data from 4 input csv file
# gom_val1, gom_val2: GOMean result
# match_idx: accuracy match id
# big_diff_idx: index list with big diff FPS.
def SaveReportCSV(sv_fn, names, performances, accuracys,
    gom_1, gom_2, gom_diff,
    match_idx,
    big_diff_val, big_diff_percent):

    with open(sv_fn, 'w', newline='') as f: 
        writer = csv.writer(f)

        # GOMean
        if len(names) == 2:
            data = [["GOM", str(gom_diff)]]
        else:
            data = [["Original GOM", str(gom_1)], ["New GOM", str(gom_2)], ["GOM diff", str(gom_diff)]]
        writer.writerows(data)
        
        # Accuracy
        WriteAccuracy(writer, accuracys, match_idx, names)

        # Performance
        WritePerformance(writer, performances, big_diff_val, big_diff_percent, names)

def WritePerformanceTopN(writer, performances, big_diff_val, big_diff_percent, names, li, topN, ascending, desc):
    writer.writerow([])
    writer.writerow(desc)
    li.sort(reverse=ascending)

    if len(performances) == 2:
        writer.writerow(["original id", "network name", "performance1", "performance2", "val_diff", "%_diff"])
    else:
        writer.writerow(["original id", "network name", "performance1", "performance2", "performance3", "performance4", "val_diff", "%_diff"])
    for i in range(min(len(li), topN)):
        idx = li[i][1]
        val = li[i][0]
        if len(performances) == 2:
            writer.writerow([idx, names[0][idx], performances[0][idx], performances[1][idx], big_diff_val[idx], big_diff_percent[idx]*100.0])
        else:
            writer.writerow([idx, names[0][idx], performances[0][idx], performances[1][idx], performances[2][idx], performances[3][idx], big_diff_val[idx], big_diff_percent[idx]*100.0])

def WritePerformance(writer, performances, big_diff_val, big_diff_percent, names):
    writer.writerow(["Performance diff:"])

    # Sort with diff val
    li = []
    for i in range(len(big_diff_val)):
        li.append([big_diff_val[i], i])

    # desc = ["Sort diff val", "big -> small"]
    # WritePerformanceTopN(writer, performances, big_diff_val, big_diff_percent, names, li, 10, 1, desc)
    # desc = ["Sort diff val", "small -> big"]
    # WritePerformanceTopN(writer, performances, big_diff_val, big_diff_percent, names, li, 10, 0, desc)
    
    # Sort with diff val
    li = []
    for i in range(len(big_diff_percent)):
        li.append([big_diff_percent[i], i])

    desc = ["Sort diff percent", "big -> small"]
    WritePerformanceTopN(writer, performances, big_diff_val, big_diff_percent, names, li, 10, 1, desc)
    desc = ["Sort diff percent", "small -> big"]
    WritePerformanceTopN(writer, performances, big_diff_val, big_diff_percent, names, li, 10, 0, desc)

def WriteAccuracy(writer, accuracys, match_idx, names):
    writer.writerow([])
    writer.writerow(["Accuracy diff"])
    if len(accuracys) == 2:
        writer.writerow(["original id", "network name", "accuracy1", "accuracy2"])
        for i in range(len(match_idx)):
            if match_idx[i] == 0:
                writer.writerow([i, names[0][i], accuracys[0][i], accuracys[1][i]])
    else:    
        writer.writerow(["original id", "network name", "accuracy1", "accuracy2", "accuracy3", "accuracy4"])
        for i in range(len(match_idx)):
            if match_idx[i] == 0:
                writer.writerow([i, names[0][i], 
                    accuracys[0][i], accuracys[1][i], accuracys[2][i], accuracys[3][i]])


    