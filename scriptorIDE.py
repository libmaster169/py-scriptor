import sys
import io
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import json
from . import RuleScript
import types

class ScriptorIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scriptor IDE")
        self.geometry("800x600")

        tk.Label(self, text="Cykle:").pack(anchor="w")
        self.cycle_text = scrolledtext.ScrolledText(self, height=1)
        self.cycle_text.pack(fill="x")

        tk.Label(self, text="Skrypt:").pack(anchor="w")
        self.script_text = scrolledtext.ScrolledText(self, height=10)
        self.script_text.pack(fill="x")

        tk.Label(self, text="Zmiennie (JSON):").pack(anchor="w")
        self.vars_text = scrolledtext.ScrolledText(self, height=5)
        self.vars_text.pack(fill="x")

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Uruchom", command=self.run_script).pack(side="left", padx=5, pady=5)
        tk.Button(btn_frame, text="Wyczyść", command=self.clear_output).pack(side="left", padx=5, pady=5)
        tk.Button(btn_frame, text="Zapisz skrypt", command=self.save_script).pack(side="left", padx=5, pady=5)
        tk.Button(btn_frame, text="Wczytaj skrypt", command=self.load_script).pack(side="left", padx=5, pady=5)

        tk.Label(self, text="Wyjście:").pack(anchor="w")
        self.output_text = scrolledtext.ScrolledText(self, height=15)
        self.output_text.pack(fill="both", expand=True)

    def run_script(self):
        script = self.script_text.get("1.0", tk.END).strip()
        try:
            vars_dict = json.loads(self.vars_text.get("1.0", tk.END))
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd w zmiennych: {e}")
            return

        self.output_text.delete("1.0", tk.END)
        rs = RuleScript(script, vars_dict)
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        try:
            result = rs.run(int(self.cycle_text.get("1.0", tk.END).strip()))
            filtered_vars = {k: v for k, v in rs.vars.items() if not isinstance(v, types.ModuleType)}
            output = mystdout.getvalue()
            self.output_text.insert(tk.END, output)
            self.output_text.insert(tk.END, f"Wynik: {result}\n")
            self.output_text.insert(tk.END,
                                    f"Zmiennie po wykonaniu:\n{json.dumps(filtered_vars, indent=2, ensure_ascii=False)}")
        except Exception as e:
            self.output_text.insert(tk.END, f"Błąd: {e}")
        finally:
            sys.stdout = old_stdout

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)

    def save_script(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Pliki JSON", "*.json")])
        if not file_path:
            return
        data = {
            "script": self.script_text.get("1.0", tk.END).strip(),
            "vars": self.vars_text.get("1.0", tk.END).strip(),
            "cycles": self.cycle_text.get("1.0", tk.END).strip()
        }
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Sukces", "Skrypt zapisany.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać: {e}")

    def load_script(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki JSON", "*.json")])
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.script_text.delete("1.0", tk.END)
            self.script_text.insert(tk.END, data.get("script", ""))
            self.vars_text.delete("1.0", tk.END)
            self.vars_text.insert(tk.END, data.get("vars", ""))
            self.cycle_text.delete("1.0", tk.END)
            self.cycle_text.insert(tk.END, data.get("cycles", ""))
            messagebox.showinfo("Sukces", "Skrypt wczytany.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać: {e}")


app = ScriptorIDE()
app.mainloop()

