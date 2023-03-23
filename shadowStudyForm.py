import tkinter as tk
import tkinter.font as tkFont
import csv
import os
from tkinter import filedialog
from tkinter.colorchooser import askcolor

class TinkerForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.title("Frank is doing Shadow Study Now !!!!")
        self.geometry("400x400")

        self.advanced_visible = False

        # data
        self.shadow_multiply_ratio = 0.7
        self.roof_lighter_ratio = 0.5
        site1color = (203, 51, 100)
        site2color = (255, 221, 21)
        site3color = (0, 74, 151)
        site4color = (204, 112, 40)
        site5color = (70, 255, 250)
        site6color = (90, 170, 255)
        site7color = (170, 110, 255)
        self.color_palette = [site1color, site2color, site3color, site4color, site5color, site6color, site7color]

        self.create_widgets()
        self.configure_grid()
        self.toggle_advanced_visibility()

    def on_ok_click(self):
        shadow_multiply_ratio = float(self.shadow_multiply_ratio_entry.get())
        site_shadow_1_color = self.site_shadow_1_color_button.cget('bg')
        site_shadow_2_color = self.site_shadow_2_color_button.cget('bg')
        self.destroy()
        self.quit()

    def on_load_click(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            # Read shadow_multiply_ratio
            self.shadow_multiply_ratio = float(next(csv_reader)[0])
            # Read roof_lighter_ratio
            self.roof_lighter_ratio = float(next(csv_reader)[0])
            # Read color_palette
            self.color_palette = [tuple(map(int, color.strip("()").split(","))) for color in next(csv_reader)]

        # Update Graphic
        self.shadow_multiply_ratio_entry.delete(0, tk.END)
        self.shadow_multiply_ratio_entry.insert(0, str(self.shadow_multiply_ratio))
        self.roof_lighter_ratio_entry.delete(0, tk.END)
        self.roof_lighter_ratio_entry.insert(0, str(self.roof_lighter_ratio))
        self.site_shadow_1_color_button.configure(bg=self.convert_To_Hex(self.color_palette[0]))
        self.site_shadow_2_color_button.configure(bg=self.convert_To_Hex(self.color_palette[1]))
        self.site_shadow_3_color_button.configure(bg=self.convert_To_Hex(self.color_palette[2]))
        self.site_shadow_4_color_button.configure(bg=self.convert_To_Hex(self.color_palette[3]))
        self.site_shadow_5_color_button.configure(bg=self.convert_To_Hex(self.color_palette[4]))

    def on_save_click(self):
        data = [[self.shadow_multiply_ratio],[self.roof_lighter_ratio],self.color_palette]
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        with open(file_path, "w", newline="") as csvfile:
            # create a CSV writer object
            writer = csv.writer(csvfile)
            # write the data to the CSV file
            for row in data:
                writer.writerow(row)

    def convert_To_Hex(self,rgb):
        return "#" + "".join([hex(x)[2:].zfill(2) for x in rgb])

    def on_color_click_1(self):
        self.color_palette[0] =askcolor(color=self.color_palette[0])[0] or self.color_palette[0]
        self.site_shadow_1_color_button.configure(bg=self.convert_To_Hex(self.color_palette[0]))

    def on_color_click_2(self):
        self.color_palette[1] =askcolor(color=self.color_palette[1])[0] or self.color_palette[1]
        self.site_shadow_2_color_button.configure(bg=self.convert_To_Hex(self.color_palette[1]))

    def on_color_click_3(self):
        self.color_palette[2] =askcolor(color=self.color_palette[2])[0] or self.color_palette[2]
        self.site_shadow_3_color_button.configure(bg=self.convert_To_Hex(self.color_palette[2]))

    def on_color_click_4(self):
        self.color_palette[3] =askcolor(color=self.color_palette[3])[0] or self.color_palette[3]
        self.site_shadow_4_color_button.configure(bg=self.convert_To_Hex(self.color_palette[3]))

    def on_color_click_5(self):
        self.color_palette[4] =askcolor(color=self.color_palette[4])[0] or self.color_palette[4]
        self.site_shadow_5_color_button.configure(bg=self.convert_To_Hex(self.color_palette[4]))

    def on_advance_click(self):
        self.advanced_visible = not self.advanced_visible
        self.toggle_advanced_visibility()

    def create_widgets(self):
        self.shadow_multiply_ratio_label = tk.Label(self, text="Shadow Multiply Ratio", font = self.label_font)
        self.shadow_multiply_ratio_entry = tk.Entry(self)
        self.shadow_multiply_ratio_entry.insert(0, self.shadow_multiply_ratio)

        self.roof_lighter_ratio_label = tk.Label(self, text="Roof Lighter Ratio", font = self.label_font)
        self.roof_lighter_ratio_entry = tk.Entry(self)
        self.roof_lighter_ratio_entry.insert(0, self.roof_lighter_ratio)

        self.site_shadow_1_color_label = tk.Label(self, text="Site Shadow 1 Color", font = self.label_font)
        self.site_shadow_1_color_button = tk.Button(self, text="Choose Color", command=self.on_color_click_1, bg=self.convert_To_Hex(self.color_palette[0]))

        self.site_shadow_2_color_label = tk.Label(self, text="Site Shadow 2 Color", font= self.label_font)
        self.site_shadow_2_color_button = tk.Button(self, text="Choose Color", command=self.on_color_click_2, bg=self.convert_To_Hex(self.color_palette[1]))

        self.site_shadow_3_color_label = tk.Label(self, text="Site Shadow 3 Color", font= self.label_font)
        self.site_shadow_3_color_button = tk.Button(self, text="Choose Color", command=self.on_color_click_3, bg=self.convert_To_Hex(self.color_palette[2]))

        self.site_shadow_4_color_label = tk.Label(self, text="Site Shadow 4 Color", font= self.label_font)
        self.site_shadow_4_color_button = tk.Button(self, text="Choose Color", command=self.on_color_click_4, bg=self.convert_To_Hex(self.color_palette[3]))

        self.site_shadow_5_color_label = tk.Label(self, text="Site Shadow 5 Color", font= self.label_font)
        self.site_shadow_5_color_button = tk.Button(self, text="Choose Color", command=self.on_color_click_5, bg=self.convert_To_Hex(self.color_palette[4]))

        self.ok_button = tk.Button(self, text="OK", command=self.on_ok_click, font = self.label_font)
        self.save_button = tk.Button(self,text = "Save Setting",command = self.on_save_click, font = self.label_font)
        self.load_button = tk.Button(self, text="Load from File", command=self.on_load_click, font = self.label_font)
        self.advance_button = tk.Button(self, text="Advance Setting", command=self.on_advance_click, font = self.label_font)

        self.ok_button.grid(row=0, column=0, padx=15, pady=5, sticky='nsew',columnspan=3)
        self.load_button.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')
        self.save_button.grid(row=1, column=1, padx=15, pady=15, sticky='nsew')
        self.advance_button.grid(row=2, column=0, columnspan=2, padx=15, pady=15, sticky='nsew')

    def configure_grid(self):
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        for i in range(4):
            self.grid_rowconfigure(i, weight=1)

    def toggle_advanced_visibility(self):
        if self.advanced_visible:
            self.shadow_multiply_ratio_label.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
            self.shadow_multiply_ratio_entry.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')
            self.shadow_multiply_ratio_entry.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')

            self.roof_lighter_ratio_label.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
            self.roof_lighter_ratio_entry.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')
            self.roof_lighter_ratio_entry.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')

            self.site_shadow_1_color_label.grid(row=5, column=0, padx=5, pady=5, sticky='nsew')
            self.site_shadow_1_color_button.grid(row=5, column=1, padx=5, pady=5, sticky='nsew')
            self.site_shadow_2_color_label.grid(row=6, column=0, padx=5, pady=5, sticky='nsew')
            self.site_shadow_2_color_button.grid(row=6, column=1, padx=5, pady=5, sticky='nsew')
            self.site_shadow_3_color_label.grid(row=7, column=0, padx=5, pady=5, sticky='nsew')
            self.site_shadow_3_color_button.grid(row=7, column=1, padx=5, pady=5, sticky='nsew')
            self.site_shadow_4_color_label.grid(row=8, column=0, padx=5, pady=5, sticky='nsew')
            self.site_shadow_4_color_button.grid(row=8, column=1, padx=5, pady=5, sticky='nsew')
            self.site_shadow_5_color_label.grid(row=9, column=0, padx=5, pady=5, sticky='nsew')
            self.site_shadow_5_color_button.grid(row=9, column=1, padx=5, pady=5, sticky='nsew')
        else:
            self.shadow_multiply_ratio_label.grid_forget()
            self.shadow_multiply_ratio_entry.grid_forget()
            self.roof_lighter_ratio_label.grid_forget()
            self.roof_lighter_ratio_entry.grid_forget()
            self.site_shadow_1_color_label.grid_forget()
            self.site_shadow_1_color_button.grid_forget()
            self.site_shadow_2_color_label.grid_forget()
            self.site_shadow_2_color_button.grid_forget()
            self.site_shadow_3_color_label.grid_forget()
            self.site_shadow_3_color_button.grid_forget()
            self.site_shadow_4_color_label.grid_forget()
            self.site_shadow_4_color_button.grid_forget()
            self.site_shadow_5_color_label.grid_forget()
            self.site_shadow_5_color_button.grid_forget()

if __name__ == "__main__":
    app = TinkerForm()
    app.advanced_visible = False
    app.mainloop()
