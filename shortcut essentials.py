import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import webbrowser
from PIL import Image, ImageTk
import json

pulsanti = []

def open_site():
    webbrowser.open("https://www.accybertech.it")

def open_manifesto():
    webbrowser.open("https://www.accybertech.it/manifesto")

def open_MIT_LICENSE():
    webbrowser.open("https://www.accybertech.it/mit-license/")

def open_email():
    webbrowser.open("mailto:accybertech@outlook.it")

def apri_link(url):
    webbrowser.open(url)

def on_enter(event):
    event.widget.config(fg="#4d4dff")

def on_leave(event):
    event.widget.config(fg="#000000")

# remove white margin of ttk buttons and creation of ttk style of ttk buttons
def set_custom_style():
    style = ttk.Style()
    style.configure("TButton", padding=(0, 0, 0, 0), font=('Helvetica', 12), background='#bfbfbf', foreground='black')

# icon next to the title in all toplevel windows
def imposta_icona(root):
    icon_path = r"images\icon_root.ico"
    root.iconbitmap(icon_path)

def apri_destinazione(url):
    if not url.startswith(("http://", "https://")):
        messagebox.showerror("Error", "The URL must start with 'http://' o 'https://'.")
        return
    try:
        # Open the URL in your default browser
        webbrowser.open(url, new=2)
    except Exception as e:
        messagebox.showerror("Error", f"The URL could not be opened '{url}': {e}")

def open_disclaimer():
    """
    This function opens a window with the disclaimer of the app.
    """
    window_disclaimer = tk.Toplevel()
    window_disclaimer.title("Disclaimer")
    window_disclaimer.geometry("400x400+750+300")
    window_disclaimer.resizable(False, False)
    window_disclaimer.configure(background="#bfbfbf")
    window_disclaimer.grid_columnconfigure(0, weight=1)
    window_disclaimer.grid_rowconfigure(0, weight=1)
    imposta_icona(window_disclaimer)

    frame = tk.Frame(window_disclaimer, bg="#bfbfbf")
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

    testo_disclaimer = "testo di prova"
    label = tk.Label(frame, text=testo_disclaimer, bg="#bfbfbf", justify="left", wraplength=450, padx=10, pady=10)
    label.pack(fill="both", expand=True)

    manifesto_link = tk.Label(window_disclaimer, text="read our manifesto", font=("Helvetica", 12, "bold"), bg="#bfbfbf", cursor="hand2")
    manifesto_link.grid(row=1, column=0, padx=40, pady=(0, 5), sticky="S")
    manifesto_link.bind("<Button-1>", lambda event: open_manifesto())

def aggiungi_preferito():
    """
    This function prompts the user to enter the URL of a bookmark and adds it to the favorites list.
    """
    while True:
        url = simpledialog.askstring("Add Bookmark", "Enter the URL of your bookmark: The URL must start with 'http://' or 'https://' ")
        if not url:
            return  # The user canceled the entry
        if url.startswith(("http://", "https://")):
            break
        messagebox.showerror("Error", "The URL must start with 'http://' or 'https://'.")

    while True:
        frame_selezionato = simpledialog.askinteger("Select Frame", "Enter frame number (1, 2, or 3):", minvalue=1, maxvalue=3)
        if frame_selezionato is None:
            return

        pulsante_selezionato = simpledialog.askinteger("Select Button", "Enter button number (1-4):", minvalue=1, maxvalue=4)
        if pulsante_selezionato is None:
            return

        # Calculate the index of the selected button
        indice_pulsante = (frame_selezionato - 1) * 4 + pulsante_selezionato - 1

        # favorites list of sufficient length
        while len(preferiti) <= indice_pulsante:
            preferiti.append(None)

        if preferiti[indice_pulsante]:
            messagebox.showerror("Error", "The selected button is already occupied. Choose another button.")
        else:
            nome_pulsante = simpledialog.askstring("Assign a Name", "Enter the name to assign to the button:")
            if nome_pulsante is None:
                return

            if nome_pulsante:
                pulsante = pulsanti[frame_selezionato - 1][pulsante_selezionato - 1]
                pulsante.config(text=nome_pulsante)
                preferiti[indice_pulsante] = {"nome": nome_pulsante, "url": url}
                salva_preferiti()
                messagebox.showinfo("Add Favorite", "Favorite added successfully!")
                break

def open_preferiti():
    """
    This function opens a window with the favorites list.
    """
    global pulsanti

    window_preferiti = tk.Toplevel()
    window_preferiti.title("Options")
    window_preferiti.geometry("400x200+700+300")
    window_preferiti.resizable(False, False)
    window_preferiti.configure(background="#bfbfbf")
    window_preferiti.grid_columnconfigure(0, weight=1)
    window_preferiti.grid_rowconfigure(0, weight=1)
    imposta_icona(window_preferiti)

    style_window_preferiti = ttk.Style(window_preferiti)
    style_window_preferiti.configure("TButton", font=('Roboto', 9))

    frames = [tk.Frame(window_preferiti, bg="#bfbfbf") for _ in range(3)]
    for frame in frames:
        frame.pack(pady=(5, 0))

    pulsanti = []
    for i in range(3):
        riga_pulsanti = []
        for j in range(4):
            index = i * 4 + j
            if preferiti[index]:
                nome_pulsante = preferiti[index]["nome"]
            else:
                nome_pulsante = f"Button {index + 1}"

            pulsante = ttk.Button(frames[i], text=nome_pulsante, command=lambda idx=index: apri_destinazione(preferiti[idx]["url"]) if preferiti[idx] else None, cursor="hand2")
            pulsante.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")
            riga_pulsanti.append(pulsante)
        pulsanti.append(riga_pulsanti)

    pulsante_aggiungi_preferito = ttk.Button(window_preferiti, text="Add Favorite", command=aggiungi_preferito, cursor="hand2")
    pulsante_aggiungi_preferito.pack(pady=3)

    pulsante_cancella_tutti_preferiti = ttk.Button(window_preferiti, text="Clear All Favorites", command=cancella_tutti_preferiti, cursor="hand2")
    pulsante_cancella_tutti_preferiti.pack(pady=3)

    pulsante_cancella_preferito = ttk.Button(window_preferiti, text="Delete Favorite", command=cancella_preferito, cursor="hand2")
    pulsante_cancella_preferito.pack(pady=3)

def salva_preferiti():
    with open("favorites.json", "w") as file:
        # Make sure a list with None values is saved
        json.dump(preferiti, file)

def carica_preferiti():
    try:
        with open("favorites.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return [None] * 12

preferiti = carica_preferiti()

def cancella_tutti_preferiti():
    """
    This function deletes all the favorites.
    """
    conferma = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all bookmarks?")
    if conferma:
        for i, riga_pulsanti in enumerate(pulsanti):
            for j, pulsante in enumerate(riga_pulsanti):
                pulsante.config(text=f"Button {i * 4 + j + 1}")
                preferiti[i * 4 + j] = None
        salva_preferiti()
        messagebox.showinfo("Delete All Favorites", "All Favorite successfully deleted!")

def cancella_preferito():
    """
    This function deletes a favorite.
    """
    frame_selezionato = simpledialog.askinteger("Select Frame", "Enter frame number (1, 2, or 3):", minvalue=1, maxvalue=3)

    # Check if the user canceled the frame selection
    if frame_selezionato is None:
        return

    pulsante_selezionato = simpledialog.askinteger("Select Button", "Enter button number (1-4):", minvalue=1, maxvalue=4)

    if pulsante_selezionato is None:
        return

    indice_pulsante = (frame_selezionato - 1) * 4 + pulsante_selezionato - 1
    if preferiti[indice_pulsante]:
        conferma = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this bookmark?")
        if conferma:
            pulsante = pulsanti[frame_selezionato - 1][pulsante_selezionato - 1]
            pulsante.config(text=f"Button {indice_pulsante + 1}")
            preferiti[indice_pulsante] = None
            salva_preferiti()
            messagebox.showinfo("Delete Favorite", "Favorite successfully deleted!")

def open_help():
    window_help = tk.Toplevel()
    window_help.title("Help")
    window_help.geometry("400x300+750+300")
    window_help.resizable(False, False)
    window_help.configure(background="#bfbfbf")
    window_help.grid_columnconfigure(0, weight=1)
    imposta_icona(window_help)

    frame = tk.Frame(window_help, bg="#bfbfbf")
    frame.grid(row=0, column=0, padx=10, pady=(10,5), sticky="NSEW")

    testo_help = """
    For any clarification or suggestion regarding this app do not
    hesitate to contact me
    """
    label = tk.Label(frame, text=testo_help, bg="#bfbfbf", justify="left", wraplength=450, padx=10, pady=10)
    label.pack(fill="both", expand=True)

    documentation_button = ttk.Button(window_help, text="Documentation", cursor="hand2", command=lambda: apri_link("https://www.accybertech.it/shortcut-essentials/"))
    documentation_button.grid(row=1, column=0, padx=10, pady=3, sticky="WE")

    about_button = ttk.Button(window_help, text="About", cursor="hand2", command=open_about)
    about_button.grid(row=2, column=0, padx=10, pady=3, sticky="WE")

    site_button = ttk.Button(window_help, text="My site", cursor="hand2", command=open_site)
    site_button.grid(row=3, column=0, padx=10, pady=3, sticky="WE")

    email_button = ttk.Button(window_help, text="Email", cursor="hand2", command=open_email)
    email_button.grid(row=4, column=0, padx=10, pady=3, sticky="WE")

    retry_image = ImageTk.PhotoImage(Image.open(r"images\retry_image .ico"))

    # Creating a Label widget in the frame and displaying the image
    label_image = tk.Label(window_help, image=retry_image, bg="#bfbfbf")
    label_image.image = retry_image

    retry_button = ttk.Button(window_help, image=retry_image, cursor="hand2", command=window_help.destroy)
    retry_button.grid(row=5, column=0, padx=10, pady=(10, 10), sticky="SE")

def open_about():
    window_about = tk.Toplevel()
    window_about.title("About")
    window_about.geometry("400x400+750+300")
    window_about.resizable(False, False)
    window_about.configure(background="#bfbfbf")
    imposta_icona(window_about)

    frame = tk.Frame(window_about, bg="#bfbfbf", padx=10, pady=0)
    frame.pack(fill="both", expand=True)

    image_SE = ImageTk.PhotoImage(Image.open(r"images\image_SE.ico"))

    # Creating a Label widget in the frame and displaying the image
    label_image = tk.Label(frame, image=image_SE, bg="#bfbfbf")
    label_image.image = image_SE
    label_image.pack(anchor="center")

    app_label= tk.Label(frame, text="shortcut essentials v1.0", font=("Helvetica", 12, "bold"), bg="#bfbfbf")
    app_label.pack(anchor="center", pady=10)

    testo_about = """
    This app was created by Antonino Cacciottoli & ACcybertech.it\n
    ACcybertech.it is a young Italian company that deals
    with the creation of websites, web applications,
    desktop & mobile applications.\n
    For more information visit our website:
    www.accybertech.it
    """

    label_text = tk.Label(frame, text=testo_about, bg="#bfbfbf", justify="left", wraplength=380)
    label_text.pack(anchor="center")

    copyright_label= tk.Label(frame, text="Antonino Cacciottoli & ACcybertech © 2021 - 2024 MIT license",bg="#bfbfbf",font=("Arial", 9, "bold"), cursor="hand2")
    copyright_label.pack(anchor="center")
    copyright_label.bind("<Enter>", on_enter)
    copyright_label.bind("<Leave>", on_leave)
    copyright_label.bind("<Button-1>", lambda event: open_MIT_LICENSE())

    ok_button= ttk.Button(frame, text="OK", cursor="hand2", command=window_about.destroy)
    ok_button.pack(anchor="center", pady=10)

    # attacco qua le icone dei social









    # finw icone dei social

# main window
root = tk.Tk()
root.geometry("300x300+600+280")
root.title("shortcut essentials v1.0")
root.resizable(False, False)
root.configure(background="#bfbfbf")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
imposta_icona(root)
set_custom_style()

facebook_button = ImageTk.PhotoImage(Image.open(r"images\facebook_button.png"))
instagram_button = ImageTk.PhotoImage(Image.open(r"images\instagram_button.png"))
linkedin_button = ImageTk.PhotoImage(Image.open(r"images\linkedin_button.png"))
x_button = ImageTk.PhotoImage(Image.open(r"images\x_button.png"))
tik_tok_button = ImageTk.PhotoImage(Image.open(r"images\tik_tok_button.png"))
twitch_button = ImageTk.PhotoImage(Image.open(r"images\twitch_button.png"))
youtube_button = ImageTk.PhotoImage(Image.open(r"images\youtube_button.png"))
whatsapp_button = ImageTk.PhotoImage(Image.open(r"images\whatsapp_button.png"))
google_button = ImageTk.PhotoImage(Image.open(r"images\google_button.png"))
google_maps_button = ImageTk.PhotoImage(Image.open(r"images\google_maps_button.png"))
google_translate_button = ImageTk.PhotoImage(Image.open(r"images\google_translate_button.png"))
wikipedia_button = ImageTk.PhotoImage(Image.open(r"images\wikipedia_button.png"))
duckduckgo_button = ImageTk.PhotoImage(Image.open(r"images\duckduckgo_button.png"))
reddit_button = ImageTk.PhotoImage(Image.open(r"images\reddit_button.png"))
discord_button = ImageTk.PhotoImage(Image.open(r"images\discord_button.png"))
quora_button = ImageTk.PhotoImage(Image.open(r"images\quora_button.png"))
telegram_button = ImageTk.PhotoImage(Image.open(r"images\telegram_button.png"))
gmail_button = ImageTk.PhotoImage(Image.open(r"images\gmail_button.png"))
outlook_button = ImageTk.PhotoImage(Image.open(r"images\outlook_button.png"))
spotify_button = ImageTk.PhotoImage(Image.open(r"images\spotify_button.png"))
onedrive_button = ImageTk.PhotoImage(Image.open(r"images\onedrive_button.png"))
dropbox_button = ImageTk.PhotoImage(Image.open(r"images\dropbox_button .png"))
google_drive_button = ImageTk.PhotoImage(Image.open(r"images/google_drive_button.png"))
amazon_button = ImageTk.PhotoImage(Image.open(r"images\amazon_button.png"))
sky_tg24_button = ImageTk.PhotoImage(Image.open(r"images\sky_tg24_button.png"))
ansa_button = ImageTk.PhotoImage(Image.open(r"images/ansa_button.png"))
sky_sport_button = ImageTk.PhotoImage(Image.open(r"images\sky_sport_button.png"))
espn_button = ImageTk.PhotoImage(Image.open(r"images\espn_button.png"))
bbc_button = ImageTk.PhotoImage(Image.open(r"images\bbc_button.png"))
cnn_button = ImageTk.PhotoImage(Image.open(r"images\cnn_button .png"))
reuters_button = ImageTk.PhotoImage(Image.open(r"images\reuters_button.png"))
il_meteo_button = ImageTk.PhotoImage(Image.open(r"images\il_meteo_button.png"))

link_disclaimer = tk.Label(root, text="Disclaimer", bg="#bfbfbf", cursor="hand2")
link_disclaimer.grid(row=0, column=0, padx=5, pady=(2, 5), sticky="NW")
link_disclaimer.bind("<Button-1>", lambda event: open_disclaimer())

link_preferiti = tk.Label(root, text="Options", bg="#bfbfbf", cursor="hand2")
link_preferiti.grid(row=0, column=0, padx=(65,5), pady=(2, 5), sticky="NW")
link_preferiti.bind("<Button-1>", lambda event: open_preferiti())

link_help = tk.Label(root, text="Help", bg="#bfbfbf", cursor="hand2")
link_help.grid(row=0, column=0, padx=112, pady=(2, 5), sticky="NW")
link_help.bind("<Button-1>", lambda event: open_help())

frame_button = tk.Frame(root, padx=0, pady=0, bg="#bfbfbf")
frame_button.grid(row=1, column=0, padx=5, pady=0, sticky="WE")

link_disclaimer.bind("<Enter>", on_enter)
link_disclaimer.bind("<Leave>", on_leave)
link_disclaimer.bind("<Button-1>", lambda event: open_disclaimer())

link_preferiti.bind("<Enter>", on_enter)
link_preferiti.bind("<Leave>", on_leave)
link_preferiti.bind("<Button-1>", lambda event: open_preferiti())

link_help.bind("<Enter>", on_enter)
link_help.bind("<Leave>", on_leave)
link_help.bind("<Button-1>", lambda event: open_help())

prime_button = ttk.Button(frame_button, image=facebook_button, cursor="hand2", command=lambda: apri_link("https://www.facebook.com"))
prime_button.grid(row=1, column=0, padx=(20, 5), pady=0, sticky="W")

second_button = ttk.Button(frame_button, image=instagram_button, cursor="hand2", command=lambda: apri_link("https://www.instagram.com"))
second_button.grid(row=1, column=0, padx=(85, 5), pady=0, sticky="W")

third_button = ttk.Button(frame_button, image=linkedin_button, cursor="hand2", command=lambda: apri_link("https://www.linkedin.com"))
third_button.grid(row=1, column=0, padx=(150, 5), pady=0, sticky="W")

fourth_button = ttk.Button(frame_button, image=x_button, cursor="hand2", command=lambda: apri_link("https://twitter.com/"))
fourth_button.grid(row=1, column=0, padx=(215, 5), pady=0, sticky="W")


frame_button2 = tk.Frame(root, padx=0, pady=0, bg="#bfbfbf")
frame_button2.grid(row=2, column=0, padx=5, pady=0, sticky="WE")

fifth_button = ttk.Button(frame_button2, image=tik_tok_button, cursor="hand2", command=lambda: apri_link("https://www.tiktok.com"))
fifth_button.grid(row=2, column=0, padx=(20, 5), pady=0, sticky="W")

sixth_button = ttk.Button(frame_button2, image=twitch_button, cursor="hand2", command=lambda: apri_link("https://www.twitch.tv/"))
sixth_button.grid(row=2, column=0, padx=(85, 5), pady=0, sticky="W")

seventh_button = ttk.Button(frame_button2, image=youtube_button, cursor="hand2", command=lambda: apri_link("https://www.youtube.com"))
seventh_button.grid(row=2, column=0, padx=(150, 5), pady=0, sticky="W")

eighth_button = ttk.Button(frame_button2, image=whatsapp_button, cursor="hand2", command=lambda: apri_link("https://web.whatsapp.com"))
eighth_button.grid(row=2, column=0, padx=(215, 5), pady=0, sticky="W")


frame_button3 = tk.Frame(root, padx=0, pady=0, bg="#bfbfbf")
frame_button3.grid(row=3, column=0, padx=5, pady=0, sticky="WE")

ninth_button = ttk.Button(frame_button3, image=google_button, cursor="hand2", command=lambda: apri_link("https://www.google.com"))
ninth_button.grid(row=3, column=0, padx=(20, 5), pady=0, sticky="W")

tenth_button = ttk.Button(frame_button3, image=google_maps_button, cursor="hand2", command=lambda: apri_link("https://www.google.it/maps"))
tenth_button.grid(row=3, column=0, padx=(85, 5), pady=0, sticky="W")

eleventh_button = ttk.Button(frame_button3, image=google_translate_button, cursor="hand2", command=lambda: apri_link("https://translate.google.it"))
eleventh_button.grid(row=3, column=0, padx=(150, 5), pady=0, sticky="W")

twelfth_button = ttk.Button(frame_button3, image=wikipedia_button, cursor="hand2", command=lambda: apri_link("https://it.wikipedia.org/wiki/Pagina_principale"))
twelfth_button.grid(row=3, column=0, padx=(215, 5), pady=0, sticky="W")


frame_button4 = tk.Frame(root, padx=0, pady=0, bg="#bfbfbf")
frame_button4.grid(row=4, column=0, padx=5, pady=0, sticky="WE")

ninth_button = ttk.Button(frame_button4, image=duckduckgo_button, cursor="hand2", command=lambda: apri_link("https://duckduckgo.com"))
ninth_button.grid(row=4, column=0, padx=(20, 5), pady=0, sticky="W")

tenth_button = ttk.Button(frame_button4, image=reddit_button, cursor="hand2", command=lambda: apri_link("https://www.reddit.com"))
tenth_button.grid(row=4, column=0, padx=(85, 5), pady=0, sticky="W")

eleventh_button = ttk.Button(frame_button4, image=discord_button, cursor="hand2", command=lambda: apri_link("https://discord.com"))
eleventh_button.grid(row=4, column=0, padx=(150, 5), pady=0, sticky="W")

twelfth_button = ttk.Button(frame_button4, image=quora_button, cursor="hand2", command=lambda: apri_link("https://it.quora.com"))
twelfth_button.grid(row=4, column=0, padx=(215, 5), pady=0, sticky="W")


frame_button5 = tk.Frame(root, padx=0, pady=0, bg="#bfbfbf")
frame_button5.grid(row=5, column=0, padx=5, pady=0, sticky="WE")

ninth_button = ttk.Button(frame_button5, image=telegram_button, cursor="hand2", command=lambda: apri_link("https://web.telegram.org"))
ninth_button.grid(row=5, column=0, padx=(20, 5), pady=0, sticky="W")

tenth_button = ttk.Button(frame_button5, image=gmail_button, cursor="hand2", command=lambda: apri_link("https://mail.google.com"))
tenth_button.grid(row=5, column=0, padx=(85, 5), pady=0, sticky="W")

eleventh_button = ttk.Button(frame_button5, image=outlook_button, cursor="hand2", command=lambda: apri_link("https://outlook.live.com"))
eleventh_button.grid(row=5, column=0, padx=(150, 5), pady=0, sticky="W")

twelfth_button = ttk.Button(frame_button5, image=spotify_button, cursor="hand2", command=lambda: apri_link("https://open.spotify.com"))
twelfth_button.grid(row=5, column=0, padx=(215, 5), pady=0, sticky="W")


frame_button6 = tk.Frame(root, padx=0, pady=0, bg="#bfbfbf")
frame_button6.grid(row=6, column=0, padx=5, pady=0, sticky="WE")

ninth_button = ttk.Button(frame_button6, image=onedrive_button, cursor="hand2", command=lambda: apri_link("https://www.microsoft.com/it-it/microsoft-365/onedrive/online-cloud-storage?market=it"))
ninth_button.grid(row=6, column=0, padx=(20, 5), pady=0, sticky="W")

tenth_button = ttk.Button(frame_button6, image=dropbox_button, cursor="hand2", command=lambda: apri_link("https://www.dropbox.com/"))
tenth_button.grid(row=6, column=0, padx=(85, 5), pady=0, sticky="W")

eleventh_button = ttk.Button(frame_button6, image=google_drive_button, cursor="hand2", command=lambda: apri_link("https://drive.google.com"))
eleventh_button.grid(row=6, column=0, padx=(150, 5), pady=0, sticky="W")

twelfth_button = ttk.Button(frame_button6, image=amazon_button, cursor="hand2", command=lambda: apri_link("https://www.amazon.it"))
twelfth_button.grid(row=6, column=0, padx=(215, 5), pady=0, sticky="W")


frame_button7 = tk.Frame(root, padx=0, pady=0, bg="#bfbfbf")
frame_button7.grid(row=7, column=0, padx=5, pady=0, sticky="WE")

ninth_button = ttk.Button(frame_button7, image=sky_tg24_button, cursor="hand2", command=lambda: apri_link("https://tg24.sky.it"))
ninth_button.grid(row=7, column=0, padx=(20, 5), pady=0, sticky="W")

tenth_button = ttk.Button(frame_button7, image=ansa_button, cursor="hand2", command=lambda: apri_link("https://www.ansa.it"))
tenth_button.grid(row=7, column=0, padx=(85, 5), pady=0, sticky="W")

eleventh_button = ttk.Button(frame_button7, image=sky_sport_button, cursor="hand2", command=lambda: apri_link("https://sport.sky.it"))
eleventh_button.grid(row=7, column=0, padx=(150, 5), pady=0, sticky="W")

twelfth_button = ttk.Button(frame_button7, image=espn_button, cursor="hand2", command=lambda: apri_link("https://www.espn.com"))

twelfth_button.grid(row=7, column=0, padx=(215, 5), pady=0, sticky="W")


frame_button8 = tk.Frame(root, padx=0, pady=0, bg="#bfbfbf")
frame_button8.grid(row=8, column=0, padx=5, pady=0, sticky="WE")

ninth_button = ttk.Button(frame_button8, image=bbc_button, cursor="hand2", command=lambda: apri_link("https://www.bbc.com/news"))
ninth_button.grid(row=8, column=0, padx=(20, 5), pady=0, sticky="W")

tenth_button = ttk.Button(frame_button8, image=cnn_button, cursor="hand2", command=lambda: apri_link("https://edition.cnn.com"))
tenth_button.grid(row=8, column=0, padx=(85, 5), pady=0, sticky="W")

eleventh_button = ttk.Button(frame_button8, image=reuters_button, cursor="hand2", command=lambda: apri_link("https://www.reuters.com/"))
eleventh_button.grid(row=8, column=0, padx=(150, 5), pady=0, sticky="W")

twelfth_button = ttk.Button(frame_button8, image=il_meteo_button, cursor="hand2", command=lambda: apri_link("https://www.ilmeteo.it"))
twelfth_button.grid(row=8, column=0, padx=(215, 5), pady=0, sticky="W")

empty_Label = tk.Label(root, bg="#bfbfbf")
empty_Label.grid(row=9, column=0, padx=10, pady=0, sticky="EW")

accybertech_link = tk.Label(root, text="accybertech.it", font=("Helvetica", 12, "bold"), bg="#bfbfbf", cursor="hand2")
accybertech_link.grid(row=10, column=0, padx=(20, 10), pady=(0, 0), sticky="S")
accybertech_link.bind("<Button-1>", lambda event: open_site())

root.mainloop()
