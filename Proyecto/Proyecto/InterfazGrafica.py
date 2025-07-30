from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import time
from playwright.sync_api import sync_playwright
from TikTokApi import TikTokApi
import asyncio
import os


color_fondo = "#295571"
# --- Ventana Principal ---
ventana = Tk()
ventana.title("App Scrapper &  Dectector") # Es buena práctica darle un título

# --- Dimensiones de la ventana ---
ancho_ventana = 900
alto_ventana = 650

# --- Lógica para centrar la ventana ---
# 1. Obtener el ancho y alto de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# 2. Calcular las coordenadas x, y para centrar
x = (ancho_pantalla // 2) - (ancho_ventana // 2)
y = int((alto_pantalla // 2.5)) - (alto_ventana // 2)

# 3. Establecer la geometría con las coordenadas calculadas
# El formato es "ancho x alto + x + y"
ventana.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')

# --- Evitar que la ventana pueda ser redimensionada (opcional pero recomendado) ---
ventana.resizable(True, True)
ventana.minsize(800, 600) 

# --- Imagen de fondo ---
try:
    # 1. Cargar la imagen original de alta calidad y guardarla. NO la redimensiones aquí.
    img_original_pil = Image.open("Tikto.jpeg")
    
    # 2. Crear el Label que contendrá la imagen de fondo.
    fondo_label = Label(ventana)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    fondo_label.lower()

    # 3. Crear una función que se encargue de redimensionar la imagen
    def redimensionar_fondo(event):
        # Redimensionar la imagen original al nuevo tamaño de la ventana
        img_redimensionada = img_original_pil.resize((event.width, event.height), Image.LANCZOS)
        
        # Convertir a PhotoImage y actualizar el Label
        # Guardar la referencia en el propio widget para que no se borre
        fondo_label.photo = ImageTk.PhotoImage(img_redimensionada)
        fondo_label.config(image=fondo_label.photo)

    # 4. Vincular esa función al evento de cambio de tamaño de la ventana
    ventana.bind("<Configure>", redimensionar_fondo)
except FileNotFoundError:
    print("Error: No se encontró el archivo 'TikTok.jpeg'.")
    
fondo_label.lower()
try:
    img_logo_pil = Image.open("pythonLogo.jpeg") 
    img_logo_pil = img_logo_pil.resize((150, 150)) 
    photo_logo = ImageTk.PhotoImage(img_logo_pil)
    logo_label = Label(ventana, image=photo_logo, bg=color_fondo) 
    logo_label.place(x=12, y=50) # Colócalo donde quieras
except FileNotFoundError:
    print("Error: No se encontró el archivo 'python_logo.png'")

text2 = Label(ventana,text="Project V1")

text2.place(relx=0.5, rely=0.15, anchor='center')
text2.config(font=("Britannic Bold",60,"normal"), fg='white',bg="#295571")

text1 = Label(ventana,text="Instrucciones:\n1.- Tener cerrado pestañas de TikTok\n2.- Leer los mensajes de las ventanas emergentes\n3.- Las casillas rojas son botones que puedes usar")

text1.place(relx=0.5, rely=0.35, anchor='center', width=880)
text1.config(font=("Britannic Bold",12,"normal"), fg='white',bg=color_fondo,justify=LEFT,)



text3 = Label(ventana,text="Ingresa el id o Link del video de TikTok, caso contrario déjalo en blanco para tomar los 10 videos mas populares. \n Ejemplo del link: https://www.tiktok.com/@worldwise14/video/7519149704454671647")
text3.place(relx=0.5, rely=0.52, anchor='center', width=880)
text3.config(font=("Britannic Bold",12,"normal"), fg='white',bg=color_fondo)



placeholderVideo = "Id o Link del video"
placeholder_color = "grey"
texto_real_color = "white"

# --- Funciones para manejar los eventos ---

def on_entry_click(event):
    if linkVideo.get() == placeholderVideo:
        linkVideo.delete(0, "end")  # Borra todo el texto
        linkVideo.config(fg=texto_real_color) # Cambia el color del texto a blanco

def on_focus_out(event):
    if linkVideo.get() == "":
        linkVideo.insert(0, placeholderVideo) # Vuelve a poner el placeholder
        linkVideo.config(fg=placeholder_color) # Vuelve a poner el color gris


linkVideo = Entry(
    ventana,
    highlightbackground="#2D9C95",
    highlightcolor="#F81157",
    highlightthickness=2,
    font=("Britannic Bold", 15, "normal"),
    bg=color_fondo,
    border=5,
    fg=placeholder_color  
)

linkVideo.place(relx=0.02, rely=0.6, relwidth=0.96, height=50)
linkVideo.insert(0, placeholderVideo)
linkVideo.bind('<FocusIn>', on_entry_click)
linkVideo.bind('<FocusOut>',on_focus_out)






color_original_bg = "#76253D"  
color_hover_bg = "#F17DA0"     
color_original_fg = "white"   
color_hover_fg = "black"      


def on_enter(event, button):
    button.config(background=color_hover_bg, foreground=color_hover_fg)

def on_leave(event, button):
    button.config(background=color_original_bg, foreground=color_original_fg)


changeWords = Button(
    ventana,
    text="Agregar/Cambiar palabras de odio buscadas",
    font=("Britannic Bold", 13, "normal"),
    fg=color_original_fg,
    bg=color_original_bg,
    relief="flat",          
    borderwidth=0,
    highlightthickness=0,   
    activebackground="#FF5733", 
    activeforeground="white"
)

generar = Button(
    ventana,
    text="Extraer Comentarios",
    font=("Britannic Bold", 13, "normal"),
    fg=color_original_fg,
    bg=color_original_bg,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    activebackground="#33A1FF",
    activeforeground="white"
)

busquedaPatron = Button(
    ventana,
    text="Realizar búsqueda de palabras de odio",
    font=("Britannic Bold", 13, "normal"),
    fg=color_original_fg,
    bg=color_original_bg,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    activebackground="#33A1FF",
    activeforeground="white"

)

generar.place(relx=0.22, rely=0.77, anchor='center', width=200, height=40)
changeWords.place(relx=0.65, rely=0.77, anchor='center', width=350, height=40)
busquedaPatron.place(relx=0.3, rely=0.9, anchor='center', width=350, height=40)

changeWords.bind("<Enter>", lambda event: on_enter(event, changeWords))
changeWords.bind("<Leave>", lambda event: on_leave(event, changeWords))

generar.bind("<Enter>", lambda event: on_enter(event, generar))
generar.bind("<Leave>", lambda event: on_leave(event, generar))

busquedaPatron.bind("<Enter>", lambda event: on_enter(event, busquedaPatron))
busquedaPatron.bind("<Leave>", lambda event: on_leave(event, busquedaPatron))


def obtenerParametros():
    texto_video = linkVideo.get()
    patron_id_video = re.compile(r"(\d{18,19})")
    coincidencia = patron_id_video.search(texto_video)
    if coincidencia:
        video_id = coincidencia.group(1)
        messagebox.showinfo("Enlace exitoso", f"Enlace válido. ID del video extraído: {video_id}")
        return video_id
    else:
        if texto_video != "" and texto_video != placeholderVideo:
            messagebox.showerror("Error de Enlace", "El enlace de TikTok no parece ser válido. Se usaran los 10 videos mas populares")
        return ""
#################################################################################################
###                                        PROGRAMA SCRAPPER                                  ###
#################################################################################################       
def obtener_mstoken():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()
        try:
            page.goto(url="https://www.tiktok.com/", timeout=6000)
        except Exception as e:
            message= f"No se pudo navegar. {e}"
            messagebox.showerror("Error MsToken", f"No se pudo navegar por TikTok: {e}")
            browser.close()
            return None

        try:
            cookies = context.cookies()
            for cookie in cookies:
                if cookie["name"] == "msToken":
                    token = cookie
                    mstokenPlano = token["value"]
                    if mstokenPlano:
                        message = "\nSe encontró el token necesario para la automatización"
                        messagebox.showinfo("MsToken exitoso", f"{message}")
                        return mstokenPlano
                    
        except Exception as e:
            message= f"No se pudo obtener el token {e}"
            messagebox.showerror("Error MsToken", f"{message}")
            return None
        finally:
            browser.close()

async def scrapper(ms_token, idt = None):
    lista = []
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "chromium"), headless=False)
        if idt:
            async for comment in api.video(id=idt).comments(count=10):    
                try:
                    if comment.text != None and len(comment.text) < 200:
                        lista.append(comment.as_dict)
                except Exception as e:
                    if "None -> TikTok returned an empty response." in str(e):
                        messagebox.showerror("Error Scrapping", f"{e}")
                        return None
        else:
            async for video in api.trending.videos(count=10):
                try:
                    async for comment in video.comments(count=2):
                        if comment.text != None and len(comment.text) < 200:
                            lista.append(comment.as_dict)    
                except Exception as e:
                    if "None -> TikTok returned an empty response." in str(e):
                        messagebox.showerror("Error Scrapping", f"{e}")
                        return None
        return lista


def extraccionComentarios():
    listaComentarios = []
    texto_video =  obtenerParametros()
    messagebox.showwarning("MsToken", f"Obteniendo msToken de forma automática")
    ms_Token  = obtener_mstoken()
    if ms_Token != None:
        messagebox.showinfo("Información", f"Se abrirá un navegador y se obtendrá los comentarios.\n Durante el proceso no lo cierres porque automáticamente\n se cerrara cuando el proceso finalice. ")
        if texto_video == "":
            try:
                listaComentarios = asyncio.run(scrapper(ms_Token))
                messagebox.showinfo("MsToken", f"Extracción exitosa")
            except Exception as e:
                messagebox.showerror("Scrap Error", f"{e}")
            
        else:
            try:
                listaComentarios = asyncio.run(scrapper(ms_Token, str(texto_video)))  
                messagebox.showinfo("MsToken", f"Extracción exitosa")
            except Exception as e:
                messagebox.showerror("Scrap Error", f"{e}")

        with open("ComentariosConAutor.txt", "w", encoding="utf-8") as archivo:
            for comment in listaComentarios:
                index = str(comment["share_info"]['desc']).rfind(":")
                comentario = str(comment["share_info"]['desc'])[index+1:]
                archivo.write(str(comment["user"]['unique_id'])+": "+comentario+"\n")



from tkinter import Toplevel, Text, Scrollbar, Frame, Button, filedialog, messagebox, LEFT, RIGHT, Y, BOTH

def abrir_ventana_palabras():
    """
    Crea y configura una nueva ventana para editar la lista de palabras de odio.
    (Versión corregida para mostrar todos los widgets)
    """
    # 1. Crear la ventana secundaria (Toplevel)
    ventana_palabras = Toplevel(ventana)
    ventana_palabras.title("Gestionar Palabras de Odio")
    ventana_palabras.geometry("500x400")
    ventana_palabras.minsize(400, 300) # Un tamaño mínimo para que no se deforme
    
    ventana_palabras.transient(ventana)
    ventana_palabras.grab_set()

    frame_botones = Frame(ventana_palabras)
    frame_botones.pack(pady=10, padx=10, fill='x') 

    frame_editor = Frame(ventana_palabras)
    frame_editor.pack(pady=5, padx=10, fill='both', expand=True) 

    scrollbar = Scrollbar(frame_editor)
    scrollbar.pack(side=RIGHT, fill=Y) 

    editor_palabras = Text(
        frame_editor,
        wrap="word",
        font=("Arial", 12),
        yscrollcommand=scrollbar.set 
    )
    editor_palabras.pack(side=LEFT, fill=BOTH, expand=True) 


    scrollbar.config(command=editor_palabras.yview)
    

    btn_cargar = Button(
        frame_botones,
        text="Cargar Palabras",
        command=lambda: cargar_palabras(editor_palabras)
    )
    btn_cargar.pack(side=LEFT, padx=10) 
    btn_guardar = Button(
        frame_botones,
        text="Guardar Cambios",
        command=lambda: guardar_palabras(editor_palabras)
    )
    btn_guardar.pack(side=LEFT, padx=10) 
    
    cargar_palabras(editor_palabras)

def cargar_palabras(editor_widget):

    try:
        with open("Patron.txt", "r", encoding="utf-8") as archivo:
            palabras = archivo.read()
            editor_widget.delete("1.0", "end")
            editor_widget.insert("1.0", palabras)
            messagebox.showinfo("Operación Exitosa", "Palabras cargadas desde Patron.txt")
            print("✅ Palabras cargadas desde Patron.txt")
            
    except FileNotFoundError:
        messagebox.showerror("Error", "\'Patron.txt\' no encontrado. El editor estará vacío.")

def guardar_palabras(editor_widget):
    contenido = editor_widget.get("1.0", "end-1c") 
    try:
        with open("Patron.txt", "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        messagebox.showinfo("Guardado", "La lista de palabras se ha guardado correctamente.")
        
    except Exception as e:
        messagebox.showerror("Error al Guardar", f"No se pudo guardar el archivo.\nError: {e}")


def find_boyer_moore(T, P):
    n, m = len(T), len(P)  # tamaños para T y P

    if m == 0:  # búsqueda de un string vacío
        return 0

    last = {}  # instanciar el diccionario last

    for k in range(m):
        last[P[k]] = k  # en el diccionario la última ocurrencia de cada
                        # elemento en P se sobrescribe

    i = m - 1  # índice en T para empezar la comparación
    k = m - 1  # último índice en P para empezar la comparación

    while i < n:
        if T[i] == P[k]:   # si el carácter hace matching
            if k == 0:
                return i   # hay un match completo y el patrón empieza en el índice i
            else:
                i -= 1     # retroceder: revisar el carácter previo en T y P
                k -= 1     
        else:
            j = last.get(T[i], -1)   # last[T[i]] es -1 si T[i] no es encontrado en el diccionario 
            i += m - min(k, j + 1)   # se calcula i para hacer salto de caracteres 
            k = m - 1                # volver a empezar en el final del patrón 

    return -1

def buscarPatronesOdio():
    patronesDeOdio = []
    with open("Patron.txt", "r", encoding="utf-8") as patrones:
        for patron in patrones:
            index = patron.find("\n")
            if patron[:index] != "":
                patronesDeOdio.append(patron[:index])

    print(patronesDeOdio)
            
    with open("ComentariosConAutor.txt", "r", encoding="utf-8") as comentarios, \
         open("MensajesConOdio.txt", "a", encoding="utf-8") as salida:
        for comentario in comentarios:
            for patron in patronesDeOdio:
                index = find_boyer_moore(comentario, patron)
                if index != -1:
                    print(f"Se encontró un mensaje de odio en el comentario: {comentario}")
                    messagebox.showinfo("Operación Exitosa", f"Se guardo los comentarios con odio en el archivo: MensajesConOdio.txt")
                    salida.write(comentario)




generar.bind("<Button-1>", lambda event: extraccionComentarios())

changeWords.bind("<Button-1>", lambda event: abrir_ventana_palabras())

busquedaPatron.bind("<Button-1>", lambda event: buscarPatronesOdio())

ventana.mainloop()
    


