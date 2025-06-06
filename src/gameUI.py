import tkinter as tk
from tkinter import messagebox
from master_mind import Match, guess, Color, play, GameStatus, select_colors
import time

EXACT = Match.EXACT
PARTIAL = Match.PARTIAL
NOT_FOUND = Match.NOT_FOUND

WON = GameStatus.WON
IN_PROGRESS = GameStatus.IN_PROGRESS
LOST = GameStatus.LOST

MAX_ATTEMPTS = 20

class MasterMindUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Master Mind Game")
        self.colors = list(Color)
        self.color_hexcodes = {color: self.get_color_hexcode(color) for color in self.colors}
        self.hexcode_to_color = {hex_code: color_enum for color_enum, hex_code in self.color_hexcodes.items()}
        self.sceen_display()

    def get_color_hexcode(self, color):
        color_map = {
            Color.RED: "red",
            Color.BLUE: "blue",
            Color.GREEN: "green",
            Color.YELLOW: "yellow",
            Color.ORANGE: "orange",
            Color.PURPLE: "purple",
            Color.CYAN: "cyan",
            Color.VIOLET: "violet",
            Color.WHITE: "white",
            Color.BLACK: "black"
        }
        return color_map.get(color)

    def set_initials(self):
        self.guess_blocks = []
        self.selected_colors = select_colors(time.time())
        print(self.selected_colors)
        self.current_attempt = 0
        self.current_color_index =[None] * len(self.selected_colors)
        self.stop_increment_highlighted_box = False

    def sceen_display(self):
        self.set_initials()

        self.color_display_frame = tk.Frame(self.master)
        self.color_display_frame.grid(row=1, column=0, columnspan=6, padx=10, pady=10)

        self.user_input_frame = tk.Frame(self.master)
        self.user_input_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=10)

        self.win_lose_notification_frame = tk.Frame(self.master, height= 23)
        self.win_lose_notification_frame.grid(row=3, column=0, columnspan=6, padx=10, pady=5)

        self.result_output_frame = tk.Frame(self.master)
        self.result_output_frame.grid(row=4, column=0, columnspan=6, padx=10, pady=10)

        self.result_output_frame_left = tk.Frame(self.result_output_frame)
        self.result_output_frame_left.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.result_output_frame_right = tk.Frame(self.result_output_frame)
        self.result_output_frame_right.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        for num, color in enumerate(self.colors):
            color_block = tk.Button(self.color_display_frame, width=7, height=3, bg=self.color_hexcodes[color], highlightthickness=1, highlightbackground="black", command=lambda c=color: self.select_color_for_box(c))
            color_block.grid(row=1, column=num, padx=10, pady=10)

        for idx in range(len(self.selected_colors)):
            select_color_frame = tk.Frame(self.user_input_frame, width=50, height=50, bg="white", highlightthickness=1, highlightbackground="black")
            select_color_frame.grid(row=2, column=idx + 1, padx=10, pady=5, sticky="nsew")
            select_color_frame.bind("<Button-1>", lambda _, i=idx: self.highlight_input_box(i))
            self.guess_blocks.append(select_color_frame)

        self.highlight_input_box(0)

        self.submit_button = tk.Button(self.user_input_frame, text="Submit", command=self.submit_guess)
        self.submit_button.grid(row=2, column=8, padx=5, pady=5)

        self.quit_button = tk.Button(self.user_input_frame, text="Give Up?", command=self.show_answer)
        self.quit_button.grid(row=2, column=9, padx=5, pady=5)
        
        self.restart_button = tk.Button(self.user_input_frame, text="Restart?", command=self.restart)
        self.restart_button.grid(row=2, column=10, padx=5, pady=5)

        for j in range(MAX_ATTEMPTS):
            self.display_input_output(j)

    def highlight_input_box(self, index):
        for i, frame in enumerate(self.guess_blocks):
            if i == index:
                frame.config(highlightbackground="gray", highlightthickness=5)
                self.selected_input_box = index
            elif self.selected_input_box == len(self.selected_colors) - 1:
                self.stop_increment_highlighted_box = True
            else:
                frame.config(highlightbackground="black", highlightthickness=1)

    def select_color_for_box(self, color):
        self.guess_blocks[self.selected_input_box].config(bg=self.get_color_hexcode(color))
        self.current_color_index[self.selected_input_box] = color
        if self.selected_input_box < len(self.guess_blocks) and self.stop_increment_highlighted_box == False:
            next_box_index = self.selected_input_box + 1
            self.highlight_input_box(next_box_index)

    def display_input_output(self, j):
        for i in range(len(self.selected_colors)):
            user_input_record = tk.Frame(self.result_output_frame_left, width=20, height=20, bg="white", highlightthickness=1, highlightbackground="black")
            user_input_record.grid(row=j, column=i, padx=10, pady=5)
            result_ouput_record = tk.Frame(self.result_output_frame_right, width=20, height=20, bg="white", highlightthickness=1, highlightbackground="black")
            result_ouput_record.grid(row=j, column=i, padx=10, pady=5)

    def submit_guess(self):
        self.user_provided_colors =[]
        self.user_provided_colors = [self.hexcode_to_color.get(frame.cget("bg")) for frame in self.guess_blocks]
        
        if self.stop_increment_highlighted_box == False:
            messagebox.showerror("Error", "Please select all colors before submitting.")
            return
        else:
            for frame in self.guess_blocks:
                frame.config(bg="white")
            self.highlight_input_box(0)
            self.stop_increment_highlighted_box = False
            self.update_input_record()
            self.update_output_record()
            self.update_game_status()
            self.current_attempt += 1

    def update_input_record(self):
        for i, color in enumerate(self.user_provided_colors):
            user_input_record = tk.Frame(self.result_output_frame_left, width=20, height=20, bg=self.color_hexcodes[color], highlightthickness=1, highlightbackground="black")
            user_input_record.grid(row=self.current_attempt, column=i, padx=10, pady=5)

    def update_output_record(self):
        result = guess(self.user_provided_colors, self.selected_colors)

        exact_count = result.get(Match.EXACT, 0)
        partial_count = result.get(Match.PARTIAL, 0)
        not_found_count = result.get(Match.NOT_FOUND, 0)

        output_colors = []
        output_colors.extend(["black"] * exact_count)
        output_colors.extend(["grey"] * partial_count)
        output_colors.extend(["white"] * not_found_count)

        for i in range(len(self.selected_colors)):
            result_ouput_record = tk.Frame(self.result_output_frame_right, width=20, height=20, bg=output_colors[i], highlightthickness=1, highlightbackground="black")
            result_ouput_record.grid(row=self.current_attempt, column=i, padx=10, pady=5)

    def update_game_status(self):
        response, attempts_count, status = play(self.selected_colors, self.user_provided_colors, self.current_attempt)
        if status == WON:
            self.win_lose_notification = tk.Label(self.win_lose_notification_frame, text="Congratulations, you won!!!", font=("Arial", 11), fg="green")
            self.win_lose_notification.grid(row=3, column=0, padx=0, pady=0)
            self.disable_buttons()
        elif status == LOST:
            self.show_answer()

    def show_answer(self):
        self.answer_label = tk.Label(self.user_input_frame, text="Answer:", font=("Arial", 11, "bold"))
        self.answer_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.win_lose_notification = tk.Label(self.win_lose_notification_frame, text="Unfortunately, you lose. Play again!", font=("Arial", 11), fg="red")
        self.win_lose_notification.grid(row=3, column=0, padx=0, pady=0)

        for idx, color in enumerate(self.selected_colors):
            select_color_frame = tk.Frame(self.user_input_frame, width=50, height=50, bg=self.color_hexcodes[color], highlightthickness=1, highlightbackground="black")
            select_color_frame.grid(row=2, column=idx + 1, padx=10, pady=5, sticky="nsew")

        self.disable_buttons()

    def disable_buttons(self):
        self.submit_button.config(state=tk.DISABLED)
        self.quit_button.config(state=tk.DISABLED)

        for child in self.color_display_frame.winfo_children():
            child.config(state=tk.DISABLED)
    
    def restart(self):
        self.set_initials()

        self.answer_label.grid_forget()
        self.win_lose_notification.grid_forget()

        self.submit_button.config(state=tk.NORMAL)
        self.quit_button.config(state=tk.NORMAL)

        for child in self.color_display_frame.winfo_children():
            child.config(state=tk.NORMAL)

        for idx in range(len(self.selected_colors)):
            select_color_frame = tk.Frame(self.user_input_frame, width=50, height=50, bg="white", highlightthickness=1, highlightbackground="black")
            select_color_frame.grid(row=2, column=idx + 1, padx=10, pady=5, sticky="nsew")
            select_color_frame.bind("<Button-1>", lambda _, i=idx: self.highlight_input_box(i))
            self.guess_blocks.append(select_color_frame)

        for widget in self.result_output_frame_left.winfo_children():
            widget.config(bg="white")
        for widget in self.result_output_frame_right.winfo_children():
            widget.config(bg="white")

        self.highlight_input_box(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = MasterMindUI(root)
    root.mainloop()
