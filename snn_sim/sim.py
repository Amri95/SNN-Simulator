import sys
import collections
#from snn_components import *

#from spike_plotter import *

# THIS FILE RUNS THE SIMULATOR MAYBE???






########## Testing out new structure here ##########

import params
import spike_plot

from components.synapse import TwinMemristive as TM
from components.neuron import LIF
from components.neuron import InputNeuron
from components.rng import RNG

user_params = {
    "Vrst": 0.6
}

params.setup(user_params)

print(params.get("LRS"))
print(params.get("VDD"))
print(params.get("Vrst"))

p1, p2, p3, p4, p5 = params.get("VDD", "VSS", "tper", "cycles", "cap")
num = (p1 - p2)/2 + p2
print(num)


input_file = sys.argv[2]
with open(input_file, "r") as f:
    lines = f.readlines()

line = lines[0].replace(' \n', '')
line = line.replace('\n', '')
line = line.split(' ')
line = [int(i) for i in line]

input_neuron = InputNeuron("INP", line)
neuron = LIF("N0", 0.6, 0.598, 1, params.get("cap"))
input_synapse = TM(delay=0, pre=input_neuron, post=neuron)
neuron.input_synapses.append(input_synapse)


SIM_CYCLES = len(line)

for clk in range(SIM_CYCLES-2):
    input_synapse.propagate_spikes(clk)
    neuron.accumulate(clk)

print(input_synapse.activity)
print(neuron.Vmem)
print(neuron.fire)

# sp = spike_plot.SpikePlot()
# sp.plot(neuron.fire)

exit()

####################################################







network_file = sys.argv[1]
input_file = sys.argv[2]

rng = Std_RNG()


with open(input_file, 'r') as f:
    lines = f.readlines()

input_neuron_list = []
input_synapse_list = []

# Create "input neurons/synapses" to carry input spikes into the network
for line in lines:
    line = line.replace(' \n', '')
    line = line.replace('\n', '')
    line = line.split(' ')
    line = [int(i) for i in line]

    # Create an input neuron and synapse, the post-neuron of the synapse is as yet unknown
    input_neuron = InputNeuron(line, "INP")
    # input_synapse = InputSynapse(Mp_in, Mn_in, 0, input_neuron, None)
    input_synapse = Synapse(3, 0, input_neuron, None)
    input_neuron_list.append(input_neuron)
    input_synapse_list.append(input_synapse)

SIM_CYCLES = len(line)


# Read the network file into a list of lines
with open(network_file, 'r') as f:
    lines = f.readlines()

neuron_dict = {}
synapse_list = []

# UNTIL I KNOW HOW THIS ACTUALLY WORKS
count = 0

for line in lines:
    line = line.replace('\n', '')
    line = line.split(' ')
    
    # Read in a neuron and create it, add it to neuron dictionary
    if line[0] == 'N':
        name = line[1]
        Vmem = Vrst
        fire = 0
        threshold = float(line[2])
        refractory = int(line[3])
        # neuron_dict[name] = StochasticNeuron(name, Vmem, threshold, refractory)
        # neuron_dict[name] = Neuron(name, Vmem, threshold, refractory)
        # neuron_dict[name] = Neuron(name, Vmem, threshold, refractory, stochastic=True, rng=rng)
        neuron_dict[name] = Neuron(name, Vmem, threshold, refractory, stochastic=False, rng=rng)
    
    # Read in a synapse and create it
    elif line[0] == 'S':
        pre = neuron_dict[line[1]]
        post = neuron_dict[line[2]]
        Geff = float(line[3])
        delay = int(line[4])
        weight = int(line[5])
        # wp = float(line[5])*1e3 # TODO --> Right place to do this conversion???
        # wn = float(line[6])*1e3
        syn = Synapse(weight, delay, pre, post)
        synapse_list.append(syn)

        # Add connected synapses to each neuron (full model of connectivity)
        post.in_syn_list.append(syn)

    #####################################################################
    # TODO --> Check how this is supposed to work with Nick or Adnan 
    #####################################################################
    # Determine if an input needs to be connected to a neuron
    elif line[0] == 'INPUT':
        #print('Input is connected to', line[2])
        neuron = neuron_dict[line[2]]
        index = count
        count += 1 # TODO --> FIX THIS (Or rather just don't use it)
        input_synapse = input_synapse_list[index]
        input_synapse.post = neuron
        neuron.in_syn_list.append(input_synapse)
        synapse_list.append(input_synapse)



    # A hacky way to stop reading network components  <-- TODO --> FIX THIS
    elif line[0] == '#':
        #print('Finished reading network')
        break

    # Default case to catch all other lines
    else:
        pass





# for line in lines:
#     line = line.replace('\n', '')
#     line = line.split(' ')
# 
#     if line [1] == 'I':
#         name = line[2]
#         Vmem = Vrst
#         fire = 0
#         threshold = line[3]
#         refractory = 0
#         neuron_dict[name] = Neuron(name, Vmem, threshold, refractory, stochastic=False, rng=rng)
#     
#     elif line[1] == 'O':
#         name = line[2]
#         Vmem = Vrst
#         fire = 0
#         threshold = float(line[3])
#         refractory = 0
#         neuron_dict[name] = Neuron(name, Vmem, threshold, refractory, stochastic=False, rng=rng)
# 
#     elif line[1] == 'S':
#         pre = neuron_dict[line[2]]
#         post = neuron_dict[line[3]]
#         delay = int(line[4])
#         weight = int(line[4])
        


for clk in range(SIM_CYCLES-2):
    for synapse in synapse_list:
        synapse.shift_spikes(clk)
    for neuron in neuron_dict:
        neuron_dict[neuron].accum(clk)
    rng.step()
    

np.set_printoptions(precision=2)

# Print the result (did the output neuron fire?)
output = neuron_dict['O0'].fire[14]
print(output)

#sp = SpikePlotter()
#sp.plot(neuron_dict['I0'].fire, neuron_dict['I1'].fire, neuron_dict['I2'].fire, neuron_dict['I3'].fire, neuron_dict['I4'].fire, neuron_dict['O0'].fire)
