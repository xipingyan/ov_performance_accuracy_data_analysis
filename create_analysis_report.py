
#!/usr/bin/python
import math
import sys
from tokenize import group
from read_csv import ReadCSV_out_performance_accuracy as ReadCSV
from save_rpt_csv import SaveReportCSV

# Parse input param
# Only support 2 or 4 param input.
def ParseArgs():
    # Default 4 param
    old_files = ["../1_test-dlbenchmark-cpu_dlbenchmark_public_22ee17fd_ubuntu20.04/out_performance_accuracy.csv",
            "../2_test-dlbenchmark-cpu_dlbenchmark_i9-9900k_public_22ee17fd_ubuntu20.04/out_performance_accuracy.csv"]
    new_files = ["../1_test-dlbenchmark-cpu_public_93e2be1d_ubuntu20.04/out_performance_accuracy.csv",
            "../2_test-dlbenchmark-cpu_public_93e2be1d_ubuntu20.04/out_performance_accuracy.csv"]
  
    print("Argv number =", len(sys.argv))
    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print("Usage: support 2 or 4 param")
        print("  $./create_analysis_report.py old_csv new_csv")
        print("  $./create_analysis_report.py old_csv1 old_csv2 new_csv1 new_csv2")
        sys.exit(0)
    if len(sys.argv) == 3:
        old_files=[str(sys.argv[1])];
        new_files=[str(sys.argv[2])];
    elif len(sys.argv) == 5:
        old_files=[str(sys.argv[1]), str(sys.argv[2])];
        new_files=[str(sys.argv[3]), str(sys.argv[4])];
    else:
        print("Param error, default param will be used.")

    if len(new_files) == 1:
        print('Old CSV file:\n  {0}'.format(old_files[0]))
        print('New CSV file:\n  {0}'.format(new_files[0]))
    else:
        print('Old CSV file:\n  {0}\n  {1}'.format(old_files[0], old_files[1]))
        print('New CSV file:\n  {0}\n  {1}'.format(new_files[0], new_files[1]))
    return old_files + new_files

# Calc avaiable indexs
# 1: FPS >= 0
# 2: Accuracy status with "PASSED"
def CalcAvaiableIndex(performances, accuracys):
    if performances is None:
        print("Can't input none data.")
        return

    list_size = len(performances[0])
    avaiable_idx = [ 0 ] * list_size
    
    # Make sure all data dim same.
    for pf in performances:
        if len(pf) != list_size :
            print("Dim is not same. {} != {}".format(len(pf), list_size))
            sys.exit(0)

    # FPS >= 0 and all passed
    for i in range(len(performances[0])):
        all_avaible = 0
        all_passed = 0
        for j in range(len(performances)):
            if float(performances[j][i]) >= 0:
                all_avaible += 1
        for j in range(len(accuracys)):
            if str(accuracys[j][i]).find("PASSED") >= 0:
                all_passed += 1 

        if all_avaible == len(performances) and all_avaible == all_passed:
            avaiable_idx[i] = 1

    return avaiable_idx
    
# Calculate 2 result's GOM
# Return: GOM value and avaiable index
def CalcGOM_of_2result(performances, avaiable_idx):
    gom_val1 = 1
    gom_val2 = 1
    gom_val3 = 1
    data_2_group = len(performances) == 2
    for i in range(len(performances[0])):
        # Only statistic avaiable value
        if avaiable_idx[i] == 1:
            if data_2_group:
                performances[0][i] = float(performances[0][i])
                performances[1][i] = float(performances[1][i])
                gom_val3 = gom_val3 * performances[0][i] / performances[1][i]
            else:
                performances[0][i] = float(performances[0][i])
                performances[1][i] = float(performances[1][i])
                performances[2][i] = float(performances[2][i])
                performances[3][i] = float(performances[3][i])
                # 4 group data
                gom_val1 = gom_val1 * performances[0][i] / performances[1][i]
                gom_val2 = gom_val2 * performances[2][i] / performances[3][i]
                gom_val3 = gom_val3 * (performances[0][i] + performances[1][i]) / (performances[2][i] +  performances[3][i])
    

    # GOM: = pow((Xi * Xj * ...), 1/n)
    n = sum(avaiable_idx)
    gom_val1 = math.pow(gom_val1, 1/n)
    gom_val2 = math.pow(gom_val2, 1/n)
    gom_val3 = math.pow(gom_val3, 1/n)

    return [gom_val1, gom_val2, gom_val3]

# Compara 4 result if all passed.
# Return match item index. -1: not go to match; 0: mismatch; 1: match
def CompareAccuracy(accuracys, avaiable_idx):
    if accuracys is None:
        print("accuracys is none.")
        return

    list_size = len(accuracys[0])
    match_idx = [ 0 ] * list_size

    for i in range(list_size):
        # # Filter?
        # if avaiable_idx[i] != 1:
        #     match_idx[i] = -1
        #     continue

        Match = 0
        all_failed = 0
        all_crashed = 0
        all_passed = 0
        all_gt = 0
        all_none = 0
        for j in range(len(accuracys)):
            # GROUND_TRUTH, don't need to compare.
            if str(accuracys[j][i]).find("GROUND_TRUTH") >= 0:
                all_gt += 1
            elif str(accuracys[j][i]).find("FAILED") >= 0:
                all_failed += 1
            elif str(accuracys[j][i]).find("CRASHED") >= 0:
                all_crashed += 1
            elif str(accuracys[j][i]).find("PASSED") >= 0:
                all_passed += 1
            elif str(accuracys[j][i]).find("NONE") >= 0:
                all_none += 1
            else:
                print("Find none.")

        if all_failed == len(accuracys):     # All FAILED
            Match = -1
        elif all_crashed == len(accuracys):  # All CRASHED
            Match = -1
        elif all_passed == len(accuracys):   # All PASSED
            Match = 1
        elif all_gt > 0:                    # Ignore groundtruth
            Match = -1
        elif all_none == len(accuracys):
            Match = -1
        else:
            Match = 0

        match_idx[i] = Match
    
    return match_idx

# Find FPS with big difference.
def FindBigDiffPerformance(performances, avaiable_idx):
    group_2_data = len(performances) == 2
    list_size = len(avaiable_idx)
    big_diff_val = [ 0 ] * list_size
    for i in range(len(performances[0])):
        if group_2_data:
            big_diff_val[i] = performances[1][i] - performances[0][i]
        else:
            val1 = (float(performances[1][i]) + float(performances[0][i])) / 2.0
            val2 = (float(performances[3][i]) + float(performances[2][i])) / 2.0
            big_diff_val[i] = val2 - val1
    
    return big_diff_val

def PrintInvalidIndex(avaiable_idx, names, performances, accuracys):
    print("All invalid idx:")
    for i in range(len(avaiable_idx)):
        if avaiable_idx[i] != 1:
            print("{0:3d} {1:60s} ".format(i, names[0][i]), end = '')
            for j in range(len(performances)):
                print("{0:10s} ".format(performances[j][i]), end = '')
            for j in range(len(accuracys)):
                print("{0:14s} ".format(accuracys[j][i]), end = '')
            print("")
    print("")

def PrintDiffAccuracy(match_idx, accuracys):
    print("Display accuracy diff:")
    for i in range(len(match_idx)):
        if match_idx[i] == 0:
            print("{0:3d} ".format(i), end = '')
            for j in range(len(accuracys)):
                print("{0:10s} ".format(accuracys[j][i]), end = '')
            print("")
    print("")

def PrintDiffPerformance(big_diff_val, performances):
    print("Display performance with big diff:")
    for i in range(len(big_diff_val)):
        if big_diff_val[i] > 1:
            print("{0:3d} ".format(i), end = '')
            for j in range(len(performances)):
                print("{0:12s} ".format(str(performances[j][i])), end = '')
            print("")
    print("")

def main():
    all_files = ParseArgs()

    # Read csv file
    names = []
    performances = []
    accuracys = []
    for f in all_files:
        name, performance, accuray = ReadCSV(f)
        names.append(name)
        performances.append(performance)
        accuracys.append(accuray)

    avaiable_idx = CalcAvaiableIndex(performances, accuracys)
    # PrintInvalidIndex(avaiable_idx, names, performances, accuracys)

    gom_1, gom_2, gom_diff = CalcGOM_of_2result(performances, avaiable_idx)
    print("if there are only 2 group data, ignore 1, 2")
    print("gom_1, gom_2, gom_diff = {}, {}, {}\n".format(gom_1, gom_2, gom_diff))

    match_idx = CompareAccuracy(accuracys, avaiable_idx)
    PrintDiffAccuracy(match_idx, accuracys)
    
    big_diff_val = FindBigDiffPerformance(performances, avaiable_idx)
    PrintDiffPerformance(big_diff_val, performances)

    # save_fn = "analysis_result.csv"
    # print("Start save result to", save_fn)
    # SaveReportCSV(save_fn, 
    #     [names1_1, names1_2, names2_1, names2_2],
    #     [performances1_1, performances1_2, performances2_1, performances2_2],
    #     [accuray1_1, accuray1_2, accuray2_1, accuray2_2],
    #     gom_val1, gom_val2, # 2 gom
    #     match_idx,      # 
    #     big_diff_idx)
    

if __name__ == "__main__":
   main()

# ReadCSV
