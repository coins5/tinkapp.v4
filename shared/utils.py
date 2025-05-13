from typing import List
def formalize_data (bolillas_str: str) -> tuple[str, tuple[int]]:
  arr = bolillas_str.split(" ")
  arr.sort()
  combo = tuple(int(a) for a in arr)
  id = "".join(arr)
  return id, combo

def formalize_data_with_str (bolillas_str: str) -> tuple[str, tuple[int]]:
  arr = bolillas_str.split(" ")
  arr.sort()
  combo = tuple(int(a) for a in arr)
  str_combo = tuple(str(a).zfill(2) for a in combo)
  id = "".join(arr)
  return id, combo, str_combo

def generate_id (bolillas_int: tuple[int]) -> str:
  arr = [str(a).zfill(2) for a in bolillas_int]
  # arr.sort()
  return "".join(arr)