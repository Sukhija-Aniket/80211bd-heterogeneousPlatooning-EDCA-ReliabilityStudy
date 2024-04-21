import sys
import os
import subprocess
from functions import convert_to_json, get_array, platoon_analysis
from constants import QUEUE_MAP

app_dir = os.path.dirname(os.path.abspath(__file__))
context_map = {}
for key, pair in QUEUE_MAP.items():
    context_map[key + "dequeue"] = f"WifiNetDevice/Mac/Txop/{key}Queue/Dequeue"
    context_map[key + "enqueue"] = f"WifiNetDevice/Mac/Txop/{key}Queue/Enqueue"

def runRandomProcessScript(executable, params):
    command = 'python3 ' + app_dir + '/randomProcessGeneration.py ' + executable + ' ' + f"'{params}'"
    print(command)
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}, exiting...")
        sys.exit(1)

def runProcessRunner(executable, params):
    command = "python3 " + app_dir + "/processRunner.py " + executable + " " + f"'{params}'"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}, exiting...")
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: python script_name.py repititions ns3_executable [parameters]")
        sys.exit(1)
    
    repititions = int(sys.argv[1])
    file_path = sys.argv[2]
    parameters = sys.argv[3] if (len(sys.argv) == 4) else '{\}'
    json_data = convert_to_json(parameters)
    
    script_dir = os.path.dirname(file_path)
    input_path = os.path.join(script_dir, "outputs")
    plot_path = os.path.join(script_dir, "plots")
    data_path = os.path.join(script_dir, "practical")
    input_file_template = f"{os.path.basename(file_path).split('.')[0]}-n"

    position_model = str(json_data.get('position_model'))
    distance = get_array(json_data.get('distance_array'))[0]

    assert str(position_model).endswith('platoon') == True

    for _ in range(repititions):
        # Run the random Generation file
        runRandomProcessScript(file_path, parameters)
        # Run processRunner
        runProcessRunner(file_path, parameters)
        # Do the analysis
        platoon_analysis(context_map, input_file_template, input_path, data_path, plot_path, json_data, distance, mom=True)


if __name__ == "__main__":
    main()