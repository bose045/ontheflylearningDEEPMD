import csv
import statistics
import matplotlib.pyplot as plt

row_count = 0 #number of atoms
col_count = 0 #number of frames
frames = []
max_values = []
results = []
values = []
with open('md.out', 'r') as csv_file:
    
    next(csv_file)

    for line in csv_file:
        row = list(map(float, line.strip().split()))
        row_count += 1
        col_count = len(row)-7
 #       print('col_count: ',col_count)
        values.append(row) #skip the first 7 columns

#print('Length ',len(values[-1]))


def read_time_series_data(filename):
    try:
        with open(filename, 'r') as dump:
            timestep = []
            Natoms = []
            x_bound = []
            y_bound = []
            z_bound = []
            atom_data = []
            
            i = 0
            for line in dump:
                id = line.strip()
                
                if id.startswith('ITEM: TIMESTEP'):
                    timestep.append(int(next(dump).strip()))
                    print('current timestep: ', timestep[-1])
                    matching_rows = [row for row in values if row[0] == timestep[-1]]
                    print('matching rows: ', matching_rows)
                    if matching_rows:
                        extra_values = matching_rows[0][7:]
                        print(extra_values)
                        print('size of extra values: ', len(extra_values))
                elif id.startswith('ITEM: NUMBER OF ATOMS'):
                    Natoms.append(int(next(dump).strip()))
                    print('Number of atoms:',Natoms[-1])

                elif id.startswith('ITEM: BOX BOUNDS'):
                    x_bound.append(list(map(float, next(dump).strip().split())))
                    y_bound.append(list(map(float, next(dump).strip().split())))
                    z_bound.append(list(map(float, next(dump).strip().split())))

                elif id.startswith('ITEM: ATOMS'):
                    atom_data_frame = []
                    for j in range(Natoms[i]):
                        atom_row = list(map(float, next(dump).strip().split()))
                        if 'extra_values' in locals():
                            atom_row.append(extra_values[j])  
                        atom_data_frame.append(atom_row)
                    atom_data.append(atom_data_frame)
                    i += 1
            return {
                'timestep': timestep,
                'Natoms': Natoms,
                'x_bound': x_bound,
                'y_bound': y_bound,
                'z_bound': z_bound,
                'atom_data': atom_data
            }
            
    except FileNotFoundError:
        print("Dumpfile not found!")
        return None
    
def write_time_series_data(filename, data):
    try:
        with open(filename, 'w') as dump:
            for i in range(len(data['timestep'])):
                dump.write("ITEM: TIMESTEP\n")
                dump.write(f"{data['timestep'][i]}\n")
                dump.write("ITEM: NUMBER OF ATOMS\n")
                dump.write(f"{data['Natoms'][i]}\n")
                dump.write("ITEM: BOX BOUNDS\n")
                dump.write(" ".join(map(str, data['x_bound'][i])) + "\n")
                dump.write(" ".join(map(str, data['y_bound'][i])) + "\n")
                dump.write(" ".join(map(str, data['z_bound'][i])) + "\n")
                dump.write("ITEM: ATOMS\n")
                for atom_row in data['atom_data'][i]:
                    dump.write(" ".join(map(str, atom_row)) + "\n")
    except FileNotFoundError:
        print("Could not write to dump file!")
        return None


filename = "lq1.dump" 
data = read_time_series_data(filename)

if data:
    filename_write = "lq_with_modvar.dump"  
    write_time_series_data(filename_write, data)

