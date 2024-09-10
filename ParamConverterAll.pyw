import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import importlib

# Mapping script names to modules
param_converters = {
    "Atk": "ParamConverterAtk",
    "Behavior": "ParamConverterBehavior",
    "Bullet": "ParamConverterBullet",
    "Npc": "ParamConverterNpc",
    "NpcThink": "ParamConverterNpcThink",
    "SpEffect": "ParamConverterSpEffect",
    "Vfx": "ParamConverterVfx"
}

def run_selected_converter(script_name):
    """Runs the selected converter script."""
    try:
        converter_module = importlib.import_module(script_name)
    except ImportError:
        messagebox.showerror("Error", f"Could not load module: {script_name}")
        return

    # Prompt user to select the file
    input_file = filedialog.askopenfilename(title="Select a CSV file to convert")
    if not input_file:
        messagebox.showerror("Error", "No file selected.")
        return

    # Execute the convert function from the chosen module
    try:
        converter_module.convert(input_file)  # Assuming each script has a `convert` function
        messagebox.showinfo("Success", "File converted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while converting: {e}")

def create_gui():
    """Creates the GUI."""
    root = tk.Tk()
    root.title("Param Converter Tool")
    root.geometry("400x200")
    root.configure(bg="black")  # Black background

    # Style configuration
    style = ttk.Style()
    style.configure("TLabel", background="black", foreground="white", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 10), foreground="black", background="#f0f0f0")
    style.map("TButton", background=[("active", "#c0c0c0")])

    # Dropdown list for selecting parameter type
    param_type_label = ttk.Label(root, text="Select Parameter Type:")
    param_type_label.pack(pady=(20, 5))

    param_type_var = tk.StringVar(root)
    param_type_var.set("Select...")  # Default value

    param_type_menu = ttk.OptionMenu(root, param_type_var, *param_converters.keys())
    param_type_menu.pack(pady=(5, 20))

    def on_convert_button():
        selected_type = param_type_var.get()
        if selected_type == "Select...":
            messagebox.showerror("Error", "Please select a parameter type.")
        else:
            script_name = param_converters[selected_type]
            run_selected_converter(script_name)

    # Convert button
    convert_button = ttk.Button(root, text="Load and Convert", command=on_convert_button)
    convert_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
