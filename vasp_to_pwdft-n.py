import os
import sys
from glob import glob

element_ref_dict = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'Na': 11,
                    'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21,
                    'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31,
                    'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40, 'Nb': 41,
                    'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50, 'Sb': 51,
                    'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'Lu': 71, 'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75,
                    'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80, 'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85,
                    'Rn': 86, 'Fr': 87, 'Ra': 88, 'Lr': 103, 'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108,
                    'Mt': 109, 'Ds': 110, 'Rg': 111, 'Cn': 112, 'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117,
                    'Og': 118, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60, 'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65,
                    'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70, 'Ac': 89, 'Th': 90, 'Pa': 91, 'U': 92, 'Np': 93,
                    'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100, 'Md': 101, 'No': 102, 'Lr': 103,
                    'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109, 'Ds': 110, 'Rg': 111, 'Cn': 112,
                    'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117, 'Og': 118 }

path = os.getcwd()
Bohr = 0.529177210905667

if not os.path.isdir("yaml_dir"):
    os.mkdir("yaml_dir")

with open('config_Au.yaml', 'r') as configf:
    configtext = configf.readlines()

dirs = glob("Au*")
for _dir in dirs:
    listdir = glob(os.path.join(_dir, "config/*.vasp"))
    for filename in listdir:
        if 'vasp' in filename and 'sg' in filename:  # if 'vasp' in filename
            with open(filename, 'r') as f:
                text = f.readlines()

                Atom_Type = text[5].split()
                Atom_Types_Num = len(Atom_Type)

                Atom_Type_element_num = []
                for Atom_Type_i in Atom_Type:
                   Atom_Type_element_num.append(str(element_ref_dict[Atom_Type_i]))

                Atom_Num = text[6].split()
                Atom_Num_total = 0
                for num in Atom_Num:
                    Atom_Num_total = Atom_Num_total + eval(num)

                if eval(text[1].split()[0]) == 1:
                    a = list(map(float, text[2].split()))
                    b = list(map(float, text[3].split()))
                    c = list(map(float, text[4].split()))
                    if a[1] < 10E-6 and a[2] < 10E-6 and b[0] < 10E-6 and b[2] < 10E-6 and c[0] < 10E-6 and c[1] < 10E-6:
                        a = a[0] / Bohr
                        b = b[1] / Bohr
                        c = c[2] / Bohr
                        Super_Cell = [a, b, c]
                        Super_Cell = list(map(str, Super_Cell))
                    else:
                        print('Error!')
                else:
                    print('Error!')

                if text[7].split()[0].lower() == 'direct':
                    with open(os.path.join(path, "yaml_dir", filename.split('\\')[-1] + '.yaml'), 'w') as p:
                        for configtext_ in configtext:
                            p.write(configtext_)
                        print('\n', file=p)
                        print('Atom_Types_Num:        ' + str(Atom_Types_Num), file=p)
                        print('Atom_Type:             [ ' + ', '.join(Atom_Type_element_num) + ' ]', file=p)  # 微修
                        print('', file=p)
                        print('Super_Cell: [ ' + ', '.join(Super_Cell) + ' ]', file=p)
                        print('', file=p)
                        print('Atom_Num:   [ ' + ', '.join(Atom_Num) + ' ]', file=p)
                        print('', file=p)
                        print('Atom_Red:', file=p)
                        for index in range(8, 8 + Atom_Num_total):
                            print(' - [ ' + ', '.join(text[index].split()[:3]) + ' ]', file=p)
                else:
                    print('Error!')
