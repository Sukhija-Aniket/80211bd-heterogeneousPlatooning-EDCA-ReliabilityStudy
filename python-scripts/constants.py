
PHY_HEADER_SIZE = 48
MAC_HEADER_SIZE = 112 
P_D = 0.9
P_S = 0.8
PROB = P_D * P_S
PACKET_SIZE = 500 * 8 # 500 bytes
PACKET_SIZE = PROB * 500 + (1-PROB) * PROB * 1000 + (1-PROB)**2 * PROB * 1500 + (1-PROB)**3 * 2000
BASIC_RATE = 1 * 1000 * 1000 # 1Mbps
DATA_RATE = 3 * 1000 * 1000 # p 
DATA_RATE = 27 * 1000 * 1000 # bd
PROPAGATION_DELAY = 2/1000000 # NOTE taken as given in paper
TRANSMISSION_TIME = PHY_HEADER_SIZE/BASIC_RATE + (MAC_HEADER_SIZE + PACKET_SIZE)/DATA_RATE + PROPAGATION_DELAY

QUEUE_MAP = {
    'BE': 0,
    'BK': 1,
    'VI': 2,
    'VO': 3
}

INVERSE_MAP = ['BE', 'BK', 'VI', 'VO']
FOLDERS = ["variable_nodes", "variable_data_rate", "variable_packet_size", "variable_critical_rate", "variable_general_rate"]