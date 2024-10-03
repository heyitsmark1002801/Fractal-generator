import tkinter as tk
from tkinter import ttk
import turtle
import random

def create_l_system(iterations, axiom, rules):
    """Generates the L-system string after a given number of iterations."""
    current_string = axiom
    for _ in range(iterations):
        next_string = ""
        for character in current_string:
            next_string += rules.get(character, character)
        current_string = next_string
    return current_string

def draw_l_system(t, instructions, angle, distance, colors, line_width):
    """Interprets the L-system string and draws the pattern using turtle graphics."""
    t.width(line_width)
    stack = []
    for cmd in instructions:
        if cmd in ('F', 'X', 'Y', 'A', 'B'):
            t.color(random.choice(colors))
            t.forward(distance)
        elif cmd == 'G':
            t.penup()
            t.forward(distance)
            t.pendown()
        elif cmd == '+':
            t.right(angle)
        elif cmd == '-':
            t.left(angle)
        elif cmd == '[':
            # Save the current turtle state
            position = t.position()
            heading = t.heading()
            stack.append((position, heading))
        elif cmd == ']':
            # Restore the last saved turtle state
            position, heading = stack.pop()
            t.penup()
            t.goto(position)
            t.setheading(heading)
            t.pendown()

def start_drawing():
    """Starts the drawing based on user inputs from the GUI."""
    # Get selected L-system rule
    lsystem_name = lsystem_choice.get()
    lsystem_data = lsystems[lsystem_name]
    axiom = lsystem_data['axiom']
    rules = lsystem_data['rules']
    default_angle = lsystem_data.get('angle', 60)

    # Get user inputs
    try:
        iterations = int(iterations_entry.get())
        if iterations < 1:
            raise ValueError
    except ValueError:
        iterations = 4  # Default value

    try:
        angle = float(angle_entry.get())
    except ValueError:
        angle = default_angle  # Use default angle if invalid input

    try:
        distance = float(distance_entry.get())
    except ValueError:
        distance = 5  # Default value

    try:
        line_width = float(line_width_entry.get())
    except ValueError:
        line_width = 1  # Default value

    color_scheme = color_choice.get()
    if color_scheme == 'Autumn':
        colors = ['#E74C3C', '#E67E22', '#F1C40F']
    elif color_scheme == 'Spring':
        colors = ['#2ECC71', '#27AE60', '#1ABC9C']
    elif color_scheme == 'Monochrome':
        colors = ['#FFFFFF']
    elif color_scheme == 'Random':
        colors = [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in range(10)]
    else:
        colors = ['#7D3C98', '#2874A6', '#239B56', '#F1C40F', '#E67E22', '#E74C3C']

    # Use default angle if entry is empty
    if angle_entry.get() == '':
        angle = default_angle
        angle_entry.delete(0, tk.END)
        angle_entry.insert(0, str(default_angle))

    # Clear previous drawing
    t.clear()
    t.penup()
    t.goto(0, 0)
    t.setheading(0)
    t.pendown()

    # Generate the L-system instructions
    instructions = create_l_system(iterations, axiom, rules)

    # Draw the L-system
    draw_l_system(t, instructions, angle, distance, colors, line_width)

def reset_drawing():
    """Resets the drawing and allows for new inputs."""
    t.clear()
    start_drawing()

def random_fractal():
    """Selects a random L-system and randomizes parameters before drawing."""
    # Randomly select a fractal
    lsystem_name = random.choice(list(lsystems.keys()))
    lsystem_choice.set(lsystem_name)

    lsystem_data = lsystems[lsystem_name]

    # Randomly decide whether to use known fractal numbers or random values
    use_known_values = random.choice([True, False])

    if use_known_values:
        # Use known fractal numbers
        iterations = lsystem_data.get('known_iterations', 4)
        angle = lsystem_data.get('known_angle', lsystem_data.get('angle', 60))
        distance = lsystem_data.get('known_distance', 5)
        line_width = lsystem_data.get('known_line_width', 1)
        color_scheme = lsystem_data.get('known_color_scheme', 'Default')
    else:
        # Randomize iterations
        iterations = random.randint(3, 6)

        # Randomize line width
        line_width = random.uniform(1, 5)

        # Randomize segment length
        distance = random.uniform(2, 10)

        # Randomize color scheme
        color_scheme = random.choice(["Default", "Autumn", "Spring", "Monochrome", "Random"])

        # Randomize angle
        angle = random.uniform(20, 90)

    # Update entries with the values
    iterations_entry.delete(0, tk.END)
    iterations_entry.insert(0, str(iterations))

    line_width_entry.delete(0, tk.END)
    line_width_entry.insert(0, f"{line_width:.2f}")

    distance_entry.delete(0, tk.END)
    distance_entry.insert(0, f"{distance:.2f}")

    color_choice.set(color_scheme)

    angle_entry.delete(0, tk.END)
    angle_entry.insert(0, f"{angle:.2f}")

    start_drawing()

def setup_gui():
    """Sets up the GUI elements."""
    # Create input fields and labels
    tk.Label(control_frame, text="Iterations:").grid(row=0, column=0, sticky='e')
    iterations_entry.grid(row=0, column=1)

    tk.Label(control_frame, text="Angle:").grid(row=1, column=0, sticky='e')
    angle_entry.grid(row=1, column=1)

    tk.Label(control_frame, text="Segment Length:").grid(row=2, column=0, sticky='e')
    distance_entry.grid(row=2, column=1)

    tk.Label(control_frame, text="Line Width:").grid(row=3, column=0, sticky='e')
    line_width_entry.grid(row=3, column=1)

    tk.Label(control_frame, text="Color Scheme:").grid(row=4, column=0, sticky='e')
    color_menu.grid(row=4, column=1)

    tk.Label(control_frame, text="L-System Rule:").grid(row=5, column=0, sticky='e')
    lsystem_menu.grid(row=5, column=1)

    # Create buttons
    draw_button.grid(row=6, column=0, columnspan=2, pady=5)
    reset_button.grid(row=7, column=0, columnspan=2, pady=5)
    random_button.grid(row=8, column=0, columnspan=2, pady=5)

def main():
    global screen, t, control_frame
    global iterations_entry, angle_entry, distance_entry, color_choice, color_menu
    global line_width_entry
    global lsystem_choice, lsystem_menu
    global draw_button, reset_button, random_button
    global lsystems, default_angle

    # Define popular L-systems with known fractal numbers
    lsystems = {
        "Koch Snowflake": {
            "axiom": "F--F--F",
            "rules": {"F": "F+F--F+F"},
            "angle": 60,
            "known_iterations": 4,
            "known_angle": 60,
            "known_distance": 5,
            "known_line_width": 1,
            "known_color_scheme": "Default",
        },
        "Sierpinski Triangle": {
            "axiom": "F-G-G",
            "rules": {"F": "F-G+F+G-F", "G": "GG"},
            "angle": 120,
            "known_iterations": 5,
            "known_angle": 120,
            "known_distance": 5,
            "known_line_width": 1,
            "known_color_scheme": "Spring",
        },
        "Dragon Curve": {
            "axiom": "FX",
            "rules": {"X": "X+YF+", "Y": "-FX-Y"},
            "angle": 90,
            "known_iterations": 10,
            "known_angle": 90,
            "known_distance": 5,
            "known_line_width": 1,
            "known_color_scheme": "Autumn",
        },
        "Fractal Tree": {
            "axiom": "X",
            "rules": {"X": "F[+X][-X]FX", "F": "FF"},
            "angle": 25,
            "random_angle": True,
            "known_iterations": 5,
            "known_angle": 25,
            "known_distance": 7,
            "known_line_width": 2,
            "known_color_scheme": "Default",
        },
        "Hilbert Curve": {
            "axiom": "A",
            "rules": {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"},
            "angle": 90,
            "known_iterations": 5,
            "known_angle": 90,
            "known_distance": 10,
            "known_line_width": 2,
            "known_color_scheme": "Monochrome",
        },
        "Gosper Curve": {
            "axiom": "A",
            "rules": {"A": "A+BF++BF-FA--FAFA-BF+", "B": "-FA+BFBF++BF+FA--FA-BF"},
            "angle": 60,
            "known_iterations": 3,
            "known_angle": 60,
            "known_distance": 5,
            "known_line_width": 1.5,
            "known_color_scheme": "Random",
        },
        "Barnsley Fern": {
            "axiom": "X",
            "rules": {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"},
            "angle": 22.5,
            "random_angle": True,
            "known_iterations": 5,
            "known_angle": 22.5,
            "known_distance": 2,
            "known_line_width": 1,
            "known_color_scheme": "Spring",
        },
    }

    # Set up the main window
    root = tk.Tk()
    root.title("Interactive L-System Fractal Generator")

    # Set up the turtle screen within a canvas
    canvas = tk.Canvas(master=root, width=800, height=600)
    canvas.pack(side=tk.LEFT)

    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor('black')

    # Create the turtle
    t = turtle.RawTurtle(screen)
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.goto(0, 0)
    t.setheading(0)
    t.pendown()

    # Control frame on the right side
    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    # Input fields
    iterations_entry = tk.Entry(control_frame)
    iterations_entry.insert(0, "4")

    angle_entry = tk.Entry(control_frame)
    angle_entry.insert(0, "")

    distance_entry = tk.Entry(control_frame)
    distance_entry.insert(0, "5")

    line_width_entry = tk.Entry(control_frame)
    line_width_entry.insert(0, "1")

    # Color scheme dropdown
    color_choice = tk.StringVar()
    color_choice.set("Default")
    color_options = ["Default", "Autumn", "Spring", "Monochrome", "Random"]
    color_menu = tk.OptionMenu(control_frame, color_choice, *color_options)

    # L-system rule dropdown
    lsystem_choice = tk.StringVar()
    lsystem_choice.set("Koch Snowflake")
    lsystem_menu = tk.OptionMenu(control_frame, lsystem_choice, *lsystems.keys())

    # Buttons
    draw_button = tk.Button(control_frame, text="Draw", command=start_drawing)
    reset_button = tk.Button(control_frame, text="Reset", command=reset_drawing)
    random_button = tk.Button(control_frame, text="Random Fractal", command=random_fractal)

    # Setup GUI elements
    setup_gui()

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
