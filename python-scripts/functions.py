import json, os, sys, math
import matplotlib.pyplot as plt
import random
import numpy as np
from constants import *

# Code for obtaining theoratical Reliability Values

def get_rel(t_cr, headway):
    x1_ac0 = 0.0566
    x2_ac0 = 0.1277
    x1_ac1 = 0.0156
    x2_ac1 = 0.057
    print(f"t_tr: {TRANSMISSION_TIME}, t_cr: {t_cr}, expo: {-1*(x1_ac0*headway + x2_ac0) * (t_cr - TRANSMISSION_TIME) * 1000}")
    if t_cr >= TRANSMISSION_TIME:
        rel_ac0 = 1 - np.exp(-1* (x1_ac0*headway + x2_ac0) * (t_cr - TRANSMISSION_TIME) * 1000) #Note: values must be in (ms)
        rel_ac1 = 1 - np.exp(-1* (x1_ac1*headway + x2_ac1) * (t_cr - TRANSMISSION_TIME) * 1000)
        return rel_ac0, rel_ac1 # TODO change it later
    else:
        return 0,0
    


# Code for Obtaining the communication and Critical Delays

# tn --> ( -1 / ( (̃d) * (2 + root(2)) ) )  * ln[ ((̃d)(a + 𝑙)(−2 − root(2)) − 𝑎𝑉′(𝑦∗)) / ( (̃d) * (−2 − root(2)) )^2 ]
# tn is the communication delay
def get_tn(y, d, a, l, x0, y_dash, ym):
    log_num = (-d * (a + l)*(-2-np.sqrt(2))) - a*V_bar(y, x0, y_dash, ym)
    log_den = (d * (-2-np.sqrt(2)))**2
    val = -1/(d*(2+np.sqrt(2)))
    tn = val * np.log(log_num/log_den)
    return tn

# This function provides the value of critical delay, considering tn as only 10% of the delay
def get_t_cr(tn, mean=0.1, std_dev=0.01):
    k = random.gauss(mu=mean, sigma=std_dev)
    return k*tn


# d_bar --> (̃d) = 𝑎𝑉′(𝑦∗)∕(𝑎 + 𝑙)
def get_d_bar(y, a, l, x0, y_dash, ym):
    num = a * V_bar(y, x0, y_dash, ym)
    den = a + l
    d_bar = num/den
    return d_bar

# Calculating value of Vo satisfying the equation --> 𝑦∗ = 𝑉^(-1)(𝑥`0)
def V_0(y, x0, y_dash, ym):
    v0 = (x0 /( np.tanh((y - ym)/y_dash) + np.tanh(ym/y_dash) )) 
    return v0

def V_bar(y, x0, y_dash, ym):
    val = (V_0(y, x0, y_dash, ym) * ( 1 - (np.tanh((y - ym)/y_dash)**2) ) * (1/y_dash))
    return val

def get_tcr(headway, a=5, l=0, x0=25, y_dash=10, ym=5):
    d_bar = get_d_bar(headway, a, l, x0, y_dash, ym)
    tn = get_tn(headway, d_bar, a, l, x0, y_dash, ym)
    t_cr = get_t_cr(tn)
    return t_cr


def convert_to_json(json_string):
    try:
        json_data = json.loads(json_string)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}, exiting...")
        sys.exit(1)


def getPlatoonRate(params):
    # Get probablity that 2-wheelers(non-communicating nodes) will intercept the platoon
    alpha, gamma, y_star, x_dot0, p = params.get('alpha'), params.get('gamma'), params.get('convergence_value'), params.get('velocity_lead_node'), params.get('tunable_param')
    term = alpha + gamma*(y_star/x_dot0)
    prob = math.exp(term)/(1 + math.exp(term))
    critical_rate = round(float(p) * prob, 3)
    return critical_rate


def getCriticalRate(headway, json_data):
    position_model = str(json_data['position_model'])
    platoon_params = updateParams(headway, json_data)
    if position_model.startswith('platoon'):
        rate = getPlatoonRate(platoon_params)
        return rate
    else:
        rate = json_data.get('critical_rate', 100)
        return rate

def updateParams(headway, json_data):
    platoon_params = {
        'alpha': float(json_data.get('alpha', -1.933)),
        'gamma': float(json_data.get('gamma', 0.652)),
        'convergence_value': int(headway),
        'velocity_lead_node': int(json_data.get('velocity_lead_node', 120)),
        'tunable_param': int(json_data.get('tunable_param', 500)),
    }
    return platoon_params

def convert_to_cli(json_data, accepted_keys):
    cli_arguments = ""
    for key, value in json_data.items():
        if key in accepted_keys:
            cli_arguments += f' --{key}={value}'
    return cli_arguments

def get_array(str):
    if str == None:
        return []
    try:
        arr = list(map(int, str.split(' ')))
        return arr
    except Exception as _:
        return get_float_array(str)

def get_float_array(str):
    arr = list(map(float, str.split(' ')))
    return arr

def Printlines(headway=None, num_nodes=None, distance=None):
    if headway and num_nodes:
        distance = distance
    elif headway and distance:
        num_nodes = int(distance/headway + 1)
    
    if headway:
        print(f'Running for headway={headway}, num_nodes={num_nodes}, distance={distance}')
    else:
        print(f'Running for num_nodes={num_nodes}, distance={distance}')

def PrintlinesBD(arr):
    if(len(arr)==5):
        print(f'Running for num_nodes={arr[0]}, data_rate={arr[1]}Mbps, packet_size={arr[2]}bytes, lamda0={arr[3]}packets/s, lamda1={arr[4]}packets/s')
    else:
        print(f'Insufficient Arguments')


def convert_headway_to_nodes(json_data, distance=100):
    position_model =  str(json_data['position_model'])
    num_nodes_array = []
    headway_array = None
    dist = int(distance)
    if position_model.startswith('platoon'): # makes use of platoon-distance
        headway_array = list(map(int, json_data['headway_array'].split(' ')))
        for x in headway_array:
            num_nodes = int(dist/x + 1)
            num_nodes_array.append(num_nodes)
    else:
        num_nodes_array = list(map(int, json_data['num_nodes_array'].split(' '))) # makes use of headway-distance
        
        

    return num_nodes_array, headway_array

def plot_figure(data_map, row, col, xvalue, xlabel, plot_path=None, distance=100):
    fontsize = 6
    col = int(col)
    plt.figure(figsize=(50, 20))
    f, ax = plt.subplots(len(row), col, gridspec_kw={'hspace':0.3, 'wspace':0.3})
    for i,x in enumerate(row):
        cnt= 0
        for key, values in data_map.items():
            if key.startswith(x):
                ax[i][cnt].plot(xvalue, values, label=str(key.split('_')[1]))
                ax[i][cnt].scatter(xvalue, values)
                ax[i][cnt].legend(fontsize=fontsize)
                ax[len(row)-1][cnt].set_xlabel(xlabel,fontsize=fontsize)
                cnt += 1
                ax[len(row)-1][cnt].set_xlabel(xlabel=xlabel, fontsize=fontsize)

        for key, values in data_map.items():
            if key.startswith(x):
                label = str(key.split('_')[1])
                ax[i][col-1].plot(xvalue, values, label=label)
                ax[i][col-1].scatter(xvalue, values)
        ax[i][0].set_ylabel(f"{x} mac delays (in ms)", fontsize=fontsize)
        ax[i][col-1].legend(fontsize=fontsize)
    for i in range(len(row)):
        for j in range(col):
            ax[i][j].tick_params(axis='x', labelsize=fontsize)
            ax[i][j].tick_params(axis='y', labelsize=fontsize)

    plt.savefig(os.path.join(plot_path, f"mtp-plot-mac-delay-{distance}.png"))
    plt.close() # Closing the figure after saved

def write_content(headways, vo, vi):
    content = ''
    for i in range(len(headways)):
        content += f'{headways[i]:.6f} {vo[i]:.6f} {vi[i]:.6f}\n'
    return content

def create_file(data_map, row, headways, path, mom=False):
    for x in row:
        baseName = x
        vo, vi = None, None
        for key, values in data_map.items():
            key = str(key)
            if key.startswith(x):
                if key.endswith('VI'):
                    vi = values
                elif key.endswith('VO'):
                    vo = values
        if not mom:
            with open(os.path.join(path, baseName + '.txt'), 'w') as file:
                file.write(write_content(headways, vo, vi))                
        else:
            with open(os.path.join(path, baseName + '-VI.csv'), 'a') as file:
                vi_str = [str(x) for x in vi]
                log = ", ".join(vi_str) + "\n"
                file.write(log)

            with open(os.path.join(path, baseName + '-VO.csv'), 'a') as file:
                vo_str = [str(x) for x in vo]
                log = ", ".join(vo_str) + "\n"
                file.write(log)


def plot_figure_solo(data_map, row, col, xvalue, xlabel, plot_path=None, distance=100, fileName=None):
    fontsize = 6
    for key, values in data_map.items():      
        plt.figure()      
        plt.plot(xvalue, values, label=str(key.split('_')[1]))
        plt.scatter(xvalue, values)
        plt.legend(fontsize = fontsize)
        plt.xlabel(xlabel)
        plt.ylabel(f"{key.split('_')[0]} mac delays (in ms)")
        if fileName:
            plt.savefig(os.path.join(plot_path, fileName))
            plt.close()
        else:
            plt.savefig(os.path.join(plot_path, f"mtp-plot-mac-delay-{key}-{distance}"))
            plt.close()

    for x in row:
        plt.figure()
        for key, values in data_map.items():
            key = str(key)
            if key.startswith(x):
                plt.plot(xvalue, values, label=str(key.split('_')[1]))
                plt.scatter(xvalue, values)
                plt.legend(fontsize = fontsize)
                plt.xlabel(xlabel)
                plt.ylabel(f"{key.split('_')[0]} mac delays (in ms)")
        if fileName:
            plt.savefig(os.path.join(plot_path, fileName))
            plt.close()
        else:
            plt.savefig(os.path.join(plot_path, f"mtp-plot-mac-delay-{x}-{distance}"))
            plt.close()

def plot_means_of_means(data_path, row, xlabel, plt_data, filename=None):
    fontsize = 6
    pass

# Code for testing the functions
def test():
    headways = np.arange(2,11,1)
    pts = []
    for headway in headways:
        pts.append(get_rel(get_tcr(headway), headway))
        
    plt.plot(headways, pts)
    plt.xticks(headways)
    plt.savefig(os.path.join(os.path.dirname(__file__), 'test.png'))
    plt.close()
    
# test()


def initialize():
    mean_delays = [[], [], [], []]
    std_delays = [[], [], [], []]
    rbl_movm_delays = [[], [], [], []]
    rbl_fvd_delays = [[], [], [], []]
    return mean_delays, std_delays, rbl_movm_delays, rbl_fvd_delays

def generate_plot(mean_delays, std_delays, rbl_movm_delays, rbl_fvd_delays, plt_data, data_path, xlabel, plot_path, distance, mom=False):
    data_map = {}
    for x in range(4):
        if sum(mean_delays[x]) == 0:
            continue
        data_map[f'mean_{INVERSE_MAP[x]}'] = mean_delays[x]
        data_map[f'std_{INVERSE_MAP[x]}'] = std_delays[x]
        data_map[f'rbl_movm_{INVERSE_MAP[x]}'] = rbl_movm_delays[x]
        data_map[f'rbl_fvd_{INVERSE_MAP[x]}'] = rbl_fvd_delays[x]
    row = ['mean', 'std', 'rbl_movm', 'rbl_fvd']
    col = len(data_map)/len(row) + 1
    # Generate Plots
    create_file(data_map, row, plt_data, data_path, mom)
    plot_figure_solo(data_map, row, col, plt_data, xlabel, plot_path, distance)

def get_mean_std_mac_delay(context_map, input_path, fileName, nodes=None, headway=None, distance=None):

    mean_delays = np.zeros(4)
    std_delays = np.zeros(4)
    rbl_movm_delays = np.zeros(4)
    rbl_fvd_delays = np.zeros(4)
    counters = np.zeros(4)
    # mean_delay = 0
    uid_enqueue = {}

    input_file = os.path.join(input_path, fileName)
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"{fileName} doesn't exist in the {input_path} directory!!")

    split_char = '-'
    outFileList = fileName.split('.log')[0].split(split_char)
    outFileList[0] = "analysis"
    outFileName = split_char.join(outFileList)

    output_file_path = os.path.join(input_path, outFileName)
    
    file_descriptor = os.open(output_file_path, os.O_WRONLY | os.O_CREAT, 0o644)
    if file_descriptor == -1:
        raise FileNotFoundError(f"{output_file_path} doesn't exist")   
    
    # Read the input files
    with open(input_file, "r") as file:
        for line in file:
            attr = line.split(' ')
            uid = int(attr[0])
            context = attr[1]
            time = float(attr[2])
            for key, value in QUEUE_MAP.items():
                if (context.endswith(context_map[key + "dequeue"]) and uid_enqueue.__contains__(uid) and uid_enqueue[uid]!=-1):
                    os.write(file_descriptor, bytes(f"Dequeue time for uid {uid} is {time}ns \n", 'utf-8'))
                    mean_delays[value] = mean_delays[value] + (time - uid_enqueue[uid])
                    std_delays[value] = std_delays[value] + (time - uid_enqueue[uid])**2
                    # Note: Comment below value in case you do not wish to calculate reliability
                    rbl_movm_delays[value] = rbl_movm_delays[value] + 1 if (get_tcr(headway,l=0) > ((time - uid_enqueue[uid])/1000000000)) else rbl_movm_delays[value]
                    rbl_fvd_delays[value] = rbl_fvd_delays[value] + 1 if (get_tcr(headway,l=2) > ((time - uid_enqueue[uid])/1000000000)) else rbl_fvd_delays[value]
                    counters[value] = counters[value] + 1
                    uid_enqueue[uid] = -1
                elif (context.endswith(context_map[key + "enqueue"]) and (not uid_enqueue.__contains__(uid))):
                    os.write(file_descriptor, bytes(f"Enqueue time for uid {uid} is {time}ns \n", 'utf-8'))
                    uid_enqueue[uid] = time

    for x in range(4):
        if counters[x] == 0:
            continue
        mean_delays[x] = mean_delays[x]/counters[x]
        std_delays[x] = std_delays[x] - (counters[x] * mean_delays[x]**2)
        std_delays[x] = np.sqrt(std_delays[x]/counters[x])
        rbl_movm_delays[x] = rbl_movm_delays[x]/counters[x]
        rbl_fvd_delays[x] = rbl_fvd_delays[x]/counters[x]
        os.write(file_descriptor, bytes(f"Mean Delay for {x}: {mean_delays[x]}ns \n", 'utf-8'))
        os.write(file_descriptor, bytes(f"std Delay for {x}: {std_delays[x]}ns \n", 'utf-8'))
        os.write(file_descriptor, bytes(f"reliability for {x}: {rbl_movm_delays[x]}ns \n", 'utf-8'))
        os.write(file_descriptor, bytes(f"reliability for {x}: {rbl_fvd_delays[x]}ns \n", 'utf-8'))

    os.close(file_descriptor)
    return mean_delays, std_delays, rbl_movm_delays, rbl_fvd_delays

def platoon_analysis(context_map, input_file_template, input_path, data_path, plot_path, json_data, distance, mom=False):
    nodes_array, headway_array = convert_headway_to_nodes(json_data, distance)
    mean_delays, std_delays, rbl_movm_delays, rbl_fvd_delays = initialize()
    
    for idx, nodes in enumerate(nodes_array):
        input_file = input_file_template + str(nodes) +'-d' + str(distance) + ".log"
        temparr_mean, temparr_std, temparr_rbl_movm, temparr_rbl_fvd = get_mean_std_mac_delay(context_map, input_path, input_file, nodes=nodes, headway=headway_array[idx], distance=distance)
        for x in range(4):
            mean_delays[x].append(round(temparr_mean[x]/1000000, 5))
            std_delays[x].append(round(temparr_std[x]/1000000, 5))
            rbl_movm_delays[x].append(temparr_rbl_movm[x])
            rbl_fvd_delays[x].append(temparr_rbl_fvd[x])

    generate_plot(mean_delays, std_delays, rbl_movm_delays, rbl_fvd_delays, headway_array, data_path, 'Headway', plot_path, distance, mom)