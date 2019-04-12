
import urllib.request
from threading import Timer

def func2():
    try:
        archivoDescargar = urllib.request.urlopen("http://mlb-s1-p.mlstatic.com/989292-MLB28693135589_112018-O.jpg", timeout=1)
    except urllib.request.URLError:
        r = Timer(1.0, func2)
        r.start()
        print("Hubo un error")

func2()