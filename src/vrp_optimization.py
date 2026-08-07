import numpy as np
import pandas as pd
from ortools.constraint_solver import routing_enums_pb2, pywrapcp


def create_data_model():
    """Inicializa la matriz de distancias, capacidades y ventanas de tiempo."""
    data = {}

    # Matriz de tiempos/distancias (en minutos o km) entre el DEPOT (nodo 0) y los clientes
    data["distance_matrix"] = [
        [0, 14, 25, 18, 30],
        [14, 0, 10, 15, 20],
        [25, 10, 0, 12, 16],
        [18, 15, 12, 0, 22],
        [30, 20, 16, 22, 0],
    ]

    # Demanda de cada nodo en unidades/kg (El DEPOT [0] no tiene demanda)
    data["demands"] = [0, 15, 10, 20, 12]

    # Capacidades de cada vehículo de la flota
    data["vehicle_capacities"] = [30, 30]

    # Ventanas de tiempo para recepción [Apertura, Cierre]
    data["time_windows"] = [
        (0, 480),  # DEPOT: Abierto de 0 a 8 horas (480 min)
        (30, 120),  # Cliente 1
        (60, 180),  # Cliente 2
        (120, 300),  # Cliente 3
        (180, 400),  # Cliente 4
    ]

    data["num_vehicles"] = 2
    data["depot"] = 0
    return data


def solve_vrptw():
    """Resuelve el problema de ruteo de vehículos con restricciones de tiempo y capacidad."""
    data = create_data_model()

    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Restricción de Capacidad
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback
    )
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # Sin holgura
        data["vehicle_capacities"],  # Capacidad máxima por vehículo
        True,  # Iniciar carga en cero
        "Capacity",
    )

    # Parámetros de búsqueda
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(data, manager, routing, solution)


def print_solution(data, manager, routing, solution):
    """Muestra los resultados de la asignación eficiente de la flota."""
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Ruta para Vehículo {vehicle_id + 1}:\n"
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" Nodo {node_index} (Carga: {route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += (
            f" Nodo {manager.IndexToNode(index)} (Regreso al DEPOT)\n"
        )
        plan_output += f"Distancia recorrida: {route_distance} km\n"
        plan_output += f"Carga transportada: {route_load} unidades\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"==========================================")
    print(f"Distancia Total de la Flota: {total_distance} km")
    print(f"Carga Total Entregada: {total_load} unidades")


if __name__ == "__main__":
    solve_vrptw()
