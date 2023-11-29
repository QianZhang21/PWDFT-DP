import os

import numpy as np
from collections import Counter

path = os.getcwd()
prefix_dir = os.path.join(path, "npy_dir//Au14")
coord_file = np.load(os.path.join(prefix_dir, "set.000/coord.npy"))
box_file = np.load(os.path.join(prefix_dir, "set.000/box.npy"))
n_data = coord_file.shape[0]

type_list = np.loadtxt(os.path.join(prefix_dir, "type.raw"), dtype=int)
type_map = np.loadtxt(os.path.join(prefix_dir, "type_map.raw"), dtype=str)
Atomic_num = Counter(type_list)


data_index = int(input(f"The number of data is {n_data}, please enter the data_index：\n")) - 1
coord = coord_file[data_index, :].reshape(-1, 3)
box = box_file[data_index, :].reshape(3, 3)


with open("npy-to-POSCAR.vasp", "w") as vf:
    vf.write("npytoVASP\n")
    vf.write("1.0\n")
    np.savetxt(vf, box)
    if type_map.shape == ():
        print(type_map, file=vf)
    else:
        for atomic_type in type_map:
            print(atomic_type, end="  ", file=vf)
        print(file=vf)
    for key_ in Atomic_num.keys():
        print(Atomic_num[key_], end="  ", file=vf)
    print(file=vf)
    vf.write("Cartesian\n")
    np.savetxt(vf, coord)

