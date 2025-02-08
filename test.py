from itertools import combinations
import csv

# Configuración
total_numbers = 50
choose = 6

# Combinaciones pasadas
past = [
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 7],
    [1, 2, 3, 4, 5, 8],
]

# Lista de números primos entre 1 y 50
prime_numbers = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}

# Generar todas las combinaciones posibles
def generate_combinations(total_numbers, choose):
    return combinations(range(1, total_numbers + 1), choose)

# Función para determinar si un número es primo
# Utilizando una tabla precalculada para mayor eficiencia
def is_prime(num):
    return num in prime_numbers

# Función para determinar si una combinación es "rara"
def is_rare_combination(combo):
    # Regla 1: Todos los números son consecutivos
    if all(combo[i] + 1 == combo[i + 1] for i in range(len(combo) - 1)):
        return True

    # Regla 2: Saltos regulares (diferencia constante entre números)
    differences = [combo[i + 1] - combo[i] for i in range(len(combo) - 1)]
    if len(set(differences)) == 1:
        return True

    # Regla 3: Saltos consecutivos iguales
    if any(differences[i] == differences[i + 1] for i in range(len(differences) - 1)):
        return True

    # Regla 4: Máximo 3 números primos
    prime_count = sum(1 for num in combo if is_prime(num))
    if prime_count > 3:
        return True

    # Regla 5: Al menos un número par
    if not any(num % 2 == 0 for num in combo):
        return True

    # Regla 6: No debe estar en combinaciones pasadas
    if list(combo) in past:
        return True

    return False

# Calcular probabilidades de izquierda a derecha
def calculate_left_scores(combo):
    left_scores = []
    min_values = [1, 2, 3, 4, 5, 6]
    max_values = [45, 46, 47, 48, 49, 50]

    for i, value in enumerate(combo):
        possible_values = max_values[i] - max(min_values[i], combo[i - 1] + 1 if i > 0 else min_values[i]) + 1
        left_scores.append(1 / possible_values)
    return left_scores

# Calcular probabilidades de derecha a izquierda
def calculate_right_scores(combo):
    right_scores = []
    max_values = [50, 49, 48, 47, 46, 45]

    for i in reversed(range(len(combo))):
        possible_values = max(combo[i - 1] + 1 if i > 0 else 1, max_values[i] - combo[i] + 1)
        right_scores.insert(0, 1 / possible_values)

    return right_scores

# Generar archivo CSV con combinaciones válidas y datos
def generate_csv():
    with open('posible.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        header = [
            "id", "b1", "b2", "b3", "b4", "b5", "b6",
            "score_left_b1", "score_left_b2", "score_left_b3", "score_left_b4", "score_left_b5", "score_left_b6",
            "score_r8_b1", "score_r8_b2", "score_r8_b3", "score_r8_b4", "score_r8_b5", "score_r8_b6",
            "score_lr_b1", "score_lr_b2", "score_lr_b3", "score_lr_b4", "score_lr_b5", "score_lr_b6", "score_row"
        ]
        writer.writerow(header)

        for combo in generate_combinations(total_numbers, choose):
            if is_rare_combination(combo):
                continue

            left_scores = calculate_left_scores(combo)
            right_scores = calculate_right_scores(combo)
            lr_scores = [round(left + right, 4) for left, right in zip(left_scores, right_scores)]
            row_score = round(sum(lr_scores), 4)

            row = [
                "".join(map(str, combo)), *combo,
                *[round(score, 4) for score in left_scores],
                *[round(score, 4) for score in right_scores],
                *lr_scores, row_score
            ]
            writer.writerow(row)

# # Ejecutar generación de CSV
# generate_csv()

# # Calcular y mostrar resultados
# rare_count, valid_combinations = filter_combinations()
# total_combinations = len(list(generate_combinations(total_numbers, choose)))

# print(f"Total combinaciones posibles: {total_combinations}")
# print(f"Combinaciones raras excluidas: {rare_count}")
# print(f"Combinaciones restantes: {valid_combinations}")






# Ejecutar generación de CSV
generate_csv()

# Calcular y mostrar resultados
total_combinations = len(list(generate_combinations(total_numbers, choose)))
valid_combinations = 0
rare_count = 0

# Contar combinaciones raras y válidas
for combo in generate_combinations(total_numbers, choose):
    if is_rare_combination(combo):
        rare_count += 1
    else:
        valid_combinations += 1

print(f"Total combinaciones posibles: {total_combinations}")
print(f"Combinaciones raras excluidas: {rare_count}")
print(f"Combinaciones restantes: {valid_combinations}")