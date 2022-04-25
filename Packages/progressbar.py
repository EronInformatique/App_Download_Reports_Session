import sys
from tkinter import *
from tkinter import ttk
import tkmacosx as tkm
class MyProgressBar:
    """Progress bar customisable en mettant le nombre maximum a atteindre pour obtenir la fin du téléchargement"""
    def __init__(self, master,max):
        self.master = master
        self.popup = master.popup()
        self.var = StringVar()
        self.progress_var =DoubleVar()
        self.progress_var.set(1)
        self.pdfdownloaded=0
        Label(self.popup, text="Fichiers en cours de téléchargement:").pack()
        Label(self.popup, textvariable=self.var).pack()
        self.my_progress = ttk.Progressbar(self.popup,
         orient=HORIZONTAL,length=300,mode='determinate',
         variable=self.progress_var, maximum=max)
        self.my_progress.pack(side="top", fill="x", ipady=20)
        self.my_progress["value"]=1
        # self.my_progress.pack(pady=20)

    
    def update_value(self):
        """Update value each time this function is called"""
        self.pdfdownloaded=self.pdfdownloaded+1
        self.my_progress["value"]=self.pdfdownloaded
        self.progress_var.set(self.pdfdownloaded)
        self.var.set(str(int(self.my_progress["value"]))+"/"+str(self.my_progress["maximum"]))
        print("ProgressBar var value:",self.progress_var.get())
        print("ProgressBar value:",self.my_progress["value"])
        print("ProgressBar Max:",self.my_progress["maximum"])
        self.my_progress.update()
        self.popup.update_idletasks()
        
        if int(self.my_progress["value"])==int(self.my_progress["maximum"]):
                    Label(self.popup,text="Téléchargement terminé").pack()
                    btn=tkm.Button(self.popup,text="Ok",
                                bg=self.master.main_color,
                                fg=self.master.secondary_color,
                                command=self.master.on_closing
                                )
                    btn.pack()
                    # btn.wait_variable()
    
    # def click_done_download(self):
    #     self.master.on_closing()
        # try:
        #     exit()
        # except:
        #     exit()

    def close_popup(self):
        self.popup.destroy()