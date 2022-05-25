import argparse
import sys
import numpy as np
from dto.labeledpolyline_dto import LabeledPolylineDTO
from json_layers import JsonLayer


def start_menu(circuit_zone: str,
               parent_directory: str):
    exit_program = False
    option = 0
    layer = JsonLayer(circuit_zone=circuit_zone,
                      parent_directory=parent_directory)
    layer.generate_json()
    while not exit_program:

        print("1. Añadir Polilyne")
        print("2. Añadir Anomaly")
        print("3. Salir")

        print("Elige una opcion")

        option = getOption()

        if option == 1:
            name = choose_circuit(layer)
            LabeledPol = createLabeledPolyline(name)
            layer.update_data(name, LabeledPol.generateLayersJSON())
        elif option == 2:
            print("Not implemented")
        elif option == 3:
            exit_program = True
        else:
            print("Introduce un numero entre 1 y 3")

    print("Finished")


def createLabeledPolyline(name):
    print("Creando LabeledPolyline para el circuito -> " + name)
    value = input("\tIngrese un nombre para la label: ")
    coords = np.array([
        -435029.019, 4925910.677, 0,
        -436366.272, 4922753.102, 0
    ])
    return LabeledPolylineDTO(id=value, coords=coords)


def getOption():
    correct = False
    num = 0
    while (not correct):
        try:
            num = int(input("Introduce un numero entero: "))
            correct = True
        except ValueError:
            print('Error, introduce un numero entero')

    return num


def choose_circuit(layer):
    arr = layer.get_circuits_name_array()
    for idx, name_circuit in enumerate(arr):
        print("\t" + str(idx) + ": ", name_circuit)

    value = int(input("\tPor favor, ingrese el valor numérico del circuito al que quiere agregarle una label: "))
    return arr[value]


def main(args):
    # example las: pc_model PC_MODEL_NAME -d path/to/las/folder -o path/to/out -l 15 -e 25830 -i -las

    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--out", help="Path to output folder where it create json", default="")
    parser.add_argument('-z', '--circuits_zone',
                        type=str,
                        choices=['NORTE', 'CENTRO', 'NOROESTE', 'CANARIAS'],
                        default='NOROESTE', required=True,
                        help='circuit zone to get')
    # parser.add_argument("-z", "--circuits_zone", help="Path to point class definition file.",
    #                     type=str, default=None)

    args = parser.parse_args(args)  # getting optionals

    if args.out is None:
        parser.print_help()
        sys.exit()

    if args.circuits_zone is None:
        parser.print_help()
        sys.exit()

    start_menu(
        circuit_zone=args.circuits_zone,
        parent_directory=args.out
    )


if __name__ == '__main__':
    main(sys.argv[1:])
