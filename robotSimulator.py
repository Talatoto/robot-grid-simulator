import tkinter as tk
from tkinter import ttk

# Define levels as tuples: (grid_size, obstacles, goal)
LEVELS = {
    "Easy": (5, [(1, 1)], (4, 4)),
    "Medium": (8, [(1, 2), (2, 3), (3, 1), (6, 6)], (7, 7)),
    "Hard": (10, [(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8)], (9,9))
}

def launch_game(level_name):
    import winsound
    import time
    from tkinter import messagebox

    grid_size, obstacles, goal = LEVELS[level_name]

    class RobotSimulatorGUI:
        DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]
        DIRECTION_SYMBOLS = {"NORTH": "🔼", "EAST": "▶️", "SOUTH": "🔽", "WEST": "◀️"}

        def __init__(self):
            self.grid_size = grid_size
            self.obstacles = obstacles
            self.goal = goal
            self.x = 0
            self.y = 0
            self.direction_index = 0
            self.battery = 100

            self.window = tk.Toplevel()
            self.window.title(f"🌌 Robot Grid - {level_name} Mode")
            self.window.configure(bg="#1e1e1e")

            style = ttk.Style()
            style.configure("TButton", font=("Segoe UI", 11), padding=6)
            style.configure("Dark.TFrame", background="#1e1e1e")
            style.configure("Dark.TLabel", background="#1e1e1e", foreground="white")

            self.main_frame = ttk.Frame(self.window, style="Dark.TFrame", padding=10)
            self.main_frame.pack()

            self.canvas_frame = ttk.LabelFrame(self.main_frame, text=f"{level_name} Arena", style="Dark.TLabel", padding=10)
            self.canvas_frame.grid(row=0, column=0, columnspan=3)

            canvas_size = 500
            self.canvas = tk.Canvas(self.canvas_frame, width=canvas_size, height=canvas_size, bg="#2b2b2b", highlightthickness=2, highlightbackground="#444444")
            self.canvas.pack()

            self.cell_size = canvas_size // self.grid_size
            self.draw_grid()

            self.info_label = ttk.Label(self.main_frame, text="", font=("Consolas", 13), style="Dark.TLabel")
            self.info_label.grid(row=1, column=0, columnspan=3, pady=10)

            ttk.Button(self.main_frame, text="↑ Move", style="TButton", command=lambda: self.execute_command("forward")).grid(row=2, column=1, pady=2)
            ttk.Button(self.main_frame, text="← Left", style="TButton", command=lambda: self.execute_command("left")).grid(row=3, column=0, pady=2)
            ttk.Button(self.main_frame, text="→ Right", style="TButton", command=lambda: self.execute_command("right")).grid(row=3, column=2, pady=2)
            ttk.Button(self.main_frame, text="📋 Report", style="TButton", command=lambda: self.execute_command("report")).grid(row=4, column=0, columnspan=3, pady=2)
            ttk.Button(self.main_frame, text="⚡ Recharge", style="TButton", command=lambda: self.execute_command("recharge")).grid(row=5, column=0, columnspan=3, pady=2)

            self.window.bind("<Up>", lambda e: self.execute_command("forward"))
            self.window.bind("<Left>", lambda e: self.execute_command("left"))
            self.window.bind("<Right>", lambda e: self.execute_command("right"))
            self.window.bind("<space>", lambda e: self.execute_command("report"))

            self.window.focus_force()
            self.update_display()

        def draw_grid(self):
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    x0 = i * self.cell_size
                    y0 = (self.grid_size - 1 - j) * self.cell_size
                    x1 = x0 + self.cell_size
                    y1 = y0 + self.cell_size
                    color = "#1db954" if (i, j) == self.goal else ("#4b4b4b" if (i, j) in self.obstacles else "#3a3a3a")
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#666")

        def animate_move(self, new_x, new_y):
            steps = 10
            dx = (new_x - self.x) * self.cell_size / steps
            dy = -(new_y - self.y) * self.cell_size / steps
            for _ in range(steps):
                self.canvas.move("robot", dx, dy)
                self.canvas.update()
                time.sleep(0.02)

        def update_display(self):
            self.canvas.delete("robot")
            self.draw_grid()
            robot_x = self.x * self.cell_size + self.cell_size // 2
            robot_y = (self.grid_size - 1 - self.y) * self.cell_size + self.cell_size // 2
            symbol = self.DIRECTION_SYMBOLS[self.DIRECTIONS[self.direction_index]]
            self.canvas.create_oval(robot_x - 22, robot_y - 22, robot_x + 22, robot_y + 22, fill="#03dac6", outline="", tags="robot")
            self.canvas.create_text(robot_x, robot_y, text=symbol, font=("Segoe UI", 18, "bold"), fill="black", tags="robot")
            self.info_label.config(text=f"📍 ({self.x}, {self.y})   ➡ {self.DIRECTIONS[self.direction_index]}   🔋 {self.battery}%")
            if (self.x, self.y) == self.goal:
                winsound.MessageBeep()
                messagebox.showinfo("🎯 Victory", "Goal reached! Mission complete!")

        def is_obstacle(self, x, y): return (x, y) in self.obstacles
        def is_within_bounds(self, x, y): return 0 <= x < self.grid_size and 0 <= y < self.grid_size

        def forward(self):
            if self.battery < 10: messagebox.showwarning("Battery", "🔋 Too low!"); return
            dx, dy = [(0,1),(1,0),(0,-1),(-1,0)][self.direction_index]
            new_x, new_y = self.x + dx, self.y + dy
            if not self.is_within_bounds(new_x, new_y): winsound.MessageBeep(); messagebox.showerror("Crash", "💥 Wall!"); return
            if self.is_obstacle(new_x, new_y): winsound.MessageBeep(); messagebox.showerror("Blocked", f"🧱 Obstacle at ({new_x},{new_y})"); return
            self.animate_move(new_x, new_y); self.x, self.y = new_x, new_y; self.battery -= 10

        def left(self):
            if self.battery < 1: messagebox.showwarning("Battery", "🔋 Too low!"); return
            self.direction_index = (self.direction_index - 1) % 4; self.battery -= 1

        def right(self):
            if self.battery < 1: messagebox.showwarning("Battery", "🔋 Too low!"); return
            self.direction_index = (self.direction_index + 1) % 4; self.battery -= 1

        def report(self): messagebox.showinfo("📋 Report", f"({self.x}, {self.y})\n{self.DIRECTIONS[self.direction_index]}\nBattery: {self.battery}%")
        def recharge(self): self.battery = 100; winsound.MessageBeep(); messagebox.showinfo("⚡ Recharged", "Battery full!")
        def execute_command(self, command): getattr(self, command)() if hasattr(self, command) else None; self.update_display()

    RobotSimulatorGUI()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("🤖 Robot Simulator - Select Level")
    root.configure(bg="#121212")

    title_frame = tk.Frame(root, bg="#121212")
    title_frame.pack(pady=30)

    tk.Label(title_frame, text="ROBOT GRID SIMULATOR", font=("Segoe UI", 24, "bold"), fg="#03dac6", bg="#121212").pack()
    tk.Label(title_frame, text="Choose Your Difficulty Level", font=("Segoe UI", 14), fg="white", bg="#121212").pack(pady=5)

    button_frame = tk.Frame(root, bg="#121212")
    button_frame.pack()

    for level in LEVELS:
        tk.Button(button_frame, text=f"🎮 {level} Mode", font=("Segoe UI", 13), bg="#03dac6", fg="black", padx=10, pady=6, command=lambda l=level: launch_game(l)).pack(pady=6)

    tk.Button(root, text="❌ Exit Game", font=("Segoe UI", 12), bg="#333333", fg="white", padx=12, pady=5, command=root.destroy).pack(pady=30)

    root.mainloop()
