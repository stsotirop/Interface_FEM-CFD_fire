import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import subprocess
import ntpath

all_input_files = []


# Read the csv output from FDS analysis and create as much txt files as the number of the &DEVC
def create_txt_temp(path, file):
    file = path + '/' + file
    test = pd.read_csv(file, skiprows=1)
    headers = test.columns
    num_output = len(headers)
    for i in range(1, num_output):
        temp = test[[headers[0], headers[i]]]
        file = path + '/' + f'{headers[i]}.txt'
        temp.to_csv(file, index=False, header=False, sep='\t')


# Plot time-temperature curve and create txt with specific step linear regression
def plot_temp(file, destination_folder, total_time, time_step):
    data = pd.read_csv(file, header=None, sep='\t', index_col=False, dtype=float)
    data = data.to_numpy()
    time_hist = data[:, 0]
    temp_hist = data[:, 1]
    file_name = os.path.basename(file)
    root, extension = os.path.splitext(file_name)
    plt.figure()
    plt.scatter(time_hist, temp_hist, color="black", s=1)
    plt.plot(time_hist, temp_hist, color="black")
    plt.savefig(destination_folder + '/' + root + ".png")
    plt.close()
    # Create file with specific time step
    file = destination_folder + '/' + root + '_' + f'{total_time}' + '_' + f'{time_step}' + extension
    with open(file, 'w', encoding='UTF8', newline='') as f:
        p1 = round(np.interp(0, time_hist, temp_hist), 6)
        f.write(f'{0}' + '\t' + f'{p1}')
        for i in range(time_step, total_time + 1, time_step):
            p1 = round(np.interp(i, time_hist, temp_hist), 6)
            f.write('\n' + f'{i}' + '\t' + f'{p1}')
    data = pd.read_csv(file, header=None, sep='\t', index_col=False, dtype=float)
    data = data.to_numpy()
    time_hist = data[:, 0]
    temp_hist = data[:, 1]
    plt.figure()
    plt.scatter(time_hist, temp_hist, color="black", s=1)
    plt.plot(time_hist, temp_hist, color="black")
    plt.savefig(destination_folder + '/' + root + '_' + f'{total_time}' + '_' + f'{time_step}' + ".png")
    plt.close()


# Create input files for SAFIR having one in file as prototype and changes the txt file that reads the time-temperature
# curve
def create_safir_input_temp(safir_file, txt_file, txt_file_0, path_folder):
    root_temp = ntpath.basename(txt_file)
    root_txt, extension_txt = os.path.splitext(root_temp)
    os.chdir(path_folder)
    root_saf, extension_saf = os.path.splitext(safir_file)
    new_name = root_saf + root_txt + extension_saf
    shutil.copy(safir_file, new_name)
    fin = open(new_name, "rt")
    data = fin.read()
    data = data.replace(txt_file_0, root_txt)
    fin.close()
    fin = open(new_name, "wt")
    fin.write(data)
    fin.close()
    all_input_files.append(root_saf + root_txt)


# Create .txt file with the temperature based on csv file that contains weight factors
def post_process_detailed_grid(weight_file, temp_files, path_folder, txt_name):
    check_files = 0
    test = pd.read_csv(weight_file)
    test = test.to_numpy()
    weight_coe = {}
    dict_id = {}
    final_temp = []
    final_time = []
    num = len(test[:, 0])
    for i in range(num):
        weight_coe[test[i, 0]] = [test[i, 1], test[i, 2]]
    for curve in temp_files:
        file_name = os.path.basename(curve)
        file1 = open(curve, 'r')
        lines = file1.readlines()
        temp_info = []
        for line in lines:
            time, temp = line.strip('\n').split('\t')
            temp_array = np.array([round(float(time), 2), round(float(temp), 2)])
            temp_info.append(temp_array)
        dict_id[os.path.splitext(file_name)[0]] = temp_info
    sum1 = 0
    keys_list1 = list(weight_coe.keys())
    keys_list2 = list(dict_id.keys())
    for key in keys_list1:
        if key not in keys_list2:
            check_files = -1
            return check_files
    for key, value in dict_id.items():
        sum2 = 0
        weight1 = weight_coe[key]
        total_weight = weight1[0] * weight1[1]
        for temp_array in value:
            new_array_w = total_weight * temp_array
            if sum1 == 0:
                final_temp.append(new_array_w[1])
                final_time.append(temp_array[0])
            else:
                final_temp[sum2] += new_array_w[1]
            sum2 += 1
        sum1 += 1
    sum1 = 0
    file = path_folder + '/' + txt_name + '.txt'
    with open(file, 'w', encoding='UTF8', newline='') as f:
        for item in final_temp:
            if sum1 == 0:
                f.write(f'{round(final_time[sum1], 2)}' + '\t' + f'{round(item, 2)}')
            else:
                f.write('\n' + f'{round(final_time[sum1], 2)}' + '\t' + f'{round(item, 2)}')
            sum1 += 1

    return check_files


# Only CMD
# Run all in the .in file that I created in the function !!create_safir_input_temp()!! with SAFIR
def run_thermal_analysis():
    for file in all_input_files:
        exe_path = r'C:\Users\stefanos\Source\CFD-FEM\main_files\test0\SAFIR.exe '
        cmd_command = exe_path + file
        process = subprocess.run(cmd_command)
        # process.wait
