import random




def generate_matrix(m: int, n: int, min_val: int, max_val: int) -> list[list[int]]:
    """Генерує двовимірний масив m x n з випадковими цілими числами."""
    return [[random.randint(min_val, max_val) for _ in range(n)] for _ in range(m)]


def print_matrix(matrix: list[list]) -> None:
    """Виводить матрицю у форматованому вигляді."""
    if not matrix or not matrix[0]:
        print("[Порожня матриця]")
        return

    rows = len(matrix)
    cols = len(matrix[0])

    # Заголовок стовпців
    headers = "\t".join([f"стовпець {j + 1}" for j in range(cols)])
    print(f"\t\t{headers}")

    # Рядки з даними
    for i in range(rows):
        row_str = "\t".join(
            f"{val:.2f}" if isinstance(val, float) else str(val)
            for val in matrix[i]
        )
        print(f"рядок {i + 1}\t{row_str}")


# =========================================================================
# ОСНОВНІ ЗАВДАННЯ
# =========================================================================

def subtract_row_mean(matrix: list[list[int]]) -> list[list[float]]:
    """Завдання 1: Відняти від елементів кожного рядка його середнє арифметичне."""
    result = []
    for row in matrix:
        mean = sum(row) / len(row)
        result.append([round(val - mean, 2) for val in row])
    return result


def cyclic_shift(matrix: list[list[int]], k_right: int, k_up: int) -> list[list[int]]:
    """Завдання 2: Циклічний зсув матриці на k_right вправо та k_up догори."""
    rows = len(matrix)
    cols = len(matrix[0])

    k_right %= cols
    k_up %= rows

    # Ініціалізація порожньої матриці
    shifted = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            new_i = (i - k_up) % rows
            new_j = (j + k_right) % cols
            shifted[new_i][new_j] = matrix[i][j]

    return shifted


def remove_max_rows_cols(matrix: list[list[int]]) -> list[list[int]]:
    """Завдання 3: Видалити всі рядки та стовпці, що містять максимальні елементи."""
    if not matrix or not matrix[0]:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    # 1. Пошук максимального значення
    max_val = max(max(row) for row in matrix)

    # 2. Визначення рядків і стовпців для видалення
    remove_rows = set()
    remove_cols = set()

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == max_val:
                remove_rows.add(i)
                remove_cols.add(j)

    # 3. Формування нової матриці
    new_matrix = []
    for i in range(rows):
        if i in remove_rows:
            continue
        new_row = [matrix[i][j] for j in range(cols) if j not in remove_cols]
        new_matrix.append(new_row)

    return new_matrix


def rotate_90_clockwise_inplace(matrix: list[list[int]]) -> None:
    """Завдання 4: Обертання квадратної матриці на 90° за годинниковою стрілкою in-place."""
    n = len(matrix)

    # Крок 1: Транспонування (заміна matrix[i][j] на matrix[j][i])
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Крок 2: Дзеркальне відображення кожного рядка
    for i in range(n):
        matrix[i].reverse()


# =========================================================================
# ДОДАТКОВЕ ЗАВДАННЯ: ТРИВИМІРНИЙ МАСИВ (РОЗКЛАД)
# =========================================================================

def has_windows(day_schedule: list[str], free_tag: str) -> bool:
    """Визначає, чи є «вікно» між першою та останньою парою дня."""
    class_indices = [i for i, subject in enumerate(day_schedule) if subject != free_tag]
    if len(class_indices) <= 1:
        return False

    # Якщо між першою і останньою парою є порожня позиція
    first, last = class_indices[0], class_indices[-1]
    return any(day_schedule[i] == free_tag for i in range(first, last + 1))


def run_schedule_task():
    days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]
    FREE = "Вільне вікно"

    # Створення масиву [3 groups][5 days][4 classes]
    schedule = [[[FREE for _ in range(4)] for _ in range(5)] for _ in range(3)]

    # Заповнення даними
    # Група 1 (Індекс 0)
    schedule[0][0] = ["Математика", "Фізика", "Програмування", "Історія"]  # 4 пари
    schedule[0][1] = ["Математика", FREE, "Англійська", FREE]  # 2 пари з «вікном»
    schedule[0][2] = [FREE, FREE, "Філософія", FREE]  # 1 пара

    # Група 2 (Індекс 1)
    schedule[1][0] = ["Математика", "Алгоритми", FREE, FREE]  # Потік на 1 парі з Гр1

    target_group = 0

    # 1. День із найбільшим навантаженням для Групи 1
    max_day_idx = max(
        range(5),
        key=lambda d: sum(1 for subject in schedule[target_group][d] if subject != FREE)
    )
    max_count = sum(1 for subject in schedule[target_group][max_day_idx] if subject != FREE)
    print(f"Найбільше навантаження для Групи {target_group + 1}: {days[max_day_idx]} ({max_count} пар/пари)")

    # 2. Пошук днів із «вікнами»
    print(f"Дні з незручним розкладом («вікна») для Групи {target_group + 1}:")
    for d_idx, day_name in enumerate(days):
        if has_windows(schedule[target_group][d_idx], FREE):
            print(f" - {day_name}")

    # 3. Перевірка занять для "потоку"
    print("\nЗаняття для потоків (спільні пари у декількох груп):")
    stream_found = False
    for d in range(5):
        for c in range(4):
            for g1 in range(3):
                for g2 in range(g1 + 1, 3):
                    subj1 = schedule[g1][d][c]
                    subj2 = schedule[g2][d][c]
                    if subj1 != FREE and subj1 == subj2:
                        print(f" - {days[d]}, Пара №{c + 1}: '{subj1}' у Групи {g1 + 1} та Групи {g2 + 1}")
                        stream_found = True
    if not stream_found:
        print(" - Потокових занять не знайдено.")


# =========================================================================
# ГОЛОВНИЙ БЛОК
# =========================================================================

if __name__ == "__main__":
    print("=== 1. ПІДГОТОВКА ТА ДВОВИМІРНІ МАСИВИ ===")
    matrix = generate_matrix(4, 4, 1, 20)
    print("Початкова матриця:")
    print_matrix(matrix)

    print("\n--- Завдання 1: Віднімання середнього арифметичного ---")
    print_matrix(subtract_row_mean(matrix))

    print("\n--- Завдання 2: Циклічний зсув (k=1 вправо, k=1 догори) ---")
    print_matrix(cyclic_shift(matrix, k_right=1, k_up=1))

    print("\n--- Завдання 3: Видалення max елементів ---")
    test_max = [
        [1, 9, 3],
        [4, 2, 9],
        [7, 5, 6]
    ]
    print("До видалення:")
    print_matrix(test_max)
    print("Після видалення:")
    print_matrix(remove_max_rows_cols(test_max))

    print("\n--- Завдання 4: Обертання на 90° in-place ---")
    square = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    rotate_90_clockwise_inplace(square)
    print_matrix(square)

    print("\n=== 2. ДОДАТКОВЕ ЗАВДАННЯ (ТРИВИМІРНИЙ МАСИВ) ===")
    run_schedule_task()