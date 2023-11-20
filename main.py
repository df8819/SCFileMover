import json
import tkinter as tk
from tkinter import messagebox, ttk, filedialog, messagebox
import shutil
import os


class StarCitizenFileManager:
    def __init__(self, root):
        self.root = root
        self.config_file = os.path.join(os.path.expanduser('~'), 'Documents', 'StarCitizenFileManagerConfig.json')
        self.default_path = self.load_config()
        self.versions = ["LIVE", "PTU", "EPTU", "HOTFIX"]

        # Setup the GUI
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Star Citizen File Manager")

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the window size
        window_width = 320  # Adjust the size as needed
        window_height = 240  # Adjust the size as needed

        # Calculate x and y coordinates for the Tk root window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window's dimensions and position
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Move from and to
        tk.Label(self.root, text="Move From:").grid(row=0, column=0, sticky="w")
        self.move_from_var = tk.StringVar(self.root)
        self.move_from_var.set(self.versions[0])
        tk.OptionMenu(self.root, self.move_from_var, *self.versions).grid(row=0, column=1)

        tk.Label(self.root, text="Move To:").grid(row=1, column=0, sticky="w")
        self.move_to_var = tk.StringVar(self.root)
        self.move_to_var.set(self.versions[1])
        tk.OptionMenu(self.root, self.move_to_var, *self.versions).grid(row=1, column=1)

        tk.Button(self.root, text="Move Files", command=self.move_files, bg="green", fg="white").grid(row=0, column=2)

        ttk.Separator(self.root, orient='horizontal').grid(row=2, pady=20, sticky="ew", columnspan=3)

        ttk.Separator(self.root, orient='horizontal').grid(row=4, pady=20, sticky="ew", columnspan=3)

        # Delete section
        tk.Label(self.root, text="Delete Files in:").grid(row=3, column=0, sticky="w")
        self.delete_var = tk.StringVar(self.root)
        self.delete_var.set(self.versions[0])
        tk.OptionMenu(self.root, self.delete_var, *self.versions).grid(row=3, column=1)

        tk.Button(self.root, text="Delete Files", command=self.delete_files, bg="red", fg="white").grid(row=3, column=2)

        # Path display and change button
        tk.Label(self.root, text="Installation Path:").grid(row=5, column=0, sticky="w")

        self.path_label = tk.Label(self.root, text=self.default_path, fg="blue")
        self.path_label.grid(row=7, column=0, columnspan=3, padx=10)

        tk.Button(self.root, text="Change Path", command=self.change_path).grid(row=5, column=2)

    def load_config(self):
        # Check if config file exists
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                # Use the default path from config if available
                default_path = config.get('default_path', "C:\\Program Files\\Roberts Space Industries\\StarCitizen")
        else:
            default_path = "C:\\Program Files\\Roberts Space Industries\\StarCitizen"

        # Check if the default path exists, otherwise prompt user with file dialog
        if not os.path.exists(default_path):
            root = tk.Tk()
            root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
            print("The default path does not exist. Please select a new path.")
            default_path = filedialog.askdirectory()  # show an "Open" dialog box and return the path to the selected folder
            root.destroy()

        return default_path

    def save_config(self):
        with open(self.config_file, 'w') as file:
            json.dump({'default_path': self.default_path}, file)

    def change_path(self):
        new_path = filedialog.askdirectory(initialdir=self.default_path)
        if new_path:
            self.default_path = new_path
            self.path_label.config(text=self.default_path)
            self.save_config()

    def move_files(self):
        src = os.path.join(self.default_path, self.move_from_var.get())
        dst = os.path.join(self.default_path, self.move_to_var.get())

        if src == dst:
            messagebox.showerror("Error", "Source and destination cannot be the same.")
            return

        try:
            # Moving the files
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                shutil.move(s, d)
            messagebox.showinfo("Success", "Files moved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_files(self):
        # Confirmation dialog
        if messagebox.askyesno("Confirm", "Really want to delete ALL files in the selected folder?"):
            folder = os.path.join(self.default_path, self.delete_var.get())
            try:
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                messagebox.showinfo("Success", "Files deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")


# Create the main window
root = tk.Tk()
app = StarCitizenFileManager(root)
root.mainloop()
