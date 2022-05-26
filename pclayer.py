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

    while not exit_program:

        print("1. Generar Json para todos los circuitos de " + circuit_zone)
        print("2. Añadir circuito por id de la zona " + circuit_zone)
        print("3. Añadir Polilyne")
        print("4. Añadir nuevo circuito a la escena")
        print("5. Salir")

        print("Elige una opcion")

        option = getOption()

        if option == 1:
            layer.generate_all_json()
        elif option == 2:
            tuple_ids = choose_circuit_name(layer, circuit_zone)
            print(tuple_ids)
            layer.generate_json_by_circuitid(tuple_ids)
        elif option == 3:
            name = choose_circuit(layer)
            if name is not None:
                LabeledPol = createLabeledPolyline(name)
                layer.update_json_labeled_polyline(name, LabeledPol.generateLayersJSON())
        elif option == 4:
            print("Not implemented yet")
        elif option == 5:
            exit_program = True
        else:
            print("Introduce un numero entre 1 y 5")

    print("Finished")


def choose_circuit_name(layer, circuit_zone):
    circuits = layer.get_circuits_by_zone(circuit_zone)
    arr = {}
    for idx, c in enumerate(circuits):
        arr[c.id] = c.mnemonico
        print("\t" + str(c.id) + ": ", c.mnemonico)
    lista = input("Ingrese los id de los circuitos a generar separados por espacios: ").split()
    id_lista = [int(x) for x in lista]
    return tuple(id_lista)


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
    while not correct:
        try:
            num = int(input("Introduce un numero entero: "))
            correct = True
        except ValueError:
            print('Error, introduce un numero entero')

    return num


def choose_circuit(layer):
    arr = layer.get_circuits_name_array()
    if len(arr) > 0:
        for idx, name_circuit in enumerate(arr):
            print("\t" + str(idx) + ": ", name_circuit)

        value = int(input("\tPor favor, ingrese el valor numérico del circuito al que quiere agregarle una label: "))
        return arr[value]
    else:
        return None


def main(args):

    # example: -z NOROESTE -o path/to/out
    # example: -z CANARIAS -o path/to/out

    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--out", help="Path to output folder where it create json", default="")
    parser.add_argument('-z', '--circuits_zone',
                        type=str,
                        choices=['NORTE', 'CENTRO', 'NOROESTE', 'CANARIAS'],
                        default='NOROESTE', required=True,
                        help='circuit zone to get, you can choose either -> NORTE, CENTRO, NOROESTE, CANARIAS')
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
