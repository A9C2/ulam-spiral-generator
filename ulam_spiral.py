import tkinter as tk
from PIL import Image
import os, time

file_directory = os.path.dirname(__file__)
os.chdir(file_directory)

# Functions
def generate():
    input_info = check_input()
    if input_info[0]:
        size = input_info[1]
        prime_rgb = input_info[2]
        non_prime_rgb = input_info[3]
        im = Image.new("RGBA", (size, size), "white")
        im = draw_spiral(size, im, prime_rgb, non_prime_rgb)
        im.save(input_info[4] + ".png")
        show_message("Spiral was successfully created")
        

def check_input():
    # Checks input, corrects it and then returns a tuple:
    # index0: bool - data correctness
    # index1: int - size
    # index2: tuple of ints - RGB for prime numbers
    # index3: tuple of ints - RGB for nonprime numbers
    # index4: filename
    try:
        not_allowed_characters = '\\:*?"<>|'
        for c in not_allowed_characters:
            if c in image_name_entry.get():
                raise ValueError
        name = image_name_entry.get()
    except:
        show_message(f"Image name can't contain: {not_allowed_characters}")
        return (False, 0)
    
    try:
        size = int(size_adjust_entry.get())
        if size < 3:
            raise ValueError
        if size % 2 == 0:
            size += 1
    except:
        show_message("Wrong input for Image Size.")
        return (False, 0)
    try:
        r0, g0, b0 = (int(prime_color_red_entry.get()), int(prime_color_green_entry.get()), int(prime_color_blue_entry.get()))
        r1, g1, b1 = (int(non_prime_color_red_entry.get()), int(non_prime_color_green_entry.get()), int(non_prime_color_blue_entry.get()))
        for value in (r0, g0, b0, r1, g1, b1):
            if value < 0 or value > 255:
                raise ValueError
        prime_colors = (r0, g0, b0)
        non_prime_colors = (r1, g1, b1)
    except:
        show_message("Wrong values for RGB. Enter numbers from 0 to 255.")
        return (False, 0)
    return (True, size, prime_colors, non_prime_colors, name)
            
def show_message(message):
    output_message.set(message)

def restore_defaults():
    image_name_entry.delete("0",tk.END)
    image_name_entry.insert(0, "spiral")
    size_adjust_entry.delete("0",tk.END)
    size_adjust_entry.insert(0, "77")
    
    prime_color_red_entry.delete("0",tk.END)
    prime_color_red_entry.insert(0, "0")
    prime_color_green_entry.delete("0",tk.END)
    prime_color_green_entry.insert(0, "0")
    prime_color_blue_entry.delete("0",tk.END)
    prime_color_blue_entry.insert(0, "0")
    
    non_prime_color_red_entry.delete("0",tk.END)
    non_prime_color_red_entry.insert(0, "255")
    non_prime_color_green_entry.delete("0",tk.END)
    non_prime_color_green_entry.insert(0, "255")
    non_prime_color_blue_entry.delete("0",tk.END)
    non_prime_color_blue_entry.insert(0, "255")
    
    show_message("Restored defaults")

def draw_spiral(size, im, prime_color, non_prime_color):
    def sieve_of_eratosthenes(n):
        bool_list = [True for x in range(n-1)]
        for i in range(len(bool_list)):
            if bool_list[i]:
                for k in range(1, (len(bool_list)+1) // (i+2)):
                    bool_list[i + (i+2) * k] = False
                
        return [False] + bool_list
    
    # Controls position change in the next iterations after reaching edge of the spiral
    def change_pos(pos, x_change, y_change):
        x, y = pos
        x += x_change
        y += y_change
        return (x, y)
    
    # Middle pixel position
    middle = size // 2
    
    #bool list
    bool_list = sieve_of_eratosthenes(size * size)

    # 7 first fields
    im.putpixel((middle, middle), non_prime_color)
    im.putpixel((middle + 1, middle), prime_color)
    im.putpixel((middle + 1, middle - 1), prime_color)
    im.putpixel((middle,middle - 1), non_prime_color)
    im.putpixel((middle - 1, middle - 1), prime_color)
    im.putpixel((middle - 1, middle), non_prime_color)
    im.putpixel((middle - 1, middle + 1), prime_color)

    x_change = 1
    y_change = 0
    
    current_size = 0
    max_size = 3
    
    pos = (middle - 1, middle + 1)

    for i in range(7, size * size):
        if current_size == max_size or current_size == 2 * max_size:
            if x_change == 1:
                x_change = 0
                y_change = -1
            elif y_change == -1:
                y_change = 0
                x_change = -1
            elif x_change == -1:
                x_change = 0
                y_change = 1
            elif y_change == 1:
                y_change = 0
                x_change = 1
        if current_size == 2 * max_size:
            max_size += 1
            current_size = 0
        pos = change_pos(pos, x_change, y_change)    
        if bool_list[i]:
            im.putpixel(pos, prime_color)
        else:
            im.putpixel(pos, non_prime_color)
        current_size += 1
    return im

# Window
window = tk.Tk()

# Program info
program_info = tk.Label(window, text="Ulam spiral")

# Image name
image_name_entry = tk.Entry(window)
image_name_entry.insert(0, "spiral")

# Image size adjustment
size_adjust_entry = tk.Entry(window)
size_adjust_entry.insert(0, "77")

# Prime
prime_color_label = tk.Label(window, text="Enter RGB value for prime numbers.")

prime_color_red_entry = tk.Entry(window, width=3)
prime_color_red_entry.insert(0, "0")

prime_color_green_entry = tk.Entry(window, width=3)
prime_color_green_entry.insert(0, "0")

prime_color_blue_entry = tk.Entry(window, width=3)
prime_color_blue_entry.insert(0, "0")

# Non-prime
non_prime_color_label = tk.Label(window, text="Enter RGB value for non-prime numbers.")

non_prime_color_red_entry = tk.Entry(window, width=3)
non_prime_color_red_entry.insert(0, "255")

non_prime_color_green_entry = tk.Entry(window, width=3)
non_prime_color_green_entry.insert(0, "255")

non_prime_color_blue_entry = tk.Entry(window, width=3)
non_prime_color_blue_entry.insert(0, "255")

# Restore defaults
restore_defaults_button = tk.Button(window, text="Restore Defaults", command=restore_defaults)

# Start gnerating image
generate_button = tk.Button(window, text="Generate Image", command=generate)

# Error messages
output_message = tk.StringVar()
output_message.set("")
output_message_label = tk.Label(window, textvariable=output_message)
    
# Displaying on screen
r = 0

program_info.grid(row=r, column=1)
r += 1

tk.Label(window, text="Image name").grid(row=r, column=0)
image_name_entry.grid(row=r, column=1)
r += 1

tk.Label(window, text="Image size in pixels").grid(row=r, column=0)
size_adjust_entry.grid(row=r, column=1)
r += 1

prime_color_label.grid(row=r, column=1)
r += 1

tk.Label(window, text="Red").grid(row=r, column=0)
prime_color_red_entry.grid(row=r, column=1)
r += 1
tk.Label(window, text="Green").grid(row=r, column=0)
prime_color_green_entry.grid(row=r, column=1)
r += 1
tk.Label(window, text="Blue").grid(row=r, column=0)
prime_color_blue_entry.grid(row=r, column=1)
r += 1

non_prime_color_label.grid(row=r, column=1)
r += 1

tk.Label(window, text="Red").grid(row=r, column=0)
non_prime_color_red_entry.grid(row=r, column=1)
r += 1
tk.Label(window, text="Green").grid(row=r, column=0)
non_prime_color_green_entry.grid(row=r, column=1)
r += 1
tk.Label(window, text="Blue").grid(row=r, column=0)
non_prime_color_blue_entry.grid(row=r, column=1)
r += 1

restore_defaults_button.grid(row=r, column=0)
generate_button.grid(row=r, column=1)
r += 1
output_message_label.grid(row=r, column=1)

r = 0

window.mainloop()