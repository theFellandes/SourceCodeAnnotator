# Coderbyte find intersection question

def find_intersection(str_arr):
  """ Finds the intersection of 2 strings """
  arr_1 = str_arr[0].split(",")
  arr_2 = str_arr[1].split(",")
  intersection_elements = [value.strip(' ') for value in arr_1 if value in arr_2]

  str_arr = convert_to_string(intersection_elements)
  return str_arr

def convert_to_string(list_of_elements: list[int]) -> str:
  """ Returns string from list of elements """
  if not list_of_elements:
    return 'false'

  str_arr = ','.join(list_of_elements)
  return str_arr

# keep this function call here 
print(find_intersection(input()))