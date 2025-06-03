import numpy as np
import time
from pathlib import Path
from PyBoltz.PyBoltzRun import *
import pandas as pd
import sys
sys.path

# Set up helper object
PBRun=PyBoltzRun()

# Show list of available gases
# PBRun.ListGases()


pressure = int(sys.argv[1])
gas_percentage = float(sys.argv[2])
Additive = sys.argv[3]
print("Using Gas Pressure: ", pressure)
print("Using CO2 Percentage: ", gas_percentage)
print("Using Gas Percentage: ", Additive)

xenon_percentage = 100-gas_percentage


# Configure settings for our simulation
MySettings   ={'Gases'                 :['XENON', Additive],
               'Fractions'             :[xenon_percentage,gas_percentage],
               'Max_collisions'        :5e8,
               'EField_Vcm'            :75,
               'Max_electron_energy'   :0,
               'Temperature_C'         :23,
               'Pressure_Torr'         :pressure*750.062,
               'BField_Tesla'          :0,
               'BField_angle'          :0,
               'Angular_dist_model'    :1,
               'Enable_penning'        :0,
               'Enable_thermal_motion' :1,
               'ConsoleOutputFlag'     :0}


# Create empty lists to store outputs
DriftVels=[]
DriftVels_err=[]
DTs=[]
DLs=[]
DT1s=[]
DL1s=[]
DTs_err=[]
DLs_err=[]
DT1s_err=[]
DL1s_err=[]


# Run for each E field
EFields = np.arange(20,140,10)
EFields = EFields*pressure
EFields = EFields[EFields < 2500]
print("Running with fields:", EFields)
# EFields=[300]

t1=time.time()
for E in EFields:
    print("Running with E Field " +str(E))

    MySettings['EField_Vcm']=E

    Output=PBRun.Run(MySettings)

    DriftVels.append(Output['Drift_vel'].val[2])
    DriftVels_err.append(Output['Drift_vel'].err[2])

    DTs.append(Output['DT'].val)
    DTs_err.append(Output['DT'].err)

    DLs.append(Output['DL'].val)
    DLs_err.append(Output['DL'].err)

    DT1s.append(Output['DT1'].val)
    DT1s_err.append(Output['DT1'].err)

    DL1s.append(Output['DL1'].val)
    DL1s_err.append(Output['DL1'].err)
t2=time.time()

print("Time elapsed:" +str(t2-t1))


df = pd.DataFrame( {"E"         : EFields,
                    "P"         : pressure,
                    "percentage": gas_percentage, 
                    "Additive"  : Additive, 
                    "vd"        : DriftVels,
                    "vd_err"    : DriftVels_err,
                    "DT"        : np.array(DTs),
                    "DTerr"     : np.array(DTs_err), 
                    "DL"        : np.array(DLs), 
                    "DLerr"     : np.array(DLs_err) ,
                    "DT1"       : np.array(DT1s)/1000, 
                    "DT1err"    : np.array(DT1s_err)/1000, 
                    "DL1"       : np.array(DL1s)/1000, 
                    "DL1err"    : np.array(DL1s_err)/1000})

print(df)

df.to_csv(f"Xe_{Additive}_{gas_percentage}percent_{pressure}bar.txt", index=False)