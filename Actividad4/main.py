from SistemaOperativo import SistemaOperativo
import sys

def main():
    sistema = SistemaOperativo()
    sistema.crearProcesos(int(sys.argv[1]))
    sistema.ejecutarProcesos()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("How to use: python main.py n_proc")
    else:
        main()
