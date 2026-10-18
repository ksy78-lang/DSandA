#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 3. Простые сортировки и QuickSort с рандомизацией — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-03 и правилами использования генеративного ИИ
(docs/ai-verification.md).

Запуск: python lab03-simple-sorts-quicksort-starter.py --variant N
"""
from __future__ import annotations

import argparse
import random
import statistics
import time
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Простые сортировки со счётчиками (сортируют КОПИЮ входа, вход не меняют)
#    Каждая функция возвращает кортеж: (отсортированный список,
#    число сравнений ключей, число обменов/перемещений элементов).
# ---------------------------------------------------------------------------


def bubble_sort(a: list) -> tuple[list, int, int]:
    """Сортировка пузырьком. Ожидаемая сложность: в лучшем O(n), в среднем и худшем O(n^2)."""
    arr = a.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
            
    return arr, comparisons, swaps

def insertion_sort(a: list) -> tuple[list, int, int]:
    """Сортировка вставками. Ожидаемая сложность: лучший O(n), худший O(n^2)."""
    arr = a.copy()
    n = len(arr)
    comparisons = 0
    shifts = 0
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            else:
                break
                
        if j + 1 != i:
            arr[j + 1] = key
            shifts += 1
            
    return arr, comparisons, shifts


def selection_sort(a: list) -> tuple[list, int, int]:
    """Сортировка выбором. Ожидаемая сложность: O(n^2) всегда (ищет минимум по всему остатку)."""
    arr = a.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
                
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
            
    return arr, comparisons, swaps


# ---------------------------------------------------------------------------
# 2. QuickSort с рандомизированным опорным элементом
# ---------------------------------------------------------------------------


def quick_sort(a: list, rng: random.Random | None = None) -> list:
    """QuickSort с выбором опорного через rng.randrange. Возвращает новый список.
    Ожидаемая сложность: в среднем O(n log n), в худшем случае O(n^2).
    """
    if rng is None:
        rng = random.Random()
        
    arr = a.copy()

    def _qs(lo: int, hi: int):
        if lo >= hi:
            return
            
        p_idx = rng.randrange(lo, hi + 1)
        pivot = arr[p_idx]

        arr[p_idx], arr[hi] = arr[hi], arr[p_idx]
        
        i = lo
        for j in range(lo, hi):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                
        arr[i], arr[hi] = arr[hi], arr[i]

        _qs(lo, i - 1)
        _qs(i + 1, hi)

    _qs(0, len(arr) - 1)
    return arr


# ---------------------------------------------------------------------------
# 3. Демонстрация стабильности на парах (ключ, метка)
# ---------------------------------------------------------------------------


def stability_demo() -> None:
    """Показать, какие из четырёх сортировок стабильны."""
    
    class Item:
        def __init__(self, key, label):
            self.key = key
            self.label = label
        def __lt__(self, other): return self.key < other.key
        def __le__(self, other): return self.key <= other.key
        def __gt__(self, other): return self.key > other.key
        def __ge__(self, other): return self.key >= other.key
        def __eq__(self, other): return self.key == other.key
        def __repr__(self): return f"({self.key}, '{self.label}')"

    raw_data = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]
    items = [Item(k, l) for k, l in raw_data]
    
    print("\n--- Демонстрация стабильности ---")
    print(f"Исходный массив: {items}")
    
    print(f"Bubble Sort    : {bubble_sort(items)[0]} (Стабильная)")
    print(f"Insertion Sort : {insertion_sort(items)[0]} (Стабильная)")
    print(f"Selection Sort : {selection_sort(items)[0]} (НЕ стабильная)")
    print(f"QuickSort      : {quick_sort(items, random.Random(0))} (НЕ стабильная)")


# ---------------------------------------------------------------------------
# 4. Классы входов (данные по варианту, детерминированно по seed)
# ---------------------------------------------------------------------------


def make_inputs(n: int, seed: int) -> dict[str, list[int]]:
    """Три класса входов размера n: упорядоченный, случайный, обратный."""
    rng = random.Random(seed + n)  # свой поток для каждого размера
    data = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
    return {
        "упорядоченный": sorted(data),
        "случайный": data,
        "обратный": sorted(data, reverse=True),
    }


# ---------------------------------------------------------------------------
# 5. Верификация (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------

ALGORITHMS = {
    "bubble_sort": lambda a: bubble_sort(a)[0],
    "insertion_sort": lambda a: insertion_sort(a)[0],
    "selection_sort": lambda a: selection_sort(a)[0],
    "quick_sort": lambda a: quick_sort(a, random.Random(0)),
}


def is_sorted(a: list) -> bool:
    """Инвариант 1: неубывающий порядок элементов."""
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def self_check() -> None:
    """Граничные случаи, инварианты сортировки и сверка с эталоном sorted()."""
    boundary = [
        [],                    # пустой массив
        [7],                   # один элемент
        [5, 5, 5, 5],          # все элементы равны
        [1, 2, 3, 4, 5],       # уже отсортирован
        [5, 4, 3, 2, 1],       # обратный порядок
    ]
    for name, fn in ALGORITHMS.items():
        for a in boundary:
            res = fn(list(a))
            assert is_sorted(res), f"{name}: нарушен порядок на {a}"
            assert sorted(res) == sorted(a), f"{name}: не перестановка входа {a}"

    # Сверка с эталоном из стандартной библиотеки на сотнях случайных входов.
    rng = random.Random(0)
    for _ in range(300):
        a = [rng.randint(-100, 100) for _ in range(rng.randint(0, 80))]
        expected = sorted(a)
        for name, fn in ALGORITHMS.items():
            assert fn(list(a)) == expected, f"{name}: расходится с sorted() на {a}"

    # Счётчики: у сортировки выбором ровно n*(n-1)/2 сравнений на любом входе.
    _, comparisons, _ = selection_sort([3, 1, 2, 5, 4])
    assert comparisons == 10, "selection_sort: неверный счётчик сравнений"
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 6. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES_QUADRATIC = [500, 1_000, 2_000, 4_000, 8_000]     # для простых сортировок
SIZES_QUICK = [1_000, 3_000, 10_000, 30_000, 100_000]   # для QuickSort
REPEATS = 5


def bench(fn, data: list) -> float:
    """Медиана времени выполнения fn(копия data) по REPEATS запускам, с прогревом."""
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        arg = list(data)  # свежая копия: сортировка не должна получать свой результат
        t0 = time.perf_counter()
        fn(arg)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    """Замеры всех алгоритмов на трёх классах входов и построение log-log графиков."""
    plans = [
        ("bubble_sort", ALGORITHMS["bubble_sort"], SIZES_QUADRATIC),
        ("insertion_sort", ALGORITHMS["insertion_sort"], SIZES_QUADRATIC),
        ("selection_sort", ALGORITHMS["selection_sort"], SIZES_QUADRATIC),
        ("quick_sort", lambda a: quick_sort(a, random.Random(seed)), SIZES_QUICK),
    ]
    
    # Словарик для хранения времени, чтобы потом нарисовать графики
    plot_data = {
        "упорядоченный": {name: ([], []) for name, _, _ in plans},
        "случайный": {name: ([], []) for name, _, _ in plans},
        "обратный": {name: ([], []) for name, _, _ in plans},
    }

    for name, fn, sizes in plans:
        print(f"\n{name}:")
        for n in sizes:
            for cls, data in make_inputs(n, seed).items():
                t = bench(fn, data)
                print(f"  n={n:>7}  вход={cls:<13} t={t:.6f} c")
                
                # Сохраняем n и t для графика
                plot_data[cls][name][0].append(n)
                plot_data[cls][name][1].append(t)

    # Строим 3 графика рядом (для каждого типа входа)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    classes = ["упорядоченный", "случайный", "обратный"]

    for ax, cls in zip(axes, classes):
        ax.set_title(f"Вход: {cls}")
        ax.set_xlabel("Размер массива n")
        ax.set_ylabel("Время t (сек)")
        
        # Включаем логарифмический масштаб по обеим осям (log-log)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.grid(True, which="both", ls="--", alpha=0.5)

        # Рисуем линии сортировок
        for name, _, _ in plans:
            ns, ts = plot_data[cls][name]
            if ns and ts:
                ax.plot(ns, ts, marker='o', label=name)
                
        ax.legend()

    plt.tight_layout()
    plt.savefig("sorting_graphs.png", dpi=300) # Эта строка сохранит файл в высоком качестве
    plt.show()                                 # А эта по-прежнему выведет окно на экран
    
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    stability_demo()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
