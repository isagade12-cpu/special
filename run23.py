import os
import subprocess
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new("http://localhost:8501")

if __name__ == "__main__":
    # Abre el navegador automáticamente a los 2 segundos
    Timer(2.0, open_browser).start()
    
    # Ejecuta app23.py usando Streamlit
    subprocess.run(["streamlit", "run", "app23.py"])