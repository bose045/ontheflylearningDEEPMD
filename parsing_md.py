import csv
import statistics
import matplotlib.pyplot as plt

row_count = 0 #number of atoms
col_count = 0 #number of frames
frames = []
max_values = []
results = []



with open('md.out', 'r') as csv_file:
    
    next(csv_file)

    for line in csv_file:
        row = list(map(float, line.strip().split()))
        row_count += 1
        col_count = len(row)-7
        values = row[7:] #skip the first 7 columns

        max_value = max(values)
        avg_value = statistics.mean(values)
        std_value = statistics.stdev(values)

        results.append([row[0], max_value, avg_value, std_value])
        frames.append(row[0])
        max_values.append(max_value)

with open('mdout_by_frame.out','w') as new_file:
    new_file.write('Step\tMax\tAvg\tStd\n')
    csv_writer = csv.writer(new_file, delimiter='\n')
    csv_writer.writerow(results)



#        print(row)



# Plotting
plt.figure(figsize=(10, 6))
plt.semilogy(frames, max_values, marker='o')
plt.xlim(5000, max(frames))
#plt.ylim(1e0, max(max_values)*1.05)
plt.ylim(1e0, 2.5e0) 
 
plt.xlabel('Frame')
plt.ylabel('Max force dev (eV/Angstrom)')
plt.title('Max Force deviation vs Frame')
plt.grid(True)
plt.show()

print(f'Row count: {row_count}')
print(f'Column count: {col_count}')