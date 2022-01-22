from matplotlib import pyplot
import numpy
import pandas

param_names = {'alpha': 'α', 'beta': 'β', 'gamma': 'γ'}

def get_parameter_grid(parameter, initial_parameters_data_frame):
  """
  Функция, возвращающая сетку значений определённого параметра, встречающегося в объекте pandas.DataFrame.
  @param parameter: str -- строковое имя требующегося параметра.
  @param initial_parameters_data_frame: pandas.DataFrame -- объект, в котором требуется найти значения параметров.
  @return Список из численных значений параметров.
  """
  result = []
  previous_value = initial_parameters_data_frame[0][parameter].item()
  for sample in initial_parameters_data_frame:
    current_value = sample[parameter].item()
    if result and (previous_value == current_value):
      continue
    elif result and (result[0] == current_value):
      break
    else:
      result.append(current_value)
      previous_value = current_value
  return result

def draw_optimal_parameter_plot(parameter, initial_parameters_data_frame, results_data_frame):
  """
  Функция, создающая график зависимости оптимального значения параметра трёхпараметрического замыкания от d и dd.
  @param parameter: str -- строковое имя параметра, для которого требуется построить график.
  @param initial_parameters_data_frame: pandas.DataFrame -- объект, содержащий информацию об исходных параметрах
    для симуляции и численного метода.
  @param results_data_frame: pandas.DataFrame -- объект, содержащий информацию о результатах работы метода поиска
    оптимальных параметров трёхпараметрического замыкания.
  """
  ds = get_parameter_grid('d', initial_parameters_data_frame)
  dds = get_parameter_grid('dd', initial_parameters_data_frame)
  b = get_parameter_grid('b', initial_parameters_data_frame)[0]

  length_of_grid_x = len(ds)
  length_of_grid_y = len(dds)
  count_of_data_frames = length_of_grid_x * length_of_grid_y

  # make data
  X, Y = numpy.meshgrid(numpy.array(ds), numpy.array(dds))

  z_list = list()
  i = 0
  while len(z_list) < length_of_grid_y:
    z_list.append([sample for sample in results_data_frame.loc[i:i+length_of_grid_x-1, 'alpha']])
    i += length_of_grid_x
  for v in z_list:
    while len(v) < length_of_grid_x:
      print('append')
      v.append(0.)

  Z = numpy.array(z_list)

  # plot
  fig, ax = pyplot.subplots()
  pcm = ax.pcolor(X, Y, Z, shading='nearest')

  fig.suptitle(f'Optimal {param_names[parameter]}', fontsize=14, fontweight='bold')
  fig.colorbar(pcm, ax=ax, label=f'Optimal {param_names[parameter]} value')
  ax.set_title(f'b={b}, σ-birth=0.2, σ-death=1.0')
  ax.set_xlabel('d value')
  ax.set_ylabel("d' value")

  pyplot.show()

def draw_population_error_plot(initial_parameters_data_frame, results_data_frame):
  """
  Функция, создающая график зависимости абсолютного значения разности первого момента,
    предсказываемого численным методом с трёхпараметрическим замыканием и оптимальными параметрами для него,
    и первого момента, полученного в результатах симуляции, от d и dd.
  @param initial_parameters_data_frame: pandas.DataFrame -- объект, содержащий информацию об исходных параметрах
    для симуляции и численного метода.
  @param results_data_frame: pandas.DataFrame -- объект, содержащий информацию о результатах работы метода поиска
    оптимальных параметров трёхпараметрического замыкания.
  """
  ds = get_parameter_grid('d', initial_parameters)
  dds = get_parameter_grid('dd', initial_parameters)
  b = get_parameter_grid('b', initial_parameters)[0]

  length_of_grid_x = len(ds)
  length_of_grid_y = len(dds)
  count_of_data_frames = length_of_grid_x * length_of_grid_y

  pyplot.style.use('classic')

  # make data
  X, Y = numpy.meshgrid(numpy.array(ds), numpy.array(dds))

  z_list = list()
  i = 0
  while len(z_list) < length_of_grid_y:
    z_list.append([sample for sample in results.loc[i:i+length_of_grid_x-1, 'pop_error']])
    i += length_of_grid_x
  for v in z_list:
    while len(v) < length_of_grid_x:
      print('append')
      v.append(-100.)

  Z = numpy.array(z_list)

  # plot
  fig, ax = pyplot.subplots()
  pcm = ax.pcolor(X, Y, Z, shading='nearest')

  fig.suptitle(f'Population error', fontsize=14, fontweight='bold')
  fig.colorbar(pcm, ax=ax, label=f'Relative value of difference between populations')
  ax.set_title(f'b={b}, σ-birth=0.2, σ-death=1.0')
  ax.set_xlabel('d value')
  ax.set_ylabel("d' value")

  pyplot.show()

count_of_data_frames_to_show = 30

results = pandas.read_csv('./out_data/result.csv').fillna(method='bfill')
initial_parameters = [
  pandas.read_csv(f'./in_data/simulations_results/initial_parameters/{i}.csv')
  for i in range(1, count_of_data_frames_to_show + 1)
]

def draw_pcf_error_plot(initial_parameters_data_frame, results_data_frame):
  """
  Функция, создающая график зависимости квадрата нормы разности второго момента,
    предсказываемого численным методом с трёхпараметрическим замыканием и оптимальными параметрами для него,
    и первого момента, полученного в результатах симуляции, в L_2 от d и dd.
  @param initial_parameters_data_frame: pandas.DataFrame -- объект, содержащий информацию об исходных параметрах
    для симуляции и численного метода.
  @param results_data_frame: pandas.DataFrame -- объект, содержащий информацию о результатах работы метода поиска
    оптимальных параметров трёхпараметрического замыкания.
  """
  ds = get_parameter_grid('d', initial_parameters)
  dds = get_parameter_grid('dd', initial_parameters)
  b = get_parameter_grid('b', initial_parameters)[0]

  length_of_grid_x = len(ds)
  length_of_grid_y = len(dds)
  count_of_data_frames = length_of_grid_x * length_of_grid_y

  pyplot.style.use('classic')

  # make data
  X, Y = numpy.meshgrid(numpy.array(ds), numpy.array(dds))

  z_list = list()
  i = 0
  while len(z_list) < length_of_grid_y:
    z_list.append([sample for sample in results.loc[i:i+length_of_grid_x-1, 'pcf_error']])
    i += length_of_grid_x
  for v in z_list:
    while len(v) < length_of_grid_x:
      print('append')
      v.append(-100.)

  Z = numpy.array(z_list)

  # plot
  fig, ax = pyplot.subplots()
  pcm = ax.pcolor(X, Y, Z, shading='nearest')

  fig.suptitle(f'PCF error', fontsize=14, fontweight='bold')
  fig.colorbar(pcm, ax=ax, label=f'Relative error of pcf norm')
  ax.set_title(f'b={b}, σ-birth=0.2, σ-death=1.0')
  ax.set_xlabel('d value')
  ax.set_ylabel("d' value")

  pyplot.show()

results = pandas.read_csv('./out_data/result.csv').fillna(method='bfill')
initial_parameters = [
  pandas.read_csv(f'./in_data/simulations_results/initial_parameters/{i}.csv')
  for i in range(1, count_of_data_frames_to_show + 1)
]

draw_optimal_parameter_plot('alpha', initial_parameters, results)
draw_population_error_plot(initial_parameters, results)
draw_pcf_error_plot(initial_parameters, results)
