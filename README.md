# 🧾 Vale Tajonal – Generador de Vouchers en PDF

Aplicación de escritorio desarrollada en **Python** que automatiza la generación de **vales/vouchers en PDF** a partir de una plantilla predefinida, permitiendo el llenado exacto de campos mediante coordenadas y una interfaz gráfica profesional.

El sistema está diseñado para **uso empresarial**, sin dependencias de internet, bases de datos ni servicios externos.

---

## Características principales

- Generación automática de vales en **PDF**
- Posicionamiento preciso de datos mediante coordenadas
- Cantidades por material alineadas a una plantilla existente
- Numeración consecutiva de vales (persistente)
- Opción para reiniciar el contador de vales
- Ventana de confirmación antes de generar el PDF
- Interfaz gráfica elegante, simétrica y responsiva (Tkinter)
- Guardado automático de vales generados
- No requiere conexión a internet
- Aplicación portable (no requiere instalación)

---

## Tecnologías utilizadas

- **Python 3.10+**
- **Tkinter** – Interfaz gráfica
- **ReportLab** – Escritura de texto en PDF
- **PyPDF2** – Manipulación y combinación de PDFs
- **PyInstaller** – Compilación a ejecutable `.exe`

---

## 📂 Estructura del proyecto
ValeTajonal/
  ├── app.py # Código principal
  ├── Vale-Tajonal.pdf # Plantilla base del vale
  ├── contador.txt # (Se genera automáticamente)
  ├── output/ # PDFs generados
  └── dist/
  └── ValeTajonal.exe # Ejecutable final


> ⚠️ El archivo `contador.txt` y la carpeta `output` se crean automáticamente al ejecutar la aplicación.

---

## Uso de la aplicación

1. Ejecutar el programa (`app.py` o `ValeTajonal.exe`)
2. Llenar los datos generales del vale
3. Ingresar las cantidades por material (opcional)
4. Revisar la información
5. Confirmar la generación
6. El PDF se guarda automáticamente en la carpeta `output`

Los vales generados pueden abrirse, imprimirse o compartirse sin necesidad de la aplicación.

---

##  Numeración de vales

- El número de vale:
  - Se incrementa **cada vez que se genera un PDF**
  - Se guarda de forma persistente
  - No se repite
- Incluye un botón para **reiniciar el contador** (con confirmación)

---

## Compilación a ejecutable (.exe)

Instalar PyInstaller:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole app.py

## El ejecutable final se genera en la carpeta:
dist/
## Renombrar:
app.exe → ValeTajonal.exe

#Colocar junto al ejecutable el archivo:
Vale-Tajonal.pdf

## 📄 Licencia
Proyecto de uso privado / empresarial.
No redistribuir sin autorización del autor.
