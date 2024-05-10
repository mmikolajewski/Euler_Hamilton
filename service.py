import os
import csv
from datetime import datetime


def appending_data_to_csv(csv_array, sample_type_name, array_size, average_time):
    if sample_type_name == "random_from_csv":
        csv_array.append([array_size * 1000, average_time])
    else:
        csv_array.append([array_size, average_time])
    return csv_array


def appending_data_to_csv2(csv_array, sample_type_name, array_size, times):
    times.sort()
    csv_array.append([array_size, times])
    return csv_array

def create_csv(array_to_save, method_name, sample_type):
    target_directory = "results/"

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    time_now = datetime.now()
    current_time = time_now.strftime("%H_%M_%S")
    time = str(current_time)

    # dodałem licznik czasu. docelowo nie musi być, ale przy testowaniu, pomaga ogarnąć który to plik.
    with open(target_directory + method_name + '_' + sample_type + '_' + time + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(array_to_save)


# W service.py
def save_results_to_csv(results, output_filename):
    try:
        target_directory = "results/"
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        full_path = os.path.join(target_directory, output_filename)
        with open(full_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['File Name', 'Density', 'Euler Cycle Time', 'Hamilton Cycle Time'])
            for result in results:
                writer.writerow([
                    result['file_name'],
                    result['density'],
                    "{:.10f}".format(result['euler_cycle_time']).replace('.', ','),
                    "{:.10f}".format(result['hamilton_cycle_time']).replace('.', ',')
                ])
        print(f"Results successfully saved to {full_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")




def print_info(sample_type_n, size, sort_name, number_of_attempt, executive_time, average_t, sample_name):
    if sample_type_n == "random_from_csv":
        print("sorting for: ", size * 1000, " elements by ", sort_name)
    else:
        print("sorting for: ", size, " elements by: ", sort_name, " sample type: ", sample_name)
    # print("sorted Array", sorted_array)
    print("time of " + str(number_of_attempt) + ":", executive_time)
    print("time without extreme values:", remove_extreme_values(executive_time))
    print("Average Time: %2d of %2d" % (average_t, len(executive_time[1:-1])))
    print("__________________________________________________________________")


# licznik plików w folderze randoms, chciałem go użyć,
# aby niezależnie od ilości plików sobie po nich przeliterował i pobrał w każdej petli 1 plik. Lekki bałagan, ale to była 1 myśl
def count_files_in_random_directory():
    files = os.listdir("randoms/")
    file_count = len(files)
    return file_count


def remove_extreme_values(sample_list):
    temp_list = sample_list.copy()
    temp_list.remove(max(sample_list))
    temp_list.remove(min(sample_list))
    return temp_list


# print(count_files_in_random_directory())
