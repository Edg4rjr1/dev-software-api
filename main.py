from estilos.estilos import configurar_tema
from telas.login import TelaLogin
from banco_setup import criar_banco


if __name__ == "__main__":
    criar_banco()
    configurar_tema()
    app = TelaLogin()
    app.mainloop()
