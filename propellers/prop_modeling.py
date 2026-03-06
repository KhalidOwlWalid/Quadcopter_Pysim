import matplotlib.pyplot as plt
import numpy as np
import typing

filename = "datasets/PER3_10x45MR.dat"

class PropellerInfo():

    def __init__(self):
        self._prop_info = dict()

    def request_data(self, prop_rpm: int, key: str):
        return self._prop_info[prop_rpm][key]

with open(filename) as f:

    def dat_file_cleanup(dataset):

        for i, data in enumerate(dataset):
            if data.isspace():
                del dataset[i]

    Propeller = PropellerInfo()

    prop_perf_data = (f.read().splitlines())

    dat_file_cleanup(prop_perf_data)
    
    # Convert the list into numpy array for easier handling
    prop_perf_data = np.array(prop_perf_data)
    prop_rpm_header_loc = np.strings.find(prop_perf_data, "PROP RPM")
    prop_rpm_header_loc = np.where(prop_rpm_header_loc > 0, True, False)
    
    test_dataset = prop_perf_data[15:30]
    prop_rpm_header = int(test_dataset[0].split()[3])

    Propeller._prop_info[prop_rpm_header] = {}

    for i, header_info in enumerate(test_dataset[1].split()):
        Propeller._prop_info[prop_rpm_header][header_info] = np.array([])


    clean_dataset = list()
    for curr_idx in range(3, len(test_dataset), 1):
        clean_dataset.append(test_dataset[curr_idx].split())

    final_dataset = np.array(clean_dataset)

    for i, header_info in enumerate(Propeller._prop_info[prop_rpm_header].keys()):
        Propeller._prop_info[prop_rpm_header][header_info] = final_dataset[:, i]

    print(Propeller._prop_info[prop_rpm_header].keys())

    plt.plot(Propeller.request_data(prop_rpm_header, 'V'), Propeller.request_data(prop_rpm_header, 'Cp'))
    plt.show()

    # for i in range(30 - 18):
    #     offset = 3
    #     curr_idx = i + offset
    #     print(test_dataset[curr_idx])
        # test_dataset[curr_idx] = np.array(test_dataset[curr_idx].split()).T

    # print(test_dataset)

    # print(prop_rpm_header)
