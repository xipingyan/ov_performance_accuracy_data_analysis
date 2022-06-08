
#!/usr/bin/python
import math
import sys
from read_csv import ReadCSV_out_performance_accuracy as ReadCSV
from save_rpt_csv import SaveReportCSV
# Parse input param
def ParseArgs():
    master_files = ["../1_test-dlbenchmark-cpu_dlbenchmark_public_22ee17fd_ubuntu20.04/out_performance_accuracy.csv",
            "../2_test-dlbenchmark-cpu_dlbenchmark_i9-9900k_public_22ee17fd_ubuntu20.04/out_performance_accuracy.csv"]
    my_pr_files = ["../1_test-dlbenchmark-cpu_public_93e2be1d_ubuntu20.04/out_performance_accuracy.csv",
            "../2_test-dlbenchmark-cpu_public_93e2be1d_ubuntu20.04/out_performance_accuracy.csv"]
  
    print("Argv number =", len(sys.argv))
    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print("Usage:")
        print("  $./create_analysis_report.py old_csv1 old_csv2 new_csv1 new_csv2")
        sys.exit(0)
    if len(sys.argv) == 5:
        my_pr_files=[str(sys.argv[1]), str(sys.argv[2])];
        master_files=[str(sys.argv[3]), str(sys.argv[4])];
    else:  
        print("Param error, default param will be used.")

    print('Old CSV file:\n  {0}\n  {1}'.format(my_pr_files[0], my_pr_files[1]))
    print('New CSV file:\n  {0}\n  {1}'.format(master_files[0], master_files[1]))
    return master_files, my_pr_files

# Calc avaiable indexs
def CalcAvaiableIndex(performances):
    if performances is None:
        print("Can't input none data.")
        return

    list_size = len(performances[0])
    avaiable_idx = [ 0 ] * list_size
    
    for pf in performances:
        if len(pf) != list_size:
            print("Dim is not same. {} != {}".format(len(pf), list_size))
            sys.exit(0)

    for i in range(len(performances[0])):
        all_avaible = 0
        for j in range(len(performances)):
            if float(performances[j][i]) >= 0:
                all_avaible += 1

        if all_avaible == len(performances):
            avaiable_idx[i] = 1

    return avaiable_idx
    
# Calculate 2 result's GOM
# Return: GOM value and avaiable index
def CalcGOM_of_2result(performance1, performance2, avaiable_idx):
    gom_val = 1
    for i in range(len(performance1)):
        # Only statistic avaiable value
        try:
            if type(performance1[i]) == str:
                performance1[i] = float(performance1[i])
            if type(performance2[i]) == str:
                performance2[i] = float(performance2[i])

            if avaiable_idx[i] == 1:
                gom_val = gom_val * performance1[i] / performance2[i]
        except ValueError as ex:
            print("Catch an exception:", ex)

    # GOM: = pow((Xi * Xj * ...), 1/n)
    n = sum(avaiable_idx)
    gom_val = math.pow(gom_val, 1/n)

    return gom_val

# Compara 4 result if all passed.
# Return match item index. -1: not go to match; 0: mismatch; 1: match
def CompareAccuracy(accurays, avaiable_idx):
    if accurays is None:
        print("accurays is none.")
        return

    list_size = len(accurays[0])
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
        for j in range(len(accurays)):
            # GROUND_TRUTH, don't need to compare.
            if str(accurays[j][i]).find("GROUND_TRUTH") >= 0:
                all_gt += 1
            elif str(accurays[j][i]).find("FAILED") >= 0:
                all_failed += 1
            elif str(accurays[j][i]).find("CRASHED") >= 0:
                all_crashed += 1
            elif str(accurays[j][i]).find("PASSED") >= 0:
                all_passed += 1
            elif str(accurays[j][i]).find("NONE") >= 0:
                all_none += 1
            else:
                print("Find none.")
            
            
        if all_failed == len(accurays):     # All FAILED
            Match = -1
        elif all_crashed == len(accurays):  # All CRASHED
            Match = -1
        elif all_passed == len(accurays):   # All PASSED
            Match = 1
        elif all_gt > 0:                    # Ignore groundtruth
            Match = -1
        elif all_none == len(accurays):
            Match = -1
        else:
            Match = 0

        match_idx[i] = Match
    
    return match_idx

# Find FPS with big difference.
def FindBigDiffPerformance(p1, p2, p3, p4, avaiable_idx):
    list_size = len(avaiable_idx)
    big_diff_idx = [ 0 ] * list_size
    for i in range(len(p1)):
        # Filter?
        # if avaiable_idx[i] != 1:
        #     continue
        val1 = (p1[i] + p2[i]) / 2.0
        val2 = (p3[i] + p4[i]) / 2.0
        diff = abs(val1 - val2)
        # diff > mean * 20% && diff > 2
        if diff > (val1 + val2) / 2.0 * 0.2 and diff > 2:
            big_diff_idx[i] = 1
    
    return big_diff_idx

def main():
    my_pr_files, master_files = ParseArgs()

    # Read csv file
    names1_1, performances1_1, accuray1_1 = ReadCSV(my_pr_files[0])
    names1_2, performances1_2, accuray1_2 = ReadCSV(my_pr_files[1])
    names2_1, performances2_1, accuray2_1 = ReadCSV(master_files[0])
    names2_2, performances2_2, accuray2_2 = ReadCSV(master_files[1])

    avaiable_idx = CalcAvaiableIndex([performances1_1, performances1_2, performances2_1, performances2_2])

    gom_val1 = CalcGOM_of_2result(performances1_1, performances1_2, avaiable_idx)
    # print("gom_val1, avaible_idx1 = {}, {}".format(gom_val1, avaible_idx1))
    gom_val2 = CalcGOM_of_2result(performances2_1, performances2_2, avaiable_idx)
    print("gom_val1, gom_val2 = {}, {}".format(gom_val1, gom_val2))

    match_idx = CompareAccuracy([accuray1_1, accuray1_2, accuray2_1, accuray2_2], avaiable_idx)
    print("Display accuracy diff:")
    for i in range(len(match_idx)):
        if match_idx[i] == 0:
            print("{0:3d} {1:60s} {2:10s} {3:10s} {4:10s} {5:10s}".format(i, names1_1[i], 
            accuray1_1[i], accuray1_2[i], accuray2_1[i], accuray2_2[i]))

    big_diff_idx = FindBigDiffPerformance(performances1_1, performances1_2, performances2_1, performances2_2, avaiable_idx)
    print("Display performance with big diff:")
    for i in range(len(big_diff_idx)):
        if big_diff_idx[i] == 1:
            print("{0:3d} {1:60s} {2:10f} {3:10f} {4:10f} {5:10f}".format(i, names1_1[i], 
            performances1_1[i], performances1_2[i], performances2_1[i], performances2_2[i]))

    save_fn = "analysis_result.csv"
    print("Start save result to", save_fn)
    SaveReportCSV(save_fn, 
        [names1_1, names1_2, names2_1, names2_2],
        [performances1_1, performances1_2, performances2_1, performances2_2],
        [accuray1_1, accuray1_2, accuray2_1, accuray2_2],
        gom_val1, gom_val2, # 2 gom
        match_idx,      # 
        big_diff_idx)
    

if __name__ == "__main__":
   main()

# ReadCSV
