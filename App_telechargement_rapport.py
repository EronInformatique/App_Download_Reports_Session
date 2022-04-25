import os
import sys
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import askokcancel, WARNING
from tkinter import messagebox
import threading
import tkmacosx as tkm
from PIL import Image,ImageTk
from Packages.send_infos_chrome import send_infos_to_chrome
from Packages.send_formation_info import send_formation_info
from Packages.download_reports import download_reports

class MyFirstGUI:
    """Telechargement de rapport de session"""
    def __init__(self, master):
        self.master = master
        master.title("Rapports Session")

        self.popup = Toplevel
        self.list_formations=[]
        self.list_gp_formations=[]
        #Setup
        self.secondary_color="#ffffff"
        self.main_color="#003166"
        hgth_ipt = 30
        wdth_ipt = 189
        font_size_label=14
        font_type="SF Compact"

        master.geometry("694x384")
        master.configure(bg = self.secondary_color)
        master.option_add('*Font', 'SF_Compact 14')
        canvas = Canvas(
            master,
            bg = self.secondary_color,
            height = 384,
            width = 794,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)
        canvas.pack()


        #Load an image in the script
        self.logo_img= Image.open(resource_path("./Images/logo-eronvidal-171x63.jpg"))
        # self.logo_img= Image.open("./Images/logo-eronvidal-171x63.jpg")
        self.new_image= ImageTk.PhotoImage(self.logo_img)
        # create label
        self.logo= Label(image=self.new_image,borderwidth = 0)
        self.logo.place(x=0,y=0)
        
        # Titre de la fenêtre
        self.titre_h1= Label(self.master,
        text="Téléchargement de rapports de sessions",
        fg=self.main_color,
        bg=self.secondary_color,
        font=("SF Compact",int(24.0)),
        wraplength=691-171,
        justify="center"
        )
        self.titre_h1.place(x=200,y=0)

        #Label et Input Id password
        # the label for user_name 
        self.user_name_label = Label(self.master, 
                        text = "1.Identifiant",
                        fg=self.main_color,
                        bg=self.secondary_color,
                        )
        self.user_name_label.place(x = 22,y = 76)  
        self.user_name_entry = Entry(self.master, 
                        fg=self.main_color,
                        bg=self.secondary_color,
                        bd =0,
                        selectborderwidth=0,
                        )
        self.user_name_entry.place(x = 22,y = 96)  
            
        # the label for user_password  
        self.user_password_label = Label(self.master, 
                            fg=self.main_color,
                            bg=self.secondary_color,
                            text = "2.Mot de passe")
        self.user_password_label.place(x = 22,y = 128)  

        self.user_passwd_entry = Entry(self.master, 
                        fg=self.main_color,
                        bg=self.secondary_color,
                        bd =0,
                        show="*",
                        selectborderwidth=0,
                        )
        self.user_passwd_entry.place(x = 22,y =150)  
        # Label et Input Reference formation
        self.ref_formation = Label(self.master, 
                            fg=self.main_color,
                            bg=self.secondary_color,
                            text = "3.Référence formation (ex: KIN002)(*)")
        self.ref_formation.place( x = 290+90,y = 128) 
        self.ref_formation_entry = Entry(self.master, 
                        fg=self.main_color,
                        bg=self.secondary_color,
                        bd =0,
                        selectborderwidth=0,
                        )
        self.ref_formation_entry.place(x = 290+90,y =150)  
        # Label et Input Temps autorisé
        self.time_limit = Label(self.master, 
                            fg=self.main_color,
                            bg=self.secondary_color,
                            text = "Temps limite d'attente de GAFEO (s)")
        self.time_limit.place( x = 290+90,y = 76) 
        self.time_limit_entry = Entry(self.master, 
                        fg=self.main_color,
                        bg=self.secondary_color,
                        bd =0,
                        selectborderwidth=0,
                        width=5
                        )
        self.time_limit_entry.place(x = 290+90,y =96)  
        self.time_limit_entry.place(x = 290+90,y =96)  

 # the label for formation to select 
        self.dpdwn_formation_label = Label(self.master, 
                            fg=self.main_color,
                            bg=self.secondary_color,
                            text = "4.Selectionner la formation(*):")
        self.dpdwn_formation_label.place(x = 22,y = 245)  

        self.dpdwn_formation = ttk.Combobox(self.master, values=["Empty"],width=30,
                            postcommand = self.updtcblist,state="disabled")
        self.dpdwn_formation.place(x = 22,y = 266)    

        self.dpdwn_formation.bind("<<ComboboxSelected>>", self.send_combox_info)
 # the label for group formation to select 
        self.dpdwn_gp_formation_label = Label(self.master, 
                            fg=self.main_color,
                            bg=self.secondary_color,
                            text = "5.Selectionner le groupe de formation (*):")
        self.dpdwn_gp_formation_label.place(x = 290+90,y = 245)  

        self.dpdwn_gp_formation = ttk.Combobox(self.master, values=["Empty"],width=32,
                            postcommand = self.updtcblist_gp,state="disabled")
        self.dpdwn_gp_formation.place(x = 290+80,y = 266)    

        # self.dpdwn_gp_fformation.bind("<<ComboboxSelected>>", self.send_combox_info)
# Premier boutton pour envoie d'informations
        self.first_button = tkm.Button(self.master,text="Envoyer les infos",
                                bg=self.main_color,
                                fg=self.secondary_color,
                                command=self.click_look_for_session
                                )
        self.first_button.place(x = 217+30,y =192)
# Deuxieme boutton pour envoie d'informations
        self.second_button = tkm.Button(self.master,text="Télécharger les rapports",
                                bg=self.main_color,
                                fg=self.secondary_color,
                                # command=self.new_process
                                command=self.click_download_reports 
                                )
        self.second_button.place(x = 200+30,y =325)

 # the label for field must be filled 
        self.info_labels = Label(self.master, 
                            fg=self.main_color,
                            bg=self.secondary_color,
                            text = "Champs obligatoire (*)")
        self.info_labels.place(x = 0,y = 360)  
    
    # def new_process(self):
    #     threading.Thread(target=self.click_download_reports).start()

    def click_look_for_session(self):
        """Look for session"""
        ref=self.ref_formation_entry.get()
        if (len(self.ref_formation_entry.get())==0):
             messagebox.showerror(title="Champs manquants", message="La référence de formation est requise",icon=WARNING)
             return
        self.list_formations,self.browser, self.directory_download = send_infos_to_chrome(ref,self.time_limit_entry,self.user_name_entry,self.user_passwd_entry)
        if self.list_formations == "error":
            self.close_browser_and_restart()
        else:
            self.dpdwn_formation["state"]="normal"
    
    def updtcblist(self):
        """Update list"""
        self.dpdwn_formation["values"] =self.list_formations

    def updtcblist_gp(self):
        """Update lsit"""
        self.dpdwn_gp_formation["values"] =self.list_gp_formations

    def send_combox_info(self,event):
        """Combobox update"""
        ref=self.ref_formation_entry.get()
        browser= self.browser
        self.formation_selected= event.widget.get()
        self.list_gp_formations = send_formation_info(self.formation_selected,ref,browser,self.time_limit_entry)
        if self.list_gp_formations == "error":
            self.close_browser_and_restart()
        else:
            self.dpdwn_gp_formation["state"]="normal"

    def click_download_reports(self):
        "download reports"
        if (self.dpdwn_formation.get()=="" or self.dpdwn_gp_formation.get()=="" or len(self.ref_formation_entry.get())==0):
             messagebox.showerror(title="Champs manquants", message="Vous devez renseigner les champs obligatoire",icon=WARNING)
             return
        self.gp_formation_selected=self.dpdwn_gp_formation.get()
        res = download_reports(self,self.gp_formation_selected,self.browser,self.time_limit_entry)
        if res == "error":
            self.close_browser_and_restart()

    def on_closing(self):   
        """Close button"""
        answer = askokcancel(
            title='Confirmation',
            message="Quitter l'application ?",
            icon=WARNING)
        if answer:
            if hasattr(self, 'browser'):
                self.browser.quit()
            self.master.quit()

    def close_browser_and_restart(self):
        """close browser and restart"""
        self.dpdwn_formation.delete(0,END)
        self.dpdwn_formation["state"]="disabled"
        self.dpdwn_gp_formation.delete(0,END)
        self.dpdwn_gp_formation["state"]="disabled"
        self.browser.quit()

def resource_path(relative_path):
    """Necessaire pour indiquer les chemins relatif des images et autres datas pour le build"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.dirname(__file__), relative_path.replace("./",""))


# def main():
if __name__ == "__main__":
    root = Tk()
    my_gui = MyFirstGUI(root)
    root.protocol("WM_DELETE_WINDOW", my_gui.on_closing)
    root.mainloop()
    root.destroy()
    print("EXIT")


