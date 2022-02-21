#All modules to be used imported
import argparse
import pandas as pd
import numpy as np
import itertools
import math
import csv
import multiprocessing
from multiprocessing import Pool
parser = argparse.ArgumentParser()
#Cheat sheet of arguments to be used with the script
parser.add_argument("-inp", "--input", dest = "input", default = "input.xyz", help="Name of input file")
parser.add_argument("-out", "--output", dest = "output", default = "output.xyz", help="Name of output file")
args = parser.parse_args()

#Here the necessary interpolation module is imported


#Here the number of atoms is determined by reading in the first value of the xyz file, the number of lines for the whole file is determined and the number of frames calculated using the aforementioned two variables
with open(args.input) as f:
    lines = f.read()
    first = lines.split('\n', 1)[0]
num_of_atoms = int(first)
num_of_lines = len(list(open(args.input)))
num_of_frames = int(num_of_lines/(num_of_atoms+2))

#Here the headers of the xyz file is removed
skiparray = []
for i in range(num_of_frames):
    k = num_of_atoms*i+2*i
    skiparray.append(k)
    skiparray.append(k+1)
df = pd.read_csv(args.input, skiprows=skiparray, names=['Atom', 'X', 'Y', 'Z'], sep="\s+" , engine='python')

#Here the dataframe is split into multiple dataframes, each making up a frame from the file
frames = [ df.iloc[i*num_of_atoms:(i+1)*num_of_atoms].copy() for i in range(num_of_frames+1) ]

for i in range(0,num_of_frames):
    frames[i] = frames[i].reset_index(drop=True)

sumx = 0
sumy = 0
sumz = 0
for i in range(len(frames[1])):
    sumx += frames[1]['X'].iloc[i]
    sumy += frames[1]['Y'].iloc[i]
    sumz += frames[1]['Z'].iloc[i]
MidPoint = (sumx/10,sumy/10,sumz/10)

Distances = []
oldDistances = []

for i in range(len(frames[0])):
    dist = np.sqrt((frames[0]['X'].iloc[i]-MidPoint[0])**2+(frames[0]['Y'].iloc[i]-MidPoint[1])**2+(frames[0]['Z'].iloc[i]-MidPoint[2])**2)
    Distances.append(dist)
    oldDistances.append(dist)

Distances.sort(reverse=True)

newPos = []
for i in range(len(Distances)):
    for j in range(len(oldDistances)):
        if np.abs(Distances[i]-oldDistances[j])<0.001:
            newPos.append(j)

dist2 = []
pos = []
for i in newPos:
    dist1 = []
    pos2 = []
    for j in range(len(frames[1])):
        if j not in pos:
            dist = np.sqrt((frames[0]['X'].iloc[i]-frames[1]['X'].iloc[j])**2+(frames[0]['Y'].iloc[i]-frames[1]['Y'].iloc[j])**2+(frames[0]['Z'].iloc[i]-frames[1]['Z'].iloc[j])**2)
            dist1.append(dist)
            pos2.append(j)
    distMin = min(dist1)
    distMinindex = pos2[dist1.index(distMin)]
    pos.append(distMinindex)

f = open(args.output,"w")
print(num_of_atoms,file=f)
print("Reorganized",file=f)
for i in newPos:
    print(frames[0]['Atom'].iloc[i],frames[0]['X'].iloc[i],frames[0]['Y'].iloc[i],frames[0]['Z'].iloc[i],file=f)
print(num_of_atoms,file=f)
print("Reorganized",file=f)
for j in pos:
    print(frames[1]['Atom'].iloc[j],frames[1]['X'].iloc[j],frames[1]['Y'].iloc[j],frames[1]['Z'].iloc[j],file=f)
f.close()
