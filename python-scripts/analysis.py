
import random
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from functions import convert_to_json, get_array, get_mean_std_mac_delay, generate_plot, initialize, platoon_analysis
from constants import QUEUE_MAP, FOLDERS

'''
    --------------------------------------------README--------------------------------------------

    Python Script to calculate the mean delay of enqueue and dequeue in the MAC layer.

    # Param
        - Takes a file name (should be in "{relative path to ns3 folder}/ns-allinone-3.36.1/ns-3.36.1/scratch/mtp/customexamples/mtpApplication/outputs" directory) or a list of file names
        - Flags
            - '--plot' to plot the mean delays calculated by processing all the log files and their corresponding node density
    # Return
        - Returns the mean delay calculated

    The results (traces of packet for enqueue and dequeue with timestamps) will be written to a file in outputs folder

'''

context_map = {}
for key, pair in QUEUE_MAP.items():
    context_map[key + "dequeue"] = f"WifiNetDevice/Mac/Txop/{key}Queue/Dequeue"
    context_map[key + "enqueue"] = f"WifiNetDevice/Mac/Txop/{key}Queue/Enqueue"


def main():
    if(len(sys.argv) < 3):
        raise TypeError("Insufficient arguments. At least two additional arguments are required.")

    file_path = sys.argv[1]
    json_data = convert_to_json(sys.argv[2])
    
    script_dir = os.path.dirname(file_path)
    input_path = os.path.join(script_dir, "outputs")
    plot_path = os.path.join(script_dir, "plots")
    data_path = os.path.join(script_dir, "practical")
    input_file_template = f"{os.path.basename(file_path).split('.')[0]}-n"
    
    position_model = str(json_data.get('position_model'))
    fixed_num_nodes = int(json_data.get('num_nodes'))
    fixed_data_rate = int(json_data.get('data_rate'))
    fixed_packet_size = int(json_data.get('packet_size'))
    fixed_lamda0 = int(json_data.get("critical_rate"))
    fixed_lamda1 = int(json_data.get("general_rate"))
    
    distance_array = get_array(json_data.get('distance_array'))
    num_nodes_array = get_array(json_data.get('num_nodes_array'))
    data_rate_array = get_array(json_data.get("data_rate_array"))
    lamda0_array = get_array(json_data.get("critical_rate_array"))
    lamda1_array = get_array(json_data.get("general_rate_array"))
    packet_size_array = get_array(json_data.get("packet_size_array"))

    
    if position_model.endswith('uniform'):
        for distance in distance_array:
            parameter_labels = ["Number of Nodes", "Data Rate", "Packet Size", "Rate of packet generation of AC0", "Rate of packet generation of AC1"]
            variable_array = [num_nodes_array, data_rate_array, packet_size_array, lamda0_array, lamda1_array]
            fixed_values = [fixed_num_nodes, fixed_data_rate, fixed_packet_size, fixed_lamda0, fixed_lamda1]    

            for idx, variable in enumerate(variable_array):
                if (variable is None) or (len(variable) == 0): # checking for empty lists
                    continue # making more flexible

                mean_delays, std_delays, rbl_movm_delays, rbl_fvd_delays = initialize()
                temp_input_path = os.path.join(input_path, FOLDERS[idx])
                temp_plot_path = os.path.join(plot_path, FOLDERS[idx])
                temp_data_path = os.path.join(data_path, FOLDERS[idx])
                if not os.path.exists(temp_plot_path): os.makedirs(temp_plot_path)
                if not os.path.exists(temp_data_path): os.makedirs(temp_data_path)
                
                for _, var in enumerate(variable):
                    temp_fixed_values = fixed_values.copy()
                    temp_fixed_values[idx] = var
                    input_file_template = f"{input_file_template}{temp_fixed_values[0]}-d{distance}-dr{temp_fixed_values[1]}-p{temp_fixed_values[2]}-l0{temp_fixed_values[3]}-l1{temp_fixed_values[4]}.log"
                    temparr_mean, temparr_std, temparr_rbl_movm, temparr_rbl_fvd = get_mean_std_mac_delay(context_map, temp_input_path, input_file_template)
                    for x in range(4):
                        mean_delays[x].append(round(temparr_mean[x]/1000000, 5))
                        std_delays[x].append(round(temparr_std[x]/1000000, 5))
                        rbl_movm_delays[x].append(temparr_rbl_movm[x])
                        rbl_fvd_delays[x].append(temparr_rbl_fvd[x])
                
                generate_plot(mean_delays, std_delays, rbl_movm_delays, rbl_fvd_delays, variable_array[idx], temp_data_path, parameter_labels[idx], temp_plot_path, distance)
               

    elif position_model.endswith('platoon'):
        for distance in distance_array:
            platoon_analysis(context_map, input_file_template, input_path, data_path, plot_path, json_data, distance)
            
      
if __name__ == "__main__":
    try:
        main()
    except (TypeError, FileNotFoundError) as e:
        print(f"Error: {e}")
