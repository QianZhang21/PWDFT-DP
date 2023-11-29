import os
import numpy as np

path = os.getcwd()


def get_position(filename):
    with open(filename, 'r') as f:
        text = f.readlines()
        Atom_Num = text[6].split()
        Atom_Num_total = 0
        for num in Atom_Num:
            Atom_Num_total = Atom_Num_total + eval(num)

        cell = np.zeros((3, 3))
        cell[0, 0] = cell[1, 1] = cell[2, 2] = list(map(float, text[2].split()))[0]

        pos_fractional = []
        for index in range(8, 8 + Atom_Num_total):
            for pos_ in text[index].split()[:3]:
                pos_fractional.append(float(pos_))
        pos_fractional = np.array(pos_fractional).reshape(-1, 3)
        pos_cartesian = np.dot(pos_fractional, cell)

        with open(os.path.join(path, "position"), 'a+') as p:
            for row in range(len(pos_cartesian)):
                for column in range(3):
                    print(pos_cartesian[row, column], end=' ', file=p)
            print(file=p)


with open("pos_dirname.txt", 'r') as file:
    read_rows = file.readlines()
    for row in read_rows:
        first_dir = row.split("-")[0]
        second_file = row.split(".")[0] + '.' + row.split(".")[1]
        get_position(os.path.join(path, first_dir, "config", second_file))

pos_array = np.loadtxt(os.path.join(path, "position"), delimiter=None)
np.save("coord.npy", pos_array.astype(np.float32))