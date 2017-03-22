from .SistemaOperativo import SistemaOperativo
import sys

def main():
    sistema = SistemaOperativo(int(sys.argv[2]))
    sistema.crearProcesos(int(sys.argv[1]))
    sistema.ejecutarProcesos()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("How to use: python -m Actividad# n_proc quantum")
    else:
        main()
