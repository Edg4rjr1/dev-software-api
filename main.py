from estilos.estilos import configurar_tema
from telas.login import TelaLogin

if __name__ == "__main__":
    configurar_tema()
    app = TelaLogin()
    app.mainloop()
