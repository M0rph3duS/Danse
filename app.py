#!/usr/bin/env python3
"""

"""
#############
### TO-DO ###
#############

"""

modifier la taille fenetre modal inscirption cours fonction si solo
valider l'inscription
rajouter un contour pour les cours déja pris, et si on double clic sur un cours existant, faudrait que le bouto ns'inscrire se change en desinscrire, ça serait topismale

permettre le choix du cours et l'inscription depuis une modale planning

mettre un carré flottant sur le planning avec description en mouseover
améliorer l'hover sur le planning la c'est moche claro


"""
#    .....     .                                                                  s    
#  .d88888Neu. 'L                                                                :8    
#  F""""*8888888F    ..    .     :     .d``                u.      .u    .      .88    
# *      `"*88*"   .888: x888  x888.   @8Ne.   .u    ...ue888b   .d88B :@8c    :888ooo 
#  -....    ue=:. ~`8888~'888X`?888f`  %8888:u@88N   888R Y888r ="8888f8888r -*8888888 
#         :88N  `   X888  888X '888>    `888I  888.  888R I888>   4888>'88"    8888    
#         9888L     X888  888X '888>     888I  888I  888R I888>   4888> '      8888    
#  uzu.   `8888L    X888  888X '888>     888I  888I  888R I888>   4888>        8888    
#,""888i   ?8888    X888  888X '888>   uW888L  888' u8888cJ888   .d888L .+    .8888Lu= 
#4  9888L   %888>  "*88%""*88" '888!` '*88888Nu88P   "*888*P"    ^"8888*"     ^%888*   
#'  '8888   '88%     `~    "    `"`   ~ '88888F`       'Y"          "Y"         'Y"    
#     "*8Nu.z*"                          888 ^                                         
#                                        *8E                                           
#                                        '8>                                           
#         

import sqlite3
import tkinter as tk
from tkinter import ttk,messagebox,colorchooser
import re
from datetime import datetime
from typing import ReadOnly



#   _                                     .                      ..          ..               .x+=:.   
#  u                                     @88>              . uW8"      x .d88"               z`    ^%  
# 88Nu.   u.                 .u    .     %8P               `t888        5888R                   .    k 
#'88888.o888c       u      .d88B :@8c     .          u      8888   .    '888R        .u       .@8Ned8" 
# ^8888  8888    us888u.  ="8888f8888r  .@88u     us888u.   9888.z88N    888R     ud8888.   .@^%8888"  
#  8888  8888 .@88 "8888"   4888>'88"  ''888E` .@88 "8888"  9888  888E   888R   :888'8888. x88:  `)8b. 
#  8888  8888 9888  9888    4888> '      888E  9888  9888   9888  888E   888R   d888 '88%" 8888N=*8888 
#  8888  8888 9888  9888    4888>        888E  9888  9888   9888  888E   888R   8888.+"     %8"    R88 
# .8888b.888P 9888  9888   .d888L .+     888E  9888  9888   9888  888E   888R   8888L        @8Wou 9%  
#  ^Y8888*""  9888  9888   ^"8888*"      888&  9888  9888  .8888  888"  .888B . '8888c. .+ .888888P`   
#    `Y"      "888*""888"     "Y"        R888" "888*""888"  `%888*%"    ^*888%   "88888%   `   ^"F     
#              ^Y"   ^Y'                  ""    ^Y"   ^Y'      "`         "%       "YP'                
#                                                                                       
#

DB = "db.sqlite"
EMAIL_REGEX = re.compile(r".+@.+")
TEL_REGEX = re.compile(r"^\d{10}$")
CP_REGEX = re.compile(r"^\d{5}$")

#      ...                ..                .x+=:.      .x+=:.                 .x+=:.   
#   xH88"`~ .x8X    x .d88"                z`    ^%    z`    ^%               z`    ^%  
# :8888   .f"8888Hf  5888R                    .   <k      .   <k                 .   <k 
#:8888>  X8L  ^""`   '888R         u        .@8Ned8"    .@8Ned8"      .u       .@8Ned8" 
#X8888  X888h         888R      us888u.   .@^%8888"   .@^%8888"    ud8888.   .@^%8888"  
#88888  !88888.       888R   .@88 "8888" x88:  `)8b. x88:  `)8b. :888'8888. x88:  `)8b. 
#88888   %88888       888R   9888  9888  8888N=*8888 8888N=*8888 d888 '88%" 8888N=*8888 
#88888 '> `8888>      888R   9888  9888   %8"    R88  %8"    R88 8888.+"     %8"    R88 
#`8888L %  ?888   !   888R   9888  9888    @8Wou 9%    @8Wou 9%  8888L        @8Wou 9%  
# `8888  `-*""   /   .888B . 9888  9888  .888888P`   .888888P`   '8888c. .+ .888888P`   
#   "888.      :"    ^*888%  "888*""888" `   ^"F     `   ^"F      "88888%   `   ^"F     
#     `""***~"`        "%     ^Y"   ^Y'                             "YP'                
#                                                                                       
                                                                                       
# --- BasePage avec utilitaire pour bind clavier ---
class BasePage(tk.Frame):
    """
    Surcharge de la frame de base
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._focusable_widgets = []

    # ------------------------
    # Enregistrer les widgets focusables
    # ------------------------
    def register_focusable(self, *widgets):
        for w in widgets:
            if w not in self._focusable_widgets:
                self._focusable_widgets.append(w)

    # ------------------------
    # Configurer la navigation Tab / Shift+Tab
    # ------------------------
    def setup_tab_navigation(self):
        widgets = self._focusable_widgets
        n = len(widgets)

        for i, widget in enumerate(widgets):
            next_widget = widgets[(i + 1) % n]
            prev_widget = widgets[(i - 1) % n]

            def on_tab(event, nxt=next_widget, prv=prev_widget):
                # event.state & 0x1 détecte Shift (1 = Shift)
                if event.state & 0x1:
                    prv.focus_set()
                else:
                    nxt.focus_set()
                return "break"  # stop propagation

            # Tab / Shift+Tab (ISO_Left_Tab pour certains OS)
            widget.bind("<Tab>", on_tab)
            widget.bind("<ISO_Left_Tab>", on_tab)

    def _focus_next(self, event, widget):
        widget.focus_set()
        return "break"
    

    def bind_shortcuts(self, shortcuts: dict):
        def bind_recursive(widget):
            for key, callback in shortcuts.items():
                widget.bind(key, callback)

            for child in widget.winfo_children():
                bind_recursive(child)

        bind_recursive(self)


class App(tk.Tk):
    """
    Controller de l'application
    """
    def __init__(self):
        super().__init__()
        self.title("Dance Manager")
        self.geometry("800x800")
        self.bind_all("<Alt-q>",lambda e: self.destroy())

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (StartPage, AddUserPage, SeekUserPage, SeekResultPage, EditUserPage, GestionEcolePage, AddCoursPage, PlanningPage):
            frame = Page(container, self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, name, *args):
        frame = self.frames[name]
        frame.tkraise()
        self.after(100, frame.focus_set())

        # --- Focus automatique si le frame a une méthode on_show
        if hasattr(frame, "on_show"):
            frame.on_show()

        if hasattr(frame, "set_data"):
            frame.set_data(*args)


                    # --- Modifier la taille selon la frame ---
        if name == "StartPage":
            self.geometry("800x250+0+0")
        elif name == "AddUserPage":
            self.geometry("800x500+0+0")
        elif name == "EditUserPage":
            self.geometry("800x800+0+0")
        elif name == "GestionEcolePage":
            self.geometry("800x800+0+0")
        elif name == "AddCoursPage":
            self.geometry("800x350+0+0")
        elif name == "PlanningPage":
            self.geometry("1300x900+0+0")


class StartPage(BasePage):
    """
    Frame de la page d'accueil
    """
    def __init__(self, parent, controller):
        super().__init__(parent,controller)

        # --- Titre ---
        tk.Label(self, text="Bienvenue dans l'application Danse", 
                 font=("Arial", 18, "bold")).grid(row=1, column=0, columnspan=3, pady=(20, 30))

        # --- Cadres horizontaux ---
        gestion_danseurs = tk.LabelFrame(self, text="Gestion Danseurs", padx=10, pady=10)
        gestion_cours = tk.LabelFrame(self, text="Gestion des Cours", padx=10, pady=10)
        gestion_ecole = tk.LabelFrame(self, text="Gestion de l'École", padx=10, pady=10)

        # Placement en grille
        gestion_danseurs.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        gestion_cours.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
        gestion_ecole.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)

        # Faire que les colonnes s'étirent de manière égale
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # --- Boutons Gestion Danseurs ---
        self.btajoutDanseur = tk.Button(gestion_danseurs, text="Ajouter Danseur", 
                  command=lambda: controller.show_frame("AddUserPage"),underline=0)
        self.btajoutDanseur.pack(fill="x", pady=5)
        self.btseekDanseur = tk.Button(gestion_danseurs, text="Rechercher Danseur", 
                  command=lambda: self.open_search(),underline=0)
        self.btseekDanseur.pack(fill="x", pady=5)

        # --- Boutons Gestion des Cours ---
        self.btPlanning = tk.Button(gestion_cours, text="Planning", 
                  command=lambda: controller.show_frame("PlanningPage"),underline=0)
        self.btPlanning.pack(fill="x", pady=5)
        self.ajoutCours = tk.Button(gestion_cours, text="Ajout de cours", 
                  command=lambda: controller.show_frame("AddCoursPage"),underline=9)
        self.ajoutCours.pack(fill="x", pady=5)

        # --- Boutons Gestion de l'École ---
        self.btGestionBdd = tk.Button(gestion_ecole, text="Gestion Base de données", 
                  command=lambda: controller.show_frame("DatabasePage"),underline=0)
        self.btGestionBdd.pack(fill="x", pady=5)
        self.btParameters = tk.Button(gestion_ecole, text="Parametres de l'école", 
                  command=lambda: controller.show_frame("GestionEcolePage"),underline=4)
        self.btParameters.pack(fill="x", pady=5)
        
        self.bind_shortcuts({
            "<Alt-a>": lambda e: controller.show_frame("AddUserPage"),
            "<Alt-m>": lambda e: controller.show_frame("GestionEcolePage"),
            "<Alt-c>": lambda e: controller.show_frame("AddCoursPage"),
            "<Alt-p>": lambda e: controller.show_frame("PlanningPage"),
            "<Alt-r>": lambda e: self.open_search()
        })

    def open_search(self):


        win = SearchUserWindow(self, self.controller)

        self.wait_window(win)   # attend que la fenêtre se ferme

        user_id = win.result

        if user_id:
            self.controller.show_frame("EditUserPage", user_id)

    def on_show(self):
        # après avoir créé tous les widgets focusables
        self.register_focusable(
            self.btajoutDanseur,
            self.btseekDanseur,
            self.btPlanning,
            self.ajoutCours,
            self.btGestionBdd,
            self.btParameters,
        )

        # configure Tab/Shift+Tab
        self.setup_tab_navigation()

########################
### Gestion Planning ###
########################
class PlanningPage(BasePage):
    """
    Vue planning des cours
    """
    WIDTH = 1100
    HEIGHT = 750
    LEFT_MARGIN = 50
    TOP_MARGIN = 50

    def __init__(self, parent, controller ,drag_enabled=True):
        super().__init__(parent, controller)

        self.controller = controller

        self.cours_items = {}  # {cours_id: {"rect": rect_id, "text": text_id}}
        self.drag_data = {}    # pour stocker les infos de drag
        self.hovered_cours_id = None  # tracking
        self.day_positions = {}

        self.LEFT_MARGIN = 30  # Marge pour les heures

        # Permettre de déplacer les cases
        self.drag_enabled = drag_enabled

        self.drag_data = {
            "cours_id": None,
            "rect": None,
            "text": None,
            "start_y": 0
        }
        
        # --- Header ---
        header_frame = tk.Frame(self)
        header_frame.pack(fill="x", pady=10)

        # Titre centré
        if self.drag_enabled:
            label_title = tk.Label(header_frame, text="Planning", font=("Arial", 16, "bold"))
        else:
            label_title = tk.Label(header_frame, text="Inscription a un cours", font=("Arial", 16, "bold"))
        label_title.pack()

        # Ligne centrée
        controls_frame = tk.Frame(header_frame)
        controls_frame.pack(pady=5)

        # --- Label Saison ---
        label_saison = tk.Label(controls_frame, text="Saison :")
        if self.drag_enabled:
            label_saison.pack(side="left", padx=(0, 5))

        # --- Combobox ---
        self.cb_saison = ttk.Combobox(controls_frame, state="readonly", width=10)
        if self.drag_enabled:
            self.cb_saison.pack(side="left", padx=5)

        load_cb_saison(self.cb_saison)
        self.cb_saison.bind("<<ComboboxSelected>>", self.on_saison_change)

        # --- Checkbox ---
        self.planning_dynamique = tk.BooleanVar()

        self.checkbox = tk.Checkbutton(
            controls_frame,
            text="Limites du planning dynamiques",  # à adapter à ton vrai besoin
            variable=self.planning_dynamique,
            command=self.on_dynamique_change
        )
        self.checkbox.pack(side="left", padx=10)




        # --- Canvas ---
        self.canvas_frame = tk.Frame(self, width=self.WIDTH, height=self.HEIGHT)
        self.canvas_frame.pack(expand=True)
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg="white"
        )
        self.canvas.pack(expand=True)

        # --- Bouton Retour ---
        self.btRetour = tk.Button(self, text="Retour", command=lambda: self.close(),underline=0)
        self.btRetour.pack(pady=10)

        # Variables pour le planning
        self.days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        self.salles = []           # remplie par get_salles
        self.first_hour = "08:00"  # par défaut
        self.last_hour = "23:00"
        self.hour_height = 50      # pixels par heure, ajustable
        self.day_width = 150       # largeur totale par jour

        self.bind_shortcuts({
            "<Alt-r>": lambda e: self.close(),
            "<Up>": lambda e: self.on_key_up(e),
            "<Down>": lambda e: self.on_key_down(e),
        })
        
        

    # ------------------------
    # On show : redessine le planning
    # ------------------------
    def on_show(self):
        self.salles = self.get_salles()
        self.first_hour, self.last_hour = self.get_time_bounds()
        self.redraw_canvas()
        self.draw_courses()

    def close(self):
        self.controller.show_frame("StartPage")
        

    # ------------------------
    # Récupérer le nombre de salles
    # ------------------------
    def get_nb_salles(self):
        return len(self.salles)

    # ------------------------
    # Récupérer les jours actifs
    # ------------------------
    def get_active_days(self):
        """
        Retourne la liste des jours qui ont au moins un cours,
        dans l'ordre de self.days
        """
        rows = self.get_all_courses()
        jours_avec_cours = set([r[0] for r in rows])  # r[0] = jour
        if not self.planning_dynamique.get():
            self.active_days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        else:
            # filtrer self.days dans l'ordre original
            self.active_days = [jour for jour in self.days if jour in jours_avec_cours]
        return self.active_days
    
    # ------------------------
    # Récupérer tous les cours
    # ------------------------
    def get_all_courses(self):
        """
        permet de calculer la taille des cases du canvas, puisqu'adapté aux jours
        """
        query = f"""
            SELECT c.jour, c.heure_debut, c.heure_fin, c.salle_id, c.id, d.nom
            FROM cours c
            LEFT JOIN danse d ON d.id = c.danse_id
            WHERE c.saison = '{self.cb_saison.get()}' 
            ORDER BY c.jour, c.heure_debut, c.salle_id
        """
        rows = lanceRequete(query, fetch=True)
        print(self.cb_saison.get())
        return rows


    # ------------------------
    # Récupérer salles
    # ------------------------
    def get_salles(self):
        query = "SELECT id, nom FROM salle ORDER BY id"
        rows = lanceRequete(query, fetch=True)
        return rows if rows else []

    def get_salle_name(self, index):
        if index < len(self.salles):
            return self.salles[index][1][:3]  # 3 premières lettres
        return f"S{index+1}"

    # ------------------------
    # Récupérer bornes horaires
    # ------------------------
    def get_time_bounds(self):
        query = f"SELECT MIN(heure_debut), MAX(heure_fin) FROM cours WHERE saison = '{self.cb_saison.get()}'"
        result = lanceRequete(query,fetchone=True)
        if not self.planning_dynamique.get():
            return "08:00", "23:00"
        if result and result[0] and result[1]:
            return result[0], result[1]
        return "08:00", "23:00"

    # ------------------------
    # Convertit HH:MM en nombre décimal d'heures
    # ------------------------
    def time_str_to_float(self, hhmm):
        h, m = map(int, hhmm.split(":"))
        return h + m/60

    def heure_to_y(self, hhmm):
        """
        Convertit une heure (HH:MM) en coordonnée Y sur le canvas
        """
        h_float = self.time_str_to_float(hhmm)

        # bornes horaires
        first_hour = self.time_str_to_float(self.first_hour)
        last_hour = self.time_str_to_float(self.last_hour)
        total_hours = last_hour - first_hour

        # hauteur utile
        height = self.HEIGHT - self.TOP_MARGIN

        # coordonnée Y relative à l'heure
        y = self.TOP_MARGIN + ((h_float - first_hour) / total_hours) * height
        return y
    
    def on_click_cours(self, cours_id):
        EditCoursModal(self, cours_id, self.controller)

    def change_saison(self, delta):
        values = list(self.cb_saison["values"])
        
        if not values:
            return

        current = self.cb_saison.get()

        if current not in values:
            index = 0
        else:
            index = values.index(current)

        new_index = index + delta

        # bloquer aux extrémités (ou boucle si tu préfères)
        if new_index < 0 or new_index >= len(values):
            return

        self.cb_saison.set(values[new_index])

        # déclencher manuellement l'événement
        self.on_saison_change(None)

    def on_key_up(self, event):
        self.change_saison(-1)

    def on_key_down(self, event):
        self.change_saison(1)
    def get_cours_duration(self, cours_id):
        query = "SELECT heure_debut, heure_fin FROM cours WHERE id = ?"
        row = lanceRequete(query, (cours_id,), fetchone=True)

        if not row:
            return 60

        h1, h2 = row
        t1 = self.time_str_to_float(h1)
        t2 = self.time_str_to_float(h2)

        return int((t2 - t1) * 60)       

    def add_minutes(self, time_str, minutes):
        h, m = map(int, time_str.split(":"))
        total = h * 60 + m + minutes
        return f"{total//60:02}:{total%60:02}"

    def minutes_to_time(self, minutes):
        h = minutes // 60
        m = minutes % 60
        return f"{h:02}:{m:02}"

    def y_to_minutes(self, y):
        first_hour = self.time_str_to_float(self.first_hour)
        last_hour = self.time_str_to_float(self.last_hour)

        total_hours = last_hour - first_hour
        height = self.HEIGHT - self.TOP_MARGIN

        relative = (y - self.TOP_MARGIN) / height
        hours = first_hour + relative * total_hours

        return int(hours * 60)

    def snap_to_30min(self, y):
        # snap en hauteur proportionnelle à 30 min
        first_hour = self.time_str_to_float(self.first_hour)
        last_hour = self.time_str_to_float(self.last_hour)
        total_hours = last_hour - first_hour
        height = self.HEIGHT - self.TOP_MARGIN
        y_rel = y - self.TOP_MARGIN
        hour = y_rel / height * total_hours + first_hour
        # arrondi à 0.5h
        hour = round(hour*2)/2
        # reconvertir en y
        y_snap = self.TOP_MARGIN + (hour - first_hour)/total_hours * height
        return y_snap

    def y_to_heure(self, y):
        first_hour = self.time_str_to_float(self.first_hour)
        last_hour = self.time_str_to_float(self.last_hour)
        total_hours = last_hour - first_hour
        height = self.HEIGHT - self.TOP_MARGIN
        y_rel = y - self.TOP_MARGIN
        hour = y_rel / height * total_hours + first_hour
        hh = int(hour)
        mm = int((hour - hh)*60)
        return f"{hh:02d}:{mm:02d}"
    
    def get_day_salle_from_x(self, x0, x1):
        """
        Retourne le jour et la salle en fonction de la position horizontale du cours.
        On utilise le centre du cours pour déterminer la salle.
        """
        center_x = (x0 + x1) / 2  # centre horizontal du cours

        for jour, (start, end) in self.day_positions.items():
            if start <= center_x <= end:
                # déterminer la salle
                nb_salles = self.get_nb_salles()
                salle_width = (end - start) / nb_salles
                salle_index = int((center_x - start) / salle_width)
                salle_index = max(0, min(nb_salles - 1, salle_index))
                return jour, salle_index + 1  # 1-based index

        # fallback
        first_jour = list(self.day_positions.keys())[0]
        return first_jour, 1

    # ------------------------
    # Drag & Drop des cours
    # ------------------------
    def enable_drag_courses(self):
        """
        Attache le drag & drop à tous les cours déjà dessinés.
        Doit être appelé après draw_courses().
        """
        self.drag_data = {"x": 0, "y": 0, "cours_id": None, "rect": None, "text": None,
                        "orig_coords": None, "current_coords": None}

        for item in self.canvas.find_all():
            # tous les rectangles (cours) ont été créés avec create_rectangle
            tags = self.canvas.gettags(item)
            # utiliser ici que les rectangles (optionnel si tu veux filtrer)
            self.canvas.tag_bind(item, "<ButtonPress-1>", self.on_drag_start)
            self.canvas.tag_bind(item, "<B1-Motion>", self.on_drag_motion)
            self.canvas.tag_bind(item, "<ButtonRelease-1>", self.on_drag_stop)

    def on_drag_start(self, event):
        if not self.drag_enabled:
            return
        # trouver l'item cliqué
        item = self.canvas.find_closest(event.x, event.y)[0]

        # chercher le cours_id correspondant dans self.cours_items
        cours_id = None
        for cid, data in self.cours_items.items():
            if item == data["rect"] or item == data["text"]:
                cours_id = cid
                break
        if not cours_id:
            self.drag_data = {}
            return

        rect = self.cours_items[cours_id]["rect"]
        text_id = self.cours_items[cours_id]["text"]
        coords = self.canvas.coords(rect)

        self.drag_data = {
            "cours_id": cours_id,
            "rect": rect,
            "text": text_id,
            "x": event.x,
            "y": event.y,
            "orig_coords": {"x0": coords[0], "y0": coords[1], "x1": coords[2], "y1": coords[3]}
        }

    def on_drag_motion(self, event):
        if not self.drag_enabled:
            return
        if not self.drag_data or "x" not in self.drag_data:
            return  # rien à faire

        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        rect = self.drag_data["rect"]
        text_id = self.drag_data["text"]

        # vérifier que les items existent
        if rect is None or text_id is None:
            return

        self.canvas.move(rect, dx, dy)
        self.canvas.move(text_id, dx, dy)

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag_stop(self, event):
        if not self.drag_enabled:
            return
        if not self.drag_data:
            return
        saison = self.cb_saison.get()

        rect = self.drag_data.get("rect")
        text_id = self.drag_data.get("text")
        cours_id = self.drag_data.get("cours_id")
        orig = self.drag_data.get("orig_coords", {})

        if not rect or not text_id or not cours_id:
            self.drag_data = {}
            return

        try:
            x0, y0, x1, y1 = self.canvas.coords(rect)
        except Exception:
            # si coords invalides, revert
            self.canvas.coords(rect, orig.get("x0", 0), orig.get("y0", 0),
                                    orig.get("x1", 0), orig.get("y1", 0))
            self.canvas.coords(text_id, (orig.get("x0",0)+orig.get("x1",0))/2,
                                        (orig.get("y0",0)+orig.get("y1",0))/2)
            self.drag_data = {}
            return

        # Snap vertical toutes les 30min
        height = y1 - y0
        new_y0 = self.snap_to_30min(y0)
        new_y1 = new_y0 + height

        # Jour et salle cible basé sur le centre
        jour, salle_index = self.get_day_salle_from_x(x0, x1)

        # Vérification disponibilité
        h_debut = self.y_to_heure(new_y0)
        h_fin = self.y_to_heure(new_y1+4)
        if not check_salle_disponible(salle_index, jour, h_debut, h_fin, saison,ignore_cours_id=cours_id):
            # revert si conflit
            self.canvas.coords(rect, orig["x0"], orig["y0"], orig["x1"], orig["y1"])
            self.canvas.coords(text_id, (orig["x0"]+orig["x1"])/2, (orig["y0"]+orig["y1"])/2)
            self.drag_data = {}
            return

        # Snap horizontal sur la colonne de la salle
        nb_salles = self.get_nb_salles()
        x_start_day, x_end_day = self.day_positions[jour]
        salle_width = (x_end_day - x_start_day) / nb_salles

        new_x0 = x_start_day + (salle_index - 1) * salle_width + 2
        new_x1 = new_x0 + salle_width - 4

        # Appliquer les coords
        self.canvas.coords(rect, new_x0, new_y0, new_x1, new_y1)
        self.canvas.coords(text_id, (new_x0+new_x1)/2, (new_y0+new_y1)/2)

        # mettre à jour la base
        updateCoursFromDrag(cours_id, jour, salle_index, h_debut, h_fin)

        self.drag_data = {}

     
    # # ------------------------
    # # Gestion du halo mouseover
    # # ------------------------
    # def on_hover_enter(self, event):
    #     item = self.canvas.find_closest(event.x, event.y)[0]

    #     cours_id = None
    #     for cid, data in self.cours_items.items():
    #         if item == data["rect"] or item == data["text"]:
    #             cours_id = cid
    #             break

    #     if not cours_id:
    #         return

    #     # éviter de refaire 50 fois le même
    #     if self.hovered_cours_id == cours_id:
    #         return

    #     self.hovered_cours_id = cours_id

    #     rect = self.cours_items[cours_id]["rect"]
    #     text_id = self.cours_items[cours_id]["text"]
    #     self.canvas.itemconfig(rect, outline="#00AEEF", width=4)
    #     self.canvas.tag_raise(rect)
    #     self.canvas.tag_raise(self.cours_items[cours_id]["text"])

    #     # effet halo (plus épais + couleur)
    #     self.canvas.itemconfig(rect, outline="#00AEEF", width=3)

    # def on_hover_leave(self, event):
    #     if not self.hovered_cours_id:
    #         return

    #     rect = self.cours_items[self.hovered_cours_id]["rect"]

    #     # reset style
    #     self.canvas.itemconfig(rect, outline="black", width=1)

    #     self.hovered_cours_id = None




    def on_saison_change(self, event):
        self.salles = self.get_salles()
        self.first_hour, self.last_hour = self.get_time_bounds()
        self.redraw_canvas()
        self.draw_courses()

    def on_dynamique_change(self):
        self.salles = self.get_salles()
        self.first_hour, self.last_hour = self.get_time_bounds()
        self.redraw_canvas()
        self.draw_courses()

    # ------------------------
    # double click sur canvas pour add un cours
    # ------------------------
    def on_canvas_double_click(self, event):
        # Vérifie si on a cliqué sur un item existant
        clicked_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)

        if not self.drag_enabled:
            return

        if clicked_items:
            return
        x, y = event.x, event.y

        # -------------------
        # déterminer le jour
        # -------------------
        jour = None
        for j, (x_start, x_end) in self.day_positions.items():
            if x_start <= x <= x_end:
                jour = j
                x_start_day, x_end_day = x_start, x_end
                break
        if not jour:
            return  # clic en dehors des jours

        # -------------------
        # déterminer la salle
        # -------------------
        nb_salles = self.get_nb_salles()
        salle_width = (x_end_day - x_start_day) / nb_salles
        salle_index = int((x - x_start_day) / salle_width)
        salle_index = max(0, min(nb_salles - 1, salle_index))
        salle_id = self.salles[salle_index][0]

        # -------------------
        # déterminer l'heure de début
        # -------------------
        first_hour = self.time_str_to_float(self.first_hour)
        last_hour = self.time_str_to_float(self.last_hour)
        total_hours = last_hour - first_hour
        height = self.HEIGHT - self.TOP_MARGIN

        # heure float correspondant à y
        h_float = first_hour + ((y - self.TOP_MARGIN) / height) * total_hours
        # arrondi à la demi-heure précédente
        h_hour = int(h_float)
        h_min = 0 if h_float - h_hour < 0.5 else 30
        heure_debut = f"{h_hour:02d}:{h_min:02d}"

        # -------------------
        # ouvrir modale d'ajout
        # -------------------
        AddCoursModal(self, jour, salle_id, heure_debut)

    # ------------------------
    # Redessine le canvas
    # ------------------------
    def redraw_canvas(self):
        self.canvas.delete("all")

        LEFT_MARGIN = self.LEFT_MARGIN  # 👈 marge pour les heures

        # --- Données ---
        first_hour_str, last_hour_str = self.get_time_bounds()
        nb_salles = self.get_nb_salles()
        jours_actifs = self.get_active_days()

        if not jours_actifs and self.planning_dynamique.get():
            jours_actifs = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

        nb_jours = len(jours_actifs)

        first_hour = self.time_str_to_float(first_hour_str)
        last_hour = self.time_str_to_float(last_hour_str)
        total_hours = last_hour - first_hour

        height = self.HEIGHT - self.TOP_MARGIN
        width = self.WIDTH - LEFT_MARGIN  # 👈 on retire la marge ici
        day_width = width / nb_jours
        salle_width = day_width / nb_salles

        # --- Dessin jours et salles ---
        self.day_positions = {}

        for i, jour in enumerate(jours_actifs):
            x_start = LEFT_MARGIN + i * day_width
            x_end = x_start + day_width
            self.day_positions[jour] = (x_start, x_end)

            # ligne verticale jour
            self.canvas.create_line(
                x_start, self.TOP_MARGIN,
                x_start, height + self.TOP_MARGIN,
                width=2, fill="black"
            )

            # texte jour
            self.canvas.create_text(
                x_start + day_width / 2,
                self.TOP_MARGIN / 2,
                text=jour,
                anchor="center",
                font=("Arial", 10, "bold")
            )

            # subdivisions salles
            for s in range(1, nb_salles):
                xs = x_start + s * salle_width
                self.canvas.create_line(
                    xs, self.TOP_MARGIN,
                    xs, height + self.TOP_MARGIN,
                    dash=(3, 5),
                    fill="gray"
                )

            # texte salle
            for s in range(nb_salles):
                xs = x_start + s * salle_width + salle_width / 2
                salle_name = self.get_salle_name(s)[:3]
                self.canvas.create_text(
                    xs,
                    self.TOP_MARGIN / 2 + 15,
                    text=salle_name,
                    anchor="center",
                    font=("Arial", 8)
                )

        # ligne finale droite
        self.canvas.create_line(
            LEFT_MARGIN + width,
            self.TOP_MARGIN,
            LEFT_MARGIN + width,
            height + self.TOP_MARGIN,
            width=2,
            fill="black"
        )

        # --- lignes horaires (sur toute largeur y compris marge) ---
        for h in range(int(first_hour), int(last_hour) + 1):
            y = self.TOP_MARGIN + (h - first_hour) / total_hours * height

            self.canvas.create_line(
                LEFT_MARGIN, y,
                LEFT_MARGIN + width, y,
                dash=(2, 4),
                fill="black"
            )

            # texte heure dans la marge gauche
            self.canvas.create_text(
                5, y,
                text=f"{h}h",
                anchor="nw",
                font=("Arial", 8)
            )


    def draw_courses(self):
        LEFT_MARGIN = self.LEFT_MARGIN

        # --- nettoyer anciens cours ---
        self.canvas.delete("cours_rect")
        self.cours_items.clear()

        # --- récupérer la saison sélectionnée ---
        saison = self.cb_saison.get()

        query = """
            SELECT c.id, c.jour, c.heure_debut, c.heure_fin, c.salle_id,
                d.nom, d.couleur, n.nom,
                GROUP_CONCAT(p.nom, ', ')
            FROM cours c
            LEFT JOIN danse d ON d.id = c.danse_id
            LEFT JOIN niveau n ON n.id = c.niveau_id
            LEFT JOIN cours_prof cp ON cp.cours_id = c.id
            LEFT JOIN prof p ON p.id = cp.prof_id
            WHERE c.saison = ?
            GROUP BY c.id
        """

        cours_list = lanceRequete(query, (saison,), fetch=True)
        nb_salles = self.get_nb_salles()

        for cours in cours_list:
            cours_id, jour, h_debut, h_fin, salle_id, danse_nom, danse_couleur, niveau_nom, profs = cours

            if jour not in self.day_positions:
                continue

            x_start_day, x_end_day = self.day_positions[jour]
            salle_width = (x_end_day - x_start_day) / nb_salles
            salle_index = salle_id - 1

            x0 = x_start_day + salle_index * salle_width + 2
            x1 = x0 + salle_width - 4
            y0 = self.heure_to_y(h_debut) + 2
            y1 = self.heure_to_y(h_fin) - 2

            rect = self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=danse_couleur or "#FFFFFF",
                outline="black",
                width=1,
                tags=("cours_rect",)  # ✅ IMPORTANT
            )

            text = f"{danse_nom}\n{niveau_nom}\n{profs or ''}"
            text_id = self.canvas.create_text(
                (x0 + x1) / 2,
                (y0 + y1) / 2,
                text=text,
                font=("Arial", 8),
                anchor="c",
                justify="center",
                width=salle_width - 6,
                tags=("cours_rect",)  # ✅ IMPORTANT
            )

            # stocker dans dictionnaire
            self.cours_items[cours_id] = {
                "rect": rect,
                "text": text_id,
                "salle_id": salle_id,
                "jour": jour
            }

            # bind double click
            self.canvas.tag_bind(rect, "<Double-Button-1>", lambda e, cid=cours_id: self.on_click_cours(cid))
            self.canvas.tag_bind(text_id, "<Double-Button-1>", lambda e, cid=cours_id: self.on_click_cours(cid))

            # bind drag & drop
            self.canvas.tag_bind(rect, "<ButtonPress-1>", self.on_drag_start)
            self.canvas.tag_bind(text_id, "<ButtonPress-1>", self.on_drag_start)
            self.canvas.tag_bind(rect, "<B1-Motion>", self.on_drag_motion)
            self.canvas.tag_bind(text_id, "<B1-Motion>", self.on_drag_motion)
            self.canvas.tag_bind(rect, "<ButtonRelease-1>", self.on_drag_stop)
            self.canvas.tag_bind(text_id, "<ButtonRelease-1>", self.on_drag_stop)

        # ⚠️ bind à faire UNE seule fois (pas dans la boucle)
        self.canvas.bind("<Double-Button-1>", self.on_canvas_double_click)
        
class AddCoursModal(tk.Toplevel):
    """
    Modale pour ajouter un cours depuis le planning (double-clic)
    """
    def __init__(self, parent, jour, salle_id, heure_debut):
        super().__init__(parent)
        self.parent = parent
        self.title("Ajouter un cours")
        self.geometry("800x350")
        self.resizable(False, False)

        # --- Modal : forcer focus ---
        self.transient(parent)
        self.update_idletasks()
        self.grab_set()
        self.focus_force()

        # --- Stocker l'ID de la salle pour la création ---
        self.salle_id_selected = salle_id

        # --- Frame principale ---
        main_frame = tk.LabelFrame(self, text="Informations du cours", padx=10, pady=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        left_frame = tk.Frame(main_frame)
        right_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # --- Combobox et Listbox ---
        self.AddCours_cb_danse = ttk.Combobox(left_frame, state="readonly")
        self.AddCours_cb_niveau = ttk.Combobox(left_frame, state="readonly")
        self.AddCours_lb_prof = tk.Listbox(left_frame, selectmode="multiple", height=3, exportselection=False)
        scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=self.AddCours_lb_prof.yview)
        self.AddCours_lb_prof.config(yscrollcommand=scrollbar.set)

        self.AddCours_cb_salle = ttk.Combobox(right_frame, state="readonly")
        self.AddCours_cb_jour = ttk.Combobox(right_frame, state="readonly")
        self.AddCours_cb_heure_debut = ttk.Combobox(right_frame, state="readonly", width=8)
        self.AddCours_cb_heure_fin = ttk.Combobox(right_frame, state="readonly", width=8)

        # --- Remplissage des combobox / listbox ---
        load_combobox("danse", self.AddCours_cb_danse)
        load_combobox("niveau", self.AddCours_cb_niveau)
        load_listbox("prof", self.AddCours_lb_prof)
        load_combobox("salle", self.AddCours_cb_salle)
        self.AddCours_cb_jour["values"] = parent.days
        heures = generate_hours()
        self.AddCours_cb_heure_debut["values"] = heures
        self.AddCours_cb_heure_fin["values"] = heures

        # --- Préremplissage ---
        self.AddCours_cb_jour.set(jour)
        # arrondi à la demi-heure précédente
        h, m = map(int, heure_debut.split(":"))
        m = 0 if m < 30 else 30
        heure_arrondie = f"{h:02d}:{m:02d}"
        self.AddCours_cb_heure_debut.set(heure_arrondie)
        # --- Auto-remplissage heure fin (1h après) ---
        if heure_arrondie in heures:
            index = heures.index(heure_arrondie)
            if index + 2 < len(heures):  # +1h si valeurs toutes les 30 min
                self.AddCours_cb_heure_fin.set(heures[index + 2])
            else:
                self.AddCours_cb_heure_fin.set(heures[-1])  # dernière valeur possible

        # Sélection de la salle via index (ID correspond à l'ordre dans le combo)
        self.AddCours_cb_salle.current(salle_id - 1)

        # --- LEFT SIDE ---
        left_fields = [("Danse", self.AddCours_cb_danse), ("Niveau", self.AddCours_cb_niveau)]
        for i, (label, widget) in enumerate(left_fields):
            tk.Label(left_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            widget.grid(row=i, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(left_frame, text="Prof").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.AddCours_lb_prof.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        scrollbar.grid(row=2, column=2, sticky="ns")
        left_frame.columnconfigure(1, weight=1)

        # --- RIGHT SIDE ---
        right_fields = [
            ("Salle", self.AddCours_cb_salle),
            ("Jour", self.AddCours_cb_jour),
            ("Heure début", self.AddCours_cb_heure_debut),
            ("Heure fin", self.AddCours_cb_heure_fin),
        ]
        for i, (label, widget) in enumerate(right_fields):
            tk.Label(right_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            widget.grid(row=i, column=1, sticky="w", padx=5, pady=5)
        right_frame.columnconfigure(1, weight=1)

        # --- Boutons ---
        button_frame = tk.Frame(self)
        button_frame.pack(fill="x", padx=20, pady=10)
        tk.Button(button_frame, text="Ajouter", command=self.addCours,underline=0).pack(side="right", padx=5)
        tk.Button(button_frame, text="Retour", command=self.destroy,underline=0).pack(side="right", padx=5)


        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Alt-r>", lambda e: self.destroy())
        self.bind("<Alt-a>", lambda e: self.addCours())

    # ------------------------
    # Ajouter le cours
    # ------------------------
    def addCours(self):
        danse_id = self.AddCours_cb_danse._mapping[self.AddCours_cb_danse.get()]
        niveau_id = self.AddCours_cb_niveau._mapping[self.AddCours_cb_niveau.get()]
        salle_id = self.AddCours_cb_salle._mapping[self.AddCours_cb_salle.get()]  # ✅ on garde l'ID exact pour la création
        debut = self.AddCours_cb_heure_debut.get()
        fin = self.AddCours_cb_heure_fin.get()
        jour = self.AddCours_cb_jour.get()
        saison = self.parent.cb_saison.get()

        selected_indices_prof = self.AddCours_lb_prof.curselection()
        ### récupération des datas de la list des profs
        if not selected_indices_prof:
            return messagebox.showerror("Erreur", "Au moins un prof requis")

        if len(selected_indices_prof) > 2:
            reponse =  messagebox.askyesno("Attention !", "Vous avez selectionné plus de 2 professeurs, êtes vous sur ?")

            if not reponse:
                return
            

        prof_ids = [self.AddCours_lb_prof._mapping[i] for i in selected_indices_prof]

        # validation salles et profs
        if not check_salle_disponible(salle_id, jour, debut, fin, saison):
            return messagebox.showerror("Erreur", f"La salle {self.AddCours_cb_salle.get()} n'est pas libre de {debut} à {fin}.")

        indisponibles = [pid for pid in prof_ids if not check_prof_disponible(pid, jour, debut, fin, saison)]
        if indisponibles:
            return messagebox.showerror("Erreur", "Profs pas disponibles sur ce créneau.")

        ajoutCours(danse_id, niveau_id, salle_id, jour, debut, fin, saison, prof_ids)
        messagebox.showinfo("OK", "Cours ajouté")
        # --- Redessiner le canvas pour voir le cours immédiatement ---
        if hasattr(self.parent, "draw_courses"):
            self.parent.draw_courses()

        self.destroy()

class EditCoursModal(tk.Toplevel):
    """
    Pop-up pour éditer un cours existant
    """
    def __init__(self, parent, cours_id, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.cours_id = cours_id
        self.title(f"Édition du cours {cours_id}")
        self.transient(parent)              # lie visuellement à la fenêtre parente
        self.focus_set()                    # donne le focus à la popup
        self.update_idletasks()
        self.grab_set()
        # --- Frame principale ---
        main_frame = tk.LabelFrame(self, text="Informations du cours", padx=10, pady=10)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # 2 colonnes internes
        left_frame = tk.Frame(main_frame)
        right_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # --- Combobox et Listbox ---
        self.cb_danse = ttk.Combobox(left_frame, state="readonly")
        self.cb_niveau = ttk.Combobox(left_frame, state="readonly")
        self.lb_prof = tk.Listbox(left_frame, selectmode="multiple", height=3, exportselection=False)
        scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=self.lb_prof.yview)
        self.lb_prof.config(yscrollcommand=scrollbar.set)

        self.cb_salle = ttk.Combobox(right_frame, state="readonly")
        self.cb_jour = ttk.Combobox(right_frame, state="readonly")
        self.cb_heure_debut = ttk.Combobox(right_frame, state="readonly", width=8)
        self.cb_heure_fin = ttk.Combobox(right_frame, state="readonly", width=8)

        # --- Jours et heures ---
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        self.cb_jour["values"] = jours
        heures = generate_hours()  # même fonction que pour AddCoursPage
        self.cb_heure_debut["values"] = heures
        self.cb_heure_fin["values"] = heures

        # --- Placement LEFT ---
        left_fields = [
            ("Danse", self.cb_danse),
            ("Niveau", self.cb_niveau),
        ]
        for i, (label, widget) in enumerate(left_fields):
            tk.Label(left_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            widget.grid(row=i, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(left_frame, text="Prof").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.lb_prof.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        scrollbar.grid(row=2, column=2, sticky="ns")
        left_frame.columnconfigure(1, weight=1)

        # --- Placement RIGHT ---
        right_fields = [
            ("Salle", self.cb_salle),
            ("Jour", self.cb_jour),
            ("Heure début", self.cb_heure_debut),
            ("Heure fin", self.cb_heure_fin),
        ]
        for i, (label, widget) in enumerate(right_fields):
            tk.Label(right_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            widget.grid(row=i, column=1, sticky="w", padx=5, pady=5)
        right_frame.columnconfigure(1, weight=1)

        # --- Zone commentaire ---
        comment_frame = tk.Frame(self)
        comment_frame.pack(padx=20, pady=(0,10), fill="x")  # juste au-dessus des boutons

        tk.Label(comment_frame, text="Commentaire :").pack(anchor="w")
        self.txt_commentaire = tk.Text(comment_frame, height=3)  # 3 lignes de haut
        self.txt_commentaire.pack(fill="x", expand=True)

        # --- Boutons bas ---
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10, fill="x")
        self.bt_modifier = tk.Button(button_frame, text="Modifier", command=self.modify_cours,underline=0)
        self.bt_afficher = tk.Button(button_frame, text="Afficher la liste des inscrits", command=self.afficher_inscrits,underline=0)
        self.bt_supprimer = tk.Button(button_frame, text="Supprimer le cours", command=self.supprimer_cours,underline=0)
        self.bt_retour = tk.Button(button_frame, text="Retour", command=self.destroy,underline=0)
        self.bt_modifier.pack(side="left", padx=5, expand=True)
        self.bt_afficher.pack(side="left", padx=5, expand=True)
        self.bt_supprimer.pack(side="left", padx=5, expand=True)
        self.bt_retour.pack(side="left", padx=5, expand=True)



        # --- Charge les données du cours ---
        self.load_cours_info()

        # Raccourci fermeture
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Alt-a>", lambda e: self.afficher_inscrits())
        self.bind("<Alt-m>", lambda e: self.modify_cours())
        self.bind("<Alt-s>", lambda e: self.supprimer_cours())
        self.bind("<Alt-r>", lambda e: self.destroy())
    
    # ------------------------
    # Récupérer le label à partir de l'id
    # ------------------------
    def get_label_from_id(self, table, _id):
        rows = lanceRequete(f"SELECT nom FROM {table} WHERE id = ?", params=(_id,), fetchone=True)
        return rows[0] if rows else ""

    # ------------------------
    # Charge les infos du cours
    # ------------------------

    def load_cours_info(self):
        # --- Récupérer le cours ---
        query = """
            SELECT c.jour, c.heure_debut, c.heure_fin, c.salle_id,
                c.danse_id, c.niveau_id,
                GROUP_CONCAT(cp.prof_id),
                c.commentaires
            FROM cours c
            LEFT JOIN cours_prof cp ON cp.cours_id = c.id
            WHERE c.id = ?
            GROUP BY c.id
        """
        row = lanceRequete(query, params=(self.cours_id,), fetchone=True)
        if not row:
            messagebox.showerror("Erreur", "Cours introuvable")
            self.destroy()
            return

        jour, h_debut, h_fin, salle_id, danse_id, niveau_id, prof_ids_str, commentaire = row

        # --- Remplir combobox et listbox ---
        load_combobox("danse", self.cb_danse)
        load_combobox("niveau", self.cb_niveau)
        load_combobox("salle", self.cb_salle)
        load_listbox("prof", self.lb_prof)  # ✅ remplir la Listbox AVANT de sélectionner

        # --- Positionner les valeurs du cours ---
        self.cb_danse.set(self.get_label_from_id("danse", danse_id))
        self.cb_niveau.set(self.get_label_from_id("niveau", niveau_id))
        self.cb_salle.set(self.get_label_from_id("salle", salle_id))
        self.cb_jour.set(jour)
        self.cb_heure_debut.set(h_debut)
        self.cb_heure_fin.set(h_fin)

        # --- Sélectionner les profs ---
        prof_ids = prof_ids_str.split(",") if prof_ids_str else []
        self.lb_prof.selection_clear(0, tk.END)
        for i in range(self.lb_prof.size()):
            prof_id = str(self.lb_prof._mapping[i])  # récupère l'ID correspondant à l'index
            if prof_id in prof_ids:
                self.lb_prof.selection_set(i)

        # --- Remplir le commentaire ---
        self.txt_commentaire.delete("1.0", tk.END)
        if commentaire:
            self.txt_commentaire.insert("1.0", commentaire)

    def modify_cours(self):
        """
        Bouton Modifier : met à jour le cours existant avec les mêmes vérifications que AddCours
        """
        danse_id = self.cb_danse._mapping.get(self.cb_danse.get())
        niveau_id = self.cb_niveau._mapping.get(self.cb_niveau.get())
        salle_id = self.cb_salle._mapping.get(self.cb_salle.get())
        debut = self.cb_heure_debut.get()
        fin = self.cb_heure_fin.get()
        jour = self.cb_jour.get()
        saison = self.parent.cb_saison.get()
        commentaires = self.txt_commentaire.get("1.0", "end-1c")

        # --- Vérifications basiques ---
        if not debut or not fin or not jour:
            return messagebox.showerror("Erreur", "Heures et/ou Jour obligatoires")
        if debut >= fin:
            return messagebox.showerror(
                "Erreur",
                "En général, on termine après avoir commencé ! \n(Heure de début < Heure de fin)"
            )

        # --- Professeurs sélectionnés ---
        selected_indices_prof = self.lb_prof.curselection()
        if not selected_indices_prof:
            return messagebox.showerror("Erreur", "Au moins un prof requis")
        prof_ids = [self.lb_prof._mapping[i] for i in selected_indices_prof]

        if len(selected_indices_prof) > 2:
            reponse = messagebox.askyesno(
                "Attention !",
                "Vous avez sélectionné plus de 2 professeurs, êtes-vous sûr ?"
            )
            if not reponse:
                return

        # --- Vérification disponibilité salle ---
        if not check_salle_disponible(salle_id, jour, debut, fin, saison, ignore_cours_id=self.cours_id):
            return messagebox.showerror(
                "Erreur",
                f"La salle {self.cb_salle.get()} n'est pas libre de {debut} à {fin}."
            )

        # --- Vérification disponibilité profs ---
        indisponibles = []
        for prof_id in prof_ids:
            if not check_prof_disponible(prof_id, jour, debut, fin, saison, ignore_cours_id=self.cours_id):
                indisponibles.append(prof_id)
        if indisponibles:
            return messagebox.showerror(
                "Erreur",
                f"Profs pas disponibles sur ce créneau."
            )

        # --- Mise à jour en base ---
        updateCours(
            self.cours_id,
            danse_id,
            niveau_id,
            salle_id,
            jour,
            debut,
            fin,
            commentaires,
            saison,
            prof_ids
        )

        self.fin()

    def afficher_inscrits(self):
        print(f"Afficher inscrits pour cours {self.cours_id}")
        # à compléter : ouvrir pop-up liste inscrits

    def supprimer_cours(self):
        confirm = messagebox.askyesno(
            "Confirmation",
            "Es-tu sûr de vouloir supprimer ce cours ?", parent=self
        )
        if not confirm:
            return

        try:
            # Supprimer les relations profs
            query1 = "DELETE FROM cours_prof WHERE cours_id = ?"
            lanceRequete(query1, (self.cours_id,))

            # Supprimer le cours
            query2 = "DELETE FROM cours WHERE id = ?"
            lanceRequete(query2, (self.cours_id,))

            messagebox.showinfo("Succès", "Cours supprimé avec succès", parent=self)

            self.fin()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}", parent=self)



    def fin(self):
        """
        Mise a jour du planning a la fin
        """
        self.parent.first_hour, self.parent.last_hour = self.parent.get_time_bounds()
        self.parent.redraw_canvas()
        self.parent.draw_courses()
        self.destroy()

class AddCoursPage(BasePage):
    """
    Frame pour l'ajout d'un cours
    """

    def __init__(self, parent, controller):
        super().__init__(parent, controller)


        # --- Titre ---
        tk.Label(
            self,
            text="Ajout d'un cours",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(15, 15))

        # --- Frame principale ---
        main_frame = tk.LabelFrame(self, text="Informations du cours", padx=10, pady=10)
        main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # 2 colonnes internes
        left_frame = tk.Frame(main_frame)
        right_frame = tk.Frame(main_frame)

        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # --- Combobox ---
        self.AddCours_cb_danse = ttk.Combobox(left_frame, state="readonly")
        self.AddCours_cb_niveau = ttk.Combobox(left_frame, state="readonly")
        self.AddCours_lb_prof = tk.Listbox(
            left_frame,
            selectmode="multiple",
            height=3,
            exportselection=False
        )
        scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=self.AddCours_lb_prof.yview)
        self.AddCours_lb_prof.config(yscrollcommand=scrollbar.set)

        self.AddCours_cb_salle = ttk.Combobox(right_frame, state="readonly")
        self.AddCours_cb_jour = ttk.Combobox(right_frame, state="readonly")

        self.AddCours_cb_heure_debut = ttk.Combobox(right_frame, state="readonly", width=8)
        self.AddCours_cb_heure_fin = ttk.Combobox(right_frame, state="readonly", width=8)

        # Jours
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        self.AddCours_cb_jour["values"] = jours

        # Heures (15 min)
        heures = generate_hours()
        self.AddCours_cb_heure_debut["values"] = heures
        self.AddCours_cb_heure_fin["values"] = heures

        # --- LEFT SIDE ---
        left_fields = [
            ("Danse", self.AddCours_cb_danse),
            ("Niveau", self.AddCours_cb_niveau),
        ]

        for i, (label, widget) in enumerate(left_fields):
            tk.Label(left_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            widget.grid(row=i, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(left_frame, text="Prof").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.AddCours_lb_prof.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        scrollbar.grid(row=2, column=2, sticky="ns")

        self.AddCours_cb_saison = ttk.Combobox(right_frame, state="readonly", width=10)

        left_frame.columnconfigure(1, weight=1)

        # --- RIGHT SIDE ---
        right_fields = [
            ("Salle", self.AddCours_cb_salle),
            ("Jour", self.AddCours_cb_jour),
            ("Heure début", self.AddCours_cb_heure_debut),
            ("Heure fin", self.AddCours_cb_heure_fin),
            ("Saison", self.AddCours_cb_saison),
        ]

        for i, (label, widget) in enumerate(right_fields):
            tk.Label(right_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            widget.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            
        right_frame.columnconfigure(1, weight=1)
        # --- Boutons ---
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.AddCours_BtAddCours = tk.Button(
            button_frame,
            text="Ajouter",
            command=self.addCours,
            underline=0
        )
        self.AddCours_BtAddCours.grid(row=0, column=0, sticky="e", padx=5)

        self.AddCours_BtRetour = tk.Button(
            button_frame,
            text="Retour",
            command=lambda: controller.show_frame("StartPage"),
            underline=0
        )
        self.AddCours_BtRetour.grid(row=0, column=1, sticky="w", padx=5)

        # Valeurs saisons
        load_cb_saison(self.AddCours_cb_saison)

        # --- Auto sélection saison actuelle ---
        from datetime import datetime
        today = datetime.today()

        year = today.year
        month = today.month

        # logique : saison commence en septembre
        if month >= 9:
            start_year = year % 100
        else:
            start_year = (year - 1) % 100

        saison_str = f"{start_year:02d} / {start_year+1:02d}"

        # --- Raccourcis ---
        self.bind_shortcuts({
            "<Alt-a>": lambda e: self.addCours(),
            "<Alt-r>": lambda e: self.controller.show_frame("StartPage")
        })

        self.AddCours_cb_heure_debut.bind("<<ComboboxSelected>>", self.auto_set_end_time)


        # après avoir créé tous les widgets focusables
        self.register_focusable(

            self.AddCours_cb_danse,
            self.AddCours_cb_niveau,
            self.AddCours_lb_prof,
            self.AddCours_cb_salle,
            self.AddCours_cb_jour,
            self.AddCours_cb_heure_debut,
            self.AddCours_cb_heure_fin,
            self.AddCours_BtAddCours,
            self.AddCours_BtRetour,
            
        )

        # configure Tab/Shift+Tab
        self.setup_tab_navigation()

    # ------------------------
    # Save 
    # ------------------------
    def addCours(self):
        """
        Bouton ajouter, step a suivre :
        vérification des contenus des champs 
        vérification de la validité du cours (pas d'overlapping salle ou prof sur un créneau en particulier)
        ajout du cours
        """

        danse_id = self.AddCours_cb_danse._mapping[self.AddCours_cb_danse.get()]
        niveau_id = self.AddCours_cb_niveau._mapping[self.AddCours_cb_niveau.get()]
        salle_id = self.AddCours_cb_salle._mapping[self.AddCours_cb_salle.get()]
        debut = self.AddCours_cb_heure_debut.get()
        fin = self.AddCours_cb_heure_fin.get()
        jour = self.AddCours_cb_jour.get()
        saison = self.AddCours_cb_saison.get()

        if not debut or not fin or not jour:
            return messagebox.showerror("Erreur", "Heures et/ou Jour obligatoires")

        if debut >= fin:
            return messagebox.showerror(
                "Erreur",
                "En général, on termine après avoir commencé ! \n(Heure de début < Heure de fin)"
            )

        selected_indices_prof = self.AddCours_lb_prof.curselection()
        ### récupération des datas de la list des profs
        if not selected_indices_prof:
            return messagebox.showerror("Erreur", "Au moins un prof requis")

        prof_ids = [self.AddCours_lb_prof._mapping[i] for i in selected_indices_prof]

        print("Profs sélectionnés :", prof_ids)
        if len(selected_indices_prof) > 2:
            reponse =  messagebox.askyesno("Attention !", "Vous avez selectionné plus de 2 professeurs, êtes vous sur ?")

            if not reponse:
                return
            
        ### Validation en base de donnée ###
        if not check_salle_disponible(salle_id, jour, debut, fin, saison):
            return messagebox.showerror(
                "Erreur",
                f"La salle {self.AddCours_cb_salle.get()} n'est pas libre de {debut} à {fin}."
            )
        
        indisponibles = []
        for prof_id in prof_ids:
            if not check_prof_disponible(prof_id, jour, debut, fin, saison):
                indisponibles.append(prof_id)

        if indisponibles:
            messagebox.showerror(
                "Erreur",
                f"Profs pas disponibles sur ce créneau."
            )
            return
        

        ### Création du cours ###
        ajoutCours( danse_id,
                    niveau_id,
                    salle_id,
                    jour,
                    debut,
                    fin,
                    saison,
                    prof_ids
                    )

        messagebox.showinfo("OK", "Cours ajouté")
        self.clear_fields()

    def auto_set_end_time(self, event):
        debut = self.AddCours_cb_heure_debut.get()
        heures = generate_hours()
        fin = self.AddCours_cb_heure_fin.get()

        if debut in heures:
            index = heures.index(debut)
            if index + 2 < len(heures):  # +1h
                if not fin:
                    self.AddCours_cb_heure_fin.set(heures[index + 2])

    # ------------------------
    # loading des data 
    # ------------------------
    def load_data(self):
        load_combobox("danse", self.AddCours_cb_danse)
        load_combobox("niveau", self.AddCours_cb_niveau)
        load_listbox("prof", self.AddCours_lb_prof)
        load_combobox("salle", self.AddCours_cb_salle)   
    # ------------------------
    # Reset champs
    # ------------------------
    def clear_fields(self):
        self.AddCours_lb_prof.selection_clear(0, tk.END)
        self.AddCours_lb_prof.yview_moveto(0)
        self.AddCours_cb_heure_debut.set("")
        self.AddCours_cb_heure_fin.set("")
        self.AddCours_cb_jour.set("")

    # ------------------------
    # On show
    # ------------------------
    def on_show(self):
        self.clear_fields()
        self.load_data()
        self.AddCours_cb_danse.focus_set()


###########################
### Gestion utilisateur ###
class AddUserPage(BasePage):
    """
    Frame pour l'ajout d'utilisateur, version plus userfriendly
    """
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # --- Titre ---
        tk.Label(self, text="Ajout d'un adhérent", 
                 font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=3, pady=(20, 30))

        # --- Cadres ---
        addUser_id_frame = tk.LabelFrame(self, text="Identification", padx=10, pady=10)
        addUser_contact_frame = tk.LabelFrame(self, text="Contact", padx=10, pady=10)
        addUser_other_frame = tk.LabelFrame(self, text="Infos supplémentaires", padx=10, pady=10)

        # Colonne gauche
        addUser_id_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)
        addUser_other_frame.grid(row=2, column=0, sticky="nsew", padx=(20, 10), pady=10)

        # Colonne droite
        addUser_contact_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=(10, 20), pady=10)

        # On fait en sorte que les colonnes s'étirent
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # --- Widgets Identification ---
        self.addUser_role = ttk.Combobox(addUser_id_frame, values=["Lead / Follow ?","Leader", "Follower"], state="readonly")
        self.addUser_role.current(0)
        self.addUser_prenom = tk.Entry(addUser_id_frame)
        self.addUser_nom = tk.Entry(addUser_id_frame)
        self.addUser_naissance = tk.Entry(addUser_id_frame, width=10) 

        tk.Label(addUser_id_frame, text="Rôle principal").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.addUser_role.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(addUser_id_frame, text="Prénom", font=("Arial", 10, "underline")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.addUser_prenom.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(addUser_id_frame, text="Nom", font=("Arial", 10, "underline")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.addUser_nom.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(addUser_id_frame, text="Date naissance").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.addUser_naissance.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        addUser_id_frame.columnconfigure(1, weight=1)

        # --- Widgets Contact ---
        self.addUser_email = tk.Entry(addUser_contact_frame)
        self.addUser_tel1 = tk.Entry(addUser_contact_frame, width=10)
        self.addUser_tel2 = tk.Entry(addUser_contact_frame, width=10)
        self.addUser_adresse = tk.Entry(addUser_contact_frame)
        self.addUser_ville = tk.Entry(addUser_contact_frame)
        self.addUser_code_postal = tk.Entry(addUser_contact_frame, width=5)

        tk.Label(addUser_contact_frame, text="Email", font=("Arial", 10, "underline")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.addUser_email.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        tk.Label(addUser_contact_frame, text="Téléphone 1").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.addUser_tel1.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(addUser_contact_frame, text="Téléphone 2").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.addUser_tel2.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        contact_widgets = [
            ("Adresse", self.addUser_adresse),
            ("Ville", self.addUser_ville)
        ]

        tk.Label(addUser_contact_frame, text="Code postal").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.addUser_code_postal.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        

        for i, (label_text, widget) in enumerate(contact_widgets):
            tk.Label(addUser_contact_frame, text=label_text).grid(row=i+3, column=0, sticky="w", padx=5, pady=5)
            widget.grid(row=i+3, column=1, sticky="ew", padx=5, pady=5)

        addUser_contact_frame.columnconfigure(1, weight=1)

        # --- Widgets Infos supplémentaires ---
        self.addUser_profession = tk.Entry(addUser_other_frame)
        self.addUser_rencontre = ttk.Combobox(addUser_other_frame, values=[
            "Bouche à oreille", "Portes ouvertes", "Affiches magasins",
            "Site internet", "Réseaux sociaux", "Flyers", "Autres"], state="readonly")
        self.addUser_rencontre.current(6)

        tk.Label(addUser_other_frame, text="Profession").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.addUser_profession.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(addUser_other_frame, text="Comment avez-vous connu l'école").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.addUser_rencontre.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        addUser_other_frame.columnconfigure(1, weight=1)

        # --- Boutons ---
        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.addUser_btSubmit = tk.Button(button_frame, text="Enregistrer", command=self.save,underline=0)
        self.addUser_btSubmit.grid(row=0,column=0, sticky="e", padx=5)
        self.addUser_btRetour = tk.Button(button_frame, text="Retour", command=lambda: controller.show_frame("StartPage"),underline=0)
        self.addUser_btRetour.grid(row=0,column=1, sticky="w", padx=5)

        self.bind_shortcuts({
            "<Alt-e>": lambda e: self.save(),
            "<Alt-r>": lambda e: self.controller.show_frame("StartPage")
        })

        # après avoir créé tous les widgets focusables
        self.register_focusable(
            self.addUser_role,
            self.addUser_prenom,
            self.addUser_nom,
            self.addUser_naissance,
            self.addUser_email,
            self.addUser_tel1,
            self.addUser_tel2,
            self.addUser_adresse,
            self.addUser_ville,
            self.addUser_code_postal,
            self.addUser_profession,
            self.addUser_rencontre,
            self.addUser_btSubmit,
            self.addUser_btRetour
        )

        # configure Tab/Shift+Tab
        self.setup_tab_navigation()

    def save(self):
        # --- VALIDATIONS ---
        if not self.addUser_nom.get() or not self.addUser_prenom.get() or not self.addUser_email.get() :
            return messagebox.showerror("Erreur", "Nom, Prénom et adresse mail obligatoire")

        # Date validation AAAA-MM-JJ
        if self.addUser_naissance.get() != '':
            try:
                date_naissance_ok = parse_date(self.addUser_naissance.get())
            except:
                return messagebox.showerror("Erreur", "La date de naissance doit être vide ou au format \nAAAA-MM-JJ\nAAAAMMJJ\nJJMMAAAA\nJJ-MM-AAAA\n")
        else:
            date_naissance_ok = ''



        # Téléphone
        if not TEL_REGEX.match(self.addUser_tel1.get()) and self.addUser_tel1.get() != '':
            return messagebox.showerror("Erreur", "Le téléphone 1 doit avoir 10 chiffres ou être vide")

        # Téléphone
        if not TEL_REGEX.match(self.addUser_tel2.get()) and self.addUser_tel2.get() != '':
            return messagebox.showerror("Erreur", "Le téléphone 2 doit avoir 10 chiffres ou être vide")

        # code_postal
        if not CP_REGEX.match(self.addUser_code_postal.get()) and self.addUser_code_postal.get() != '':
            return messagebox.showerror("Erreur", "Le code postal doit avoir 5 chiffres ou être vide")

        # Email simple
        if not EMAIL_REGEX.match(self.addUser_email.get()) and self.addUser_email.get() != '':
            return messagebox.showerror("Erreur", "Email invalide")

        # Verification présence doublon
        if select_user_unique(self.addUser_nom.get(),self.addUser_prenom.get(),self.addUser_email.get()):
            return messagebox.showerror("Erreur", "Utilisateur déjà existant \n-nom\n-prenom\n-Adresse mail")

        # Verification Sélection role
        if self.addUser_role.get() == "Lead / Follow ?":
            return messagebox.showerror("Erreur", "Il faut choisir un rôle dominant : Leader / Follower")


        try:
            add_user(
            self.addUser_nom.get(),
            self.addUser_prenom.get(),
            date_naissance_ok,
            self.addUser_tel1.get(),
            self.addUser_tel2.get(),
            self.addUser_email.get(),
            self.addUser_adresse.get(),
            self.addUser_ville.get(),
            self.addUser_code_postal.get(),
            self.addUser_role.get(),
            self.addUser_profession.get(),
            self.addUser_rencontre.get(),
            datetime.now().year
            )
        except:
            return messagebox.showerror("Erreur", "Erreur requete add_user FROM BDD")


        messagebox.showinfo("OK", "Utilisateur ajouté")

        id_nouvellement_crée = select_user_unique(self.addUser_nom.get().upper(),self.addUser_prenom.get().capitalize(),self.addUser_email.get())
        self.clear_fields()
        self.addUser_role.focus_set()
        self.controller.show_frame("EditUserPage", id_nouvellement_crée[0])

    def clear_fields(self):
        self.addUser_nom.delete(0, tk.END)
        self.addUser_prenom.delete(0, tk.END)
        self.addUser_email.delete(0, tk.END)
        self.addUser_naissance.delete(0, tk.END)
        self.addUser_tel1.delete(0, tk.END)
        self.addUser_tel2.delete(0, tk.END)
        self.addUser_adresse.delete(0, tk.END)
        self.addUser_ville.delete(0, tk.END)
        self.addUser_code_postal.delete(0, tk.END)
        self.addUser_role.current(0)         # reset combobox
        self.addUser_profession.delete(0, tk.END)
        self.addUser_rencontre.current(6)         # reset combobox

    def on_show(self):
        self.clear_fields()
        self.addUser_role.focus_set()

class EditUserPage(BasePage):
    """
    Frame pour la modification de l'utilisateur, inscription aux cours, gestion du couple et des paiements
    """
    def __init__(self, parent, controller):
        super().__init__(parent, controller)


        # --- Titre ---
        self.frameTitle = tk.Label(self, text="Mise à jour adhérent", 
                 font=("Arial", 18, "bold"))
        self.frameTitle.grid(row=0, column=0, columnspan=3, pady=(20, 30))

        # --- Cadres ---
        editUser_id_frame = tk.LabelFrame(self, text="Identification", padx=10, pady=10)
        editUser_contact_frame = tk.LabelFrame(self, text="Contact", padx=10, pady=10)
        editUser_other_frame = tk.LabelFrame(self, text="Infos supplémentaires", padx=10, pady=10)
        editUser_couple_frame = tk.LabelFrame(self, text="En couple", padx=10, pady=10)

        # Colonne gauche
        editUser_id_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)
        editUser_other_frame.grid(row=2, column=0, sticky="nsew", padx=(20, 10), pady=10)

        # Colonne droite
        editUser_contact_frame.grid(row=1, column=1, rowspan=2, sticky="new", padx=(10, 20), pady=10)
        editUser_couple_frame.grid(row=2, column=1, sticky="sew", padx=(10, 20), pady=10)

        # On fait en sorte que les colonnes s'étirent
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # --- Widgets Identification ---
        self.editUser_role = ttk.Combobox(editUser_id_frame, values=["Leader", "Follower"], state="readonly")
        self.editUser_role.current(0)
        self.editUser_prenom = tk.Entry(editUser_id_frame)
        self.editUser_nom = tk.Entry(editUser_id_frame)
        self.editUser_naissance = tk.Entry(editUser_id_frame, width=10) 

        tk.Label(editUser_id_frame, text="Rôle principal").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.editUser_role.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(editUser_id_frame, text="Prénom", font=("Arial", 10, "underline")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.editUser_prenom.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(editUser_id_frame, text="Nom", font=("Arial", 10, "underline")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.editUser_nom.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(editUser_id_frame, text="Date naissance").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.editUser_naissance.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        editUser_id_frame.columnconfigure(1, weight=1)

        # --- Widgets Contact ---
        self.editUser_email = tk.Entry(editUser_contact_frame)
        self.editUser_tel1 = tk.Entry(editUser_contact_frame, width=10)
        self.editUser_tel2 = tk.Entry(editUser_contact_frame, width=10)
        self.editUser_adresse = tk.Entry(editUser_contact_frame)
        self.editUser_ville = tk.Entry(editUser_contact_frame)
        self.editUser_code_postal = tk.Entry(editUser_contact_frame, width=5)

        tk.Label(editUser_contact_frame, text="Email", font=("Arial", 10, "underline")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.editUser_email.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        tk.Label(editUser_contact_frame, text="Téléphone 1").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.editUser_tel1.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(editUser_contact_frame, text="Téléphone 2").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.editUser_tel2.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        contact_widgets = [
            ("Adresse", self.editUser_adresse),
            ("Ville", self.editUser_ville)
        ]

        tk.Label(editUser_contact_frame, text="Code postal").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.editUser_code_postal.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        

        for i, (label_text, widget) in enumerate(contact_widgets):
            tk.Label(editUser_contact_frame, text=label_text).grid(row=i+3, column=0, sticky="w", padx=5, pady=5)
            widget.grid(row=i+3, column=1, sticky="ew", padx=5, pady=5)

        editUser_contact_frame.columnconfigure(1, weight=1)

        # --- Widgets Infos supplémentaires ---
        self.editUser_profession = tk.Entry(editUser_other_frame)
        self.editUser_rencontre = ttk.Combobox(editUser_other_frame, values=[
            "Bouche à oreille", "Portes ouvertes", "Affiches magasins",
            "Site internet", "Réseaux sociaux", "Flyers", "Autres"], state="readonly")
        self.editUser_rencontre.current(6)

        tk.Label(editUser_other_frame, text="Profession").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.editUser_profession.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(editUser_other_frame, text="Comment avez-vous connu l'école").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.editUser_rencontre.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        editUser_other_frame.columnconfigure(1, weight=1)

        # --- Widgets En couple ---
        self.partner_button = tk.Button(editUser_couple_frame, text="Accoupler", command=self.accoupler,underline=0)
        self.partner_button.grid(row=0,column=0,columnspan=3, sticky="ew", padx=5)
        self.cancel_couple = tk.Canvas(editUser_couple_frame, width=20, height=20, highlightthickness=0)

        # Cercle rouge
        self.cancel_couple.create_oval(2.5, 2.5, 17.5, 17.5, outline="red", width=1.5)

        # Barre rouge diagonale
        self.cancel_couple.create_line(5, 5, 15, 15, fill="red", width=1.5)
        self.cancel_couple.bind("<Button-1>", lambda e: self.divorce())

        # --- Cadres Commentaires / Règlements ---
        editUser_cours_frame = tk.LabelFrame(self, text="Cours", padx=10, pady=10,width=50)
        editUser_comment_frame = tk.LabelFrame(self, text="Commentaire", padx=10, pady=10,width=50)
        editUser_payment_frame = tk.LabelFrame(self, text="Règlements", padx=10, pady=10)

        editUser_payment_frame.grid(row=3, column=1, rowspan=2 ,sticky="nsew", padx=(10,20), pady=10)
        editUser_cours_frame.grid(row=3, column=0, sticky="nsw", padx=(20,10), pady=10)
        editUser_comment_frame.grid(row=4, column=0, sticky="nsw", padx=(20,10), pady=10)

        self.editUser_commentaire = tk.Text(editUser_comment_frame, height=4, wrap="word",width=50)
        self.editUser_commentaire.grid(row=0, column=0, sticky="new")
        editUser_comment_frame.rowconfigure(0, weight=1)
        editUser_comment_frame.columnconfigure(0, weight=1)

        self.editUser_montant_du = tk.Entry(editUser_payment_frame, width=10)

        self.editUser_montant_regle = tk.Entry(editUser_payment_frame, width=10)

        self.editUser_commentaire_paiement = tk.Text(editUser_payment_frame, height=3, wrap="word", width=10)
        self.editUser_commentaire_conjoint = tk.Text(editUser_payment_frame, height=3, wrap="word", width=10, state="disabled",bg="#9E9C9C")

        tk.Label(editUser_payment_frame, text="Montant dû").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.editUser_montant_du.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        tk.Label(editUser_payment_frame, text="Montant réglé").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.editUser_montant_regle.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Label(editUser_payment_frame, text="Commentaire paiement").grid(row=2, column=0, columnspan=2, sticky="w", padx=5)
        self.editUser_commentaire_paiement.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        tk.Label(editUser_payment_frame, text="Commentaire paiement conjoint").grid(row=4, column=0, columnspan=2, sticky="w", padx=5)
        self.editUser_commentaire_conjoint.grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        editUser_payment_frame.columnconfigure(1, weight=1)

        self.add_course_btn = tk.Button(
            editUser_cours_frame,
            text="Ajouter un cours",
            command=lambda: self.open_planning_modal(self.user_id),
            underline=11
        )
        self.add_course_btn.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        # --- Boutons ---
        button_frame = tk.Frame(self)
        button_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        


        editUser_couple_frame.columnconfigure(1, weight=1)

        self.editUser_btSubmit = tk.Button(button_frame, text="Valider", command=self.update_process,underline=0)
        self.editUser_btSubmit.grid(row=0,column=0, sticky="e", padx=5)
        self.editUser_btRetour = tk.Button(button_frame, text="Retour", command=lambda: controller.show_frame("StartPage"),underline=0)
        self.editUser_btRetour.grid(row=0,column=1, sticky="w", padx=5)

        self.bind_shortcuts({
            "<Alt-v>": lambda e: self.update_process(),
            "<Alt-r>": lambda e: self.controller.show_frame("StartPage"),
            "<Alt-a>": lambda e: self.accoupler(),
            "<Alt-c>": lambda e: self.open_planning_modal(self.user_id),
            "<Alt-x>": lambda e: self.divorce()
        })

        # après avoir créé tous les widgets focusables
        self.register_focusable(
            self.editUser_role,
            self.editUser_prenom,
            self.editUser_nom,
            self.editUser_naissance,
            self.editUser_email,
            self.editUser_tel1,
            self.editUser_tel2,
            self.editUser_adresse,
            self.editUser_ville,
            self.editUser_code_postal,
            self.editUser_profession,
            self.editUser_rencontre,
            self.partner_button,
            self.editUser_commentaire,
            self.editUser_montant_du,
            self.editUser_montant_regle,
            self.editUser_commentaire_paiement,
            self.editUser_btSubmit,
            self.editUser_btRetour
        )

        # configure Tab/Shift+Tab
        self.setup_tab_navigation()

    def open_planning_modal(self,id_user):
        win = PlanningModal(self, self.controller, id_user)
        self.wait_window(win) 
        self.set_data(id_user)
        print('plop')
        


    def update_process(self):
        self.update()

        messagebox.showinfo("OK", "Adhérent modifié")

        self.clear_fields()
        self.controller.show_frame("StartPage") 

    def update(self):
        # --- VALIDATIONS ---
        if not self.editUser_nom.get() or not self.editUser_prenom.get() or not self.editUser_email.get() :
            return messagebox.showerror("Erreur", "Nom, Prénom et adresse mail obligatoire")

        # Date validation AAAA-MM-JJ
        if self.editUser_naissance.get() != '':
            try:
                date_naissance_ok = parse_date(self.editUser_naissance.get())
            except:
                return messagebox.showerror("Erreur", "La date de naissance doit être vide ou au format \nAAAA-MM-JJ\nAAAAMMJJ\nJJMMAAAA\nJJ-MM-AAAA\n")
        else:
            date_naissance_ok = ''



        # Téléphone
        if not TEL_REGEX.match(self.editUser_tel1.get()) and self.editUser_tel1.get() != '':
            return messagebox.showerror("Erreur", "Le téléphone 1 doit avoir 10 chiffres ou être vide")

        # Téléphone
        if not TEL_REGEX.match(self.editUser_tel2.get()) and self.editUser_tel2.get() != '':
            return messagebox.showerror("Erreur", "Le téléphone 2 doit avoir 10 chiffres ou être vide")

        # code_postal
        if not CP_REGEX.match(self.editUser_code_postal.get()) and self.editUser_code_postal.get() != '':
            return messagebox.showerror("Erreur", "Le code postal doit avoir 5 chiffres ou être vide")

        # Email simple
        if not EMAIL_REGEX.match(self.editUser_email.get()) and self.editUser_email.get() != '':
            return messagebox.showerror("Erreur", "Email invalide")

        try:
            update_user(
            self.editUser_nom.get(),
            self.editUser_prenom.get(),
            date_naissance_ok,
            self.editUser_tel1.get(),
            self.editUser_tel2.get(),
            self.editUser_email.get(),
            self.editUser_adresse.get(),
            self.editUser_ville.get(),
            self.editUser_code_postal.get(),
            self.editUser_role.get(),
            self.editUser_profession.get(),
            self.editUser_rencontre.get(),
            self.editUser_commentaire.get("1.0", "end").strip(),
            self.editUser_commentaire_paiement.get("1.0", "end").strip(),
            self.editUser_montant_du.get(),
            self.editUser_montant_regle.get(),
            self.user_id)
        except:
            return messagebox.showerror("Erreur", "Modification impossible, il existe déjà un adhérent avec ce Nom, Prenom, et Email")

    def clear_fields(self):
        self.editUser_nom.delete(0, tk.END)
        self.editUser_prenom.delete(0, tk.END)
        self.editUser_email.delete(0, tk.END)
        self.editUser_naissance.delete(0, tk.END)
        self.editUser_tel1.delete(0, tk.END)
        self.editUser_tel2.delete(0, tk.END)
        self.editUser_adresse.delete(0, tk.END)
        self.editUser_ville.delete(0, tk.END)
        self.editUser_code_postal.delete(0, tk.END)
        self.editUser_role.current(0)         # reset combobox
        self.editUser_profession.delete(0, tk.END)
        self.editUser_rencontre.current(6)         # reset combobox
        self.editUser_commentaire.delete("1.0", tk.END)
        self.editUser_montant_du.delete(0, tk.END)
        self.editUser_montant_regle.delete(0, tk.END)
        self.editUser_commentaire_paiement.delete("1.0", tk.END)
        self.modifier_bouton_couple_séparé()

    def on_show(self):
        self.clear_fields()
        self.editUser_role.focus_set()

    def set_data(self,user_id):
        """
        Permet de récupérer les données d'un utilisateur via son id
        """
        data = select_user_data(user_id)
        self.user_id = user_id

            # --- Modification du titre ---
        self.frameTitle.config(text=f"Adhérent depuis {data[13]}")

        self.user_id = user_id
            # --- Identification ---
        self.editUser_role.set(data[10])
        self.editUser_prenom.delete(0, tk.END)
        self.editUser_prenom.insert(0, data[2])

        self.editUser_nom.delete(0, tk.END)
        self.editUser_nom.insert(0, data[1])

        self.editUser_naissance.delete(0, tk.END)
        self.editUser_naissance.insert(0, format_date_human_readable(data[3]))

            # --- Contact ---
        self.editUser_email.delete(0, tk.END)
        self.editUser_email.insert(0, data[6])
        self.editUser_tel1.delete(0, tk.END)
        self.editUser_tel1.insert(0, data[4])
        self.editUser_tel2.delete(0, tk.END)
        self.editUser_tel2.insert(0, data[5])
        self.editUser_adresse.delete(0, tk.END)
        self.editUser_adresse.insert(0, data[7])
        self.editUser_ville.delete(0, tk.END)
        self.editUser_ville.insert(0, data[8])
        self.editUser_code_postal.delete(0, tk.END)
        self.editUser_code_postal.insert(0, data[9])

            # --- Infos supplémentaires ---
        self.editUser_profession.delete(0, tk.END)
        self.editUser_profession.insert(0, data[11])
        self.editUser_rencontre.set(data[12])


            # --- Cadres Commentaires / Règlements ---
        self.editUser_commentaire.delete("1.0", tk.END)
        self.editUser_commentaire.insert("1.0", data[14])
        self.editUser_montant_du.delete(0, tk.END)
        self.editUser_montant_du.insert(0, data[16])
        self.editUser_montant_regle.delete(0, tk.END)
        self.editUser_montant_regle.insert(0, data[17])
        self.editUser_commentaire_paiement.delete("1.0", tk.END)
        self.editUser_commentaire_paiement.insert("1.0", data[15])

        self.partner_id = data[20]
        # Si la personne est en couple
        if self.partner_id != None:
            self.modifier_bouton_couple_ensemble(self.partner_id)
        else:
            self.modifier_bouton_couple_séparé()

    def accoupler(self):
        
        # Si pas de partenaire, création d'un couple
        if self.partner_id == None:
            partner_id = SearchUserWindow(self,self.controller).show()

                # --- le partenaire choisi était déja en couple ---
            if est_deja_en_couple(partner_id) != None:
                return messagebox.showerror("Erreur", "Désolé, mais cette personne est déjà en couple, pas de ça chez nous !")

                # --- auto selection bloquante ---
            if partner_id == self.user_id :
                return messagebox.showerror("Erreur", "Il est assez difficile, sauf pour Alain Delon, de danser en couple avec soit même...")

                # --- le partenaire est libre ---
            if partner_id != None:
                    # --- le role du partenaire est identique ---
                if not verification_role_ok(self.user_id,partner_id):
                    reponse = messagebox.askyesno(
                        "Rôle identique",
                        "Les deux partenaires sont du même role.\nModifier le rôle du partenaire ?"
                    )

                    if reponse:
                        print("modification")
                        modifier_role_sql(partner_id)

                self.modifier_bouton_couple_ensemble(partner_id)
                set_couple(partner_id,self.user_id)
                self.partner_id = partner_id
        else:
            # sinon changement de partenaire, on sauvegarde et on passe sur la fiche du conjoint
            self.update()
            self.controller.show_frame("EditUserPage", self.partner_id)

    def divorce(self):
        self.modifier_bouton_couple_séparé()
        unset_couple(self.user_id,self.partner_id)
        self.partner_id = None

    def modifier_bouton_couple_ensemble(self, user_id):

        data = select_user_data(user_id)

        self.partner_id = user_id
        self.partner_button.config(text=f"{data[2]} - {data[1]}")
        self.partner_button.config(underline=-1)

        self.partner_button.grid(row=0,column=0,columnspan=2, sticky="ew", padx=5)
        self.cancel_couple.grid(row=0,column=3,columnspan=2, sticky="ew", padx=5)

        self.editUser_commentaire_conjoint.config(state="normal")
        self.editUser_commentaire_conjoint.delete("1.0", "end")
        self.editUser_commentaire_conjoint.insert("1.0", data[15])
        self.editUser_commentaire_conjoint.config(state="disabled")

    def modifier_bouton_couple_séparé(self):

        # --- Widgets En couple ---
        self.partner_button.config(text=f"Accoupler")
        self.partner_button.grid(row=0,column=0,columnspan=3, sticky="ew", padx=5)
        self.partner_button.config(underline=0)
        self.cancel_couple.grid_forget()
        self.editUser_commentaire_conjoint.config(state="normal")
        self.editUser_commentaire_conjoint.delete("1.0", "end")
        self.editUser_commentaire_conjoint.config(state="disabled")

class PlanningModal(tk.Toplevel):
    def __init__(self, parent, controller, id_user, on_select_callback=None):
        super().__init__(parent)

        self.title("Sélection du cours")
        self.geometry("1300x900")

        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.id_user = id_user
        self.controller = controller 

        # callback quand on clique sur un cours
        self.on_select_callback = on_select_callback

        # injecter le planning
        self.planning = PlanningPage(self, controller,drag_enabled=False)
        self.planning.pack(fill="both", expand=True)
        self.planning.on_show()

        self.planning.drag_enabled = False
        

        # 🔥 override du comportement click cours
        self.planning.on_click_cours = self.on_click_cours

        # 🔥 override du comportement close
        self.planning.close = self.close

        # Suppression du drag n drop
        self.planning.on_drag_start = self.on_drag_start
        self.planning.on_drag_stop = self.on_drag_stop
        self.planning.on_drag_motion = self.on_drag_motion
        



        # self.bind_all("<Alt-r>",lambda e: self.destroy())
        self.bind("<Alt-r>", lambda e: self.destroy())
        
        # Override des fonctions
    def close(self):
        self.destroy()

    def on_drag_start():
        """
        Override des fonctions
        """
        pass
    def on_drag_motion():
        """
        Override des fonctions
        """
        pass
    def on_drag_stop():
        """
        Override des fonctions
        """
        pass

    def on_click_cours(self, cours_id):
        print(f"Double clic sur le cours avec ID :{cours_id} et pour le user {self.id_user}")
        modal = EditInscriptionModal(
            parent=self,
            controller=self.controller,
            id_user=self.id_user,
            id_cours=cours_id
        )
        self.wait_window(modal)
        self.grab_set()
        self.focus_force()


    def on_cours_choisi(self, cours_id):
        modal = EditInscriptionModal(
            parent=self,
            controller=self.planning.controller,
            id_user=self.id_user,
            id_cours=cours_id
        )
        
        # si tu veux attendre que la modale soit fermée avant de continuer
        self.wait_window(modal)

class EditInscriptionModal(tk.Toplevel):
    def __init__(self, parent, controller, id_user, id_cours):
        super().__init__(parent)
        self.title("Inscription au cours")
        self.transient(parent)
        self.update_idletasks()
        self.grab_set()
        self.focus_force()

        self.controller = controller
        self.id_user = id_user
        self.id_cours = id_cours

        self.cours_info = self.get_cours_info(id_cours)
        self.user_info = self.get_user_info(id_user)
        self.partenaire_info = self.get_partenaire_info(self.user_info)

        if self.partenaire_info != None:
            self.geometry("400x350")
        else:
            self.geometry("400x280")


        self.build_widgets()

    # ----------------------
    # Build widgets
    # ----------------------
    def build_widgets(self):
        # --- Récapitulatif cours ---
        recap_frame = tk.Frame(self)
        recap_frame.pack(pady=10, fill="x")

        tk.Label(recap_frame, text=f"Danse : {self.cours_info['danse']}").pack(fill="x")
        tk.Label(recap_frame, text=f"Niveau : {self.cours_info['niveau']}").pack(fill="x")
        tk.Label(recap_frame, text=f"Jour : {self.cours_info['jour']}").pack(fill="x")
        tk.Label(recap_frame, text=f"Heure : {self.cours_info['debut']} - {self.cours_info['fin']}").pack(fill="x")
        tk.Label(recap_frame, text=f"Prof : {self.cours_info['prof']}").pack(fill="x")

        # --- Zone d'inscription ---
        inscrit_frame = tk.Frame(self)
        inscrit_frame.pack(pady=10, fill="x")

        if self.partenaire_info:  # user en couple
            notebook = ttk.Notebook(inscrit_frame)
            notebook.pack(expand=True, fill="both")

            # Onglet En couple
            couple_frame = tk.Frame(notebook)
            notebook.add(couple_frame, text="En couple")

            # user 1
            tk.Label(couple_frame, text=f"Role {self.user_info['prenom']} :").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.user_role_cb = ttk.Combobox(couple_frame, values=["Leader", "Follower"],state="readonly")
            self.user_role_cb.set(self.user_info['role'])
            self.user_role_cb.grid(row=0, column=1, padx=5, pady=5)

            # partenaire
            tk.Label(couple_frame, text=f"Role {self.partenaire_info['prenom']} :").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.partner_role_cb = ttk.Combobox(couple_frame, values=["Leader", "Follower"],state="readonly")
            self.partner_role_cb.set(self.partenaire_info['role'])
            self.partner_role_cb.grid(row=1, column=1, padx=5, pady=5)

            # Onglet Solo
            solo_frame = tk.Frame(notebook)
            notebook.add(solo_frame, text="Solo")
            tk.Label(solo_frame, text="Role :").pack(side="left", padx=5, pady=5)
            self.solo_role_cb = ttk.Combobox(solo_frame, values=["Leader", "Follower"], state="readonly")
            self.solo_role_cb.set(self.user_info['role'])
            self.solo_role_cb.pack(side="left", padx=5)


        else:  # user solo sans couple
            self.solo_role_cb = ttk.Combobox(inscrit_frame, values=["Leader", "Follower"],state="readonly")
            self.solo_role_cb.set(self.user_info['role'])
            self.solo_role_cb.pack(padx=5)

        # --- Boutons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Inscrire", width=12, command=self.inscrire).pack(padx=10)
        tk.Button(btn_frame, text="Retour", width=12, command=self.destroy,underline=0).pack(padx=10)


        self.bind("<Alt-r>",lambda e: self.destroy())
        self.bind("<Alt-i>",lambda e: self.inscrire())

    def get_cours_info(self, id_cours):
        """
        Récupère les infos d'un cours pour l'affichage dans la modale.
        Retourne un dict : danse, niveau, jour, debut, fin, prof
        """
        query = """
            SELECT 
                d.nom AS danse,
                n.nom AS niveau,
                c.jour,
                c.heure_debut,
                c.heure_fin,
                GROUP_CONCAT(p.nom, ', ') AS profs
            FROM cours c
            JOIN danse d ON c.danse_id = d.id
            JOIN niveau n ON c.niveau_id = n.id
            LEFT JOIN cours_prof cp ON cp.cours_id = c.id
            LEFT JOIN prof p ON cp.prof_id = p.id
            WHERE c.id = ?
            GROUP BY c.id
        """
        row = lanceRequete(query, (id_cours,), fetchone=True)
        if not row:
            return None  # ou raise Exception("Cours introuvable")

        danse, niveau, jour, debut, fin, profs = row
        return {
            "danse": danse,
            "niveau": niveau,
            "jour": jour,
            "debut": debut,
            "fin": fin,
            "prof": profs or ""
        }
    
    def get_user_info(self, id_user):
        """
        Récupère les infos d'un utilisateur depuis la table users.
        Retourne un dict : id, nom, prenom, id_partenaire, role_par_defaut
        """
        query = """
            SELECT id, nom, prenom, partner_id, role
            FROM users
            WHERE id = ?
        """
        row = lanceRequete(query, (id_user,), fetchone=True)
        if not row:
            return None  # ou raise Exception("Utilisateur introuvable")

        user_id, nom, prenom, partner_id, role = row
        return {
            "id": user_id,
            "nom": nom,
            "prenom": prenom,
            "id_partenaire": partner_id,
            "role": role  # rôle par défaut, pour préremplir le combobox
        }
    
    def get_partenaire_info(self, user_info):
        """
        Récupère les infos du partenaire d'un utilisateur, si existant.
        Retourne None si pas de partenaire.
        """
        if not user_info.get("id_partenaire"):
            return None

        query = """
            SELECT id, nom, prenom, role
            FROM users
            WHERE id = ?
        """
        row = lanceRequete(query, (user_info["id_partenaire"],), fetchone=True)
        if not row:
            return None  # partenaire introuvable

        part_id, nom, prenom, role = row
        return {
            "id": part_id,
            "nom": nom,
            "prenom": prenom,
            "role": role  # rôle par défaut du partenaire
        }

    def inscrire(self):
        print("Inscrire clicked")
        # 🔹 placeholder, logique d'inscription ici
        self.destroy()
###########################

##########################
### Gestion de l'école ###
class GestionEcolePage(BasePage):
    """
    Page de gestion de l'école
    """

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Titre
        tk.Label(
            self,
            text="Gestion de l'école",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(20))

    ###################
    ### Frame Danse ###
    ###################
        danse_frame = tk.LabelFrame(
            self,
            text="Gestion des danses",
            padx=10,
            pady=10
        )
        danse_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ### Left side ###

        left = tk.Frame(danse_frame)
        left.grid(row=0, column=0, padx=(0, 20), sticky="n")

        self.entry_danse = tk.Entry(left, width=15)
        self.entry_danse.pack(pady=5)

        tk.Button(
            left,
            text="Ajouter",
            command=lambda: self.add_item("danse", self.entry_danse, self.list_danse)
        ).pack(fill="x", pady=5)

        ### Right side ###

        right = tk.Frame(danse_frame)
        right.grid(row=0, column=1, sticky="n")

        # Horizontal scrollbar
        h_scroll = tk.Scrollbar(right, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")

        self.list_danse = tk.Listbox(
            right,
            height=5,
            width=20,
            xscrollcommand=h_scroll.set
        )
        self.list_danse.pack(side="left", fill="y", expand=True)  # Remplir verticalement

        # Scrollbar verical
        scrollbar = tk.Scrollbar(right, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.list_danse.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.list_danse.yview)


        # Lier scrollbar horizontale à la listbox
        h_scroll.config(command=self.list_danse.xview)

        # Double clic
        self.list_danse.bind("<Double-Button-1>", lambda event: self.open_edit(event, self.list_danse, "danse"))

    ###################
    ### Frame niveau ###
    ###################
        niveau_frame = tk.LabelFrame(
            self,
            text="Gestion des niveaux",
            padx=10,
            pady=10
        )
        niveau_frame.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        ### Left side ###

        left = tk.Frame(niveau_frame)
        left.grid(row=0, column=0, padx=(0, 20), sticky="n")

        self.entry_niveau = tk.Entry(left, width=15)
        self.entry_niveau.pack(pady=5)

        tk.Button(
            left,
            text="Ajouter",
            command=lambda: self.add_item("niveau", self.entry_niveau, self.list_niveau)
        ).pack(fill="x", pady=5)

        ### Right side ###

        right = tk.Frame(niveau_frame)
        right.grid(row=0, column=1, sticky="n")

        # Horizontal scrollbar
        h_scroll = tk.Scrollbar(right, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")

        self.list_niveau = tk.Listbox(
            right,
            height=5,
            width=20,
            xscrollcommand=h_scroll.set
        )
        self.list_niveau.pack(side="left", fill="y")  # Remplir verticalement

        # Scrollbar verical
        scrollbar = tk.Scrollbar(right, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.list_niveau.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.list_niveau.yview)


        # Lier scrollbar horizontale à la listbox
        h_scroll.config(command=self.list_niveau.xview)

        # Double clic
        self.list_niveau.bind("<Double-Button-1>", lambda event: self.open_edit(event, self.list_niveau, "niveau"))

    ###################
    ### Frame prof ###
    ###################
        prof_frame = tk.LabelFrame(
            self,
            text="Gestion des profs",
            padx=10,
            pady=10
        )
        prof_frame.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        ### Left side ###

        left = tk.Frame(prof_frame)
        left.grid(row=0, column=0, padx=(0, 20), sticky="n")

        self.entry_prof = tk.Entry(left, width=15)
        self.entry_prof.pack(pady=5)

        tk.Button(
            left,
            text="Ajouter",
            command=lambda: self.add_item("prof", self.entry_prof, self.list_prof)
        ).pack(fill="x", pady=5)

        ### Right side ###

        right = tk.Frame(prof_frame)
        right.grid(row=0, column=1, sticky="n")

        # Horizontal scrollbar
        h_scroll = tk.Scrollbar(right, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")

        self.list_prof = tk.Listbox(
            right,
            height=5,
            width=20,
            xscrollcommand=h_scroll.set
        )
        self.list_prof.pack(side="left", fill="y")  # Remplir verticalement

        # Scrollbar verical
        scrollbar = tk.Scrollbar(right, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.list_prof.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.list_prof.yview)


        # Lier scrollbar horizontale à la listbox
        h_scroll.config(command=self.list_prof.xview)

        # Double clic
        self.list_prof.bind("<Double-Button-1>", lambda event: self.open_edit(event, self.list_prof, "prof"))

    ###################
    ### Frame salle ###
    ###################
        salle_frame = tk.LabelFrame(
            self,
            text="Gestion des salles",
            padx=10,
            pady=10
        )
        salle_frame.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")

        ### Left side ###

        left = tk.Frame(salle_frame)
        left.grid(row=0, column=0, padx=(0, 20), sticky="n")

        self.entry_salle = tk.Entry(left, width=15)
        self.entry_salle.pack(pady=5)

        tk.Button(
            left,
            text="Ajouter",
            command=lambda: self.add_item("salle", self.entry_salle, self.list_salle)
        ).pack(fill="x", pady=5)

        ### Right side ###

        right = tk.Frame(salle_frame)
        right.grid(row=0, column=1, sticky="n")

        # Horizontal scrollbar
        h_scroll = tk.Scrollbar(right, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")

        self.list_salle = tk.Listbox(
            right,
            height=5,
            width=20,
            xscrollcommand=h_scroll.set
        )
        self.list_salle.pack(side="left", fill="y")  # Remplir verticalement

        # Scrollbar verical
        scrollbar = tk.Scrollbar(right, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.list_salle.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.list_salle.yview)


        # Lier scrollbar horizontale à la listbox
        h_scroll.config(command=self.list_salle.xview)

        # Double clic
        self.list_salle.bind("<Double-Button-1>", lambda event: self.open_edit(event, self.list_salle, "salle"))


        ################
        #### Boutons ###
        ################

        tk.Button(
            self,
            text="Reset base",
            command=self.reset_database,
            bg="red",
            fg="white"
        ).grid(row=99, column=0, pady=20)

        self.btRetour = tk.Button(self, text="Retour", command=lambda: controller.show_frame("StartPage"),underline=0)
        self.btRetour.grid(row=99,column=1, sticky="w", padx=5)

        danse_frame.columnconfigure(1, weight=1)
        niveau_frame.columnconfigure(1, weight=1)
        prof_frame.columnconfigure(1, weight=1)
        salle_frame.columnconfigure(1, weight=1)

        # Gestion des binds
        self.bind_shortcuts({
            "<Alt-r>": lambda e: self.controller.show_frame("StartPage")
        })
        self.entry_danse.bind("<Return>", lambda event: self.add_item("danse", self.entry_danse, self.list_danse))
        self.entry_salle.bind("<Return>", lambda event: self.add_item("salle", self.entry_salle, self.list_salle))
        self.entry_prof.bind("<Return>", lambda event: self.add_item("prof", self.entry_prof, self.list_prof))
        self.entry_niveau.bind("<Return>", lambda event: self.add_item("niveau", self.entry_niveau, self.list_niveau))


        for lb, table_name in [
            (self.list_danse, "danse"),
            (self.list_niveau, "niveau"),
            (self.list_prof, "prof"),
            (self.list_salle, "salle"),
        ]:
            lb.bind("<Return>", lambda e, l=lb, t=table_name: self.open_edit(e, l, t))
    # -------------------------
    # Actions
    # -------------------------
    def choose_danse_color(self):
        color_code = colorchooser.askcolor(title="Choisir une couleur")[1]
        if color_code:
            return color_code
        else:
            return "#FFFFFF"
            
    def on_show(self):
        self.load_danses()
        self.entry_danse.focus()

        # après avoir créé tous les widgets focusables
        self.register_focusable(
            self.entry_danse,
            self.list_danse,
            self.entry_niveau,
            self.list_niveau,
            self.entry_prof,
            self.list_prof,
            self.entry_salle,
            self.list_salle,
            self.btRetour
            
        )

        # configure Tab/Shift+Tab
        self.setup_tab_navigation()

    def reset_database(self):
        confirm = messagebox.askyesno(
            "Tout supprimer",
            "Attention, confirmation ici va supprimer tous les cours, danse, niveaux, professeur, et salle ?"
        )

        if not confirm:
            return

        lanceRequete("""
                DELETE FROM cours_prof;
                DELETE FROM cours;
                DELETE FROM salle;
                DELETE FROM prof;
                DELETE FROM danse;
                DELETE FROM niveau;

                DELETE FROM sqlite_sequence 
                WHERE name IN ('salle', 'prof', 'cours_prof', 'cours', 'danse', 'niveau')""",many=True)
        
        self.load_danses()
        
    def add_item(self, table, entry, listbox):
        value = entry.get().strip()

        if not value:
            entry.focus_set()
            return

        value = value.capitalize()
        try:
            if table == "danse":
                danseColor = self.choose_danse_color()
                lanceRequete(
                    f"INSERT INTO {table}(nom,couleur) VALUES (?,?)",
                    (value,danseColor)
                )
            else:
                lanceRequete(
                    f"INSERT INTO {table}(nom) VALUES (?)",
                    (value,)
                )
        except Exception:
            messagebox.showinfo("Info", f"{value} existe déjà")
        else:
            listbox.insert("end", value)
            entry.delete(0, "end")

        self.load_danses()

        entry.focus_set()

    def load_danses(self):
        """
        recharge les data des listsbox
        """
        self.load_listbox(self.list_danse,"danse")
        self.load_listbox(self.list_salle,"salle")
        self.load_listbox(self.list_niveau,"niveau")
        self.load_listbox(self.list_prof,"prof")

    def load_listbox(self, listbox, table, display_col="nom"):
        import sqlite3

        conn = connect()
        cur = conn.cursor()

        if table == "danse":
            # On récupère la couleur en plus du nom
            cur.execute(f"SELECT id, {display_col}, couleur FROM {table} ORDER BY ID")
            rows = cur.fetchall()
            listbox.delete(0, tk.END)
            for i, row in enumerate(rows):
                listbox.insert(tk.END, row[1])
                # colorier le fond avec la couleur de la danse
                if row[2]:
                    listbox.itemconfig(i, bg=row[2])
        else:
            cur.execute(f"SELECT id, {display_col} FROM {table} ORDER BY ID")
            rows = cur.fetchall()
            listbox.delete(0, tk.END)
            for row in rows:
                listbox.insert(tk.END, row[1])

        conn.close()
        return rows

    def open_edit(self, event, listbox, table):

        selection = listbox.curselection()

        if not selection:
            return

        index = selection[0]
        nom = listbox.get(index)

        win = EditItemWindow(self, nom, table)
        self.wait_window(win) 
        self.load_danses()

class EditItemWindow(tk.Toplevel):

    def __init__(self, parent, nom, table):

        super().__init__(parent)

        self.title(f"Modifier {table.capitalize()}")
        self.after(10, self.grab_set)
        self.transient(parent)

        tk.Label(self, text="Nom").pack(pady=(10, 0))

        self.entry_nom = tk.Entry(self, width=30)
        self.entry_nom.pack(pady=5)

        tk.Label(self, text="Description").pack(pady=(10, 0))

        self.description = tk.Text(self, height=4, width=30)
        self.description.pack(pady=5)

        # boutons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.btn_modify = tk.Button(
            btn_frame,
            text="Modifier",
            command=self.update_item,
            underline=0
        )
        self.btn_modify.grid(row=0, column=0, padx=5)

        self.btn_delete = tk.Button(
            btn_frame,
            text="Supprimer",
            command=self.delete_item,
            underline=0
        )
        self.btn_delete.grid(row=0, column=1, padx=5)

        self.btn_close = tk.Button(
            btn_frame,
            text="Retour",
            command=self.destroy,
            underline=0
        )
        self.btn_close.grid(row=0, column=2, padx=5)

        # ---------------------------
        # Si table == "danse", ajouter bouton couleur
        # ---------------------------
        if table == "danse":
            self.btn_color = tk.Button(
                self,
                text="Modifier couleur",
                command=self.change_color,
                underline=9
            )
            self.btn_color.pack(pady=5)

        ### Remplissage des datas ###
        data = lanceRequete(f"select * from {table} where nom = ?", (nom,), fetchone=True)
        self.entry_nom.insert(0, data[1])
        self.id_item = data[0]
        self.table = table
        self.description.delete("1.0", tk.END)
        self.description.insert("1.0", data[2])
        # couleur si danse
        self.color = data[3] if table == "danse" else None

        # ---------------------------
        # Bindings clavier
        # ---------------------------
        self.entry_nom.bind("<Return>", lambda e: self.update_item())
        self.bind("<Alt-m>", lambda e: self.update_item())
        self.bind("<Alt-s>", lambda e: self.delete_item())
        self.bind("<Alt-c>", lambda e: self.change_color())
        self.bind("<Alt-r>", lambda e: self.destroy())
        self.entry_nom.focus()


    def delete_item(self):
        try:
            lanceRequete(f"DELETE FROM {self.table} WHERE id = '{self.id_item}'")
        except:
            return messagebox.showerror(
                "Erreur",
                f"Il existe au moins un cours qui utilise : {self.entry_nom.get()} dans la table {self.table}"
            )
        self.destroy()

    def update_item(self):
        # Met à jour nom, description, et couleur si danse
        if self.table == "danse":
            lanceRequete(
                "UPDATE danse SET nom = ?, description = ?, couleur = ? WHERE id = ?",
                (self.entry_nom.get().capitalize(),
                 self.description.get("1.0", "end").strip(),
                 self.color,
                 self.id_item)
            )
        else:
            lanceRequete(
                f"UPDATE {self.table} SET nom = ?, description = ? WHERE id = ?",
                (self.entry_nom.get().capitalize(),
                 self.description.get("1.0", "end").strip(),
                 self.id_item)
            )
        self.destroy()

    def change_color(self):
        from tkinter import colorchooser
        new_color = colorchooser.askcolor(title="Choisir une couleur", color=self.color)[1]
        if new_color:
            self.color = new_color
            # Optionnel : changer le fond de l'entry_nom pour visualiser
            self.entry_nom.config(bg=new_color)
##########################

#############################################################
### Recherche d'un utilisateur pour avoir son identifiant ###
class SearchUserWindow(tk.Toplevel):
    """
    Nouvelle fenêtre pour la recherche d'utilisateur qui retourne un ID
    """
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.result = None  # Résultat de la recherche
        self.parent = parent

        self.title("Recherche danseur")
        

        # dimensions souhaitées
        width = 800
        height = 500

        self.geometry(f"{width}x{height}")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for Page in (SeekUserPage, SeekResultPage):
            frame = Page(container, self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SeekUserPage")
        self.transient(parent)   # optionnel, si tu veux que la fenêtre soit au-dessus de la fenêtre principale
        self.grab_set()          # bloque la fenêtre principale
        self.focus_set()         # donne le focus à la Toplevel
        self.after(100, lambda: self.frames["SeekUserPage"].seekUser_nom.focus_set())

    def show_frame(self, name, data=None):
        frame = self.frames[name]

        self.result = None  # Résultat de la recherche

        if hasattr(frame, "set_data"):
            frame.set_data(data)

        frame.tkraise()

        # --- Focus sur la frame si elle a on_show
        if hasattr(frame, "on_show"):
            frame.on_show()
        else:
            frame.focus_set()  # sinon focus par défaut

                                # --- Modifier la taille selon la frame ---
        if name == "SeekUserPage" or name == "SeekResultPage":
            self.geometry("800x180")
        else:
            pass

    def show(self):
        self.wait_window()
        return self.result

    def select_user(self, user_id):
        self.result = user_id
        self.destroy()

class SeekUserPage(BasePage):
    """
    Frame de recherche utilisateur
    Champs en 4 colonnes (Label + Entry côte à côte)
    """
    def __init__(self, parent, controller):
        super().__init__(parent, controller)


        # --- Champs ---
        self.seekUser_nom = tk.Entry(self)
        self.seekUser_prenom = tk.Entry(self)
        self.seekUser_naissance = tk.Entry(self,width=12)
        self.seekUser_email = tk.Entry(self)
        self.seekUser_tel = tk.Entry(self,width=10)
        self.seekUser_ville = tk.Entry(self)

        # --- Labels et Entries en 4 colonnes ---
        tk.Label(self, text="Nom").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.seekUser_nom.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(self, text="Prénom").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.seekUser_prenom.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(self, text="Date de naissance").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.seekUser_naissance.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Email").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.seekUser_email.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        tk.Label(self, text="Téléphone").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.seekUser_tel.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        tk.Label(self, text="Ville").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.seekUser_ville.grid(row=2, column=3, sticky="ew", padx=5, pady=5)

        # Étirement des colonnes
        for i in range(4):
            self.columnconfigure(i, weight=1)

        # --- Boutons ---
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)

        self.seekUser_btSeek = tk.Button(btn_frame, text="Rechercher", command=self.recherche, underline=1)
        self.seekUser_btSeek.pack(side="left", padx=5)
        self.seekUser_btRetour = tk.Button(btn_frame, text="Retour", command=lambda: self.master.master.destroy(), underline=0)
        self.seekUser_btRetour.pack(side="left", padx=5)

        # --- Bindings raccourcis ---
        self.bind_shortcuts({
            "<Alt-e>": lambda e: self.recherche(),
            "<Return>": lambda e: self.recherche(),
            "<Alt-r>": lambda e: self.master.master.destroy()
        })


        # après avoir créé tous les widgets focusables
        self.register_focusable(
            self.seekUser_nom,
            self.seekUser_prenom,
            self.seekUser_naissance,
            self.seekUser_email,
            self.seekUser_tel,
            self.seekUser_ville,
            self.seekUser_btSeek,
            self.seekUser_btRetour,
            
        )

        # configure Tab/Shift+Tab
        self.setup_tab_navigation()

    def recherche(self):

        results = select_users(
            self.seekUser_nom.get(),
            self.seekUser_prenom.get(),
            self.seekUser_naissance.get(),
            self.seekUser_tel.get(),
            self.seekUser_email.get(),
            self.seekUser_ville.get()
        )

        if not results:
            messagebox.showinfo("Info", "Aucun résultat")
            return

        self.controller.show_frame("SeekResultPage", results)
        
    def clear_fields(self):
        self.seekUser_nom.delete(0, tk.END)
        self.seekUser_prenom.delete(0, tk.END)
        self.seekUser_naissance.delete(0, tk.END)
        self.seekUser_tel.delete(0, tk.END)
        self.seekUser_email.delete(0, tk.END)
        self.seekUser_ville.delete(0, tk.END)
    
    def on_show(self):
        self.focus_set()   
        self.seekUser_nom.focus_set()
        self.clear_fields()

class SeekResultPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        columns = ("id", "Nom", "Prenom", "Naissance", "Telephone")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column("id", width=0)

        self.tree.pack(fill="both", expand=True)

        # double clic sur ligne
        self.tree.bind("<Double-1>", self.on_double_click)
        # ENTER sur ligne
        self.tree.bind("<Return>", self.on_enter)

    def set_data(self, results):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in results:
            self.tree.insert("", "end", values=row)

        # --- focus et sélection de la première ligne si elle existe
        self.after(50, self.focus_tree)

    def focus_tree(self):
        if self.tree.get_children():
            first = self.tree.get_children()[0]
            self.tree.focus(first)
            self.tree.selection_set(first)
        self.tree.focus_set()  # focus sur le Treeview

    def on_double_click(self, event):
        self.validate_selection()

    def on_enter(self, event):
        self.validate_selection()

    def validate_selection(self):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        user_id = values[0]

        self.controller.select_user(user_id)
#############################################################


#
#    .....                                                   s       .                                 .x+=:.   
#__H8888888x.  '`+                                          :8      @88>                              z`    ^%  
# 888888888888x.  !        u.      u.    u.                .88      %8P          u.      u.    u.        .    k 
#8~    `"*88888888"  ...ue888b   x@88k u@88c.       .     :888ooo    .     ...ue888b   x@88k u@88c.    .@8Ned8" 
#!      .  `f""""    888R Y888r ^"8888""8888"  .udR88N  -*8888888  .@88u   888R Y888r ^"8888""8888"  .@^%8888"  
# ~:...-` :8L <)88:  888R I888>   8888  888R  <888'888k   8888    ''888E`  888R I888>   8888  888R  x88:  `)8b. 
#    .   :888:>X88!  888R I888>   8888  888R  9888 'Y"    8888      888E   888R I888>   8888  888R  8888N=*8888 
# :~"88x 48888X ^`   888R I888>   8888  888R  9888        8888      888E   888R I888>   8888  888R   %8"    R88 
#<  :888k'88888X    u8888cJ888    8888  888R  9888       .8888Lu=   888E  u8888cJ888    8888  888R    @8Wou 9%  
#  d8888f '88888X    "*888*P"    "*88*" 8888" ?8888u../  ^%888*     888&   "*888*P"    "*88*" 8888" .888888P`   
# :8888!    ?8888>     'Y"         ""   'Y"    "8888P'     'Y"      R888"    'Y"         ""   'Y"   `   ^"F     
# X888!      8888~                               "P'                 ""                                         
# '888       X88f                                                                                               
#  '%8:     .8*"                                                                                                
#     ^----~"`           
#

def connect():
    """
    Connexion à la base de donnée, retourne un handler de connexion à la Bdd
    """
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def center_window(win, parent=None, width=None, height=None):

    """
    Centre une fenêtre Tkinter par rapport à son parent ou à l'écran si parent=None.
    """
    win.update_idletasks()

    if width is None:
        width = win.winfo_width()
    if height is None:
        height = win.winfo_height()

    if parent:
        # coordonnées du parent
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()

        x = px + (pw - width) // 2
        y = py + (ph - height) // 2
    else:
        # par défaut écran principal
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2

    win.geometry(f"{width}x{height}+{x}+{y}")
# USERS ------------------------

def add_user(nom, 
            prenom, 
            naissance, 
            tel1, 
            tel2, 
            email, 
            adresse, 
            ville, 
            code_postal, 
            role, 
            profession, 
            rencontre, 
            annee):
    
    conn = connect()
    c = conn.cursor()
    query = """
        INSERT INTO users(nom, prenom, date_naissance, telephone1, telephone2, email, adresse, ville, code_postal, role, profession, rencontre, annee_inscription)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    params = (nom.upper(),
         prenom.capitalize(),
         naissance,
         tel1,
         tel2,
         email,
         adresse,
         ville,
         code_postal,
         role,
         profession,
         rencontre,
         annee)
    c.execute(query,params)
    conn.commit()
    conn.close()

def update_user(nom, 
            prenom, 
            naissance, 
            tel1, 
            tel2, 
            email, 
            adresse, 
            ville, 
            code_postal, 
            role, 
            profession, 
            rencontre, 
            commentaire,
            commentaire_paiement,
            montant_du,
            montant_regle,
            user_id):
    
    conn = connect()
    c = conn.cursor()
    query = """
        UPDATE users
        SET nom = ?,
            prenom = ?,
            date_naissance = ?,
            telephone1 = ?,
            telephone2 = ?,
            email = ?,
            adresse = ?,
            ville = ?,
            code_postal = ?,
            role = ?,
            profession = ?,
            rencontre = ?,
            commentaire = ?,
            commentaire_paiement = ?,
            montant_du = ?,
            montant_regle = ?
        WHERE id = ?
    """
    params = (nom.upper(),
        prenom.capitalize(),
        naissance,
        tel1,
        tel2,
        email,
        adresse,
        ville,
        code_postal,
        role,
        profession,
        rencontre,
        commentaire,
        commentaire_paiement,
        montant_du,
        montant_regle,
        user_id)
    c.execute(query,params)
    conn.commit()
    conn.close()

def select_users(nom, prenom, naissance, tel, email, ville):
    """
    Retourne tous les utilisateurs qui match les différents critères
    """
    conn = connect()
    c = conn.cursor()

    query = """
        SELECT id, nom,prenom,date_naissance,telephone1 FROM users
        WHERE
        nom LIKE ? AND
        prenom LIKE ? AND
        date_naissance LIKE ? AND
        (telephone1 LIKE ? OR telephone2 LIKE ?) AND
        email LIKE ? AND
        ville LIKE ?
    """

    params = (
        f"%{nom}%",
        f"%{prenom}%",
        f"%{parse_date(naissance)}%",
        f"%{tel}%",
        f"%{tel}%",
        f"%{email}%",
        f"%{ville}%"
    )
    data = c.execute(query,params).fetchall()
    conn.close()
    return data

def select_user_unique(nom,prenom,email):
    """
    Vérifie la présence d'un utilisateur en fonction de son nom, prénom, et mail
    """
    conn = connect()
    c = conn.cursor()

    query = """
        SELECT id FROM users
        WHERE nom = ?
        AND prenom = ?
        AND email = ? 
        LIMIT 1
    """
    data = c.execute(query,(nom.upper(),prenom.capitalize(),email)).fetchone()
    conn.close()
    return data

def select_user_data(id_user):
    """
    Retourne les données d'un utilisateur via son id
    """
    conn = connect()
    c = conn.cursor()

    query = """
        SELECT * FROM users
        WHERE id = ? 
        LIMIT 1
    """
    
    data = c.execute(query,(id_user,)).fetchone()
    conn.close()
    return data

def parse_date(input_date: str) -> str:
    """
    Accepte :
    - YYYY-MM-DD
    - YYYYMMDD
    - DDMMYYYY
    - DD-MM-YYYY

    Retourne : YYYY-MM-DD
    """

    s = input_date.strip()

    if s == '':
        return s

    # 1️⃣ Format ISO déjà correct
    try:
        dt = datetime.strptime(s, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass

    # 2️⃣ Retirer les tirets pour test compact
    s_clean = re.sub(r"[-/ ]", "", s)

    # YYYYMMDD
    if re.fullmatch(r"\d{8}", s_clean):
        # Essaye YYYYMMDD
        try:
            dt = datetime.strptime(s_clean, "%Y%m%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass

        # Essaye DDMMYYYY
        try:
            dt = datetime.strptime(s_clean, "%d%m%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass

    # 3️⃣ Format DD-MM-YYYY
    try:
        dt = datetime.strptime(s, "%d-%m-%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass

    raise ValueError("Format de date invalide")

def format_date_human_readable(date_str):
    """
    Transforme une date 'yyyy-mm-dd' en 'dd-mm-yyyy'
    """
    if date_str != "":
        y, m, d = date_str.split("-")
        return f"{d}-{m}-{y}"  
    else:
        return ""

def set_couple(id1, id2):
    conn = connect()
    cur = conn.cursor()

    cur.execute("UPDATE users SET partner_id = ? WHERE id = ?", (id2, id1))
    cur.execute("UPDATE users SET partner_id = ? WHERE id = ?", (id1, id2))

    conn.commit()

def unset_couple(id1, id2):
    conn = connect()
    cur = conn.cursor()

    cur.execute("UPDATE users SET partner_id = NULL WHERE id = ?", (id2,))
    cur.execute("UPDATE users SET partner_id = NULL WHERE id = ?", (id1,))

    conn.commit()

def est_deja_en_couple(id):
    """
    Vérifie si un adhérent est déjà en couple
    """
    query = """
        SELECT partner_id FROM users
        WHERE id = ? 
        LIMIT 1
    """
    data = lanceRequete(query,(id,),fetchone=True)
    if data == None:
        resultat = None
    else:
        resultat = data[0]
    print(data)
    return resultat

def verification_role_ok(id1,id2):
    """
    On vérifie si 2 id (théoriquement en couple) ont le même rôle par defaut
    """
    conn = connect()
    c = conn.cursor()

    query = """
        SELECT role
        FROM users
        WHERE id IN (?, ?);
    """
    
    data = c.execute(query,(id1,id2)).fetchall()
    conn.close()
    if data[0][0] == data[1][0]:
        print("false")
        return False
    else:
        print("true")
        return True
        
def modifier_role_sql(id):
    """
    Modifie le role d'un utilisateur, simple bascule entre Leader et Follower
    """
    query = """
            UPDATE users
            SET role = CASE
                WHEN role = 'Leader' THEN 'Follower'
                WHEN role = 'Follower' THEN 'Leader'
            END
            WHERE id = ?;
    """
    params = (id,)
    lanceRequete(query,params)
    
def updateCours(cours_id, danse_id, niveau_id, salle_id, jour, debut, fin, commentaires, saison, prof_ids):
    """
    Met à jour un cours existant et ses professeurs associés.
    
    - cours_id : ID du cours à modifier
    - danse_id : ID de la danse
    - niveau_id : ID du niveau
    - salle_id : ID de la salle
    - jour : jour du cours
    - debut, fin : horaires HH:MM
    - prof_ids : liste des IDs des professeurs
    """

    # 1️⃣ Mettre à jour le cours dans la table 'cours'
    query_update = """
        UPDATE cours
        SET danse_id = ?, niveau_id = ?, salle_id = ?, jour = ?, heure_debut = ?, heure_fin = ?, commentaires = ?, saison = ?
        WHERE id = ?
    """
    lanceRequete(query_update, (danse_id, niveau_id, salle_id, jour, debut, fin, commentaires, saison, cours_id))

    # 2️⃣ Supprimer les anciens liens professeurs
    query_delete_profs = "DELETE FROM cours_prof WHERE cours_id = ?"
    lanceRequete(query_delete_profs, (cours_id,))

    # 3️⃣ Ajouter les nouveaux professeurs
    query_insert_prof = "INSERT INTO cours_prof (cours_id, prof_id, saison) VALUES (?, ?, ?)"
    for prof_id in prof_ids:
        lanceRequete(query_insert_prof, (cours_id, prof_id, saison))

def ajoutCours(danse_id, niveau_id, salle_id, jour, heure_debut, heure_fin, saison, list_prof):
    """
    ajoute un cours a la table cours, ainsi que la liaison dans la table cours_prof
    """

    lastID = lanceRequete("INSERT INTO cours (danse_id, niveau_id, salle_id, jour, heure_debut, heure_fin, saison) VALUES (?, ?, ?, ?, ?, ?, ?)",
                 (danse_id, niveau_id, salle_id, jour, heure_debut, heure_fin,saison),
                 insert=True, debug=True
                 )
    print(lastID)
    for idProf in list_prof:
        lanceRequete("INSERT INTO cours_prof (cours_id, prof_id, saison) VALUES (?,?,?)",(lastID,idProf, saison))
   
def generate_hours(step=30):
    """
    Génère une liste d'heures de 08:00 à 22:45 (ou 23:00 selon step)
    step : intervalle en minutes (ex: 15, 30, 60)
    """
    hours = []
    h, m = 8, 0
    while h < 23 or (h == 23 and m == 0):
        hours.append(f"{h:02d}:{m:02d}")
        m += step
        if m >= 60:
            h += m // 60
            m = m % 60
    return hours

def load_listbox(table, listbox):
    query = f"SELECT id, nom FROM {table} ORDER BY id"
    rows = lanceRequete(query, fetch=True)

    listbox.delete(0, tk.END)

    mapping = {}

    for index, (_id, nom) in enumerate(rows):
        listbox.insert(tk.END, nom)
        mapping[index] = _id

    listbox._mapping = mapping

def load_combobox(table, combobox):
    query = f"SELECT id, nom FROM {table} ORDER BY id"
    rows = lanceRequete(query, fetch=True)

    values = []
    mapping = {}

    for _id, nom in rows:
        values.append(nom)
        mapping[nom] = _id

    # 🔥 on sauvegarde l'ancienne valeur AVANT update
    current_value = combobox.get()

    # on met à jour les données
    combobox["values"] = values
    combobox._mapping = mapping

    # 🔥 restauration intelligente
    if current_value in values:
        combobox.set(current_value)
    elif values:
        combobox.current(0)

def check_salle_disponible(salle_id, jour, debut, fin, saison, ignore_cours_id=None):
    """
    Vérifie si la salle est libre sur le créneau donné.
    ignore_cours_id : ID du cours à ignorer (utile lors de la modification)
    """
    query = """
        SELECT COUNT(*) 
        FROM cours
        WHERE salle_id = ?
          AND jour = ?
          AND heure_debut < ?
          AND heure_fin > ?
          AND saison = ?
    """
    params = [salle_id, jour, fin, debut, saison]

    if ignore_cours_id is not None:
        query += " AND id != ?"
        params.append(ignore_cours_id)

    result = lanceRequete(query, tuple(params), fetch=True)
    return result[0][0] == 0  # True si dispo, False si conflit

def check_prof_disponible(prof_id, jour, debut, fin, saison, ignore_cours_id=None):
    """
    Vérifie si le prof est libre sur le créneau donné.
    ignore_cours_id : ID du cours à ignorer (utile lors de la modification)
    """
    query = """
        SELECT COUNT(*)
        FROM cours c
        JOIN cours_prof cp ON cp.cours_id = c.id
        WHERE cp.prof_id = ?
          AND c.jour = ?
          AND c.heure_debut < ?
          AND c.heure_fin > ?
          AND c.saison = ?
    """
    params = [prof_id, jour, fin, debut, saison]

    if ignore_cours_id is not None:
        query += " AND c.id != ?"
        params.append(ignore_cours_id)

    result = lanceRequete(query, tuple(params), fetch=True)
    return result[0][0] == 0  # True = dispo, False = conflit

def get_courses_with_info():
    """
    Retourne une liste de tous les cours avec :
    - jour
    - heure_debut, heure_fin
    - salle_id
    - nom danse, couleur danse
    - nom niveau
    - liste des profs (concaténée)
    """
    query = """
        SELECT 
            c.id,
            c.jour,
            c.heure_debut,
            c.heure_fin,
            c.salle_id,
            d.nom AS danse_nom,
            d.couleur AS danse_couleur,
            n.nom AS niveau_nom,
            GROUP_CONCAT(p.nom, ', ') AS profs
        FROM cours c
        JOIN danse d ON d.id = c.danse_id
        JOIN niveau n ON n.id = c.niveau_id
        LEFT JOIN cours_prof cp ON cp.cours_id = c.id
        LEFT JOIN prof p ON p.id = cp.prof_id
        GROUP BY c.id
        ORDER BY c.jour, c.heure_debut, c.salle_id
    """
    return lanceRequete(query, fetch=True)

def updateCoursFromDrag(cours_id, jour, salle_id, heure_debut, heure_fin):
    """
    Met à jour un cours après drag & drop.
    cours_id : ID du cours
    jour : nouveau jour
    salle_id : nouvelle salle
    heure_debut, heure_fin : nouvelles heures (HH:MM)
    """
    query = """
        UPDATE cours
        SET jour = ?, salle_id = ?, heure_debut = ?, heure_fin = ?
        WHERE id = ?
    """
    params = (jour, salle_id, heure_debut, heure_fin, cours_id)
    lanceRequete(query, params=params)

def get_saisons_possibles():
    from datetime import datetime

    # --- 1. récupérer saisons en DB ---
    query = "SELECT DISTINCT saison FROM cours"
    result = lanceRequete(query, fetch=True)

    saisons = set()
    for row in result:
        if row[0]:
            saisons.add(row[0].strip())

    # --- 2. calcul saison suivante basée sur aujourd'hui ---
    now = datetime.now()
    year = now.year % 100  # ex: 2026 -> 26

    # règle métier : saison = année / année+1
    saison_suivante = f"{year} / {year + 1}"

    saisons.add(saison_suivante)

    # --- 3. tri propre ---
    def saison_key(s):
        try:
            return int(s.split("/")[0].strip())
        except:
            return 0

    saisons_sorted = sorted(saisons, key=saison_key)

    return saisons_sorted

def load_cb_saison(cb):
    from datetime import datetime

    cb["values"] = get_saisons_possibles()

    now = datetime.now()
    year = now.year % 100
    month = now.month

    # --- logique saison ---
    if month >= 7:
        # nouvelle saison
        saison = f"{year} / {year + 1}"
    else:
        # encore dans la saison précédente
        saison = f"{year - 1} / {year}"

    cb.set(saison)


def lanceRequete(query, params=(), fetch=False, fetchone=False, debug=False, many=False, insert=False):
    """
    Le fameux LanceRequete, mondiallement connu dans son quartier !
    """
    conn = connect()
    result = None

    try:
        cur = conn.cursor()

        if debug:
            print(f"Requete lancé : {query}")
            print('---------')
            print(f'parametres utilisés : {params}')


        if many:
            cur.executescript(query)
        else:
            cur.execute(query, params)

        result = None
        if fetch:
            result = cur.fetchall()
        elif fetchone:
            result = cur.fetchone()
        elif insert:
            result = cur.lastrowid

        conn.commit()
    

    finally:
        conn.close()

    return result




#      ...                                                                                                                        s    
#   xH88"`~ .x8X      .uef^"                                                                                                     :8    
# :8888   .f"8888Hf :d88E                      .u    .                             ..    .     :                  u.    u.      .88    
#:8888>  X8L  ^""`  `888E             u      .d88B :@8c       uL          .u     .888: x888  x888.       .u     x@88k u@88c.   :888ooo 
#X8888  X888h        888E .z8k     us888u.  ="8888f8888r  .ue888Nc..   ud8888.  ~`8888~'888X`?888f`   ud8888.  ^"8888""8888" -*8888888 
#88888  !88888.      888E~?888L .@88 "8888"   4888>'88"  d88E`"888E` :888'8888.   X888  888X '888>  :888'8888.   8888  888R    8888    
#88888   %88888      888E  888E 9888  9888    4888> '    888E  888E  d888 '88%"   X888  888X '888>  d888 '88%"   8888  888R    8888    
#88888 '> `8888>     888E  888E 9888  9888    4888>      888E  888E  8888.+"      X888  888X '888>  8888.+"      8888  888R    8888    
#`8888L %  ?888   !  888E  888E 9888  9888   .d888L .+   888E  888E  8888L        X888  888X '888>  8888L        8888  888R   .8888Lu= 
# `8888  `-*""   /   888E  888E 9888  9888   ^"8888*"    888& .888E  '8888c. .+  "*88%""*88" '888!` '8888c. .+  "*88*" 8888"  ^%888*   
#   "888.      :"   m888N= 888> "888*""888"     "Y"      *888" 888&   "88888%      `~    "    `"`    "88888%      ""   'Y"      'Y"    
#     `""***~"`      `Y"   888   ^Y"   ^Y'                `"   "888E    "YP'                           "YP'                            
#                         J88"                           .dWi   `88E                                                                   
#                         @%                             4888~  J8%                                                                    
#                       :"                                ^"===*"`                                                                    




#    ....      ..                                                                                       
#  +^""888h. ~"888h                                                                                     
# 8X.  ?8888X  8888f     .u    .          u.                  .u    .                  ..    .     :    
#'888x  8888X  8888~   .d88B :@8c   ...ue888b       uL      .d88B :@8c        u      .888: x888  x888.  
#'88888 8888X   "88x: ="8888f8888r  888R Y888r  .ue888Nc.. ="8888f8888r    us888u.  ~`8888~'888X`?888f` 
# `8888 8888X  X88x.    4888>'88"   888R I888> d88E`"888E`   4888>'88"  .@88 "8888"   X888  888X '888>  
#   `*` 8888X '88888X   4888> '     888R I888> 888E  888E    4888> '    9888  9888    X888  888X '888>  
#  ~`...8888X  "88888   4888>       888R I888> 888E  888E    4888>      9888  9888    X888  888X '888>  
#   x8888888X.   `%8"  .d888L .+   u8888cJ888  888E  888E   .d888L .+   9888  9888    X888  888X '888>  
#  '%"*8888888h.   "   ^"8888*"     "*888*P"   888& .888E   ^"8888*"    9888  9888   "*88%""*88" '888!` 
#  ~    888888888!`       "Y"         'Y"      *888" 888&      "Y"      "888*""888"    `~    "    `"`   
#       X888^"""                                `"   "888E               ^Y"   ^Y'                      
#       `88f                                   .dWi   `88E                                              
#        88                                    4888~  J8%                                               
#        ""                                     ^"===*"`     


if __name__ == "__main__":
    App().mainloop()


#      ..      .                      ..       
#   x88f` `..x88. .>                dF         
# :8888   xf`*8888%     u.    u.   '88bu.      
#:8888f .888  `"`     x@88k u@88c. '*88888bu   
#88888' X8888. >"8x  ^"8888""8888"   ^"*8888N  
#88888  ?88888< 888>   8888  888R   beWE "888L 
#88888   "88888 "8%    8888  888R   888E  888E 
#88888 '  `8888>       8888  888R   888E  888E 
#`8888> %  X88!        8888  888R   888E  888F 
# `888X  `~""`   :    "*88*" 8888" .888N..888  
#   "88k.      .~       ""   'Y"    `"888*""   
#     `""*==~~`                        ""     

""" Temps passé à dev :
18/02 3h train
27/02 3h train 6
03/03 9h work 15
05/03 4h home 19
06/03 2h home 21
07/03 3h home 24
09/03 5h home 28
19/03 5h home 33
20/03 3h home 36
27/03 10h work 9 / train 3 48

"""