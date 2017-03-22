from SistemaOperativo import SistemaOperativo
import sys

def main():
    sistema = SistemaOperativo(int(sys.argv[1]))
    sistema.crearProcesos()
    sistema.ejecutarProcesos()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("How to use: python __main__.py n_proc")
    else:
        main()
