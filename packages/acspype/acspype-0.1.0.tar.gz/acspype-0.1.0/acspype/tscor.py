import numpy as np
import os
import xarray as xr


class ACSTSCor:
    """
    A class for parsing ACS TS4.cor files and putting them into a format that is easier to work with for larger or
    multiple file datasets.
    """

    def __init__(self, filepath: str) -> None:
        """
        Parse the .cor file and assign data as attributes.

        :param filepath: The filepath of the TS4.cor file.
        """

        self.filepath = os.path.normpath(filepath)
        self.__read_cor()
        self.__parse_lines()


    def __read_cor(self) -> None:
        """
        Read .cor file and store lines as a class attribute.

        :return: None
        """

        with open(self.filepath, 'r') as _file:
            self._lines = _file.readlines()


    def __parse_lines(self) -> None:
        """
        Parse the lines of the .cor file to get correction information.

        :return: None
        """

        wavelengths = []
        psi_t = []
        psi_s_c = []
        psi_s_a = []
        for line in self._lines:
            line_data = line.split('\t')
            line_data = [v.replace('\n', '') for v in line_data]
            line_data = [v.replace(' ', '') for v in line_data]
            if line_data == ['']:
                break
            line_data = [float(v) for v in line_data]
            wavelengths.append(line_data[0])
            psi_t.append(line_data[1])
            psi_s_c.append(line_data[2])
            psi_s_a.append(line_data[3])
        if len(wavelengths) != len(psi_t) != len(psi_s_c) != len(psi_s_a):
            raise ValueError('Mismatch in length of TS4cor file.')
        else:
            self.wavelengths = np.array(wavelengths)
            self.psi_t = np.array(psi_t)
            self.psi_s_c = np.array(psi_s_c)
            self.psi_s_a = np.array(psi_s_a)


    def to_xarray(self) -> xr.Dataset:
        """
        Export class attributes to an xarray dataset.

        :return: An xarray dataset containing correction data.
        """
        ds = xr.Dataset()
        ds = ds.assign_coords({'wavelength': self.wavelengths})
        ds['psi_t'] = (['wavelength'], self.psi_t)
        ds['psi_s_c'] = (['wavelength'], self.psi_s_c)
        ds['psi_s_a'] = (['wavelength'], self.psi_s_a)

        ds.attrs['tscor_data'] = 'Sullivan et al., 2006'
        return ds
