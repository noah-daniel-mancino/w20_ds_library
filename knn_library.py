import pandas as pd

def ordered_distances(target_vector:list, crowd_table, answer_column:str, dfunc) -> list:
  assert isinstance(target_vector, list), f'target_vector not a list but instead a {type(target_vector)}'
  assert isinstance(crowd_table, pd.core.frame.DataFrame), f'crowd_table not a dataframe but instead a {type(crowd_table)}'
  assert isinstance(answer_column, str), f'answer_column not a string but instead a {type(answer_column)}'
  assert callable(dfunc), f'dfunc not a function but instead a {type(dfunc)}'
  assert answer_column in crowd_table, f'{answer_column} is not a legit column in crowd_table - check case and spelling'
  crowd_table = crowd_table.drop(answer_column, axis=1) # Would it be bad to 
  distance_list = []                                    # drop in-place instead?
  for index, row in crowd_table.iterrows():
    row_vector = [row[i] for i in range(row.size)]
    distance = dfunc(row_vector, target_vector)
    distance_list.append((index, distance))
  
  distance_list.sort(key = lambda dist_tup: dist_tup[1])
  return distance_list

def knn(target_vector:list, crowd_table, answer_column:str, k:int, dfunc) -> int:
  assert isinstance(target_vector, list), f'target_vector not a list but instead a {type(target_vector)}'
  assert isinstance(crowd_table, pd.core.frame.DataFrame), f'crowd_table not a dataframe but instead a {type(crowd_table)}'
  assert isinstance(answer_column, str), f'answer_column not a string but instead a {type(answer_column)}'
  assert answer_column in crowd_table, f'{answer_column} is not a legit column in crowd_table - check case and spelling'
  assert crowd_table[answer_column].isin([0,1]).all(), f"answer_column must be binary"
  assert callable(dfunc), f'dfunc not a function but instead a {type(dfunc)}'
  polled = ordered_distances(target_vector, crowd_table, answer_column, dfunc)[:k]
  polled_id = [i for i,d in polled]
  print(polled)
  polled_survival = [crowd_table.loc[i, 'label'] for i in polled_id]
  return int(sum(polled_survival)/len(polled_survival) > .5)
  
def knn_tester(test_table, crowd_table, answer_column:str, k:int, dfunc) -> float:
  assert isinstance(test_table, pd.core.frame.DataFrame), f'test_table not a dataframe but instead a {type(test_table)}'
  assert isinstance(crowd_table, pd.core.frame.DataFrame), f'crowd_table not a dataframe but instead a {type(crowd_table)}'
  assert isinstance(answer_column, str), f'answer_column not a string but instead a {type(answer_column)}'
  assert answer_column in crowd_table, f'{answer_column} is not a legit column in crowd_table - check case and spelling'
  assert crowd_table[answer_column].isin([0,1]).all(), f"answer_column must be binary"
  assert callable(dfunc), f'dfunc not a function but instead a {type(dfunc)}'
  possible_points = test_table.shape[0]
  points = 0
  for index, row in test_table.iterrows():
    answer_col_val = row[answer_column]
    row.drop(answer_column, inplace=True)
    target_vector = [row[i] for i in range(row.size)]
    prediction = knn(target_vector, crowd_table, answer_column, k, dfunc)
    match = prediction == answer_col_val
    points += int(match)

  return points/possible_points
  
def knn_confusion(test_table, crowd_table, answer_column, k, dfunc) -> dict:
  assert isinstance(test_table, pd.core.frame.DataFrame), f'test_table not a dataframe but instead a {type(test_table)}'
  assert isinstance(crowd_table, pd.core.frame.DataFrame), f'crowd_table not a dataframe but instead a {type(crowd_table)}'
  assert isinstance(answer_column, str), f'answer_column not a string but instead a {type(answer_column)}'
  assert answer_column in crowd_table, f'{answer_column} is not a legit column in crowd_table - check case and spelling'
  assert crowd_table[answer_column].isin([0,1]).all(), f"answer_column must be binary"
  assert callable(dfunc), f'dfunc not a function but instead a {type(dfunc)}'
  condition_count = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
  for index, row in test_table.iterrows():
    outcome = row[answer_column]
    row.drop(answer_column, inplace=True)
    target_vector = [row[i] for i in range(row.size)]
    prediction = knn(target_vector, crowd_table, answer_column, k, dfunc)
    condition_count[(prediction, outcome)] += 1

  return condition_count
