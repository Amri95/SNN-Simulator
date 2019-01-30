# FOR NOW FORMAT AS SCRIPT, NEED TO REFACTOR AS PARAMS CLASS

import configparser

config = configparser.ConfigParser()
config.sections()
config.read('params.ini')

# Dict-like structures for parameters from ini file
gp = config['general_params']
mp = config['memristance_params']
np = config['neuron_params']
ss = config['simulator_settings']

# Set up circuit operating voltages
VDD = float(ss['VDD'])
VSS = float(ss['VSS'])
Vt = VDD - VSS

# Set up STDP and number of simulated cycles
cycles = int(ss['cycles'])
STDP_cycle = int(ss['STDP_cycle'])

# Generate all necessary memristance parameters
HRS = float(mp['HRS'])
LRS = float(mp['LRS'])
tswp = float(mp['tswp'])
tswn = float(mp['tswn'])
Vthp = float(mp['Vthp'])
Vthn = float(mp['Vthn'])
delT = float(mp['delT'])

# Standard deviation multipliers (percent of mean)
_hrs = float(mp['m_HRS'])
_lrs = float(mp['m_LRS'])
_tswn = float(mp['m_tswn'])
_tswp = float(mp['m_tswp'])
_Vthn = float(mp['m_Vthn'])
_Vthp = float(mp['m_Vthp'])

# Statistical memristor parameters
mu_hrs, sigma_hrs = HRS, HRS*_hrs
mu_lrs, sigma_lrs = LRS, LRS*_lrs
mu_tswn, sigma_tswn = tswn, tswn*_tswn
mu_tswp, sigma_tswp = tswp, tswp*_tswp
mu_vtn, sigma_vtn = Vthn, Vthn*_Vthn # Is this right?
mu_vtp, sigma_vtp = Vthp, Vthp*_Vthp # Is this right?

# Memristor increase and decrease intervals
M_dec = (HRS-LRS)*(delT/tswp)*(Vt/Vthp)
M_inc = (HRS-LRS)*(delT/tswn)*(Vt/Vthn)

# Print for verification
print(M_dec)
print(M_inc)
print(cycles)
print(STDP_cycle)
