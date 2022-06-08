
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
    gom_val1, gom_val2,
    match_idx,
    big_diff_idx):

    with open(sv_fn, 'w', newline='') as f: 
        writer = csv.writer(f)

        # GOMean
        data = [["Original GOM", str(gom_val1)], ["New GOM", str(gom_val2)]]
        writer.writerows(data)

        # Performance
        writer.writerow([])
        writer.writerow(["Performance diff"])
        writer.writerow(["original id", "network name", "performance1", "performance2", "performance3", "performance4"])
        for i in range(len(big_diff_idx)):
            if big_diff_idx[i] == 1:
                writer.writerow([i, names[0][i], 
                    performances[0][i], performances[1][i], performances[2][i], performances[3][i]])
        
        # Accuracy
        writer.writerow([])
        writer.writerow(["Accuracy diff"])
        writer.writerow(["original id", "network name", "accuracy1", "accuracy2", "accuracy3", "accuracy4"])
        for i in range(len(match_idx)):
            if match_idx[i] == 0:
                writer.writerow([i, names[0][i], 
                    accuracys[0][i], accuracys[1][i], accuracys[2][i], accuracys[3][i]])


    