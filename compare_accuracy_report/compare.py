
#!/usr/bin/python
import math
from pickle import TRUE
import sys
from tokenize import group
import csv
from tkinter.messagebox import NO
import math

# Parse input param
def ParseArgs():
    # CSV1
    csv1 = "../../report_master_int8/accuracy.cpu.20221021_15_53.csv"
    csv2 = "../../report_rm_patch_int8/accuracy.cpu.20221023_11_09.csv"
    thr = 0.001

    print("Argv number =", len(sys.argv))
    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print("Usage: 2 accurayc CSV files and threshold")
        print("  $./compare.py file1.csv file2.csv 0.01")
        sys.exit(0)
    if len(sys.argv) == 4:
        csv1=str(sys.argv[1])
        csv2=str(sys.argv[2])
        thr = float(sys.argv[3])

    else:
        print("Param error, default param will be used.")

    print('CSV file 1:\n  {0}'.format(csv1))
    print('CSV file 2:\n  {0}'.format(csv2))
    print('Threshold:\n  {0}'.format(thr))
    return csv1, csv2, thr

# Read CSV file
# Return context of files.
def ReadCSVFile(csv_fn):
    model = []
    framework = []
    precision = []
    result = []
    metric = []
    value = []
    ref_value = []
    path = []
    description = []

    with open(csv_fn, newline='') as f:
        reader = csv.reader(f)
        idx = -1
        try:
            for row in reader:
                idx += 1

                # print(row)
                if idx == 0:
                    print("Ignore title of CSV.")
                else:
                    model.append(row[0])
                    framework.append(row[1])
                    precision.append(row[2])
                    result.append(row[3])
                    metric.append(row[4])
                    value.append(row[5])
                    ref_value.append(row[6])
                    path.append(row[7])
                    description.append(row[8])

        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(fn, reader.line_num, e))
    
    return [model, framework, precision, result, metric, value, ref_value, path, description]

# Calc avaiable indexs
def CalcAvaiableIndex(data_1, data_2):
    if data_1[0] is None or data_2[0] is None:
        print("model_1 or model_2 is None.")
        return

    avaiable_idx_1 = [ 0 ] * len(data_1[0])
    avaiable_idx_2 = [ 0 ] * len(data_2[0])

    # Loop model_1
    for i in range(len(data_1[0])):
        model_name = data_1[0][i]
        framework = data_1[1][i]
        metric_name = data_1[4][i]

        # Loop model_2
        for j in range(len(data_2[0])):
            if model_name == data_2[0][j] and framework == data_2[1][j] and metric_name == data_2[4][j]:
                avaiable_idx_1[i] = j
                avaiable_idx_2[j] = i
                break

    return avaiable_idx_1, avaiable_idx_2

# Compare
def CompareAccuracy(model_1, metric_1, value_1, model_2, metric_2, value_2, thr, available_idx_1, available_idx_2):
    if model_1 is None:
        print("model_1 is none.")
        return
    
    diff_index = [ 0 ] * len(model_1)

    # Loop model_1
    for i in range(len(available_idx_1)):
        if available_idx_1[i] > 0:
            if value_1[i] is "" or value_2[available_idx_1[i]] is "":
                diff_index[i] = -1
                continue

            diff = math.fabs(float(value_1[i]) - float(value_2[available_idx_1[i]]))
            if diff > thr:
                diff_index[i] = diff
                print("i=", i, value_1[i], value_2[available_idx_1[i]], "diff=", diff)

    return diff_index

def SaveReportCSV(save_fn, data_1, data_2, 
    diff_index, available_idx_1, available_idx_2, thr,
    csv1, csv2):

    with open(save_fn, 'w', newline='') as f: 
        writer = csv.writer(f)
        
        # Save > threshold items 
        title = [["Greater than thread:", str(thr)]]
        writer.writerows(title)
        writer.writerows([["model", "framework", "metric", "ref_value", "value_1", "value_2", "diff_fabs"]])

        for i in range(len(diff_index)):
            if diff_index[i] != 0 :
                data = [data_1[0][i], data_1[1][i], data_1[4][i], data_1[6][i], data_1[5][i], data_2[5][available_idx_1[i]], diff_index[i]]
                writer.writerows([data])

        # Save no match items for 1
        writer.writerows([[]])
        writer.writerows([["Save no match items:", csv1]])
        writer.writerows([["model", "framework", "result", "metric", "ref_value", "value_1"]])
        for i in range(len(available_idx_1)):
            if available_idx_1[i] == 0 :
                data = [data_1[0][i], data_1[1][i], data_1[3][i], data_1[4][i], data_1[5][i], data_1[6][i]]
                writer.writerows([data])

        # Save no match items for 2
        writer.writerows([[]])
        writer.writerows([["Save no match items:", csv2]])
        writer.writerows([["model", "framework", "result", "metric", "ref_value", "value_2"]])
        for i in range(len(available_idx_2)):
            if available_idx_2[i] == 0 :
                data = [data_2[0][i], data_2[1][i], data_2[3][i], data_2[4][i], data_2[5][i], data_2[6][i]]
                writer.writerows([data])

def main():
    csv1, csv2, thr = ParseArgs()

    # Read csv file
    # Return: model, framework, precision, result, metric, value, ref_value, path, description
    data_1 = ReadCSVFile(csv1)
    data_2 = ReadCSVFile(csv2)

    # Because the CSV file maybe have different model number, 
    # and they also have random order,so we need to find avaiable compare items.
    available_idx_1, available_idx_2 = CalcAvaiableIndex(data_1, data_2)
    # 0 mean not available for available_idx, other value mean index in correspoding available_idx.

    # Compare acurracy
    diff_index = CompareAccuracy(data_1[0], data_1[4], data_1[5], 
        data_2[0], data_2[4], data_2[5], thr, 
        available_idx_1, available_idx_2)

    # Save result.
    save_fn = "compare_result.csv"
    print("Start saving results to", save_fn)
    SaveReportCSV(save_fn, data_1, data_2, diff_index, available_idx_1, available_idx_2, thr, csv1, csv2)

    print("Done.")

if __name__ == "__main__":
   main()
