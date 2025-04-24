#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of CASCADe package
#
# Developed within the ExoplANETS-A H2020 program.
#
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2018  Jeroen Bouwman
"""
JWST Observatory and Instruments specific module of the CASCADe package
"""
import os
import collections
import ast
from types import SimpleNamespace
import numpy as np
import astropy.units as u
from astropy.io import fits
from astropy.convolution import Gaussian2DKernel
from astropy.convolution import Gaussian1DKernel
from astropy.stats import sigma_clipped_stats
from tqdm import tqdm
import pathlib

from ...initialize import cascade_configuration
from ...initialize import cascade_default_data_path
from ...data_model import SpectralDataTimeSeries
from ...utilities import find, get_data_from_fits
from ..InstrumentsBaseClasses import ObservatoryBase, InstrumentBase
from ...spectral_extraction import rebin_to_common_wavelength_grid


__all__ = ['JWST', 'JWSTMIRILRS', 'JWSTNIRISS', 'JWSTNIRSPEC', 'JWSTNIRCAM']


def get_jwst_instrument_setup(configuration, default_data_path):
    """
    Retrieve all relevant parameters defining the instrument and data setup

    Parameters
    ----------
    configuration :
        CASCADe configuration
    default_data_path :
       CASCADe default data path

    Returns
    -------
    par : `collections.OrderedDict`
        Dictionary containg all relevant parameters

    Raises
    ------
    ValueError
        If obseervationla parameters are not or incorrect defined an
        error will be raised
    """
    # instrument parameters
    inst_obs_name = configuration.instrument_observatory
    inst_inst_name = configuration.instrument
    inst_filter = configuration.instrument_filter

    try:
        inst_spec_order = \
            ast.literal_eval(cascade_configuration.instrument_spectral_order)
    except AttributeError:
        inst_spec_order = None

    # object parameters
    obj_period = \
        u.Quantity(configuration.object_period).to(u.day)
    obj_period = obj_period.value
    obj_ephemeris = \
        u.Quantity(configuration.object_ephemeris).to(u.day)
    obj_ephemeris = obj_ephemeris.value

    # observation parameters
    obs_type = configuration.observations_type
    obs_mode = configuration.observations_mode
    obs_data = configuration.observations_data
    obs_path = configuration.observations_path

    if not os.path.isabs(obs_path):
        obs_path = os.path.join(default_data_path, obs_path)

    obs_id = configuration.observations_id

    obs_data_product = configuration.observations_data_product
    obs_target_name = configuration.observations_target_name
    obs_has_backgr = ast.literal_eval(configuration.
                                      observations_has_background)

    #processing
    try:
        proc_extend_roi = cascade_configuration.processing_extend_roi
        proc_extend_roi = ast.literal_eval(proc_extend_roi)
    except AttributeError:
        proc_extend_roi = [1.0, 1.0, 1.0, 1.0]
    # cpm
    try:
        cpm_ncut_first_int = \
           configuration.cpm_ncut_first_integrations
        cpm_ncut_first_int = ast.literal_eval(cpm_ncut_first_int)
    except AttributeError:
        cpm_ncut_first_int = 0
    try:
        cpm_ncut_last_int = \
           configuration.cpm_ncut_last_integrations
        cpm_ncut_last_int = ast.literal_eval(cpm_ncut_last_int)
    except AttributeError:
        cpm_ncut_last_int = -1
    try:
        proc_rebin_time = int(ast.literal_eval(
            cascade_configuration.processing_rebin_number_time_steps))
    except AttributeError:
        proc_rebin_time = 1
    try:
        proc_rebin_factor = ast.literal_eval(
            cascade_configuration.processing_rebin_factor_spectral_channels)
    except AttributeError:
        proc_rebin_factor = 1.0
    try:
       proc_auto_adjust_rebin_factor = ast.literal_eval(
           cascade_configuration.processing_auto_adjust_rebin_factor_spectral_channels)
    except AttributeError:
        proc_auto_adjust_rebin_factor = False


    par = collections.OrderedDict(
        inst_obs_name=inst_obs_name,
        inst_inst_name=inst_inst_name,
        inst_filter=inst_filter,
        inst_spec_order=inst_spec_order,
        obj_period=obj_period,
        obj_ephemeris=obj_ephemeris,
        obs_type=obs_type,
        obs_mode=obs_mode,
        obs_data=obs_data,
        obs_path=obs_path,
        obs_id=obs_id,
        obs_data_product=obs_data_product,
        obs_target_name=obs_target_name,
        obs_has_backgr=obs_has_backgr,
        cpm_ncut_first_int=cpm_ncut_first_int,
        cpm_ncut_last_int=cpm_ncut_last_int,
        proc_extend_roi=proc_extend_roi,
        proc_rebin_time=proc_rebin_time,
        proc_rebin_factor=proc_rebin_factor,
        proc_auto_adjust_rebin_factor=proc_auto_adjust_rebin_factor)

    return par


def create_mask_from_dq(dq_cube, bits_not_to_flag):
    """
    Create mask from DQ cube.

    Parameters
    ----------
    dq_cube : 'ndarray' of 'float'
        DESCRIPTION.
    bits_not_to_flag : 'list'
        Bit values not to flag

    Returns
    -------
    mask : TYPE
        DESCRIPTION.

    Note
    ----
    Standard bit values not to flag are 0, 12 and 14.
    Bit valiue 10 (blobs) is not set by default but can be selected not to
    be flagged in case of problem.
    """
    bits_to_flag = []
    for ibit in range(1, 16):
        if ibit not in bits_not_to_flag:
            bits_to_flag.append(ibit)
    all_flag_values = np.unique(dq_cube)
    bit_select = np.zeros_like(all_flag_values, dtype='int')
    for ibit in bits_to_flag:
        bit_select = bit_select + (all_flag_values & (1 << (ibit - 1)))
    bit_select = bit_select.astype('bool')
    mask = np.zeros_like(dq_cube, dtype='bool')
    for iflag in all_flag_values[bit_select]:
        mask = mask | (dq_cube == iflag)
    return mask


def read_x1dints_files(data_files, bits_not_to_flag, first_integration,
                       last_integration, spectral_order=None):
    """
    Read the jwst pipeline product x1dints.

    Parameters
    ----------
    data_files : 'list'
        List of x1d.first files.
    bits_not_to_flag : 'list'
        Bit numbers not to use when creating boolean mask from DQ data.
    first_integration : 'int'
        Index of first integration to be used in fit of the entiere data set.
    last_integration : 'int'
        Index of last integration to use.

    Returns
    -------
    wavelength_data : TYPE
        DESCRIPTION.
    spectral_data : TYPE
        DESCRIPTION.
    uncertainty_spectral_data : TYPE
        DESCRIPTION.
    time_bjd : TYPE
        DESCRIPTION.
    mask : TYPE
        DESCRIPTION.
    all_data_files : TYPE
        DESCRIPTION.

    """
    time_bjd = []
    wavelength_data = []
    spectral_data = []
    uncertainty_spectral_data = []
    dq = []

    all_data_files = []

    for data_file in data_files:
        with fits.open(data_file) as hdu_list:
            fits_header = hdu_list[0].header
            nints_end = fits_header['INTEND']
            nints_start = fits_header['INTSTART']
            nints = nints_end-nints_start+1
            all_data_files += [data_file]*nints

            time_bjd += list(hdu_list['INT_TIMES'].data['int_mid_BJD_TDB'])
            for hdu in hdu_list:
                if not (hdu.name == 'EXTRACT1D'):
                    continue
                if spectral_order is not None:
                    if int(hdu.header['SPORDER']) != spectral_order:
                        continue
                idx = np.argsort(hdu.data['WAVELENGTH'])
                wavelength_data.append(hdu.data['WAVELENGTH'][idx])
                spectral_data.append(hdu.data['FLUX'][idx])
                uncertainty_spectral_data.append(hdu.data['FLUX_ERROR'][idx])
                dq.append(hdu.data['DQ'][idx])

    wavelength_data = np.array(wavelength_data, dtype=float).T
    spectral_data = np.array(spectral_data, dtype=float).T
    uncertainty_spectral_data = np.array(uncertainty_spectral_data, dtype=float).T
    dq = np.array(dq, dtype=int).T
    time_bjd = np.array(time_bjd, dtype=float)
    mask = np.ma.masked_invalid(spectral_data).mask
    mask = mask | create_mask_from_dq(dq, bits_not_to_flag)

    idx = np.argsort(time_bjd)[first_integration:last_integration]
    time_bjd = time_bjd[idx]
    spectral_data = spectral_data[:, idx]
    uncertainty_spectral_data = uncertainty_spectral_data[:, idx]
    wavelength_data = wavelength_data[:, idx]
    mask = mask[:, idx]
    all_data_files = [all_data_files[i] for i in idx]

    return (wavelength_data, spectral_data, uncertainty_spectral_data,
            time_bjd, mask, all_data_files)

def read_position_file(data_file, first_integration, last_integration):
    """
    Read file containing position info of spectral source in time.

    Parameters
    ----------
    data_file : 'str'
        Name of file containing position info.
    first_integration : 'int'
        Index of first integration to be used in fit of the entiere data set.
    last_integration : 'int'
        Index of last integration to use.

    Returns
    -------
    'dict'
        Dictionary containing position information.

    """
    position_list = ["POSITION", "TIME_BJD", "DISP_POS", "ANGLE", "SCALE"]
    header_list = ["MEDPOS", "MPUNIT", "PUNIT","DPUNIT", "AUNIT", "SUNIT"]

    if pathlib.Path(data_file).is_file:
        position_dict = {}
        with fits.open(data_file) as hdu_list:

            for key in header_list:
                try:
                    value = hdu_list['PRIMARY'].header[key]
                    position_dict[key] = value
                except:
                    pass
            for key in position_list:
                try:
                    value = hdu_list[1].data[key]
                    position_dict[key] = value[first_integration:last_integration]
                except:
                    pass
        return position_dict
    else:
        return {}


def read_FWHM_file(data_file, first_integration, last_integration):
    """
    Read file containing position info of FWHM of the disperced light in time.

    Parameters
    ----------
    data_file : 'str'
        Name of file containing position info.
    first_integration : 'int'
        Index of first integration to be used in fit of the entiere data set.
    last_integration : 'int'
        Index of last integration to use.

    Returns
    -------
    'dict'
        Dictionary continging FWHM info.

    """
    position_list = ["FWHM", "TIME_BJD"]
    header_list = ['MEDFWHM']

    if pathlib.Path(data_file).is_file:
        position_dict = {}
        with fits.open(data_file) as hdu_list:

            for key in header_list:
                try:
                    value = hdu_list['PRIMARY'].header[key]
                    position_dict[key] = value
                except:
                    pass
            for key in position_list:
                try:
                    value = hdu_list[1].data[key]
                    position_dict[key] = value[first_integration:last_integration]
                except:
                    pass
        return position_dict
    else:
        return {}


class JWST(ObservatoryBase):
    """
    This observatory class defines the instuments and data handling for the
    spectropgraphs of JWST
    """

    def __init__(self):
        # check if cascade is initialized
        if cascade_configuration.isInitialized:
            # check if model is implemented and pick model
            if (cascade_configuration.instrument in
                self.observatory_instruments.keys()):
                factory = self.observatory_instruments[cascade_configuration.instrument]()
                cascade_configuration.telescope_collecting_area = \
                    self.collecting_area
                self.par = factory.par
                self.data = factory.data
                self.spectral_trace = factory.spectral_trace
                if self.par['obs_has_backgr']:
                    self.data_background = factory.data_background
                self.instrument = factory.name
                self.instrument_calibration = \
                    factory.instrument_calibration
                cascade_configuration.instrument_dispersion_scale = \
                     factory.dispersion_scale
            else:
                raise ValueError("JWST instrument not recognized, \
                                 check your init file for the following \
                                 valid instruments: {}. Aborting loading \
                                 instrument".format((self.observatory_instruments).key()))
        else:
            raise ValueError("CASCADe not initialized, \
                                 aborting loading Observatory")

    @property
    def name(self):
        """Set to 'JWST'"""
        return "JWST"

    @property
    def location(self):
        """Set to 'SPACE'"""
        return "SPACE"

    @property
    def collecting_area(self):
        """
        Size of the collecting area of the telescope.

        Returns
        -------
        25.4 m**2
        """
        return '25.40 m2'

    @property
    def NAIF_ID(self):
        """Set to -170 for JWST"""
        return -170

    @property
    def observatory_instruments(self):
        """Returns {'MIRILRS', 'NIRSPECBOTS'}"""
        return {"MIRILRS":JWSTMIRILRS, "NIRSPECBOTS":JWSTNIRSPEC,
                "NIRISSSOSS":JWSTNIRISS, "NIRCAMLW":JWSTNIRCAM}


class JWSTMIRILRS(InstrumentBase):
    """
    JWST MIRI low resolution spectrograph  class.

    This instrument class defines the properties for the LRS spectrograph,
    which is part of the MIRI intrument of JWST.

    For the instrument and observations the following valid options are
    available:

       - data type : {'SPECTRUM'}
       - observing strategy : {'STARING'}
    """

    __valid_data = {'SPECTRUM'}
    __valid_observing_strategy = {'STARING'}

    def __init__(self):
        self.par = self.get_instrument_setup()
        if self.par['obs_has_backgr']:
            self.data, self.data_background = self.load_data()
        else:
            self.data = self.load_data()
        self.spectral_trace = self.get_spectral_trace()
        self._define_region_of_interest()
        try:
            self.instrument_calibration = self.mirilrs_cal
        except AttributeError:
            self.instrument_calibration = None

    @property
    def name(self):
        """
        Name of the JWST instrument: 'MIRILRS'
        """
        return "MIRILRS"

    @property
    def dispersion_scale(self):
        __all_scales = {'P750L': '343.247 Angstrom'}
        return __all_scales[self.par["inst_filter"]]

    @property
    def detector_gain(self):
        """
        Detector gain of the miri detectors.

        Returns
        -------
        4.0 * u.electron / u.DN
        """
        return 4.0 * u.electron / u.DN


    def load_data(self):
        """
        Load the observations.

        This function loads the JWST/MIRI/LRS data form disk based on the
        parameters defined during the initialization of the TSO object.
        """
        if self.par["obs_data"] == 'SPECTRUM':
            data = self.get_spectra()
            if self.par['obs_has_backgr']:
                data_back = self.get_spectra(is_background=True)
        else:
            raise ValueError("The MIRI/LRS insrtrument can currently only be "
                             "used with the observational data parameter "
                             f"set to {self.__valid_data}")
        if self.par['obs_has_backgr']:
            return data, data_back
        else:
            return data

    def get_instrument_setup(self):
        """
        Retrieve all relevant parameters defining the instrument and data setup

        Returns
        -------
        par : `collections.OrderedDict`
            Dictionary containg all relevant parameters

        Raises
        ------
        ValueError
            If obseervationla parameters are not or incorrect defined an
            error will be raised
        """
        par = get_jwst_instrument_setup(cascade_configuration,
                                        cascade_default_data_path)

        return par

    def get_spectra(self, is_background=False):
        """
        Read the input spectra.

        This function combines all functionallity to read fits files
        containing the (uncalibrated) spectral timeseries, including
        orbital phase and wavelength information

        Parameters
        ----------
        is_background : `bool`
            if `True` the data represents an observaton of the IR background
            to be subtracted of the data of the transit spectroscopy target.

        Returns
        -------
        SpectralTimeSeries : `cascade.data_model.SpectralDataTimeSeries`
            Instance of `SpectralDataTimeSeries` containing all spectroscopic
            data including uncertainties, time, wavelength and bad pixel mask.

        Raises
        ------
        AssertionError, KeyError
            Raises an error if no data is found or if certain expected
            fits keywords are not present in the data files.
        """
        # get data files
        if is_background:
            # obsid = self.par['obs_backgr_id']
            target_name = self.par['obs_backgr_target_name']
        else:
            # obsid = self.par['obs_id']
            target_name = self.par['obs_target_name']

        path_to_files = os.path.join(self.par['obs_path'],
                                     self.par['inst_obs_name'],
                                     self.par['inst_inst_name'],
                                     target_name,
                                     'SPECTRA/')

        data_files = find('*' + self.par['obs_id'] + '*' +
                          self.par['obs_data_product']+'.fits',
                          path_to_files)

        # number of integrations
        nintegrations = len(data_files)
        if nintegrations < 1:
            raise AssertionError("No Timeseries data found in dir " +
                                 path_to_files)

        bits_not_to_flag = []
        (wavelength_data, spectral_data, uncertainty_spectral_data, time_bjd,
         mask, all_data_files) = \
            read_x1dints_files(data_files, bits_not_to_flag,
                               self.par["cpm_ncut_first_int"],
                               self.par["cpm_ncut_last_int"])

        # positon info
        position_file = find('target_trace_position.fits', path_to_files)
        if len(position_file) == 0:
            position = np.ones((len(time_bjd)))
            position_unit = u.pix
            median_position = np.median(position)
        else:
            position_dict = read_position_file(position_file[0],
                                      self.par["cpm_ncut_first_int"],
                                      self.par["cpm_ncut_last_int"])
            position = position_dict['POSITION']
            try:
                median_position = position_dict['MEDPOS']
            except:
                median_position = np.median(position)
                position = position - median_position
            try:
                position_unit =  position_dict['PUNIT']
            except:
                position_unit = u.pix

        # FWHM info
        fwhm_file = find('target_FWHM.fits', path_to_files)
        if len(fwhm_file) == 0:
            fwhm = np.ones((len(time_bjd)))
            fwhm_unit = u.pix
            median_fwhm = np.median(fwhm)
        else:
            fwhm_dict = read_FWHM_file(fwhm_file[0],
                                      self.par["cpm_ncut_first_int"],
                                      self.par["cpm_ncut_last_int"])
            fwhm = fwhm_dict['FWHM']
            try:
                median_fwhm = fwhm_dict['MEDFWHM']
            except:
                median_fwhm = np.median(fwhm)
                fwhm = fwhm - median_fwhm
            try:
                fwhm_unit =  fwhm_dict['FWHMUNIT']
            except:
                fwhm_unit = u.pix


        # orbital phase
        phase = ((time_bjd+2400000.5 - self.par['obj_ephemeris']) /
                 self.par['obj_period'])
        phase = phase - int(np.max(phase))
# BUG FIX
        #if np.max(phase) < 0.0:
        #    phase = phase + 1.0
        #phase = phase - np.rint(phase)
        #if self.par['obs_type'] == 'ECLIPSE':
        #    phase[phase < 0] = phase[phase < 0] + 1.0

        detector_gain = self.detector_gain

        scaling = (wavelength_data/7.5)**4
        scaling_unit = u.dimensionless_unscaled
        spectral_data *= detector_gain.value * scaling
        uncertainty_spectral_data *= detector_gain.value * scaling

        wave_unit = u.micron
        flux_unit = u.electron / u.s

        SpectralTimeSeries = \
            SpectralDataTimeSeries(
                                   wavelength=wavelength_data,
                                   wavelength_unit=wave_unit,
                                   data=spectral_data.data,
                                   data_unit=flux_unit,
                                   uncertainty=uncertainty_spectral_data,
                                   time=phase,
                                   time_unit=u.dimensionless_unscaled,
                                   mask=mask,
                                   time_bjd=time_bjd,
                                   position=position,
                                   position_unit=position_unit,
                                   fwhm=fwhm,
                                   fwhm_unit=fwhm_unit,
                                   scaling=scaling,
                                   scaling_unit=scaling_unit,
                                   isRampFitted=True,
                                   isNodded=False,
                                   target_name=target_name,
                                   dataProduct=self.par['obs_data_product'],
                                   dataFiles=all_data_files
                                   )

        # make sure that the date units are as "standard" as posible
        data_unit = (1.0*SpectralTimeSeries.data_unit).decompose().unit
        SpectralTimeSeries.data_unit = data_unit
        wave_unit = (1.0*SpectralTimeSeries.wavelength_unit).decompose().unit
        SpectralTimeSeries.wavelength_unit = wave_unit

        # To make the as standard as posible, by defaut change to
        # mean nomalized data units and use micron as wavelength unit
        mean_signal, _, _ = \
            sigma_clipped_stats(SpectralTimeSeries.return_masked_array("data"),
                                sigma=3, maxiters=10)
        data_unit = u.Unit(mean_signal*SpectralTimeSeries.data_unit)
        SpectralTimeSeries.data_unit = data_unit
        SpectralTimeSeries.wavelength_unit = u.micron

        SpectralTimeSeries.period = self.par['obj_period']
        SpectralTimeSeries.ephemeris = self.par['obj_ephemeris']

        # # rebin in time
        # if self.par['proc_rebin_time'] != 1:
        #     scanDict = {}
        #     idx_scandir = np.ones(spectral_data.shape[-1], dtype=bool)
        #     scanDict[0] = \
        #             {'nsamples': self.par['proc_rebin_time'],
        #              'nscans': sum(idx_scandir),
        #              'index': idx_scandir}

        #     from cascade.spectral_extraction import combine_scan_samples
        #     SpectralTimeSeries = \
        #         combine_scan_samples(SpectralTimeSeries,
        #                              scanDict, verbose=False)

        # # rebin spectra
        # if self.par['proc_auto_adjust_rebin_factor']:
        #     nrebin =  (spectral_data.shape[0]+10) / spectral_data.shape[1]
        # else:
        #     nrebin=self.par['proc_rebin_factor']
        # if nrebin > 1.0:
        #     SpectralTimeSeries = \
        #         rebin_to_common_wavelength_grid(SpectralTimeSeries, 0,
        #                                         nrebin=nrebin, verbose=False,
        #                                         verboseSaveFile=None)

        self._define_convolution_kernel()

        return SpectralTimeSeries


    def get_spectral_trace(self):
        """Get spectral trace."""
        dim = self.data.data.shape
        wave_pixel_grid = np.arange(dim[0]) * u.pix
        position_pixel_grid = np.zeros_like(wave_pixel_grid)
        spectral_trace = \
            collections.OrderedDict(wavelength_pixel=wave_pixel_grid,
                                    positional_pixel=position_pixel_grid,
                                    wavelength=self.data.wavelength.
                                    data[:, 0])
        return spectral_trace

    def _define_region_of_interest(self):
        """
        Defines region on detector which containes the intended target star.
        """
        dim = self.data.data.shape

        wavelength_min = \
            self.par['proc_extend_roi'][0]*4.4*u.micron
        wavelength_max = \
            self.par['proc_extend_roi'][1]*12.5*u.micron

        trace = self.spectral_trace.copy()
        mask_min = trace['wavelength'] > wavelength_min
        mask_max = trace['wavelength'] < wavelength_max
        mask_not_defined = trace['wavelength'] == 0.
        idx_min = int(np.min(trace['wavelength_pixel'].value[mask_min]))
        idx_max = int(np.max(trace['wavelength_pixel'].value[mask_max]))
        roi = np.zeros((dim[0]), dtype=bool)
        roi[0:idx_min] = True
        roi[idx_max+1:] = True
        roi[mask_not_defined] = True

        try:
            self.mirilrs_cal
        except AttributeError:
            self.mirilrs_cal = SimpleNamespace()
        finally:
            self.mirilrs_cal.roi = roi
        return

    def _define_convolution_kernel(self):
        """
        Define convolution kernel.

        Define the instrument specific convolution kernel which will be used
        in the correction procedure of bad pixels.
        """
        if self.par["obs_data"] == 'SPECTRUM':
            kernel = Gaussian1DKernel(4.0, x_size=19)
        else:
            kernel = Gaussian2DKernel(x_stddev=0.2, y_stddev=4.0,
                                      theta=-0.0092, x_size=5, y_size=19)
        try:
            self.mirilrs_cal
        except AttributeError:
            self.mirilrs_cal = SimpleNamespace()
        finally:
            self.mirilrs_cal.convolution_kernel = kernel
        return


class JWSTNIRSPEC(InstrumentBase):
    """
    NIRSPEC instrument module.

    This instrument class defines the properties for the NIRSPEC intrument
    of JWST.

    For the instrument and observations the following valid options are
    available:

       - data type : {'SPECTRUM'}
       - observing strategy : {'STARING'}
    """
    __valid_data = {'SPECTRUM'}
    __valid_observing_strategy = {'STARING'}

    def __init__(self):
        self.par = self.get_instrument_setup()
        if self.par['obs_has_backgr']:
            self.data, self.data_background = self.load_data()
        else:
            self.data = self.load_data()
        self.spectral_trace = self.get_spectral_trace()
        self._define_region_of_interest()
        try:
            self.instrument_calibration = self.nirspecbots_cal
        except AttributeError:
            self.instrument_calibration = None

    @property
    def name(self):
        """
        Name of the JWST instrument: 'NIRSPECBOTS'
        """
        return "NIRSPECBOTS"

    @property
    def dispersion_scale(self):
        __all_scales = {'PRISM-CLEAR': '121.3 Angstrom',
                        'G395M-F290LP': '17.4 Angstrom'}
        return __all_scales[self.par["inst_filter"]]


    @property
    def detector_gain(self):
        """
        Detector gain of the miri detectors.

        Returns
        -------
        0.996 * u.electron / u.DN
        """
        return 0.996 * u.electron / u.DN

    def load_data(self):
        """
        Load the observations.

        This function loads the NIRSPEC BOTS data form disk based on the
        parameters defined during the initialization of the TSO object.
        """
        if self.par["obs_data"] == 'SPECTRUM':
            data = self.get_spectra()
            if self.par['obs_has_backgr']:
                data_back = self.get_spectra(is_background=True)
        else:
            raise ValueError("The NIRSPEC insrtrument can currently only be "
                             "used with the observational data parameter "
                             f"set to {self.__valid_data}")
        if self.par['obs_has_backgr']:
            return data, data_back
        else:
            return data

    def get_instrument_setup(self):
        """
        Retrieve all relevant parameters defining the instrument and data setup

        Returns
        -------
        par : `collections.OrderedDict`
            Dictionary containg all relevant parameters

        Raises
        ------
        ValueError
            If obseervationla parameters are not or incorrect defined an
            error will be raised
        """
        par = get_jwst_instrument_setup(cascade_configuration,
                                        cascade_default_data_path)

        return par

    def get_spectra(self, is_background=False):
        """
        Read the input spectra.

        This function combines all functionallity to read fits files
        containing the (uncalibrated) spectral timeseries, including
        orbital phase and wavelength information

        Parameters
        ----------
        is_background : `bool`
            if `True` the data represents an observaton of the IR background
            to be subtracted of the data of the transit spectroscopy target.

        Returns
        -------
        SpectralTimeSeries : `cascade.data_model.SpectralDataTimeSeries`
            Instance of `SpectralDataTimeSeries` containing all spectroscopic
            data including uncertainties, time, wavelength and bad pixel mask.

        Raises
        ------
        AssertionError, KeyError
            Raises an error if no data is found or if certain expected
            fits keywords are not present in the data files.
        """
        # get data files
        if is_background:
            # obsid = self.par['obs_backgr_id']
            target_name = self.par['obs_backgr_target_name']
        else:
            # obsid = self.par['obs_id']
            target_name = self.par['obs_target_name']

        path_to_files = os.path.join(self.par['obs_path'],
                                     self.par['inst_obs_name'],
                                     self.par['inst_inst_name'],
                                     target_name,
                                     'SPECTRA/')

        data_files = find('*' + self.par['obs_id'] + '*' +
                          self.par['obs_data_product']+'.fits',
                          path_to_files)

        # number of integrations
        nintegrations = len(data_files)
        if nintegrations < 1:
            raise AssertionError("No Timeseries data found in dir " +
                                 path_to_files)

        bits_not_to_flag = []
        (wavelength_data, spectral_data, uncertainty_spectral_data, time_bjd,
         mask, all_data_files) = \
            read_x1dints_files(data_files, bits_not_to_flag,
                               self.par["cpm_ncut_first_int"],
                               self.par["cpm_ncut_last_int"])

        # positon info
        position_file = find('target_trace_position.fits', path_to_files)
        if len(position_file) == 0:
            position = np.ones((len(time_bjd)))
            position_unit = u.pix
            median_position = np.median(position)
        else:
            position_dict = read_position_file(position_file[0],
                                      self.par["cpm_ncut_first_int"],
                                      self.par["cpm_ncut_last_int"])
            position = position_dict['POSITION']
            try:
                median_position = position_dict['MEDPOS']
            except:
                median_position = np.median(position)
                position = position - median_position
            try:
                position_unit =  position_dict['PUNIT']
            except:
                position_unit = u.pix

        # FWHM info
        fwhm_file = find('target_FWHM.fits', path_to_files)
        if len(fwhm_file) == 0:
            fwhm = np.ones((len(time_bjd)))
            fwhm_unit = u.pix
            median_fwhm = np.median(fwhm)
        else:
            fwhm_dict = read_FWHM_file(fwhm_file[0],
                                      self.par["cpm_ncut_first_int"],
                                      self.par["cpm_ncut_last_int"])
            fwhm = fwhm_dict['FWHM']
            try:
                median_fwhm = fwhm_dict['MEDFWHM']
            except:
                median_fwhm = np.median(fwhm)
                fwhm = fwhm - median_fwhm
            try:
                fwhm_unit =  fwhm_dict['FWHMUNIT']
            except:
                fwhm_unit = u.pix

        # orbital phase
        phase = ((time_bjd+2400000.5 - self.par['obj_ephemeris']) /
                 self.par['obj_period'])
        phase = phase - int(np.max(phase))
#        if np.max(phase) < 0.0:
#            phase = phase + 1.0
#        phase = phase - np.rint(phase)
#        if self.par['obs_type'] == 'ECLIPSE':
#            phase[phase < 0] = phase[phase < 0] + 1.0

        detector_gain = self.detector_gain

        scaling = (wavelength_data/3.0)**4
        scaling_unit = u.dimensionless_unscaled
        spectral_data *= detector_gain.value * scaling
        uncertainty_spectral_data *= detector_gain.value * scaling

        wave_unit = u.micron
        flux_unit = u.electron / u.s

        SpectralTimeSeries = \
            SpectralDataTimeSeries(
                                   wavelength=wavelength_data,
                                   wavelength_unit=wave_unit,
                                   data=spectral_data.data,
                                   data_unit=flux_unit,
                                   uncertainty=uncertainty_spectral_data,
                                   time=phase,
                                   time_unit=u.dimensionless_unscaled,
                                   mask=mask,
                                   time_bjd=time_bjd,
                                   position=position,
                                   position_unit=position_unit,
                                   fwhm=fwhm,
                                   fwhm_unit=fwhm_unit,
                                   scaling=scaling,
                                   scaling_unit=scaling_unit,
                                   isRampFitted=True,
                                   isNodded=False,
                                   target_name=target_name,
                                   dataProduct=self.par['obs_data_product'],
                                   dataFiles=all_data_files
                                   )

        # make sure that the date units are as "standard" as posible
        data_unit = (1.0*SpectralTimeSeries.data_unit).decompose().unit
        SpectralTimeSeries.data_unit = data_unit
        wave_unit = (1.0*SpectralTimeSeries.wavelength_unit).decompose().unit
        SpectralTimeSeries.wavelength_unit = wave_unit

        # To make the as standard as posible, by defaut change to
        # mean nomalized data units and use micron as wavelength unit
        mean_signal, _, _ = \
            sigma_clipped_stats(SpectralTimeSeries.return_masked_array("data"),
                                sigma=3, maxiters=10)
        data_unit = u.Unit(mean_signal*SpectralTimeSeries.data_unit)
        SpectralTimeSeries.data_unit = data_unit
        SpectralTimeSeries.wavelength_unit = u.micron

        SpectralTimeSeries.period = self.par['obj_period']
        SpectralTimeSeries.ephemeris = self.par['obj_ephemeris']

        # # rebin in time
        # if self.par['proc_rebin_time'] != 1:
        #     scanDict = {}
        #     idx_scandir = np.ones(spectral_data.shape[-1], dtype=bool)
        #     scanDict[0] = \
        #             {'nsamples': self.par['proc_rebin_time'],
        #              'nscans': sum(idx_scandir),
        #              'index': idx_scandir}

        #     from cascade.spectral_extraction import combine_scan_samples
        #     SpectralTimeSeries = \
        #         combine_scan_samples(SpectralTimeSeries,
        #                              scanDict, verbose=False)

        # # rebin spectra
        # if self.par['proc_auto_adjust_rebin_factor']:
        #     nrebin =  (spectral_data.shape[0]+10) / spectral_data.shape[1]
        # else:
        #     nrebin=self.par['proc_rebin_factor']
        # if nrebin > 1.0:
        #     SpectralTimeSeries = \
        #         rebin_to_common_wavelength_grid(SpectralTimeSeries, 0,
        #                                         nrebin=nrebin, verbose=False,
        #                                         verboseSaveFile=None)

        self._define_convolution_kernel()

        return SpectralTimeSeries


    def get_spectral_images(self):
        """
        Read spectral images.

        Returns
        -------
        None.

        """
        # get data files
        target_name = self.par['obs_target_name']

        path_to_files = os.path.join(self.par['obs_path'],
                                     self.par['inst_obs_name'],
                                     self.par['inst_inst_name'],
                                     target_name,
                                     'SPECTRAL_IMAGES/')

        data_files = find('*' + self.par['obs_id'] + '*rateints.fits',
                          path_to_files)

        # number of integrations
        nintegrations = len(data_files)
        if nintegrations < 1:
            raise AssertionError("No Timeseries data found in dir " +
                                 path_to_files)
        time_bjd = []

        spectral_data = []
        uncertainty_spectral_data = []
        dq = []

        #all_data_files = []

        for data_file in data_files:
            with fits.open(data_file) as hdu_list:
                fits_header = hdu_list[0].header
                exp_start = fits_header['EXPSTART']
                exp_end = fits_header['EXPEND']

                nints_total = fits_header['nints']

                nints = nints_total
                nints_start = 1

                delta_time = (exp_end - exp_start) / nints_total
                start_time = exp_start + 0.5 * delta_time + 2400000.5

                for i in range(2, nints+2):
                    # EXTNAME = 'EXTRACT1D'
                    time_bjd.append(start_time + ((i-2)+(nints_start-1))*delta_time)

                spectral_data.append(hdu_list['SCI'].data)
                uncertainty_spectral_data.append(hdu_list['ERR'].data)
                dq.append(hdu_list['DQ'].data)

        spectral_data = np.concatenate(spectral_data, axis=0, dtype=float).T
        wavelength_data = self.define_wavelength_calibration(spectral_data.shape)
        uncertainty_spectral_data =  np.concatenate(uncertainty_spectral_data, axis=0, dtype=float).T
        dq = np.concatenate(dq, axis=0, dtype=int)

        all_data_files = ['ERS_{0:0=4d}_rateints.fits'.format(i) for i in range(spectral_data.shape[-1])]

        time_bjd = np.array(time_bjd, dtype=float)
        exp_start = np.array(exp_start, dtype=float)

        spectral_data = np.ma.masked_invalid(spectral_data)

        mask = spectral_data.mask

        # orbital phase
        phase = (time_bjd - self.par['obj_ephemeris']) / self.par['obj_period']
        phase = phase - int(np.max(phase))
        if np.max(phase) < 0.0:
            phase = phase + 1.0
        phase = phase - np.rint(phase)
        if self.par['obs_type'] == 'ECLIPSE':
            phase[phase < 0] = phase[phase < 0] + 1.0

        wave_unit = u.micron
        flux_unit = u.ct/u.s

        SpectralTimeSeries = \
            SpectralDataTimeSeries(
                                   wavelength=wavelength_data,
                                   wavelength_unit=wave_unit,
                                   data=spectral_data.data,
                                   data_unit=flux_unit,
                                   uncertainty=uncertainty_spectral_data,
                                   time=phase,
                                   time_unit=u.dimensionless_unscaled,
                                   mask=mask,
                                   time_bjd=time_bjd,
                                   isRampFitted=True,
                                   isNodded=False,
                                   target_name=target_name,
                                   dataProduct=self.par['obs_data_product'],
                                   dataFiles=all_data_files
                                   )
        # make sure that the date units are as "standard" as posible
        data_unit = (1.0*SpectralTimeSeries.data_unit).decompose().unit
        SpectralTimeSeries.data_unit = data_unit
        wave_unit = (1.0*SpectralTimeSeries.wavelength_unit).decompose().unit
        SpectralTimeSeries.wavelength_unit = wave_unit
        # To make the as standard as posible, by defaut change to
        # mean nomalized data units and use micron as wavelength unit
        mean_signal, _, _ = \
            sigma_clipped_stats(SpectralTimeSeries.return_masked_array("data"),
                                sigma=3, maxiters=10)
        data_unit = u.Unit(mean_signal*SpectralTimeSeries.data_unit)
        SpectralTimeSeries.data_unit = data_unit
        SpectralTimeSeries.wavelength_unit = u.micron

        SpectralTimeSeries.period = self.par['obj_period']
        SpectralTimeSeries.ephemeris = self.par['obj_ephemeris']


        if self.par['obs_has_backgr']:
            SpectralTimeSeriesBackground = self.determine_background(SpectralTimeSeries)
            return SpectralTimeSeries, SpectralTimeSeriesBackground

        return SpectralTimeSeries

    def determine_background(self, SpectralTimeSeries):
        import copy
        SpectralTimeSeriesBackground = copy.deepcopy(SpectralTimeSeries)
        data = SpectralTimeSeriesBackground.data.data.value
        background = np.nanmedian(data[:, [0,1,2,3,4,  25,26,27,28,29,30,31], :], axis=1)
        background = np.repeat(background[:,None, :], 32, axis=1)
        background = background * SpectralTimeSeriesBackground.data_unit
        background = np.ma.array(background, mask=SpectralTimeSeriesBackground.mask)
        SpectralTimeSeriesBackground.data = background
        return SpectralTimeSeriesBackground

    def define_wavelength_calibration(self, data_shape):
        coeff = [-5.49471141e-19,  9.88675530e-16, -7.23417941e-13,
                 2.73519357e-10, -5.53539904e-08,  5.33082106e-06,
                 -1.15990213e-04,  3.92862378e-03, 5.61153919e-01]
        x = np.arange(432)
        wave = np.zeros(data_shape[0])
        wave[30:-50] = np.polyval(coeff, x)
        wave_image = np.repeat(wave[..., None], data_shape[1], axis=1)
        wave_cube = np.repeat(wave_image[..., None], data_shape[2], axis=2)
        return wave_cube


    def get_spectral_trace(self):
        """Get spectral trace."""
        dim = self.data.data.shape
        wave_pixel_grid = np.arange(dim[0]) * u.pix
        position_pixel_grid = np.zeros_like(wave_pixel_grid)
        spectral_trace = \
            collections.OrderedDict(wavelength_pixel=wave_pixel_grid,
                                    positional_pixel=position_pixel_grid,
                                    wavelength=self.data.wavelength.
                                    data[:, 0])
        return spectral_trace

    def _define_region_of_interest(self):
        """
        Defines region on detector which containes the intended target star.
        """
        dim = self.data.data.shape

        if 'F290LP' in self.par['inst_filter']:
            wavelength_min = \
                self.par['proc_extend_roi'][0]*2.82*u.micron
            wavelength_max = \
                self.par['proc_extend_roi'][1]*5.172*u.micron
        elif 'CLEAR' in self.par['inst_filter']:
            wavelength_min = \
                self.par['proc_extend_roi'][0]*0.7*u.micron
            wavelength_max = \
                self.par['proc_extend_roi'][1]*5.1*u.micron
        else:
            raise ValueError("NIRSPEC Filter not implemented in ROI definition")

        trace = self.spectral_trace.copy()
        mask_min = trace['wavelength'] > wavelength_min
        mask_max = trace['wavelength'] < wavelength_max
        mask_not_defined = trace['wavelength'] == 0.
        idx_min = int(np.min(trace['wavelength_pixel'].value[mask_min]))
        idx_max = int(np.max(trace['wavelength_pixel'].value[mask_max]))
        roi = np.zeros((dim[0]), dtype=bool)
        roi[0:idx_min] = True
        roi[idx_max+1:] = True
        roi[mask_not_defined] = True


        try:
            self.nirspecbots_cal
        except AttributeError:
            self.nirspecbots_cal = SimpleNamespace()
        finally:
            self.nirspecbots_cal.roi = roi
        return

    def _define_convolution_kernel(self):
        """
        Define convolution kernel.

        Define the instrument specific convolution kernel which will be used
        in the correction procedure of bad pixels.
        """
        if self.par["obs_data"] == 'SPECTRUM':
            kernel = Gaussian1DKernel(4.0, x_size=19)
        else:
            kernel = Gaussian2DKernel(x_stddev=0.2, y_stddev=4.0,
                                      theta=-0.0092, x_size=5, y_size=19)
        try:
            self.nirspecbots_cal
        except AttributeError:
            self.nirspecbots_cal = SimpleNamespace()
        finally:
            self.nirspecbots_cal.convolution_kernel = kernel
        return


class JWSTNIRISS(InstrumentBase):
    """
    NIRISS instrument module.

    This instrument class defines the properties for the NIRISS intrument
    of JWST.

    For the instrument and observations the following valid options are
    available:

       - data type : {'SPECTRUM'}
       - observing strategy : {'STARING'}
    """
    __valid_data = {'SPECTRUM'}
    __valid_observing_strategy = {'STARING'}

    def __init__(self):
        self.par = self.get_instrument_setup()
        if self.par['obs_has_backgr']:
            self.data, self.data_background = self.load_data()
        else:
            self.data = self.load_data()
        self.spectral_trace = self.get_spectral_trace()
        self._define_region_of_interest()
        try:
            self.instrument_calibration = self.nirisssoss_cal
        except AttributeError:
            self.instrument_calibration = None

    @property
    def name(self):
        """
        Name of the JWST instrument: 'NIRISS'
        """
        return "NIRISS"

    @property
    def dispersion_scale(self):
        __all_scales = {'GR700XD-CLEAR': '24.0 Angstrom'}
        return __all_scales[self.par["inst_filter"]]

    @property
    def detector_gain(self):
        """
        Detector gain of the miri detectors.

        Returns
        -------
        1.61 * u.electron / u.DN
        """
        return 1.61 * u.electron / u.DN

    def load_data(self):
        """
        Load the observations.

        This function loads the NIRISS SOSS data form disk based on the
        parameters defined during the initialization of the TSO object.
        """
        if self.par["obs_data"] == 'SPECTRUM':
            data = self.get_spectra()
            if self.par['obs_has_backgr']:
                data_back = self.get_spectra(is_background=True)
        else:
            raise ValueError("The NIRISS insrtrument can currently only be "
                             "used with the observational data parameter "
                             f"set to {self.__valid_data}")
        if self.par['obs_has_backgr']:
            return data, data_back
        else:
            return data

    def get_instrument_setup(self):
        """
        Retrieve all relevant parameters defining the instrument and data setup

        Returns
        -------
        par : `collections.OrderedDict`
            Dictionary containg all relevant parameters

        Raises
        ------
        ValueError
            If obseervationla parameters are not or incorrect defined an
            error will be raised
        """
        par = get_jwst_instrument_setup(cascade_configuration,
                                        cascade_default_data_path)

        return par

    def get_spectra(self, is_background=False):
        """
        Read the input spectra.

        This function combines all functionallity to read fits files
        containing the (uncalibrated) spectral timeseries, including
        orbital phase and wavelength information

        Parameters
        ----------
        is_background : `bool`
            if `True` the data represents an observaton of the IR background
            to be subtracted of the data of the transit spectroscopy target.

        Returns
        -------
        SpectralTimeSeries : `cascade.data_model.SpectralDataTimeSeries`
            Instance of `SpectralDataTimeSeries` containing all spectroscopic
            data including uncertainties, time, wavelength and bad pixel mask.

        Raises
        ------
        AssertionError, KeyError
            Raises an error if no data is found or if certain expected
            fits keywords are not present in the data files.
        """
        # get data files
        if is_background:
            # obsid = self.par['obs_backgr_id']
            target_name = self.par['obs_backgr_target_name']
        else:
            # obsid = self.par['obs_id']
            target_name = self.par['obs_target_name']

        path_to_files = os.path.join(self.par['obs_path'],
                                     self.par['inst_obs_name'],
                                     self.par['inst_inst_name'],
                                     target_name,
                                     'SPECTRA/')

        data_files = find('*' + self.par['obs_id'] + '*' +
                          self.par['obs_data_product']+'.fits',
                          path_to_files)

        # number of integrations
        nintegrations = len(data_files)
        if nintegrations < 1:
            raise AssertionError("No Timeseries data found in dir " +
                                 path_to_files)

        bits_not_to_flag = []
        (wavelength_data, spectral_data, uncertainty_spectral_data, time_bjd,
         mask, all_data_files) = \
            read_x1dints_files(data_files, bits_not_to_flag,
                               self.par["cpm_ncut_first_int"],
                               self.par["cpm_ncut_last_int"],
                               self.par["inst_spec_order"])

        # positon info
        position_file = find('target_trace_position.fits', path_to_files)
        if len(position_file) == 0:
            position = np.ones((len(time_bjd)))
            position_unit = u.pix
            median_position = np.median(position)
        else:
            position_dict = read_position_file(position_file[0],
                                      self.par["cpm_ncut_first_int"],
                                      self.par["cpm_ncut_last_int"])
            position = position_dict['POSITION']
            try:
                median_position = position_dict['MEDPOS']
            except:
                median_position = np.median(position)
                position = position - median_position
            try:
                position_unit =  position_dict['PUNIT']
            except:
                position_unit = u.pix

        # FWHM info
        fwhm_file = find('target_FWHM.fits', path_to_files)
        if len(fwhm_file) == 0:
            fwhm = np.ones((len(time_bjd)))
            fwhm_unit = u.pix
            median_fwhm = np.median(fwhm)
        else:
            fwhm_dict = read_FWHM_file(fwhm_file[0],
                                      self.par["cpm_ncut_first_int"],
                                      self.par["cpm_ncut_last_int"])
            fwhm = fwhm_dict['FWHM']
            try:
                median_fwhm = fwhm_dict['MEDFWHM']
            except:
                median_fwhm = np.median(fwhm)
                fwhm = fwhm - median_fwhm
            try:
                fwhm_unit =  fwhm_dict['FWHMUNIT']
            except:
                fwhm_unit = u.pix

        # orbital phase
        phase = ((time_bjd+2400000.5 - self.par['obj_ephemeris']) /
                 self.par['obj_period'])
        phase = phase - int(np.max(phase))

        detector_gain = self.detector_gain

        scaling = (wavelength_data/1.0)**2
        scaling_unit = u.dimensionless_unscaled
        spectral_data *= detector_gain.value * scaling
        uncertainty_spectral_data *= detector_gain.value * scaling

        wave_unit = u.micron
        flux_unit = u.electron / u.s

        SpectralTimeSeries = \
            SpectralDataTimeSeries(
                                   wavelength=wavelength_data,
                                   wavelength_unit=wave_unit,
                                   data=spectral_data.data,
                                   data_unit=flux_unit,
                                   uncertainty=uncertainty_spectral_data,
                                   time=phase,
                                   time_unit=u.dimensionless_unscaled,
                                   mask=mask,
                                   time_bjd=time_bjd,
                                   position=position,
                                   position_unit=position_unit,
                                   fwhm=fwhm,
                                   fwhm_unit=fwhm_unit,
                                   scaling=scaling,
                                   scaling_unit=scaling_unit,
                                   isRampFitted=True,
                                   isNodded=False,
                                   target_name=target_name,
                                   dataProduct=self.par['obs_data_product'],
                                   dataFiles=all_data_files
                                   )

        # make sure that the date units are as "standard" as posible
        data_unit = (1.0*SpectralTimeSeries.data_unit).decompose().unit
        SpectralTimeSeries.data_unit = data_unit
        wave_unit = (1.0*SpectralTimeSeries.wavelength_unit).decompose().unit
        SpectralTimeSeries.wavelength_unit = wave_unit

        # To make the as standard as posible, by defaut change to
        # mean nomalized data units and use micron as wavelength unit
        mean_signal, _, _ = \
            sigma_clipped_stats(SpectralTimeSeries.return_masked_array("data"),
                                sigma=3, maxiters=10)
        data_unit = u.Unit(mean_signal*SpectralTimeSeries.data_unit)
        SpectralTimeSeries.data_unit = data_unit
        SpectralTimeSeries.wavelength_unit = u.micron

        SpectralTimeSeries.period = self.par['obj_period']
        SpectralTimeSeries.ephemeris = self.par['obj_ephemeris']

        self._define_convolution_kernel()

        return SpectralTimeSeries

    def get_spectral_images(self):
        """
        Read spectral images.

        Returns
        -------
        None.

        """
        pass

    def get_spectral_trace(self):
        """Get spectral trace."""
        dim = self.data.data.shape
        wave_pixel_grid = np.arange(dim[0]) * u.pix
        position_pixel_grid = np.zeros_like(wave_pixel_grid)
        spectral_trace = \
            collections.OrderedDict(wavelength_pixel=wave_pixel_grid,
                                    positional_pixel=position_pixel_grid,
                                    wavelength=self.data.wavelength.
                                    data[:, 0])
        return spectral_trace

    def _define_region_of_interest(self):
        """
        Defines region on detector which containes the intended target star.
        """
        dim = self.data.data.shape

        if self.par['inst_spec_order'] == 1:
            wavelength_min = \
                self.par['proc_extend_roi'][0]*0.85*u.micron
            wavelength_max = \
                self.par['proc_extend_roi'][1]*2.83*u.micron
        else:
            wavelength_min = \
                self.par['proc_extend_roi'][0]*0.60*u.micron
            wavelength_max = \
                self.par['proc_extend_roi'][1]*0.90*u.micron

        trace = self.spectral_trace.copy()
        mask_min = trace['wavelength'] > wavelength_min
        mask_max = trace['wavelength'] < wavelength_max
        mask_not_defined = trace['wavelength'] == 0.
        idx_min = int(np.min(trace['wavelength_pixel'].value[mask_min]))
        idx_max = int(np.max(trace['wavelength_pixel'].value[mask_max]))
        roi = np.zeros((dim[0]), dtype=bool)
        roi[0:idx_min] = True
        roi[idx_max+1:] = True
        roi[mask_not_defined] = True

        try:
            self.nirisssoss_cal
        except AttributeError:
            self.nirisssoss_cal = SimpleNamespace()
        finally:
            self.nirisssoss_cal.roi = roi
        return

    def _define_convolution_kernel(self):
        """
        Define convolution kernel.

        Define the instrument specific convolution kernel which will be used
        in the correction procedure of bad pixels.
        """
        if self.par["obs_data"] == 'SPECTRUM':
            kernel = Gaussian1DKernel(4.0, x_size=19)
        else:
            kernel = Gaussian2DKernel(x_stddev=0.8, y_stddev=4.0,
                                      theta=0.0090, x_size=5, y_size=19)
        try:
            self.nirisssoss_cal
        except AttributeError:
            self.nirisssoss_cal = SimpleNamespace()
        finally:
            self.nirisssoss_cal.convolution_kernel = kernel
        return


class JWSTNIRCAM(InstrumentBase):
    """
    NIRCAM LW.

    This instrument class defines the properties for the LW spectrograph,
    which is part of the NIRCAM instrument of the JWST.

    For the instrument and observations the following valid options are
    available:

       - data type : {'SPECTRUM'}
       - observing strategy : {'STARING'}
    """

    __valid_data = {'SPECTRUM'}
    __valid_observing_strategy = {'STARING'}

    def __init__(self):
        self.par = self.get_instrument_setup()
        if self.par['obs_has_backgr']:
            self.data, self.data_background = self.load_data()
        else:
            self.data = self.load_data()
        self.spectral_trace = self.get_spectral_trace()
        self._define_region_of_interest()
        try:
            self.instrument_calibration = self.nircamlw_cal
        except AttributeError:
            self.instrument_calibration = None

    @property
    def name(self):
        """
        Name of the JWST instrument: 'NIRCAMLW'
        """
        return "NIRCAMLW"

    @property
    def dispersion_scale(self):
        __all_scales = {'LW': '100.0 Angstrom'}
        return __all_scales[self.par["inst_filter"]]

    def load_data(self):
        """
        Load the observations.

        This function loads the JWST/NIRCAM/LW data form disk based on the
        parameters defined during the initialization of the TSO object.
        """
        if self.par["obs_data"] == 'SPECTRUM':
            data = self.get_spectra()
            if self.par['obs_has_backgr']:
                data_back = self.get_spectra(is_background=True)
        else:
            raise ValueError("MIRI/LRS instrument can currently only be used \
                              with observational data parameter \
                              set to 'SPECTRUM'")
        if self.par['obs_has_backgr']:
            return data, data_back
        else:
            return data

    def get_instrument_setup(self):
        """
        Retrieve all relevant parameters defining the instrument and data setup

        Returns
        -------
        par : `collections.OrderedDict`
            Dictionary containg all relevant parameters

        Raises
        ------
        ValueError
            If obseervationla parameters are not or incorrect defined an
            error will be raised
        """
        par = get_jwst_instrument_setup(cascade_configuration,
                                        cascade_default_data_path)

        return par

    def get_spectra(self, is_background=False):
        """
        Read the input spectra.

        This function combines all functionallity to read fits files
        containing the (uncalibrated) spectral timeseries, including
        orbital phase and wavelength information

        Parameters
        ----------
        is_background : `bool`
            if `True` the data represents an observaton of the IR background
            to be subtracted of the data of the transit spectroscopy target.

        Returns
        -------
        SpectralTimeSeries : `cascade.data_model.SpectralDataTimeSeries`
            Instance of `SpectralDataTimeSeries` containing all spectroscopic
            data including uncertainties, time, wavelength and bad pixel mask.

        Raises
        ------
        AssertionError, KeyError
            Raises an error if no data is found or if certain expected
            fits keywords are not present in the data files.
        """
        # get data files
        if is_background:
            # obsid = self.par['obs_backgr_id']
            target_name = self.par['obs_backgr_target_name']
        else:
            # obsid = self.par['obs_id']
            target_name = self.par['obs_target_name']

        path_to_files = os.path.join(self.par['obs_path'],
                                     self.par['inst_obs_name'],
                                     self.par['inst_inst_name'],
                                     target_name,
                                     'SPECTRA/')

        data_files = find('*' + self.par['obs_id'] + '*x1dints.fits',
                          path_to_files)

        # number of integrations
        nintegrations = len(data_files)
        if nintegrations < 1:
            raise AssertionError("No Timeseries data found in dir " +
                                 path_to_files)

        bits_not_to_flag = []
        (wavelength_data, spectral_data, uncertainty_spectral_data, time_bjd,
         mask, all_data_files) = \
            read_x1dints_files(data_files, bits_not_to_flag,
                               self.par["cpm_ncut_first_int"])

        # orbital phase
        phase = (time_bjd - self.par['obj_ephemeris']) / self.par['obj_period']
        phase = phase - int(np.max(phase))
        if np.max(phase) < 0.0:
            phase = phase + 1.0
        phase = phase - np.rint(phase)
        if self.par['obs_type'] == 'ECLIPSE':
            phase[phase < 0] = phase[phase < 0] + 1.0

        wave_unit = u.micron
        flux_unit = u.Jy

        #print(np.any(wavelength_data <=0.0))
       # mask[wavelength_data <= 0.0] = True

       # import matplotlib.pyplot as plt
       # plt.imshow(mask)
       # plt.show()


        mask[wavelength_data>4.08] = True

        SpectralTimeSeries = \
            SpectralDataTimeSeries(
                                   wavelength=wavelength_data,
                                   wavelength_unit=wave_unit,
                                   data=spectral_data.data,
                                   data_unit=flux_unit,
                                   uncertainty=uncertainty_spectral_data,
                                   time=phase,
                                   time_unit=u.dimensionless_unscaled,
                                   mask=mask,
                                   time_bjd=time_bjd,
                                   isRampFitted=True,
                                   isNodded=False,
                                   target_name=target_name,
                                   dataProduct=self.par['obs_data_product'],
                                   dataFiles=all_data_files
                                   )
        # make sure that the date units are as "standard" as posible
        data_unit = (1.0*SpectralTimeSeries.data_unit).decompose().unit
        SpectralTimeSeries.data_unit = data_unit
        wave_unit = (1.0*SpectralTimeSeries.wavelength_unit).decompose().unit
        SpectralTimeSeries.wavelength_unit = wave_unit
        # To make the as standard as posible, by defaut change to
        # mean nomalized data units and use micron as wavelength unit
        mean_signal, _, _ = \
            sigma_clipped_stats(SpectralTimeSeries.return_masked_array("data"),
                                sigma=3, maxiters=10)
        data_unit = u.Unit(mean_signal*SpectralTimeSeries.data_unit)
        SpectralTimeSeries.data_unit = data_unit
        SpectralTimeSeries.wavelength_unit = u.micron

        SpectralTimeSeries.period = self.par['obj_period']
        SpectralTimeSeries.ephemeris = self.par['obj_ephemeris']

        ROI = SpectralTimeSeries.mask[:,0]
        from cascade.spectral_extraction import compressDataset
        SpectralTimeSeries, compressMask = compressDataset(SpectralTimeSeries, ROI)


        #print(SpectralTimeSeries.data.shape)
        #print(SpectralTimeSeries.wavelength.shape)
        #print(np.all(np.isfinite(SpectralTimeSeries.wavelength.data)))
        #print(np.any(SpectralTimeSeries.wavelength.data.value <=0.0))

        #print(SpectralTimeSeries.mask[:,0])
        #print(SpectralTimeSeries.mask[:,1])


        #print(SpectralTimeSeries.data)

        if spectral_data.shape[-1] > 512:
            scanDict = {}
            idx_scandir = np.ones(spectral_data.shape[-1], dtype=bool)
            scanDict[0] = \
                    {'nsamples': 2,
                      'nscans': sum(idx_scandir),
                      'index': idx_scandir}

            from cascade.spectral_extraction import combine_scan_samples
            SpectralTimeSeries = \
                combine_scan_samples(SpectralTimeSeries,
                                      scanDict, verbose=False)

        # print(SpectralTimeSeries.data)

        nrebin =  (SpectralTimeSeries.data.shape[0]+10) / SpectralTimeSeries.data.shape[1]
        print(nrebin)
        if nrebin > 1.0:
            SpectralTimeSeries = \
                rebin_to_common_wavelength_grid(SpectralTimeSeries, 0,
                                                nrebin=nrebin, verbose=False,
                                                verboseSaveFile=None)

        self._define_convolution_kernel()

        return SpectralTimeSeries


    def get_spectral_trace(self):
        """Get spectral trace."""
        dim = self.data.data.shape
        wave_pixel_grid = np.arange(dim[0]) * u.pix
        position_pixel_grid = np.zeros_like(wave_pixel_grid)
        spectral_trace = \
            collections.OrderedDict(wavelength_pixel=wave_pixel_grid,
                                    positional_pixel=position_pixel_grid,
                                    wavelength=self.data.wavelength.
                                    data[:, 0])
        return spectral_trace

    def _define_region_of_interest(self):
        """
        Defines region on detector which containes the intended target star.
        """
        dim = self.data.data.shape
        roi = np.zeros((dim[0]), dtype=bool)

        try:
            self.nircamlw_cal
        except AttributeError:
            self.nircamlw_cal = SimpleNamespace()
        finally:
            self.nircamlw_cal.roi = roi
        return

    def _define_convolution_kernel(self):
        """
        Define convolution kernel.

        Define the instrument specific convolution kernel which will be used
        in the correction procedure of bad pixels.
        """
        if self.par["obs_data"] == 'SPECTRUM':
            kernel = Gaussian1DKernel(4.0, x_size=19)
        else:
            kernel = Gaussian2DKernel(x_stddev=0.2, y_stddev=4.0,
                                      theta=-0.0092, x_size=5, y_size=19)
        try:
            self.nircamlw_cal
        except AttributeError:
            self.nircamlw_cal = SimpleNamespace()
        finally:
            self.nircamlw_cal.convolution_kernel = kernel
        return