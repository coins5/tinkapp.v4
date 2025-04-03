from dataclasses import dataclass
from enum import Enum
from typing import List

class RARE_REASONS(Enum):
  MAX_PRIMES = 1
  HAVENT_EVENS = 2
  HAVENT_ODDS = 4
  CONSECUTIVES = 8
  HAVENT_N = 16
  


class InnerRandomRules:
  PRIME_NUMBERS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}

@dataclass
class RandomRules (InnerRandomRules):
  # Configuración
  TOTAL_NUMBERS: int
  CHOOSE: int
  MAX_PRIMES: int
  N_VALUES: List[str]

  # Rangos de valores de las bolillas
  MIN_B_VALUES: List[int]
  MAX_B_VALUES: List[int]

  # Función para determinar si un número es primo
  # Utilizando una tabla precalculada para mayor eficiencia
  def is_prime(cls, num: int):
    return num in cls.PRIME_NUMBERS

  # Función para determinar si una combinación es "rara"
  def is_rare_combination(cls, combo: tuple[int], comboid: str) -> tuple[bool, int]:
    reasons = 0

    # Regla 1: Máximo 3 números primos
    prime_count = sum(1 for num in combo if cls.is_prime(num))
    if prime_count > cls.MAX_PRIMES:
      reasons += RARE_REASONS.MAX_PRIMES.value

    # Regla 2: Al menos un número par
    if not any(num % 2 == 0 for num in combo):
      reasons += RARE_REASONS.HAVENT_EVENS.value

    # Regla 3: Al menos un número impar
    if not any(num % 2 == 1 for num in combo):
      reasons += RARE_REASONS.HAVENT_ODDS.value

    # Regla 4: Saltos regulares (diferencia constante entre números)
    differences = [combo[i + 1] - combo[i] for i in range(len(combo) - 1)]
    # if len(set(differences)) == 1:
      # reasons += RARE_REASONS.CONSECUTIVES.value
    if any(differences[i] == differences[i + 1] for i in range(len(differences) - 1)):
      reasons += RARE_REASONS.CONSECUTIVES.value
    
    # Regla 5: Al menos un número de N VALUES en el id
    for nv in cls.N_VALUES:
      if nv not in comboid:
        reasons += RARE_REASONS.HAVENT_N.value
        break

    return reasons > 0, reasons


  # Calcular probabilidades de izquierda a derecha
  def calculate_left_scores(cls, combo):
    left_scores = []

    for i, value in enumerate(combo):
      if i == 0:
        possible_values = combo[i + 1] - 1
      else:
        possible_values = cls.MAX_B_VALUES[i] - (combo[i - 1] + 1) + 1
      
      left_scores.append(1 / possible_values)

    return left_scores

  # Calcular probabilidades de derecha a izquierda
  def calculate_right_scores(cls, combo):
    right_scores = []

    for i, value in enumerate(combo):
      if (i == cls.CHOOSE - 1):
        possible_values = cls.MAX_B_VALUES[i] - (combo[i - 1] + 1) + 1
      else:
        possible_values = (combo[i + 1] - 1) - cls.MIN_B_VALUES[i] + 1
      
      right_scores.append(1 / possible_values)

    return right_scores


  # Calcular los saltos entre valores
  def jumps_map (cls, combo: tuple[int]):
    differences = [combo[i + 1] - combo[i] for i in range(cls.CHOOSE-1)]
    # differences.sort()
    result = "_".join([str.zfill(str(d), 2) for d in differences])
    return result
  
  def unijump (cls, combo: tuple[int]) -> int:
    differences = [combo[i + 1] - combo[i] for i in range(cls.CHOOSE-1)]
    
    while len(differences) > 1:
      result = []
      for i in range(len(differences) - 1):
        result.append(differences[i + 1] - differences[i])
      differences = result
      # print(differences)
    
    return differences[0]
  
  def check_shared_values (cls, left_arr: List[float], right_arr: List[float]):
    shared_values = []
    if (left_arr[0] == right_arr[cls.CHOOSE - 1]):
      shared_values.append(left_arr[0])
    if (left_arr[cls.CHOOSE - 1] == right_arr[0]):
      shared_values.append(left_arr[cls.CHOOSE - 1])

    for i in range(len(left_arr)):
      for j in range(1, len(right_arr) - 1):
        if left_arr[i] == right_arr[j]:
          shared_values.append(left_arr[i])
    return shared_values