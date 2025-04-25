"""Оптимальное вычисление linegraph и vector centrality"""
# Made by TimurPshITMO

from .cpp_functions.convert.line_graph import compute_line_graph_edges
import igraph as ig
import numpy as np


def line_graph(H, s=1, weights=None, max_threads=0):
    """
    Создает линейный граф (line graph) из гиперграфа H.

    Параметры:
    - H: Гиперграф, представленный объектом класса, который содержит методы _edge и edges.
    - s: Минимальное количество общих узлов между гиперребрами для создания ребра в линейном графе.
    - weights: Способ вычисления весов рёбер ('absolute', 'normalized') или None (без весов).
    - max_threads: Максимальное количество потоков для распараллеливания. Если <= 0, используются все доступные потоки.

    Возвращает:
    - LG: Линейный граф, представленный как объект igraph.Graph.
    """
    # Проверяем корректность параметра weights
    if weights not in [None, "absolute", "normalized"]:
        raise ValueError(
            f"{weights} is not a valid weights option. Choices are "
            "None, 'absolute', and 'normalized'."
        )

    # Создаем пустой неориентированный граф
    LG = ig.Graph(directed=False)

    # Извлекаем гиперрёбра из гиперграфа
    hyperedges = list(H._edge.items())

    # Добавляем вершины в линейный граф, соответствующие гиперрёбрам
    LG.add_vertices(len(hyperedges))
    LG.vs["name"] = [k for k, _ in hyperedges]  # Названия вершин (ключи гиперрёбер)
    LG.vs["original_hyperedge"] = [v for _, v in hyperedges]  # Оригинальные множества узлов

    # Преобразуем гиперрёбра в список множеств для передачи в C++ функцию
    hyperedge_sets = [set(e[1]) for e in hyperedges]

    # Вызываем C++ функцию для вычисления рёбер линейного графа
    edges_with_weights = compute_line_graph_edges(
        hyperedge_sets, s, weights if weights else "None", max_threads
    )

    # Извлекаем пары рёбер из результата C++ функции
    edges_pairs = [(e[0], e[1]) for e in edges_with_weights]

    # Добавляем рёбра в линейный граф
    LG.add_edges(edges_pairs)

    # Если указан параметр weights, добавляем веса рёбер
    if weights:
        LG.es["weight"] = [e[2] for e in edges_with_weights]

    return LG


def vector_centrality(H, max_threads=0):
    """
    Вычисляет векторную центральность для узлов гиперграфа H на основе линейного графа.

    Параметры:
    - H: Гиперграф, представленный объектом класса, который содержит методы _edge и edges.
    - max_threads: Максимальное количество потоков для распараллеливания. Если <= 0, используются все доступные потоки.

    Возвращает:
    - vc: Словарь, где ключи — узлы гиперграфа, а значения — списки центральностей для разных размерностей гиперрёбер.
    """
    # Создаем линейный граф из гиперграфа
    LG = line_graph(H, max_threads=max_threads)

    # Вычисляем собственную центральность для линейного графа
    LGcent = LG.eigenvector_centrality(scale=False)

    # Инициализируем словарь для хранения векторной центральности
    vc = {node: [] for node in H.nodes}

    # Создаем словарь для отображения гиперрёбер в индексы
    edge_label_dict = {tuple(sorted(edge)): index for index, edge in H._edge.items()}

    # Создаем словарь для определения размерности каждого гиперребра
    hyperedge_dims = {tuple(sorted(edge)): len(edge) for edge in H.edges.members()}

    # Находим максимальную размерность гиперрёбер
    D = H.edges.size.max()

    # Вычисляем центральность для каждой размерности гиперрёбер
    for k in range(2, D + 1):  # Размерности от 2 до D
        c_i = np.zeros(len(H.nodes))  # Вектор центральности для текущей размерности

        # Фильтруем гиперрёбра по текущей размерности
        for edge, _ in list(filter(lambda x: x[1] == k, hyperedge_dims.items())):
            for node in edge:
                try:
                    # Добавляем центральность гиперребра к узлу
                    c_i[node] += LGcent[edge_label_dict[edge]]
                except IndexError:
                    raise Exception(
                        "Nodes must be written with the Pythonic indexing (0,1,2...)"
                    )

        # Нормализуем центральность на количество узлов в гиперребре
        c_i *= 1 / k

        # Добавляем результаты в словарь векторной центральности
        for node in H.nodes:
            vc[node].append(c_i[node])

    return vc