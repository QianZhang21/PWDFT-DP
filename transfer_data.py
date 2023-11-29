import os
from glob import glob

import numpy as np


def generate_type_files(filename):
    type_raw = []
    type_map_raw = []
    atom_counter = 0
    with open(filename, 'r') as f:
        lines = f.readlines()
        atomic_symbols = lines[5].split()
        atom_counts = list(map(int, lines[6].split()))

    for i, symbol in enumerate(atomic_symbols):
        type_raw.extend([f"{atom_counter}\n" for type_id in range(atom_counts[i])])
        type_map_raw.extend([f"{symbol}\n"])
        atom_counter += 1
    return type_raw, type_map_raw


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
    return pos_cartesian.reshape(1, -1), cell.reshape(1, -1)


def count_folders(directory):
    return sum(os.path.isdir(os.path.join(directory, d)) for d in os.listdir(directory))


if __name__ == "__main__":
    path = os.getcwd()
    if not os.path.isdir(os.path.join(path, "npy_dir")):
        os.mkdir(os.path.join(path, "npy_dir"))
    else:  # Recreate folder!!
        import shutil
        shutil.rmtree(os.path.join(path, "npy_dir"))
        os.mkdir(os.path.join(path, "npy_dir"))

    txt_prefix = "txt_dir"
    position_prefix = "vasp_dir"
    nopbc = True

    listdir = glob(os.path.join(path, txt_prefix, "*_pos_dirname.txt"))
    for position_file in listdir:
        pos_list = []
        box_list = []
        with open(position_file, 'r') as file:
            read_rows = file.readlines()
            for row in read_rows:
                first_dir = row.split("-")[0]
                second_file = row.split(".")[0] + '.' + row.split(".")[1]
                vasp_position = os.path.join(path, position_prefix, first_dir, "config", second_file)
                pos_, box_ = get_position(vasp_position)
                pos_list.append(pos_)
                box_list.append(box_)
        pos_array = np.squeeze(np.array(pos_list), axis=1).astype(np.float32)
        box_array = np.squeeze(np.array(box_list), axis=1).astype(np.float32)

        if not os.path.isdir(os.path.join(path, "npy_dir", first_dir)):
            os.mkdir(os.path.join(path, "npy_dir", first_dir))

        set_num = count_folders(os.path.join(path, "npy_dir", first_dir))
        save_dir_path = os.path.join(path, "npy_dir", first_dir, "set.00" + str(set_num))
        os.mkdir(save_dir_path)

        np.save(os.path.join(save_dir_path, "coord.npy"), pos_array)
        np.save(os.path.join(save_dir_path, "box.npy"), box_array)

        energy_unit = 27.211324570273
        energy_array = np.loadtxt(os.path.join(path, txt_prefix, first_dir+"_energy.txt"), delimiter=None)
        energy_array /= energy_unit
        np.save(os.path.join(save_dir_path, "energy.npy"), energy_array.astype(np.float32))

        force_unit = 27.2114 / 0.529177
        force_array = np.loadtxt(os.path.join(path, txt_prefix, first_dir+"_force.txt"), delimiter=None)
        force_array *= force_unit
        np.save(os.path.join(save_dir_path, "force.npy"), force_array.astype(np.float32))

        type_raw, type_map_raw = generate_type_files(vasp_position)
        with open(os.path.join(path, "npy_dir", first_dir, 'type.raw'), 'w') as f:
            f.writelines(type_raw)
        with open(os.path.join(path, "npy_dir", first_dir, 'type_map.raw'), 'w') as f:
            f.writelines(type_map_raw)
        if nopbc:
            with open(os.path.join(path, "npy_dir", first_dir, 'nopbc'), 'w') as file:
                pass
