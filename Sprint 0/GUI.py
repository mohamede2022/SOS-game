import tkinter as tk # GUI Library used and will be used for the project.

class GuiApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SOS GUI Demo")
        self.root.geometry("320x240")

        # Text label (Header)
        tk.Label(root, text="Hello, SOS GUI!").pack(pady=(10, 5))

        # horizontal Canvas line below the Label
        canvas = tk.Canvas(root, width=260, height=40)
        canvas.create_line(10, 20, 250, 20)
        canvas.pack(pady=5)

        # Option Checkbox that enables you to change options
        self.check_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Enable Option", variable=self.check_var).pack(pady=5)

        # Radio buttons, Options (Choice A & Choice B)
        self.radio_var = tk.StringVar(value="A")
        frame = tk.Frame(root) # Frame for each Choice
        tk.Radiobutton(frame, text="Choice A", variable=self.radio_var, value="A").pack(side="left", padx=5)
        tk.Radiobutton(frame, text="Choice B", variable=self.radio_var, value="B").pack(side="left", padx=5)
        frame.pack(pady=5)

        # Status label for selected Option
        self.status = tk.Label(root, text=f"Selected: {self.radio_var.get()}")
        self.status.pack(pady=10)

        # Update status when radio changes (Selected Option changes)
        self.radio_var.trace_add(
            "write",
            lambda var_name, index, mode: self.status.config(
                text=f"Selected: {self.radio_var.get()}"
            )
        )
def main():
    root = tk.Tk()
    app = GuiApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
