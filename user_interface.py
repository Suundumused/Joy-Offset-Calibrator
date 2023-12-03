import os
import sys
import threading
import time
import customtkinter

from translation import translate_txt
from rw_config import write_config

class UI:
    def translate_msg_display(self, vars):
        if vars.msg != '':
            self.SenseLabel12.configure(text = translate_txt(vars.msg))
            
        else:
            self.SenseLabel12.configure(text = '')
        
    def real_time_update_texts(self, vars):
        while vars.KeepMain:
            self.SenseLabel6.configure(text = f"DL_X - O: {vars.axis[0]:.4f} | M: {vars.new_axis[0]:.4f}")
            self.SenseLabel7.configure(text = f"DL_Y - O: {vars.axis[1]:.4f} | M: {vars.new_axis[1]:.4f}")
            self.SenseLabel8.configure(text = f"DR_X - O: {vars.axis[2]:.4f} | M: {vars.new_axis[2]:.4f}")
            self.SenseLabel9.configure(text = f"DR_Y - O: {vars.axis[3]:.4f} | M: {vars.new_axis[3]:.4f}")
            self.SenseLabel10.configure(text = f"LT - O: {vars.axis[4]:.4f} | M: {vars.new_axis[4]:.4f}")
            self.SenseLabel11.configure(text = f"RT - O: {vars.axis[5]:.4f} | M: {vars.new_axis[5]:.4f}")
            
            thread4 = threading.Thread(target = self.translate_msg_display, args=(vars, ))
            thread4.daemon = False
            thread4.start()
            
            time.sleep(0.125)
    
    def reset_slider(selft, slider, label):
        slider.set(0.0)
        
        label.configure(text=f"{label.cget('text')[:label.cget('text').find('|')]}|  {0.0}")
        
    def on_slider_release(self, slider, label):
        value = slider.get()
        label.configure(text=f"{label.cget('text')[:label.cget('text').find('|')]}|  {value:.2f}")
            
    def save_config(self, vars):
        if (self.entry.get()).isnumeric():
            vars.joy_id = int(self.entry.get())
            
        else:
            vars.joy_id = -1

        context = {
            "usages": {
                "use_l_analog": bool(self.switch_1.get()), 
                "use_r_analog": bool(self.switch_2.get()),
                "use_l_trigger": bool(self.switch_3.get()),
                "use_r_trigger": bool(self.switch_4.get()),
                "replicate_btns": bool(self.switch_5.get()),
                "joy_id": vars.joy_id        
            },
                
            "offsets": {
                "l_analog_offset_x": self.slider.get(),
                "l_analog_offset_y": self.slider1.get(),
                "r_analog_offset_x": self.slider2.get(),
                "r_analog_offset_y": self.slider3.get(),
                "l_trigger_offset": self.slider4.get(),
                "r_trigger_offset": self.slider5.get() 
            }
        }

        vars.config = context
                
        write_config(context)

    def shutdown(self, vars):
        vars.ReadInput = False
        vars.KeepMain = False
        
        sys.exit()
        
    def __init__(self, vars):
        self.root = customtkinter.CTk()
        customtkinter.set_default_color_theme("green")
        
        config_name = 'ico'
        
        if getattr(sys, 'frozen', False):  #-----ATUALIZADO-----
            # Executando como executable (PyInstaller)
            path = os.path.dirname(sys.executable)
        else:
            # Executando como  script .py
            path = os.path.dirname(os.path.abspath(sys.argv[0]))
                
        icon_path = os.path.join(path, config_name+"/emucon.ico")
        
        self.cwd = os.path.expanduser(os.getenv('USERPROFILE'))
        self.cwd = self.cwd=str(str(self.cwd) + '\AppData\Local\Joy_Offset\Settings')

        self.root.title("Joy Offset")
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.shutdown(vars))
        self.root.iconbitmap(icon_path)
        
        self.app_width = int(0.33 * self.root.winfo_screenwidth())
        self.app_height = int(0.89 * self.root.winfo_screenheight())
        
        self.root.resizable(0,0)
        self.root.eval('tk::PlaceWindow . center')
        self.root.geometry('%dx%d+%d+%d' % (self.app_width, self.app_height, (self.root.winfo_screenwidth() //2 - self.app_width // 2), (self.root.winfo_screenheight() // 2 - self.app_height // 2 - 48)))
        
        self.title = customtkinter.CTkLabel(master = self.root, text = "Joy Offset", font = ("Roboto", 22))
        self.title.pack(pady=(20,0), padx=0)
        
        self.frameA = customtkinter.CTkFrame(master=self.root)
        self.frameA.pack(pady=(20,0), padx=60, fill="x", expand=False)
        
        self.entry = customtkinter.CTkEntry(master = self.frameA, placeholder_text = f"Joystick ID {vars.joy_id}", justify="center")
        self.entry.pack(pady=12, padx=(10), fill="x")
        
        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=(20,0), padx=60, fill="x", expand=False)
        
        self.switch1_var = customtkinter.IntVar(value = vars.config['usages']['use_l_analog'])
        self.switch_1 = customtkinter.CTkSwitch(master=self.frame, text="Use left analog",  onvalue=1, offvalue=0, variable = self.switch1_var)
        self.switch_1.pack(pady=6, padx=6, fill="x", expand=True)
        
        self.switch2_var = customtkinter.IntVar(value = vars.config['usages']['use_r_analog'])
        self.switch_2 = customtkinter.CTkSwitch(master=self.frame, text="Use right analog",  onvalue=1, offvalue=0, variable = self.switch2_var)
        self.switch_2.pack(pady=6, padx=6, fill="x", expand=True)
        
        self.switch3_var = customtkinter.IntVar(value = vars.config['usages']['use_l_trigger'])
        self.switch_3 = customtkinter.CTkSwitch(master=self.frame, text="Use left trigger",  onvalue=1, offvalue=0, variable = self.switch3_var)
        self.switch_3.pack(pady=6, padx=6, fill="x", expand=True)
        
        self.switch4_var = customtkinter.IntVar(value = vars.config['usages']['use_r_trigger'])
        self.switch_4 = customtkinter.CTkSwitch(master=self.frame, text="Use right trigger",  onvalue=1, offvalue=0, variable = self.switch4_var)
        self.switch_4.pack(pady=6, padx=6, fill="x", expand=True)
        
        self.switch5_var = customtkinter.IntVar(value = vars.config['usages']['replicate_btns'])
        self.switch_5 = customtkinter.CTkSwitch(master=self.frame, text="Replicate buttons",  onvalue=1, offvalue=0, variable = self.switch5_var)
        self.switch_5.pack(pady=6, padx=6, fill="x", expand=True)
        
        self.frame3 = customtkinter.CTkFrame(master=self.root)
        self.frame3.pack(pady=(20,0),  padx=60, fill="x", expand=False)
        
        self.slider = customtkinter.CTkSlider(master=self.frame3, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider.pack(pady=1, padx=(1,6), fill="x", expand=False, side = "left")
        self.slider.set(vars.config['offsets']['l_analog_offset_x'])
        
        self.SenseLabel = customtkinter.CTkLabel(master = self.frame3, text=f"Left analog offset X  |  {vars.config['offsets']['l_analog_offset_x']:.2f}", font = ("Roboto", 14))
        self.SenseLabel.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_0 = customtkinter.CTkButton(master=self.frame3, border_width=0, corner_radius=8, text="Reset", width=30, command = lambda: self.reset_slider(self.slider, self.SenseLabel))
        self.button_0.pack(pady=0, padx=6, side = "right")
        
        self.slider.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider, self.SenseLabel))
        
        self.frame4 = customtkinter.CTkFrame(master=self.root)
        self.frame4.pack(pady=(0,0),  padx=60, fill="x", expand=False)
        
        self.slider1 = customtkinter.CTkSlider(master=self.frame4, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider1.pack(pady=1, padx=(1,6), fill="x", expand=False, side = "left")
        self.slider1.set(vars.config['offsets']['l_analog_offset_y'])
        
        self.SenseLabel1 = customtkinter.CTkLabel(master = self.frame4, text=f"Left analog offset Y  |  {vars.config['offsets']['l_analog_offset_y']:.2f}", font = ("Roboto", 14))
        self.SenseLabel1.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_1 = customtkinter.CTkButton(master=self.frame4, border_width=0, corner_radius=8, text="Reset", width=30, command = lambda: self.reset_slider(self.slider1, self.SenseLabel1))
        self.button_1.pack(pady=0, padx=6, side = "right")
        
        self.slider1.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider1, self.SenseLabel1))
        
        self.frame5 = customtkinter.CTkFrame(master=self.root)
        self.frame5.pack(pady=(20,0),  padx=60, fill="x", expand=False)
        
        self.slider2 = customtkinter.CTkSlider(master=self.frame5, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider2.pack(pady=1, padx=(1,6), fill="x", expand=False, side = "left")
        self.slider2.set(vars.config['offsets']['r_analog_offset_x'])
        
        self.SenseLabel2 = customtkinter.CTkLabel(master = self.frame5, text=f"Right analog offset X  |  {vars.config['offsets']['r_analog_offset_x']:.2f}", font = ("Roboto", 14))
        self.SenseLabel2.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_2 = customtkinter.CTkButton(master=self.frame5, border_width=0, corner_radius=8, text="Reset", width=30, command = lambda: self.reset_slider(self.slider2, self.SenseLabel2))
        self.button_2.pack(pady=0, padx=6, side = "right")
        
        self.slider2.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider2, self.SenseLabel2))
        
        self.frame6 = customtkinter.CTkFrame(master=self.root)
        self.frame6.pack(pady=(0,0),  padx=60, fill="x", expand=False)
        
        self.slider3 = customtkinter.CTkSlider(master=self.frame6, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider3.pack(pady=1, padx=(1,6), fill="x", expand=False, side = "left")
        self.slider3.set(vars.config['offsets']['r_analog_offset_y'])
        
        self.SenseLabel3 = customtkinter.CTkLabel(master = self.frame6, text=f"Right analog offset Y  |  {vars.config['offsets']['r_analog_offset_y']:.2f}", font = ("Roboto", 14))
        self.SenseLabel3.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_3 = customtkinter.CTkButton(master=self.frame6, border_width=0, corner_radius=8, text="Reset", width=30, command = lambda: self.reset_slider(self.slider3, self.SenseLabel3))
        self.button_3.pack(pady=0, padx=6, side = "right")
        
        self.slider3.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider3, self.SenseLabel3))
        
        self.frame7 = customtkinter.CTkFrame(master=self.root)
        self.frame7.pack(pady=(20,0),  padx=60, fill="x", expand=False)
        
        self.slider4 = customtkinter.CTkSlider(master=self.frame7, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider4.pack(pady=1, padx=(1,6), fill="x", expand=False, side = "left")
        self.slider4.set(vars.config['offsets']['l_trigger_offset'])
        
        self.SenseLabel4 = customtkinter.CTkLabel(master = self.frame7, text=f"Left trigger_offset  |  {vars.config['offsets']['l_trigger_offset']:.2f}", font = ("Roboto", 14))
        self.SenseLabel4.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_4 = customtkinter.CTkButton(master=self.frame7, border_width=0, corner_radius=8, text="Reset", width=30, command = lambda: self.reset_slider(self.slider4, self.SenseLabel4))
        self.button_4.pack(pady=0, padx=6, side = "right")
        
        self.slider4.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider4, self.SenseLabel4))
        
        self.frame8 = customtkinter.CTkFrame(master=self.root)
        self.frame8.pack(pady=(0,0),  padx=60, fill="x", expand=False)
        
        self.slider5 = customtkinter.CTkSlider(master=self.frame8, border_width=5.5, width = 150, from_ = -1, to = 1)
        self.slider5.pack(pady=1, padx=(1,6), fill="x", expand=False, side = "left")
        self.slider5.set(vars.config['offsets']['r_trigger_offset'])
        
        self.SenseLabel5 = customtkinter.CTkLabel(master = self.frame8, text=f"Right trigger_offset  |  {vars.config['offsets']['r_trigger_offset']:.2f}", font = ("Roboto", 14))
        self.SenseLabel5.pack(pady=3, padx=(6,1), side = "left")
        
        self.button_5 = customtkinter.CTkButton(master=self.frame8, border_width=0, corner_radius=8, text="Reset", width=30, command = lambda: self.reset_slider(self.slider5, self.SenseLabel5))
        self.button_5.pack(pady=0, padx=6, side = "right")
        
        self.slider5.bind("<ButtonRelease-1>", lambda event: self.on_slider_release(self.slider5, self.SenseLabel5))
        
        self.frame9 = customtkinter.CTkFrame(master=self.root)
        self.frame9.pack(pady=(20,0),  padx=60, fill="x", expand=False)
        
        self.SenseLabel6 = customtkinter.CTkLabel(master = self.frame9, font = ("Roboto", 14))
        self.SenseLabel6.pack(pady=3, padx=(6,1), side = "top")
        
        self.SenseLabel7 = customtkinter.CTkLabel(master = self.frame9, font = ("Roboto", 14))
        self.SenseLabel7.pack(pady=3, padx=(6,1), side = "top")
        
        self.SenseLabel8 = customtkinter.CTkLabel(master = self.frame9, font = ("Roboto", 14))
        self.SenseLabel8.pack(pady=3, padx=(6,1), side = "top")
        
        self.SenseLabel9 = customtkinter.CTkLabel(master = self.frame9, font = ("Roboto", 14))
        self.SenseLabel9.pack(pady=3, padx=(6,1), side = "top")
        
        self.SenseLabel10 = customtkinter.CTkLabel(master = self.frame9, font = ("Roboto", 14))
        self.SenseLabel10.pack(pady=3, padx=(6,1), side = "top")
        
        self.SenseLabel11 = customtkinter.CTkLabel(master = self.frame9, font = ("Roboto", 14))
        self.SenseLabel11.pack(pady=3, padx=(6,1), side = "top")
        
        self.SenseLabel12 = customtkinter.CTkLabel(master = self.root, text = vars.msg,font = ("Roboto", 16))
        self.SenseLabel12.pack(pady=20, padx=(6,1), side = "top")
        
        self.button_x = customtkinter.CTkButton(master=self.root, border_width=0, corner_radius=8, text="Settings Folder", command = lambda: os.startfile(self.cwd))
        self.button_x.pack(pady=6, padx=1, side = "bottom", expand = True)
        
        self.button = customtkinter.CTkButton(master=self.root, border_width=0, corner_radius=8, text="Save", command = lambda: self.save_config(vars))
        self.button.pack(pady=6, padx=1, side = "bottom", expand = True)
        
        thread3 = threading.Thread(target = self.real_time_update_texts, args=(vars, ))
        thread3.daemon = True
        thread3.start()
                
        self.root.mainloop()
