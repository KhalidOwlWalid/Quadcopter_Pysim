import matplotlib.pyplot as plt
import numpy as np
import typing
import matplotlib.pyplot as plt

filename = "propellers/datasets/PER3_10x45MR.dat"

class PropellerInfo():

    def __init__(self, dat_file):
        self._dat_filepath = dat_file
        self._prop_info = dict()

        self._df = open(self._dat_filepath, "r")
        
        self._df = self._df.read().splitlines()
        self._df = np.array(self._df)
        # Clean the dataset from whitespaces
        self._df = self._df[np.char.strip(self._df) != '']

        self.field_keyword_str = {
            "vel_mph": "",
            "adv_ratio": "",
            "pe": "",
            "ct": "",
            "cp": "",
            "pwr_hp": "",
            "torque_inlbf": "",
            "thrust_lbf": "",
            "pwr_w": "",
            "torque_nm": "",
            "thrust_n": "",
            "thr_pwr": "",
            "mach": "",
            "reyn": "",
            "fom": "",
        }

        prop_header_idx = self._find_prop_header()
        for i, rpm_info_idx in enumerate(prop_header_idx):
            # If this is the last prop rpm dataset, then to get the full dataset line number, substract with the total number of lines
            if i == (len(prop_header_idx) - 1):
                self._process_dataset(rpm_info_idx, (len(self._df) - prop_header_idx[i]))
            else:
                self._process_dataset(rpm_info_idx, (prop_header_idx[i + 1] - prop_header_idx[i]))

    def get_all_available_prop_rpm(self):
        return self._prop_info.keys()

    def request_data(self, prop_rpm: int, key: str):
        header_str = self.field_keyword_str[key]
        return self._prop_info[prop_rpm][header_str]

    def request_all_data_header(self):
        # Use on of the prop rpm for getting all of the header keys
        # This should be the same for every prop rpm
        return list(self.field_keyword_str.values())

    def print_all_data_header(self) -> None:
        for keyword, header in self.field_keyword_str.items():
            print(f"{keyword}: {header}")

    def plot_thrust_vs_prop_rpm(self, wind_vel_mph: float) -> None:
        """_summary_

        Args:
            wind_vel (float): _description_
        """
        thrust_interp_dataset = list()
        torque_interp_dataset = list()
        for i, prop_rpm in enumerate(data.get_all_available_prop_rpm()):
            vel_data = data.request_data(prop_rpm, "vel_mph")
            idx = np.searchsorted(vel_data, wind_vel_mph)

            if (idx >= len(vel_data)):
                idx = len(vel_data) - 1

            idx_range = np.array([idx - 1, idx])
            thrust_data = data.request_data(prop_rpm, "thrust_n")[idx_range]
            torque_data = data.request_data(prop_rpm, "torque_nm")[idx_range]
            thrust_interp = np.interp(wind_vel_mph, vel_data[idx_range], thrust_data)
            torque_interp = np.interp(wind_vel_mph, vel_data[idx_range], torque_data)
            thrust_interp_dataset.append(thrust_interp)
            torque_interp_dataset.append(torque_interp)
        
        thrust_interp_dataset = np.array(thrust_interp_dataset)
        torque_interp_dataset = np.array(torque_interp_dataset)

        return thrust_interp_dataset, torque_interp_dataset


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

        prop_data = np.array(prop_rpm_segment[1].split())
        prop_data_unit = np.array(prop_rpm_segment[2].split())

        prop_data = prop_data + ":" + prop_data_unit

        all_field_keyword_keys = list(self.field_keyword_str.keys())
        for i, header_info in enumerate(prop_data):
            self.field_keyword_str[all_field_keyword_keys[i]] = header_info
            self._prop_info[prop_rpm_header][header_info] = np.array([])

        clean_dataset = list()
        for curr_idx in range(3, len(prop_rpm_segment), 1):
            curr_prop_rpm_seg = prop_rpm_segment[curr_idx].split()

            if (len(curr_prop_rpm_seg) != len(prop_data)):
                continue

            clean_dataset.append(prop_rpm_segment[curr_idx].split())

        final_dataset = np.array(clean_dataset)

        for i, header_info in enumerate(self._prop_info[prop_rpm_header].keys()):
            self._prop_info[prop_rpm_header][header_info] = final_dataset[:, i].astype(float, copy=False)

if __name__ == "__main__":
    data = PropellerInfo(filename)
    # data.plot_thrust_vs_prop_rpm(0.38)
    # fig, ax = plt.figure()

    ws_list = np.arange(5.0, 25.0, 5.0)

    for i, wind_speed in enumerate(ws_list):
        thrust_interp, torque_interp = data.plot_thrust_vs_prop_rpm(wind_speed)
        plt.plot(data.get_all_available_prop_rpm(), thrust_interp, label=f"{wind_speed} mph")

    plt.xlabel("Propeller speed (rpm)")
    plt.ylabel("Thrust (N)")
    plt.legend()
    plt.grid()
    plt.show()
