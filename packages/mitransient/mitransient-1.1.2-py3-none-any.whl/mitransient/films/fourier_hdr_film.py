from typing import Sequence

import mitsuba as mi
from mitsuba import (
    Float,
    Int32,
    ScalarInt32,
    TensorXf,
)
import drjit as dr

from mitransient.render.fourier_image_block import FourierImageBlock


class FourierHDRFilm(mi.Film):
    r"""

    .. film-fourier_hdr_film:

    Fourier HDR Film

    TODO(diego): docs

    See also:
        - width/height (uint32)
        - crop_width/crop_height (uint32)
        - crop_offset_x/crop_offset_y (uint32)
        - sample_border (bool)
        - rfilters?
    """

    def __init__(self, props: mi.Properties):
        super().__init__(props)
        self.wl_1 = props.get("wl_1", mi.Float(0.1))
        self.wl_2 = props.get("wl_2", mi.Float(0.15))
        self.start_opl = props.get("start_opl", mi.Float(0))

        # FIXME: use mi.Log ERROR
        assert self.crop_size.x() == self.size().x and self.crop_size.y() == self.size().y, \
            "FourierHDRFilm: crop_size must match size"
        assert self.crop_offset.x() == 0 and self.crop_offset.y() == 0, \
            "FourierHDRFilm: crop_offset must be (0, 0)"
        assert self.sample_border == False, \
            "FourierHDRFilm: sample_border must be False"

        # FIXME generate from arbitrary list
        # maybe do Dist1D, or look at specfilm
        self.frequencies = [1/self.wl_1, 1/self.wl_2]

    def prepare(self, aovs: Sequence[str]):
        assert mi.is_monochromatic, "FourierHDRFilm: Only monochromatic rendering supported"
        assert len(aovs) == 0, "FourierHDRFilm: AOVs not supported"
        alpha = mi.has_flag(self.flags(), mi.FilmFlags.Alpha)

        base_channels = "L"
        extra_channels = "AW" if alpha else "W"

        channels = []
        for i in range(len(base_channels)):
            for j in range(len(self.frequencies)):
                channels.append(
                    base_channels[i] + f'_fq{j:03d}_Re')
                channels.append(
                    base_channels[i] + f'_fq{j:03d}_Im')

        for i in range(len(extra_channels)):
            channels.append(extra_channels[i])

        # for i in range(len(aovs)):
        #     channels.append(aovs[i])

        self.storage = FourierImageBlock(
            size=self.size,
            offset=self.crop_offset,
            channel_count=len(channels),
            frequencies=self.frequencies,
        )
        self.channels = channels

        if len(set(channels)) != len(channels):
            mi.Log(mi.LogLevel.Error,
                   "Film::prepare_transient_(): duplicate channel name.")

        return len(self.channels)

    def clear(self):
        self.storage.clear()

    def develop(self, raw: bool = False):
        if not self.transient_storage:
            mi.Log(mi.LogLevel.Error,
                   "No transient storage allocated, was prepare_transient_() called first?")

        return self.storage.tensor

        # if raw:
        #     return self.transient_storage.tensor

        # data = self.transient_storage.tensor

        # pixel_count = dr.prod(data.shape[0:-1])
        # source_ch = data.shape[-1]
        # # Remove alpha and weight channels
        # alpha = mi.has_flag(self.flags(), mi.FilmFlags.Alpha)
        # target_ch = source_ch - (ScalarInt32(2) if alpha else ScalarInt32(1))

        # idx = dr.arange(Int32, pixel_count * target_ch)
        # pixel_idx = idx // target_ch
        # channel_idx = dr.fma(pixel_idx, -target_ch, idx)

        # values_idx = dr.fma(pixel_idx, source_ch, channel_idx)
        # weight_idx = dr.fma(pixel_idx, source_ch, source_ch - 1)

        # weight = dr.gather(Float, data.array, weight_idx)
        # values_ = dr.gather(Float, data.array, values_idx)

        # values = values_ / dr.select((weight == 0.0), 1.0, weight)

        # return TensorXf(values, tuple(list(data.shape[0:-1]) + [target_ch]))

    def add_transient_data(self, pos: mi.Vector2f, distance: mi.Float,
                           wavelengths: mi.UnpolarizedSpectrum, spec: mi.Spectrum,
                           ray_weight: mi.Float, active: mi.Bool):
        """
        Add a path's contribution to the film:
        * pos: pixel position
        * distance: distance traveled by the path (opl)
        * wavelengths: for spectral rendering, wavelengths sampled
        * spec: Spectrum / contribution of the path
        * ray_weight: weight of the ray given by the sensor
        * active: mask
        """
        pos_distance = (distance - self.start_opl)
        coords = mi.Vector3f(pos.x, pos.y, pos_distance)
        self.transient_storage.put(
            pos=coords,
            wavelengths=wavelengths,
            value=spec * ray_weight,
            alpha=mi.Float(0.0),
            # value should have the sample scale already multiplied
            weight=mi.Float(0.0),
            active=active,
        )

    def to_string(self):
        string = "FourierHDRFilm[\n"
        string += f"  size = {self.size()},\n"
        string += f"  frequencies = {self.frequencies},\n"
        string += f"  start_opl = {self.start_opl},\n"
        string += f"]"
        return string

    def traverse(self, callback):
        super().traverse(callback)
        callback.put_parameter(
            "frequencies", self.frequencies, mi.ParamFlags.NonDifferentiable)
        callback.put_parameter(
            "start_opl", self.start_opl, mi.ParamFlags.NonDifferentiable)

    def parameters_changed(self, keys):
        super().parameters_changed(keys)


mi.register_film("fourier_hdr_film", lambda props: FourierHDRFilm(props))
