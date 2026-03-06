import matplotlib.pyplot as plt
import numpy as np
import typing

filename = "datasets/PER3_10x45MR.dat"

class PropellerInfo():

    def __init__(self, dat_file):
        self._dat_filepath = dat_file
        self._prop_info = dict()

        self._df = open(self._dat_filepath, "r")
        
        self._df = self._df.read().splitlines()

        for i, data in enumerate(self._df):
            if data.isspace():
                del self._df[i]

        self._df = np.array(self._df)

        for i, rpm_info_idx in enumerate(self._find_prop_header()):
            # So far, the number of lines for each prop rpm dataset is 15
            self._process_dataset(rpm_info_idx, 15)

    def request_data(self, prop_rpm: int, key: str):
        return self._prop_info[prop_rpm][key]

    def _find_prop_header(self):
        prop_rpm_header_loc = np.strings.find(self._df, "PROP RPM")
        prop_rpm_header_loc = np.where(prop_rpm_header_loc > 0, True, False)
        prop_rpm_header_idx = np.nonzero(prop_rpm_header_loc)
        return prop_rpm_header_idx[0]

    def _process_dataset(self, start_idx: int, n_lines: int):
        prop_rpm_segment = self._df[start_idx:start_idx + n_lines]
        
        # The output of the element that contains "PROP RPM" should look like the following
        # PROP RPM = xxxx
        # In this case, we care about the prop rpm, hence I am simply slicing the bit where it contains the actual
        # rotor speed (e.g. 1000)
        prop_rpm_header = int(prop_rpm_segment[0].split()[3])

        self._prop_info[prop_rpm_header] = {}

        for i, header_info in enumerate(prop_rpm_segment[1].split()):
            self._prop_info[prop_rpm_header][header_info] = np.array([])


        clean_dataset = list()
        for curr_idx in range(3, len(prop_rpm_segment), 1):
            clean_dataset.append(prop_rpm_segment[curr_idx].split())

        final_dataset = np.array(clean_dataset)

        for i, header_info in enumerate(self._prop_info[prop_rpm_header].keys()):
            self._prop_info[prop_rpm_header][header_info] = final_dataset[:, i] 


if __name__ == "__main__":
    data = PropellerInfo(filename)
