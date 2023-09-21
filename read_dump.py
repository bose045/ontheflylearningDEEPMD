# Initialize variables
timesteps = []
frames = []
total_lines_read = 0  # Counter for total number of lines read

# Open the LAMMPS dump file
with open('lq1.dump', 'r') as file:
    reading_atoms = False
    atom_data = []
    
    for line in file:
        total_lines_read += 1  # Increment the counter
        line = line.strip()
        
        # Check for timestep
        if line == "ITEM: TIMESTEP":
            timestep = int(next(file).strip())
            timesteps.append(timestep)
            total_lines_read += 1  # Increment the counter for the skipped line
        
        # Check for atom data header
        elif line.startswith("ITEM: ATOMS"):
            reading_atoms = True
            atom_data = []
        
        # Skip other headers
        elif line.startswith("ITEM:"):
            reading_atoms = False
        
        # Read atom data
        elif reading_atoms:
            atom_info = list(map(float, line.split()))
            atom_data.append(atom_info)
        
        # Save atom data for the current frame
        if atom_data and not reading_atoms:
            frames.append({"timestep": timestep, "atom_data": atom_data})

# Output the number of frames read and total lines read
print(f"Number of frames read: {len(frames)}")
print(f"Total number of lines read: {total_lines_read}")

# Print timesteps and first frame's atom data to verify
#print("Timesteps:", timesteps)
#print("First frame's atom data:", frames[0]['atom_data'])
