next=False
Background_color_hexStr=""
CmdNum=0
font= {'family': 'Cascadia code ', 'size': 14}
from tkinter import *
from pathlib import Path
Usr_home_dir=str(Path.home())
from tkinter import colorchooser
from tkfontchooser import askfont
from tkinter import filedialog
pathToSettingFile=Usr_home_dir+'\\AppData\\Local\\Packages\\Microsoft.WindowsTerminal_8wekyb3d8bbwe\\LocalState\\settings.json'
import json
def uncommentJson():
    a_file = open(pathToSettingFile, "r")

    lines = a_file.readlines()
    a_file.close()

    new_file = open(pathToSettingFile, "w")
    for line in lines:
        print(line)
        tempLine=line.replace(' ','')
        if not tempLine.startswith("//"):
            new_file.write(line)

    new_file.close()
uncommentJson()
CMD_OPTIONS = [
"Command Prompt",
"Windows PowerShell"
] 
COLOR_SCHEMES=[
    "Tango Light",
    "Tango Dark",
    "Solarized Light",
    "Solarized Dark",
    "One Half Light",
    "One Half Dark",
    "Vintage",
    "Campbell Powershell",
    "Campbell"
]

with open(pathToSettingFile) as json_file:
    data = json.load(json_file)
    cmdLinePref=data['profiles']['list']
    print(cmdLinePref)
    master = Tk()

    hidden_checkbox_var=BooleanVar()

    no_transparency_var=BooleanVar()

    default_shell_checkbox_var=BooleanVar()

    No_background_checkbox_var=BooleanVar()

    Cmdvariable = StringVar(master)
    Cmdvariable.set('Choose Shell')

    ClrScheme_var= StringVar(master)
    ClrScheme_var.set('Choose Theme')
#CMD PROMPT
    chooseCmd = OptionMenu(master, Cmdvariable, *CMD_OPTIONS)
    chooseCmd.pack(side="top")

#Theme
    choose_color_scheme= OptionMenu(master,ClrScheme_var, *COLOR_SCHEMES)
    choose_color_scheme.pack(side="top")
#Hidden?
    choose_hidden_checkbox=Checkbutton(master, text="Hide Shell?", variable=hidden_checkbox_var,onvalue=True,offvalue=False)
    choose_hidden_checkbox.pack(side="top")
#Set shell as default?
    default_shell= Checkbutton(master,text="Set shell as default?", variable=default_shell_checkbox_var, onvalue=True, offvalue=False)
    default_shell.pack(side="top")
#No background color for
    Background_is_transparent=Checkbutton(master, text="No Background Color", variable=No_background_checkbox_var,onvalue=True,offvalue=False)
    Background_is_transparent.pack(side="top")
#Background color
    def choose_background_color():
        global Background_color_hexStr
        Background_color_hexStr=colorchooser.askcolor()[1]
        choose_background_color_button.config(bg=Background_color_hexStr)

    choose_background_color_button= Button(master, text="Pick a color", command=choose_background_color)
    choose_background_color_button.pack(side='top')
#Background Image
    #TODO
#Slider
    Choose_background_transparency = Scale(master, from_=00, to=100, orient=HORIZONTAL)
    Choose_background_transparency.pack(side="top")
# No Tranparency
    no_transparency = Checkbutton(master, text="Set No Transparency", variable=no_transparency_var, onvalue=True, offvalue=False)
    no_transparency.pack(side='top')

    def choose_font():
        global font
        font = askfont(master)
    choose_font_button= Button(master, text="Pick Font", command=choose_font)
    choose_font_button.pack(side='top')


    def Apply_Changes():
        global Choose_background_transparency, no_transparency_var
        global data, default_shell_checkbox_var
        global Background_color_hexStr
        global chooseCmd, next, CmdNum
        cmdName= Cmdvariable.get()
        for CmdNum in range(len(cmdLinePref)-1):
            
            if cmdName==cmdLinePref[CmdNum]['name']:
                break
        if ClrScheme_var.get() in  COLOR_SCHEMES:
            cmdLinePref[CmdNum]['colorScheme']=ClrScheme_var.get()
        cmdLinePref[CmdNum]['hidden']=hidden_checkbox_var.get()
        if No_background_checkbox_var.get()==False and not Background_color_hexStr=="":
            cmdLinePref[CmdNum]['background']=Background_color_hexStr
        else:
            if 'background' in cmdLinePref[CmdNum]:
                del cmdLinePref[CmdNum]['background']
        cmdLinePref[CmdNum]['fontFace']=font['family']
        cmdLinePref[CmdNum]['fontSize']=font['size']
        id=""
        if default_shell_checkbox_var.get():
            id=cmdLinePref[CmdNum]['guid']
            data['defaultProfile']=id
        print(no_transparency_var.get())
        if no_transparency_var.get():
            cmdLinePref[CmdNum]['useAcrylic']=False
        
        else:
            cmdLinePref[CmdNum]['useAcrylic']=True
            cmdLinePref[CmdNum]['acrylicOpacity']=float(Choose_background_transparency.get()/100)
        with open(pathToSettingFile, 'w') as outfile:
            json.dump(data, outfile)
    button = Button(master, text="Set_All", command=Apply_Changes)
    button.pack(side="top")   
mainloop()