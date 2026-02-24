import os
import datetime
import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PyPDF2 import PdfReader, PdfWriter
import subprocess
import sys



# ================= CONFIG =================

DEBUG = False

TEMPLATE_PDF = "Vale-Tajonal.pdf"
OUTPUT_DIR = "output"
CONTADOR_FILE = "contador.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

PAGE_WIDTH = 139.7 * mm
PAGE_HEIGHT = 215.9 * mm

COORDS = {
    "no_vale": (317, 530),
    "fecha": (310, 492),

    "empresa": (120, 460),
    "sindicato": (120, 435),
    "permisionario": (160, 410),
    "operador": (130, 386),
    "placas": (120, 362),
    "destino": (120, 339),

    "recibido_nombre": (35, 60),
    "recibido_fecha": (35, 50),
}

MATERIALES = [
    "ARENA", "BASE HI", "BLOCK", "GRAVA",
    "GRAVON", "PIEDRA", "POLVO",
    "SACKCAB", "SELLO", "TRITURADO"
]

CANTIDAD_BASE_X = 74
CANTIDAD_BASE_Y = 281
ROW_HEIGHT = 18

MATERIAL_COORDS = {
    material: (
        CANTIDAD_BASE_X,
        CANTIDAD_BASE_Y - i * ROW_HEIGHT
    )
    for i, material in enumerate(MATERIALES)
}

# ================= CONTADOR =================

def leer_no_vale():
    if not os.path.exists(CONTADOR_FILE):
        with open(CONTADOR_FILE, "w") as f:
            f.write("1")
        return "00001"

    with open(CONTADOR_FILE, "r") as f:
        c = f.read().strip()

    num = int(c) if c.isdigit() else 1
    return str(num).zfill(5)


def incrementar_no_vale():
    if not os.path.exists(CONTADOR_FILE):
        actual = 1
    else:
        with open(CONTADOR_FILE, "r") as f:
            c = f.read().strip()
            actual = int(c) if c.isdigit() else 1

    with open(CONTADOR_FILE, "w") as f:
        f.write(str(actual + 1))


def resetear_no_vale():
    if messagebox.askyesno(
        "Reiniciar contador",
        "¿Deseas reiniciar el número de vale a 00001?\n\nEsta acción no se puede deshacer."
    ):
        with open(CONTADOR_FILE, "w") as f:
            f.write("1")
        actualizar_no_vale()

# ================= PDF =================

def generar_pdf(datos, cantidades):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_pdf = f"{OUTPUT_DIR}/Vale_{datos['no_vale']}_{ts}.pdf"
    overlay_pdf = "overlay_tmp.pdf"

    c = canvas.Canvas(overlay_pdf, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    c.setFont("Helvetica", 10)

    for campo, valor in datos.items():
        if campo in COORDS and valor.strip():
            c.drawString(*COORDS[campo], valor)

    for material, cantidad in cantidades.items():
        if cantidad.strip():
            x, y = MATERIAL_COORDS[material]
            c.drawString(x, y, cantidad)

    c.save()

    base = PdfReader(TEMPLATE_PDF)
    overlay = PdfReader(overlay_pdf)

    writer = PdfWriter()
    page = base.pages[0]
    page.merge_page(overlay.pages[0])
    writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    os.remove(overlay_pdf)
    return output_pdf

# ================= LOGICA =================

def abrir_output():
    path = os.path.abspath(OUTPUT_DIR)
    if sys.platform == "win32":
        os.startfile(path)

def actualizar_no_vale():
    entry_no_vale.config(state="normal")
    entry_no_vale.delete(0, tk.END)
    entry_no_vale.insert(0, leer_no_vale())
    entry_no_vale.config(state="readonly")


def procesar():
    if not messagebox.askyesno(
        "Confirmar generación",
        "¿Deseas generar el vale con los datos actuales?\n\nRevisa la información antes de continuar."
    ):
        return

    datos = {
        "no_vale": entry_no_vale.get(),
        "fecha": entry_fecha.get(),
        "empresa": entry_empresa.get(),
        "sindicato": entry_sindicato.get(),
        "permisionario": entry_permisionario.get(),
        "operador": entry_operador.get(),
        "placas": entry_placas.get(),
        "destino": entry_destino.get(),
        "recibido_nombre": entry_recibido.get(),
        "recibido_fecha": entry_recibido_fecha.get(),
    }

    cantidades = {
        mat: entries_materiales[mat].get()
        for mat in MATERIALES
    }

    pdf = generar_pdf(datos, cantidades)

    incrementar_no_vale()
    actualizar_no_vale()

    messagebox.showinfo("Vale generado", f"PDF creado correctamente:\n{pdf}")

# ================= UI =================

root = tk.Tk()
root.title("Vale Tajonal")
root.minsize(520, 720)

root.columnconfigure(0, weight=1)

main = tk.Frame(root, padx=15, pady=15)
main.grid(sticky="nsew")
main.columnconfigure(0, weight=1)

LABEL_OPTS = {"anchor": "e", "padx": 5, "pady": 4}
ENTRY_OPTS = {"sticky": "ew", "padx": 5, "pady": 4}

# ----- HEADER -----
header = tk.LabelFrame(main, text="Información del Vale", padx=10, pady=10)
header.grid(row=0, column=0, sticky="ew", pady=5)
header.columnconfigure((1, 3), weight=1)

tk.Label(header, text="No. Vale", **LABEL_OPTS).grid(row=0, column=0)
entry_no_vale = tk.Entry(header, state="readonly")
entry_no_vale.grid(row=0, column=1, **ENTRY_OPTS)

tk.Label(header, text="Fecha", **LABEL_OPTS).grid(row=0, column=2)
entry_fecha = tk.Entry(header)
entry_fecha.grid(row=0, column=3, **ENTRY_OPTS)
entry_fecha.insert(0, datetime.date.today().strftime("%d/%m/%Y"))

actualizar_no_vale()

# ----- DATOS -----
datos = tk.LabelFrame(main, text="Datos Generales", padx=10, pady=10)
datos.grid(row=1, column=0, sticky="ew", pady=5)
datos.columnconfigure((1, 3), weight=1)

def campo(parent, text, r, c):
    tk.Label(parent, text=text, **LABEL_OPTS).grid(row=r, column=c)
    e = tk.Entry(parent)
    e.grid(row=r, column=c + 1, **ENTRY_OPTS)
    return e

entry_empresa = campo(datos, "Empresa", 0, 0)
entry_sindicato = campo(datos, "Sindicato", 0, 2)
entry_permisionario = campo(datos, "Permisionario", 1, 0)
entry_operador = campo(datos, "Operador", 1, 2)
entry_placas = campo(datos, "Placas", 2, 0)
entry_destino = campo(datos, "Destino", 2, 2)

# ----- MATERIALES -----
materiales = tk.LabelFrame(main, text="Cantidades por Material", padx=10, pady=10)
materiales.grid(row=2, column=0, sticky="ew", pady=5)
materiales.columnconfigure(1, weight=1)

entries_materiales = {}

for i, mat in enumerate(MATERIALES):
    tk.Label(materiales, text=mat).grid(row=i, column=0, sticky="w", padx=5, pady=3)
    e = tk.Entry(materiales, width=10, justify="center")
    e.grid(row=i, column=1, sticky="w", padx=5, pady=3)
    entries_materiales[mat] = e

# ----- RECIBIDO -----
recibido = tk.LabelFrame(main, text="Recibido", padx=10, pady=10)
recibido.grid(row=3, column=0, sticky="ew", pady=5)
recibido.columnconfigure((1, 3), weight=1)

entry_recibido = campo(recibido, "Nombre", 0, 0)
entry_recibido_fecha = campo(recibido, "Fecha", 0, 2)
entry_recibido_fecha.insert(0, datetime.date.today().strftime("%d/%m/%Y"))

# ----- BOTONES -----
tk.Button(
    main,
    text="GENERAR VALE",
    command=procesar,
    bg="#2c7be5",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    height=2
).grid(row=4, column=0, sticky="ew", pady=10)

tk.Button(
    main,
    text="Reiniciar contador",
    command=resetear_no_vale
).grid(row=5, column=0, pady=5)

tk.Button(
    main,
    text="Ver vales generados",
    command=abrir_output
).grid(row=6, column=0, pady=5)

root.mainloop()