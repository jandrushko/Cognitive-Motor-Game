import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import re

def plot_combined_data(group_files, output_directory, group_name, show_axes=True, show_grid=True, show_legend=True):
    # Initialize a figure for combined path plotting
    plt.figure(figsize=(15, 7))
    ax = plt.gca()

    # Colors for each file
    colors = plt.cm.viridis(np.linspace(0, 1, len(group_files)))

    # Flags to ensure legend entries are only added once
    mouse_path_added = False
    target_path_added = False

    # Flags to ensure star legends are only added once
    start_added = False
    target_intercept_added = False
    end_added = False

    # To store overall min and max coordinates for centering
    all_x = []
    all_y = []

    # To store start and target box coordinates
    start_box_coords = None
    target_box_coords = None

    for idx, file_path in enumerate(group_files):
        # Load the data from CSV
        data = pd.read_csv(file_path)

        # Ensure the required columns exist
        if data.shape[1] > 7:
            x = data.iloc[:, 0]
            y = data.iloc[:, 1]
            velocity = data.iloc[:, 3]
            all_x.extend(x)
            all_y.extend(y)
            
            # Get start and target box coordinates from the first row of the file
            if start_box_coords is None and target_box_coords is None:
                start_box_coords = (data.iloc[0, 4], data.iloc[0, 5])
                target_box_coords = (data.iloc[0, 6], data.iloc[0, 7])
        else:
            print(f"File {file_path} does not have enough columns.")
            continue

    if not all_x or not all_y:
        print("No valid data found in the files.")
        return

    # Shift the coordinates to center the paths
    all_x = np.array(all_x)
    all_y = np.array(all_y)
    x_shift = start_box_coords[0]
    y_shift = start_box_coords[1]
    all_x -= x_shift
    all_y -= y_shift

    # Update the start and target box coordinates based on the shift
    start_box_coords = (0, 0)
    target_box_coords = (target_box_coords[0] - x_shift, target_box_coords[1] - y_shift)

    # Plot the start and target boxes first
    if start_box_coords:
        start_box = plt.Rectangle((start_box_coords[0] - 50, start_box_coords[1] - 50), 100, 100, linewidth=2, edgecolor='yellow', facecolor='none', label='Start Box')
        ax.add_patch(start_box)

    if target_box_coords:
        target_box = plt.Rectangle((target_box_coords[0] - 75, target_box_coords[1] - 100), 150, 200, linewidth=2, edgecolor='purple', facecolor='none', label='Target Box')
        ax.add_patch(target_box)

    for idx, file_path in enumerate(group_files):
        # Load the data from CSV
        data = pd.read_csv(file_path)

        if data.shape[1] <= 7:
            continue

        # Assuming the columns by index as earlier explained
        x = data.iloc[:, 0] - x_shift
        y = data.iloc[:, 1] - y_shift
        velocity = data.iloc[:, 3]

        # Prepare the data for LineCollection
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # Choose color palette and legend label based on file name
        if 'congruent_coords' in file_path:
            lc = LineCollection(segments, colors='black', linestyles='dashed')
            if not target_path_added:
                label = "Target Path"
                target_path_added = True
            else:
                label = "_nolegend_"  # Hide subsequent labels
        else:
            lc = LineCollection(segments, cmap='viridis', norm=plt.Normalize(velocity.min(), velocity.max()), linestyles='solid')
            lc.set_array(velocity[:-1])  # Color the lines based on velocity
            if not mouse_path_added:
                label = "Mouse Path"
                mouse_path_added = True
            else:
                label = "_nolegend_"  # Hide subsequent labels
            
            # Add stars for the phase-start and phase-deliver points
            if 'phase-start' in file_path:
                # Mark the starting point of phase-start
                if not start_added:
                    ax.plot(x.iloc[0], y.iloc[0], marker='*', markersize=10, color='blue', label='Start')
                    start_added = True
                else:
                    ax.plot(x.iloc[0], y.iloc[0], marker='*', markersize=10, color='blue')
            elif 'phase-deliver' in file_path:
                # Mark the beginning and end points of phase-deliver
                if not target_intercept_added:
                    ax.plot(x.iloc[0], y.iloc[0], marker='*', markersize=10, color='green', label='Target Intercept')
                    target_intercept_added = True
                else:
                    ax.plot(x.iloc[0], y.iloc[0], marker='*', markersize=10, color='green')
                
                if not end_added:
                    ax.plot(x.iloc[-1], y.iloc[-1], marker='*', markersize=10, color='red', label='End')
                    end_added = True
                else:
                    ax.plot(x.iloc[-1], y.iloc[-1], marker='*', markersize=10, color='red')

        lc.set_linewidth(2)  # Set the line width

        # Add the line collection to the plot
        ax.add_collection(lc)
        
        # Add a legend entry
        ax.plot([], [], color='black' if 'congruent_coords' in file_path else colors[idx % len(colors)], 
                linestyle='dashed' if 'congruent_coords' in file_path else 'solid', label=label)

    plt.colorbar(lc, label='Velocity (pixels/second)')
    plt.title(f'Movement Paths Coloured by Velocity - {group_name}')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    if show_grid:
        plt.grid(True)
    else:
        plt.grid(False)
    if not show_axes:
        ax.axis('off')
    if show_legend:
        plt.legend()
    plt.savefig(os.path.join(output_directory, group_name + '_combined.png'))
    plt.close()

    # Plot Velocity for each file
    for file_path in group_files:
        # Load the data from CSV
        data = pd.read_csv(file_path)

        if data.shape[1] <= 7:
            continue

        velocity = data.iloc[:, 3]

        # Plot Velocity for phase-start, ignoring zeros
        if 'phase-start' in file_path or 'phase-deliver' in file_path:
            plt.figure(figsize=(10, 5))
            filtered_velocity = velocity[velocity != 0]
            filtered_time = filtered_velocity.index

            plt.plot(filtered_time, filtered_velocity, marker='o', linestyle='-', color='r')
            plt.title(f'Velocity Over Time (Non-Zero Values) - {group_name}')
            plt.xlabel('Time')
            plt.ylabel('Velocity (pixels/second)')
            if show_grid:
                plt.grid(True)
            else:
                plt.grid(False)
            if not show_axes:
                plt.gca().axis('off')
            if show_legend:
                plt.legend()
            plt.savefig(os.path.join(output_directory, os.path.basename(file_path).replace('.csv', '_velocity.png')))
            plt.close()

# Set the root directory to the 'rawdata' directory within the user's home directory
home_dir = os.path.expanduser("~")
root_directory = os.path.join(home_dir, 'Cognitive-Motor_Game_Results', 'rawdata')
sub_dirs = glob.glob(os.path.join(root_directory, 'sub-*', 'ses-*'))

# Regular expression to extract the round and level numbers
round_level_pattern = re.compile(r'round-(\d+)_level-(\d+)')

for directory in sub_dirs:
    print(f"Processing directory: {directory}")  # Debug print

    # Collect all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    
    # Group files by round and level
    groups = {}
    for file in csv_files:
        match = round_level_pattern.search(os.path.basename(file))
        if match:
            group_name = f'round-{match.group(1)}_level-{match.group(2)}'
            if group_name not in groups:
                groups[group_name] = []
            groups[group_name].append(file)
    
    # Plot data for each group (round and level)
    for group_name, group_files in groups.items():
        plot_combined_data(group_files, directory, group_name, show_axes=True, show_grid=False, show_legend=False)
