import os
import sys
import random
import time
import numpy as np
import tkinter as tk
from tkinter import ttk
import pygame
import csv

def start_game():
    global difficulty_level, subject, session, hand, max_rounds, block, movement, total_blocks, current_block, paused, study_id, initial_window_size
    global font_large_size, movement_speed, words_per_level, use_advanced_settings
    
    # Get the values from the GUI entries
    subject = subject_entry.get()
    session = session_entry.get()
    total_blocks = int(total_blocks_entry.get())
    hand = hand_entry.get()
    max_rounds = int(max_rounds_entry.get())
    movement = move_targets_var.get()
    study_id = study_id_entry.get()
    current_block = 1  # Start with the first block
    block = str(current_block)  # Set the initial block number
    paused = False  # Resume the game

    # Check if Advanced Control is enabled
    if advanced_control_var.get():
        try:
            # User-defined settings
            font_size = int(font_size_combo.get())
            speed = int(speed_combo.get())
            num_targets = int(num_targets_entry.get())

            # Override the default settings with user-defined settings
            font_large_size = {1: font_size}
            movement_speed = {1: speed}
            words_per_level = {1: num_targets}
            use_advanced_settings = True  # Flag to indicate advanced settings are in use
        except ValueError:
            print("Invalid input for advanced control fields. Please enter valid integers.")
            return
    else:
        # Use the difficulty level to determine settings
        difficulty_level = int(difficulty_var.get())
        font_large_size = {1: 70, 2: 65, 3: 60, 4: 55, 5: 50, 6: 45, 7: 40, 8: 35, 9: 30, 10: 25, 11: 25, 12: 25, 13: 25, 14: 25, 15: 25}
        movement_speed = {1: 2, 2: 2, 3: 3, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7, 12: 7, 13: 8, 14: 8, 15: 9}
        words_per_level = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15}
        use_advanced_settings = False  # Flag to indicate default difficulty settings are in use

    # Initialize Pygame and set the initial window size
    pygame.init()
    screen_info = pygame.display.Info()
    initial_window_size = (screen_info.current_w - 300, screen_info.current_h - 300)
    
    reset_game_state()

    # Close the Tkinter GUI window
    root.quit()
    root.destroy()

def reset_game_state():
    global screen, font_large, font_small, current_round, correct_responses, incorrect_responses, missed_targets, block_complete
    global initial_window_size  # Ensure initial_window_size is accessible

    # Reset game state variables
    current_round = 0
    correct_responses = 0
    incorrect_responses = 0
    missed_targets = 0
    block_complete = False

    # Reinitialize pygame display with the previous window size
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(initial_window_size, pygame.RESIZABLE)
    pygame.display.set_caption('Game: Cognitive-Motor')

    font_small = pygame.font.Font(None, 24)
    if use_advanced_settings:
        font_large = pygame.font.Font(None, font_large_size[1])
    else:
        font_large = pygame.font.Font(None, font_large_size[difficulty_level])

def open_input_gui(subject="", session="", total_blocks="", hand="", max_rounds="", difficulty_level="", movement=True, study_id=""):
    global difficulty_var, subject_entry, session_entry, total_blocks_entry, hand_entry, max_rounds_entry
    global move_targets_var, root, study_id_entry, advanced_control_var, font_size_combo, speed_combo, num_targets_entry, difficulty_combo

    root = tk.Tk()
    root.title("Game Settings")

    instructions = """
    Welcome to the Cognitive-Motor Game!
    Written by Dr. Justin W. Andrushko, PhD
    Department of Sport, Exercise and Rehabilitation, Northumbria University.
    Enjoy the game!
    """

    instructions_label = ttk.Label(root, text=instructions, font=('Arial', 10))
    instructions_label.grid(row=0, columnspan=2, padx=10, pady=10)

    subject_label = ttk.Label(root, text="Subject Number:")
    subject_label.grid(row=1, column=0, padx=5, pady=5)
    subject_entry = ttk.Entry(root)
    subject_entry.insert(0, subject)
    subject_entry.grid(row=1, column=1, padx=5, pady=5)

    session_label = ttk.Label(root, text="Session Number:")
    session_label.grid(row=2, column=0, padx=5, pady=5)
    session_entry = ttk.Entry(root)
    session_entry.insert(0, session)
    session_entry.grid(row=2, column=1, padx=5, pady=5)

    study_id_label = ttk.Label(root, text="Study ID:")
    study_id_label.grid(row=3, column=0, padx=5, pady=5)
    study_id_entry = ttk.Entry(root)
    study_id_entry.insert(0, study_id)
    study_id_entry.grid(row=3, column=1, padx=5, pady=5)

    total_blocks_label = ttk.Label(root, text="Number of Blocks:")
    total_blocks_label.grid(row=4, column=0, padx=5, pady=5)
    total_blocks_entry = ttk.Entry(root)
    total_blocks_entry.insert(0, total_blocks)
    total_blocks_entry.grid(row=4, column=1, padx=5, pady=5)

    max_rounds_label = ttk.Label(root, text="Number of Rounds per Block:")
    max_rounds_label.grid(row=5, column=0, padx=5, pady=5)
    max_rounds_entry = ttk.Entry(root)
    max_rounds_entry.insert(0, str(max_rounds))
    max_rounds_entry.grid(row=5, column=1, padx=5, pady=5)
    
    hand_label = ttk.Label(root, text="Hand Assessed:")
    hand_label.grid(row=6, column=0, padx=5, pady=5)
    hand_entry = ttk.Entry(root)
    hand_entry.insert(0, hand)
    hand_entry.grid(row=6, column=1, padx=5, pady=5)

    difficulty_label = ttk.Label(root, text="Difficulty Level:")
    difficulty_label.grid(row=7, column=0, padx=5, pady=5)
    difficulty_var = tk.StringVar()
    difficulty_combo = ttk.Combobox(root, textvariable=difficulty_var)
    difficulty_combo['values'] = tuple(range(1, 16))
    difficulty_combo.set(str(difficulty_level))
    difficulty_combo.grid(row=7, column=1, padx=5, pady=5)

    move_targets_label = ttk.Label(root, text="Move Targets:")
    move_targets_label.grid(row=8, column=0, padx=5, pady=5)
    move_targets_var = tk.BooleanVar(value=movement)
    move_targets_checkbutton = ttk.Checkbutton(root, text="Enable", variable=move_targets_var, onvalue=True, offvalue=False)
    move_targets_checkbutton.grid(row=8, column=1, padx=5, pady=5)

    # Advanced Control
    advanced_control_label = ttk.Label(root, text="Advanced Control:")
    advanced_control_label.grid(row=9, column=0, padx=5, pady=5)
    advanced_control_var = tk.BooleanVar(value=False)
    advanced_control_checkbutton = ttk.Checkbutton(root, text="Enable", variable=advanced_control_var, onvalue=True, offvalue=False, command=toggle_advanced_controls)
    advanced_control_checkbutton.grid(row=9, column=1, padx=5, pady=5)

    # Font size control (using Combobox)
    font_size_label = ttk.Label(root, text="Target Font Size:")
    font_size_label.grid(row=10, column=0, padx=5, pady=5)
    font_size_combo = ttk.Combobox(root, values=[70, 65, 60, 55, 50, 45, 40, 35, 30, 25])
    font_size_combo.grid(row=10, column=1, padx=5, pady=5)
    font_size_combo.config(state="disabled")

    # Movement speed control (using Combobox)
    speed_label = ttk.Label(root, text="Movement Speed:")
    speed_label.grid(row=11, column=0, padx=5, pady=5)
    speed_combo = ttk.Combobox(root, values=list(range(2, 11)))
    speed_combo.grid(row=11, column=1, padx=5, pady=5)
    speed_combo.config(state="disabled")

    # Number of targets control
    num_targets_label = ttk.Label(root, text="Number of Targets:")
    num_targets_label.grid(row=12, column=0, padx=5, pady=5)
    num_targets_entry = ttk.Entry(root)
    num_targets_entry.grid(row=12, column=1, padx=5, pady=5)
    num_targets_entry.config(state="disabled")

    start_button = ttk.Button(root, text="Enter", command=start_game)
    start_button.grid(row=13, columnspan=2, padx=5, pady=5)

    root.mainloop()

def toggle_advanced_controls():
    if advanced_control_var.get():
        font_size_combo.config(state="normal")
        speed_combo.config(state="normal")
        num_targets_entry.config(state="normal")
        difficulty_combo.config(state="disabled")  # Disable difficulty level selection
    else:
        font_size_combo.config(state="disabled")
        speed_combo.config(state="disabled")
        num_targets_entry.config(state="disabled")
        difficulty_combo.config(state="normal")  # Enable difficulty level selection

# Initialize game by opening the input GUI
open_input_gui()

pygame.init()
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((width - 300, height - 300), pygame.RESIZABLE)
pygame.display.set_caption('Game: Cognitive-Motor')

font_small = pygame.font.Font(None, 24)
if use_advanced_settings:
    font_large = pygame.font.Font(None, font_large_size[1])
else:
    font_large = pygame.font.Font(None, font_large_size[difficulty_level])

# Define the colors for buttons
button_color = (0, 200, 0)
button_hover_color = (0, 255, 0)

def calculate_positions(width, height):
    start_box = pygame.Rect(width // 2 - 50, height // 2 - 50, 100, 100)
    left_box = pygame.Rect(50, height - 300, 150, 200)
    
    # Adjust these values to change the size of the button
    button_width = 200  # New width of the button
    button_height = 60  # New height of the button

    button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 + 50, button_width, button_height)
    
    word_area_start = 300
    word_area_width = width - 600
    return start_box, left_box, button_rect, word_area_start, word_area_width

def update_positions():
    global start_box, left_box, button_rect, word_area_start, word_area_width, width, height
    width, height = screen.get_size()
    start_box, left_box, button_rect, word_area_start, word_area_width = calculate_positions(width, height)

# Initial calculation of positions
start_box, left_box, button_rect, word_area_start, word_area_width = calculate_positions(width, height)

# Force an initial update of the positions and the display
update_positions()
pygame.display.flip()

colors = {'ORANGE': (255, 140, 0), 'Yellow': (255, 255, 0), 'Red': (255, 0, 0)}
color_names = list(colors.keys())

start_label_text = 'Start'
congruent_label_text = 'Congruent'

start_label_surface = font_small.render(start_label_text, True, (255, 255, 255))
congruent_label_surface = font_small.render(congruent_label_text, True, (255, 255, 255))

start_label_rect = start_label_surface.get_rect(center=start_box.center)
congruent_label_rect = congruent_label_surface.get_rect(center=left_box.center)

screen.blit(font_small.render("Start", True, (255, 255, 255)), (start_box.x + 10, start_box.top + 5))
screen.blit(font_small.render("Congruent", True, (255, 255, 255)), (left_box.x + 10, left_box.top + 5))

waiting = False
start_time = None
target_words_appear_time = None  # New variable to track target words appearance time

clock = pygame.time.Clock()
fps = 60

current_words = []
start_phase_coords = []
target_phase_coords = []
current_round = 0
in_round = False
selected_word = None
dragging = False
path_length = 0
path_length_outside_target = 0
last_mouse_pos = None
correct_responses = 0
incorrect_responses = 0
missed_targets = 0
mouse_left_start_time = None
reaction_times = {'congruent_correct': [], 'congruent_incorrect': [], 'incongruent_correct': [], 'incongruent_incorrect': []}
round_coordinates = {'start_phase_coords': {}, 'target_phase_coords': {}}
congruent_word_coords = {}
reaction_time_to_target = []
reaction_time_from_start = 0
mouse_left_target_time = None
block_start_time = None
block_end_time = None
block_times = []
block_path_lengths = []
block_path_lengths_outside_target = []
last_click_time = 0
click_threshold = 50
dwell_time_from_appearance_to_start = []  # Use a list for multiple rounds
block_complete = False

def create_stroop_words():
    global target_words_appear_time  # Declare it global to modify the value
    
    if use_advanced_settings:
        words_count = words_per_level[1]  # Use advanced user-defined settings
        speed = movement_speed[1]
    else:
        words_count = words_per_level[difficulty_level]
        speed = movement_speed[difficulty_level]

    congruent_index = random.randint(0, words_count - 1)
    words = []

    padding = 20  # Define the minimum distance between words
    max_attempts = 100  # Maximum attempts to place a word without overlap

    for i in range(words_count):
        if i == congruent_index:
            word = color = random.choice(color_names)
        else:
            word, color = random.sample(color_names, 2)

        text_surface = font_large.render(word, True, colors[color])
        text_rect = text_surface.get_rect()

        dx, dy = 0, 0  # Ensure movement is either horizontal or vertical
        placed_successfully = False

        for attempt in range(max_attempts):
            if movement:  # If movement is enabled, assign dx, dy based on a random side
                sides = ['top', 'bottom', 'left', 'right']
                side = random.choice(sides)
                if side == 'top':
                    x = random.randint(text_rect.width // 2 + padding, width - text_rect.width // 2 - padding)
                    y = -text_rect.height // 2  # Start above the screen
                    dx = 0  # No horizontal movement
                    dy = speed  # Move down
                elif side == 'bottom':
                    x = random.randint(text_rect.width // 2 + padding, width - text_rect.width // 2 - padding)
                    y = height + text_rect.height // 2  # Start below the screen
                    dx = 0  # No horizontal movement
                    dy = -speed  # Move up
                elif side == 'left':
                    x = -text_rect.width // 2  # Start to the left of the screen
                    y = random.randint(text_rect.height // 2 + padding, height - text_rect.height // 2 - padding)
                    dx = speed  # Move right
                    dy = 0  # No vertical movement
                elif side == 'right':
                    x = width + text_rect.width // 2  # Start to the right of the screen
                    y = random.randint(text_rect.height // 2 + padding, height - text_rect.height // 2 - padding)
                    dx = -speed  # Move left
                    dy = 0  # No vertical movement

                text_rect.center = (x, y)
            else:  # Random position if movement is not enabled
                x = random.randint(text_rect.width // 2 + padding, width - text_rect.width // 2 - padding)
                y = random.randint(text_rect.height // 2 + padding, height - text_rect.height // 2 - padding)
                text_rect.center = (x, y)

            # Check for overlap with existing words considering the padding
            overlap = False
            for existing_word in words:
                expanded_rect = existing_word['rect'].inflate(padding * 2, padding * 2)
                if text_rect.colliderect(expanded_rect):
                    overlap = True
                    break

            if not overlap:
                placed_successfully = True
                break

        if placed_successfully:
            words.append({
                'text': word, 'color': colors[color], 'congruent': i == congruent_index,
                'rect': text_rect, 'dx': dx, 'dy': dy,
                'original_position': (x, y)  # Save the original position
            })
        else:
            print(f"Failed to place word '{word}' without overlap after {max_attempts} attempts.")

    target_words_appear_time = time.time()

    # Adjust the number of words if space is tight
    if len(words) < words_count:
        print("Not all words could be placed without overlap. Consider reducing word count or padding.")

    return words

def convert_to_cartesian(pygame_pos, height):
    x, y = pygame_pos
    cartesian_y = height - y
    return x, cartesian_y

def adjust_coordinates(coords, origin):
    return [(x - origin[0], y - origin[1], t) for (x, y, t) in coords]

def handle_mouse_movement(phase, round_num):
    global round_coordinates
    pos = pygame.mouse.get_pos()
    current_time = time.time()
    pos = convert_to_cartesian(pos, height)
    if phase == "before_click":
        if round_num not in round_coordinates['start_phase_coords']:
            round_coordinates['start_phase_coords'][round_num] = []
        round_coordinates['start_phase_coords'][round_num].append((pos[0], pos[1], current_time))
    elif phase == "after_click":
        if round_num not in round_coordinates['target_phase_coords']:
            round_coordinates['target_phase_coords'][round_num] = []
        round_coordinates['target_phase_coords'][round_num].append((pos[0], pos[1], current_time))

def save_all_coords():
    # Use expanduser("~") to get the home directory
    results_directory = os.path.join(os.path.expanduser("~"), "Cognitive-Motor_Game_Results", "rawdata", f"ID-{study_id}", f"sub-{subject}", f"ses-{session}")
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
        print(f"Created directory {results_directory}")

    start_box_x, start_box_y = convert_to_cartesian(start_box.center, height)

    for round_num, coords in round_coordinates['start_phase_coords'].items():
        if advanced_control_var.get():
            # Use font size, speed, and number of targets in the filename
            filename = os.path.join(results_directory, f"sub-{subject}_ses-{session}_ID-{study_id}_hand-{hand}_block-{block}_round-{round_num}_font-{font_large_size[1]}_speed-{movement_speed[1]}_targets-{words_per_level[1]}_phase-start.csv")
        else:
            # Use difficulty level in the filename
            filename = os.path.join(results_directory, f"sub-{subject}_ses-{session}_ID-{study_id}_hand-{hand}_block-{block}_round-{round_num}_level-{difficulty_level}_phase-start.csv")
        
        adjusted_coords = adjust_coordinates(coords, (start_box_x, start_box_y))
        save_coords_to_csv(adjusted_coords, filename, save_boxes=True, start_box_origin=(start_box_x, start_box_y))

    for round_num, coords in round_coordinates['target_phase_coords'].items():
        if advanced_control_var.get():
            # Use font size, speed, and number of targets in the filename
            filename = os.path.join(results_directory, f"sub-{subject}_ses-{session}_ID-{study_id}_hand-{hand}_block-{block}_round-{round_num}_font-{font_large_size[1]}_speed-{movement_speed[1]}_targets-{words_per_level[1]}_phase-deliver.csv")
        else:
            # Use difficulty level in the filename
            filename = os.path.join(results_directory, f"sub-{subject}_ses-{session}_ID-{study_id}_hand-{hand}_block-{block}_round-{round_num}_level-{difficulty_level}_phase-deliver.csv")
        
        adjusted_coords = adjust_coordinates(coords, (start_box_x, start_box_y))
        save_coords_to_csv(adjusted_coords, filename, save_boxes=True, start_box_origin=(start_box_x, start_box_y))

def save_congruent_coords():
    # Use expanduser("~") to get the home directory
    results_directory = os.path.join(os.path.expanduser("~"), "Cognitive-Motor_Game_Results", "rawdata", f"ID-{study_id}", f"sub-{subject}", f"ses-{session}")
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)

    start_box_x, start_box_y = convert_to_cartesian(start_box.center, height)

    for round_num, coords in congruent_word_coords.items():
        if advanced_control_var.get():
            # Use font size, speed, and number of targets in the filename
            filename = os.path.join(results_directory, f"sub-{subject}_ses-{session}_ID-{study_id}_hand-{hand}_block-{block}_round-{round_num}_font-{font_large_size[1]}_speed-{movement_speed[1]}_targets-{words_per_level[1]}_congruent_coords.csv")
        else:
            # Use difficulty level in the filename
            filename = os.path.join(results_directory, f"sub-{subject}_ses-{session}_ID-{study_id}_hand-{hand}_block-{block}_round-{round_num}_level-{difficulty_level}_congruent_coords.csv")
        
        adjusted_coords = adjust_coordinates(coords, (start_box_x, start_box_y))
        save_coords_to_csv(adjusted_coords, filename, save_boxes=True, start_box_origin=(start_box_x, start_box_y))

def save_coords_to_csv(coords, filename, save_boxes=False, start_box_origin=(0, 0)):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        start_box_x, start_box_y = start_box_origin
        target_box_x, target_box_y = convert_to_cartesian(left_box.center, height)
        target_box_x -= start_box_x
        target_box_y -= start_box_y

        if save_boxes:
            writer.writerow(['X', 'Y', 'Time', 'Velocity (pixels/second)', 'start_box_x', 'start_box_y', 'target_box_x', 'target_box_y'])
        else:
            writer.writerow(['X', 'Y', 'Time', 'Velocity (pixels/second)'])
        
        for i in range(1, len(coords)):
            x1, y1, t1 = coords[i-1]
            x2, y2, t2 = coords[i]
            distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            time_diff = t2 - t1
            if time_diff > 0:
                velocity = distance / time_diff
            else:
                velocity = 0
            if save_boxes:
                writer.writerow([x1, y1, t1, velocity, 0, 0, target_box_x, target_box_y])
            else:
                writer.writerow([x1, y1, t1, velocity])
        if coords:
            x, y, t = coords[-1]
            if save_boxes:
                writer.writerow([x, y, t, 0, 0, 0, target_box_x, target_box_y])
            else:
                writer.writerow([x, y, t, 0])

def save_results():
    # Use expanduser("~") to get the home directory
    results_directory = os.path.join(os.path.expanduser("~"), "Cognitive-Motor_Game_Results", "rawdata", f"ID-{study_id}", f"sub-{subject}", f"ses-{session}")
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
        print(f"Created directory {results_directory}")
    
    # Determine the filename based on whether advanced control is enabled
    if advanced_control_var.get():
        # Use font size, speed, and number of targets in the filename
        filename = os.path.join(results_directory, f"sub-{subject}_ses-{session}_ID-{study_id}_hand-{hand}_block-{block}_font-{font_large_size[1]}_speed-{movement_speed[1]}_targets-{words_per_level[1]}_results.txt")
    else:
        # Use difficulty level in the filename
        filename = os.path.join(results_directory, f"sub-{subject}_ses-{session}_ID-{study_id}_hand-{hand}_block-{block}_level-{difficulty_level}_results.txt")
    
    with open(filename, "w") as file:
        file.write(f"Date/Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Subject: {subject}\n")
        file.write(f"Session: {session}\n")
        file.write(f"Study ID: {study_id}\n")
        file.write(f"Block: {block}\n")
        file.write(f"Total Rounds: {max_rounds}\n")
        file.write(f"Hand: {hand}\n")
        file.write(f"Movement: {movement}\n")
        if advanced_control_var.get():
            file.write(f"Advanced Controls: Enabled\n")
            file.write(f"Font Size: {font_large_size[1]}\n")
            file.write(f"Movement Speed: {movement_speed[1]}\n")
            file.write(f"Number of Targets: {words_per_level[1]}\n")
        else:
            file.write(f"Difficulty Level: {difficulty_level}\n")
        file.write(f"Incorrect Responses: {incorrect_responses}\n")
        file.write(f"Missed Trials: {missed_targets}\n")
        success_rate = ((max_rounds - missed_targets) / max_rounds) * 100
        file.write(f"Success Rate: {success_rate:.2f}%\n")
        file.write(f"====================================\n")
        
        for result in round_results:
            if result['block_number'] == int(block):  # Only save results for the current block
                file.write(f"Block {block}, Round {result['round_number']} Completion Time: {result['block_time']:.2f} seconds\n")
                if result['status'] == 'success':
                    file.write(f"Block {block}, Round {result['round_number']} Status: Correct\n")
                    file.write(f"Round {result['round_number']} Time to target from start zone: {result['reaction_time_to_target']:.2f} ms\n")
                    file.write(f"Round {result['round_number']} Dwell time: {result['dwell_time']:.2f} ms\n")
                    file.write(f"Round {result['round_number']} Drag Reaction Time: {result['reaction_time']:.2f} ms\n")
                    file.write(f"Round {result['round_number']} Drag Path Length: {result['path_length']:.2f} pixels\n")
                    file.write(f"Round {result['round_number']} Total Path Length: {result['path_length_outside_target']:.2f} pixels\n")
                elif result['status'] == 'incorrect':
                    file.write(f"Block {block}, Round {result['round_number']} Status: Incorrect\n")
                    file.write(f"Round {result['round_number']} Time to target from start zone: {result['reaction_time_to_target']:.2f} ms\n")
                    file.write(f"Round {result['round_number']} Dwell time: {result['dwell_time']:.2f} ms\n")
                    file.write(f"Round {result['round_number']} Drag Reaction Time: {result['reaction_time']:.2f} ms\n")
                    file.write(f"Round {result['round_number']} Drag Path Length: {result['path_length']:.2f} pixels\n")
                    file.write(f"Round {result['round_number']} Total Path Length: {result['path_length_outside_target']:.2f} pixels\n")
                else:
                    file.write(f"Block {block}, Round {result['round_number']} Status: Missed\n")
                file.write(f"====================================\n")

def start_next_block():
    global block, current_block, total_blocks, block_complete
    current_block += 1
    if current_block <= total_blocks:
        block = str(current_block)
        reset_game_state()
        block_complete = False
    else:
        global running
        running = False  # End the game after the last block
        print("All blocks completed. Saving Results...")
        save_results()
        save_all_coords()
        save_congruent_coords()
        pygame.quit()
        sys.exit()

def display_instructions(screen, font):
    instructions_text = [
        "To begin, maximize the game window.",
        "During gameplay, drag the congruent target (the word and color match) to the 'congruent' box.",
        "The goal is to be as fast and accurate as possible.",
        "Place the mouse in the start box and wait for the targets to appear.",
        "After all rounds are completed, click the button to start the next block."
    ]

    width, height = screen.get_size()
    text_height = font.get_height()
    padding = 10
    total_height = padding * 2 + (text_height * len(instructions_text)) + ((len(instructions_text) - 1) * 5)
    text_widths = [font.size(line)[0] for line in instructions_text]
    max_width = max(text_widths) + 2 * padding
    box_x = (width - max_width) // 2
    box_y = 20

    background_color = (0, 0, 139)  # Dark blue
    pygame.draw.rect(screen, background_color, (box_x, box_y, max_width, total_height))

    text_color = (255, 255, 224)  # Light yellow
    for idx, line in enumerate(instructions_text):
        text_surface = font.render(line, True, text_color)
        text_x = box_x + (max_width - text_widths[idx]) // 2
        text_y = box_y + padding + idx * (text_height + 5)
        screen.blit(text_surface, (text_x, text_y))

def draw_button(screen, text, rect, color, hover_color):
    mouse = pygame.mouse.get_pos()
    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)

    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# Main game loop
show_instructions = True
running = True
paused = False  # New flag to pause the game
missed_rounds = []  # List to track missed rounds
round_results = []  # List to track results of each round

while running:
    if paused:
        pygame.event.wait()  # Wait for an event and avoid consuming CPU
        continue
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game window closed. Saving Results...")
            save_results()
            save_all_coords()
            save_congruent_coords()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            update_positions()
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            display_instructions(screen, font_small)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if block_complete and button_rect.collidepoint(event.pos):
                if current_block < total_blocks:
                    start_next_block()
                else:
                    running = False
                    print("All blocks completed. Saving Results...")
                    save_results()
                    save_all_coords()
                    save_congruent_coords()
                    pygame.quit()
                    sys.exit()

            current_click_time = pygame.time.get_ticks()
            if last_click_time and current_click_time - last_click_time < click_threshold:
                print("Double click detected, ignoring.")
            else:
                for word in current_words:
                    inflated_rect = word['rect'].inflate(40, 40)
                    if inflated_rect.collidepoint(event.pos):
                        selected_word = word
                        dragging = True
                        selected_word['start_time'] = time.time()
                        handle_mouse_movement("before_click", current_round)
                        last_mouse_pos = event.pos
                        if mouse_left_start_time is not None and selected_word['congruent']:
                            reaction_time_from_start = round((time.time() - mouse_left_start_time) * 1000, 2)
                            print(f"Reaction time from start zone: {reaction_time_from_start:.2f} ms")
                            reaction_time_to_target.append(reaction_time_from_start)
                        break
            last_click_time = current_click_time
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging and selected_word:
                dragging = False
                handle_mouse_movement("after_click", current_round)
                correct = left_box.collidepoint(event.pos) and selected_word['congruent']
                block_end_time = time.time()
                block_time = block_end_time - block_start_time
                if correct:
                    end_time = time.time()
                    reaction_time = (end_time - selected_word['start_time']) * 1000
                    category_key = 'congruent_correct'
                    reaction_times[category_key].append(reaction_time)
                    correct_responses += 1
                    if selected_word in current_words:
                        current_words.remove(selected_word)
                    in_round = False
                    round_results.append({
                        'round_number': current_round,
                        'status': 'success',
                        'block_number': int(block),  # Add block number to each round's result
                        'block_time': block_time,
                        'reaction_time_to_target': reaction_time_from_start,
                        'dwell_time': dwell_time_from_appearance_to_start[-1],
                        'reaction_time': reaction_time,
                        'path_length': path_length,
                        'path_length_outside_target': path_length_outside_target
                    })
                    block_times.append(block_time)
                    block_path_lengths.append(path_length)
                    block_path_lengths_outside_target.append(path_length_outside_target)
                    path_length = 0
                    path_length_outside_target = 0

                    # After the final round's completion, set block_complete to True
                    if current_round >= max_rounds:
                        block_complete = True

                    if in_round == False:
                        current_words.clear()
                        in_round = False
                else:
                    incorrect_responses += 1
                    round_results.append({
                        'round_number': current_round,
                        'status': 'incorrect',
                        'block_number': int(block),  # Add block number to each round's result
                        'block_time': block_time,
                        'reaction_time_to_target': reaction_time_from_start,
                        'dwell_time': dwell_time_from_appearance_to_start[-1],
                        'reaction_time': (time.time() - selected_word['start_time']) * 1000,
                        'path_length': path_length,
                        'path_length_outside_target': path_length_outside_target
                    })
                    selected_word['rect'].center = selected_word['original_position']
                selected_word = None
        elif event.type == pygame.MOUSEMOTION:
            if in_round:
                current_pos = np.array(event.pos)
                if last_mouse_pos is not None:
                    last_pos = np.array(last_mouse_pos)
                    movement_vector = current_pos - last_pos
                    movement_distance = np.linalg.norm(movement_vector)
                    path_length_outside_target += movement_distance
                if start_box.collidepoint(event.pos):
                    mouse_left_start_time = None
                elif mouse_left_start_time is None:
                    mouse_left_start_time = time.time()
                    if target_words_appear_time is not None:
                        dwell_time_from_appearance_to_start_value = (mouse_left_start_time - target_words_appear_time) * 1000
                        dwell_time_from_appearance_to_start.append(dwell_time_from_appearance_to_start_value)
                        print(f"Dwell time: {dwell_time_from_appearance_to_start_value:.2f} ms")
                handle_mouse_movement("after_click" if dragging else "before_click", current_round)
                if dragging and selected_word and last_mouse_pos is not None:
                    selected_word['rect'].center = pygame.mouse.get_pos()
                    path_length += movement_distance
                last_mouse_pos = event.pos

    screen.fill((0, 0, 0))

    if show_instructions:
        display_instructions(screen, font_small)
        if current_round > 0:
            show_instructions = False

    if not block_complete:
        if start_box.collidepoint(pygame.mouse.get_pos()):
            current_time = time.time()
            if not waiting and not in_round and current_round < max_rounds:
                waiting = True
                start_wait_time = random.randint(2, 4)
                start_time = current_time
            elif waiting and (current_time - start_time) >= start_wait_time:
                waiting = False
                current_words = create_stroop_words()
                in_round = True
                current_round += 1
                block_start_time = current_time

        if move_targets_var.get():
            for word in current_words:
                word['rect'].x += word['dx']
                word['rect'].y += word['dy']

                if word['rect'].top > height or word['rect'].bottom < 0 or word['rect'].left > width or word['rect'].right < 0:
                    if word['congruent']:
                        missed_targets += 1
                        print("Congruent word missed. Ending round...")
                        missed_rounds.append(current_round)
                        round_results.append({
                            'round_number': current_round,
                            'status': 'missed',
                            'block_number': int(block),  # Add block number to each round's result
                            'block_time': 0,
                            'reaction_time_to_target': 0,
                            'dwell_time': 0,
                            'reaction_time': 0,
                            'path_length': 0,
                            'path_length_outside_target': 0
                        })
                        in_round = False
                        current_words.clear()
                        break
                    else:
                        current_words.remove(word)

        pygame.draw.rect(screen, (255, 140, 0), start_box)
        pygame.draw.rect(screen, (255, 255, 255), left_box, 5)
        screen.blit(start_label_surface, start_label_surface.get_rect(center=start_box.center))
        screen.blit(congruent_label_surface, congruent_label_surface.get_rect(center=left_box.center))

        for word in current_words:
            if word['congruent']:
                round_num = current_round
                if round_num not in congruent_word_coords:
                    congruent_word_coords[round_num] = []
                word_pos_cartesian = convert_to_cartesian(word['rect'].center, height)
                congruent_word_coords[round_num].append((word_pos_cartesian[0], word_pos_cartesian[1], time.time()))
            screen.blit(font_large.render(word['text'], True, word['color']), word['rect'].topleft)

    if block_complete:
        # Save results immediately after block completion
        save_results()
        save_all_coords()
        save_congruent_coords()

        # Display "Block Complete" message
        block_complete_surface = font_large.render("Block Complete", True, (255, 255, 255))
        block_complete_rect = block_complete_surface.get_rect(center=(start_box.centerx, start_box.centery - 100))
        screen.blit(block_complete_surface, block_complete_rect)

        # Update the button text based on whether it's the last block
        if current_block < total_blocks:
            button_text = "Start Next Block"
        else:
            button_text = "End Game"

        # Draw the button
        draw_button(screen, button_text, button_rect, button_color, button_hover_color)

    else:
        # Check if all rounds have been completed before setting block_complete to True
        if current_round >= max_rounds:
            # Ensure that the final round has been fully processed before completing the block
            if not in_round:  # in_round is False when the current round has been processed
                block_complete = True

    # Keep the metrics displayed even after block completion
    success_rate = ((max_rounds - missed_targets) / max_rounds) * 100
    metrics_text = [
        f"Rounds: {current_round}/{max_rounds}",
        f"Correct: {correct_responses}",
        f"Incorrect: {incorrect_responses}",
        f"Missed: {missed_targets}",
        f"Success Rate: {success_rate:.2f}%"
    ]
    for idx, text in enumerate(metrics_text):
        metrics_surface = font_small.render(text, True, (255, 255, 255))
        screen.blit(metrics_surface, (10, 10 + idx * 20))

    pygame.display.flip()
    clock.tick(fps)

print("Game Over. Saving Results...")
save_results()
save_all_coords()
save_congruent_coords()
pygame.quit()
