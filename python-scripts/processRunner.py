import os, subprocess, sys
from functions import convert_to_json, convert_to_cli, convert_headway_to_nodes, get_array, Printlines, PrintlinesBD

app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ns3_directory = app_dir.split('/scratch')[0]
script_directory = app_dir
accepted_keys = ['time', 'pcap']

# Functions
def run_ns3_process(fileName, paramString, num_nodes, distance):
    command = ns3_directory + '/ns3 run "' + fileName + paramString + f' --num_nodes={num_nodes} --distance={distance}"'
    print(command)
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}, exiting...")
        sys.exit(1)

def run_ns3_process_bd(fileName, paramString, arr, dir, distance):
    command = ns3_directory + '/ns3 run "' + fileName + paramString
    [folder, file] = dir

    if(len(arr) == 5):
        if(folder and file):
            command = command + f' --num_nodes={arr[0]} --data_rate={arr[1]} --packet_size={arr[2]} --critical_rate={arr[3]} --general_rate={arr[4]} --distance={distance} --folder={folder} --file={file}"'
        else:
            command = command + f' --num_nodes={arr[0]} --data_rate={arr[1]} --packet_size={arr[2]} --critical_rate={arr[3]} --general_rate={arr[4]} --distance={distance}"'
    else:
        raise Exception("command is invalid, less number of arguments to run_ns3_process_bd")

    print(f"Command: {command}")

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}, exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}, exiting...")
        sys.exit(1)



# Main Script
if len(sys.argv) == 1:
    print("Usage: python script_name.py ns3_executable [parameters]")
    sys.exit(1)
elif len(sys.argv) >= 2:

    ns3_executable = os.path.basename(sys.argv[1])
    script_directory = os.path.dirname(sys.argv[1])
    outpath_path = os.path.join(script_directory, "outputs")
    parameters = sys.argv[2] if (len(sys.argv) == 3) else "{}"
    json_data = convert_to_json(parameters)
    position_model = json_data.get('position_model')
    cli_args = convert_to_cli(json_data, accepted_keys)
    distance_array = get_array(json_data.get('distance_array'))

    num_nodes_array = get_array(json_data.get('num_nodes_array'))
    headway_array = get_array(json_data.get('headway_array'))


    if str(position_model).endswith('uniform'):
        for distance in distance_array:
            fixed_num_nodes = json_data.get('num_nodes')
            data_rate_array = get_array(json_data.get("data_rate_array"))
            fixed_data_rate = json_data.get('data_rate')
            packet_size_array = get_array(json_data.get("packet_size_array"))
            fixed_packet_size = json_data.get('packet_size')

            critical_rate_array = get_array(json_data.get("critical_rate_array"))
            fixed_critical_rate = int(json_data.get("critical_rate"))
            general_rate_array = get_array(json_data.get("general_rate_array"))
            fixed_general_rate = int(json_data.get("general_rate"))

            variable_array = [num_nodes_array, data_rate_array, packet_size_array, critical_rate_array, general_rate_array]
            fixed_values = [fixed_num_nodes, fixed_data_rate, fixed_packet_size, fixed_critical_rate, fixed_general_rate]
            parameter_labels = ["Number of Nodes", "Data Rate", "Packet Size", "Rate of packet generation of AC0", "Rate of packet generation of AC1"]
            folder_names = ["variable_nodes", "variable_data_rate", "variable_packet_size", "variable_critical_rate", "variable_general_rate"]
            

            for idx, variable in enumerate(variable_array):
                # Create subdirectories for the outputs only those that are supplied
                if (variable is None) or (len(variable) == 0): #checking for empty lists
                    continue # making more flexible
                print(variable)
                dir_path = os.path.join(outpath_path, folder_names[idx])
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                print(f"\n\nVarying {parameter_labels[idx]} from {variable[0]} to {variable[len(variable)-1]} while keeping all other things constant")
                for jdx, var in enumerate(variable):
                    temp_fixed_values = fixed_values.copy()
                    temp_fixed_values[idx] = var
                    file = f"testbd-n{temp_fixed_values[0]}-d{temp_fixed_values[1]}-p{temp_fixed_values[2]}-l0{temp_fixed_values[3]}-l1{temp_fixed_values[4]}"
                    PrintlinesBD(temp_fixed_values)
                    run_ns3_process_bd(ns3_executable, cli_args, temp_fixed_values, [folder_names[idx], file], distance)
                
    elif str(position_model).endswith('platoon'):
        # TODO: write some real code here!
        for distance in distance_array:
            num_nodes_array, headway_aray = convert_headway_to_nodes(json_data, distance)
            for idx, num_nodes in enumerate(num_nodes_array):
                Printlines(headway=headway_array[idx], num_nodes=num_nodes, distance=distance)
                run_ns3_process(ns3_executable, cli_args, num_nodes, distance)