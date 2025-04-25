from typing import Sequence

import drjit as dr
import mitsuba as mi

from ..utils import indent


class FourierImageBlock(mi.ImageBlock):
    """
    TODO(diego): docs
    """

    def __init__(
        self,
        size: mi.ScalarVector3u,
        offset: mi.ScalarPoint3i,
        channel_count: int,
        frequencies=[],
        warn_negative: bool = False,
        warn_invalid: bool = False
    ):
        alpha = mi.has_flag(self.flags(), mi.FilmFlags.Alpha)
        assert channel_count == 2 * len(frequencies) + (2 if alpha else 1), \
            "FourierImageBlock: channel_count must match frequencies and alpha"
        super().__init__(
            size=size,
            offset=offset,
            channel_count=channel_count,
            rfilter=None,
            border=False,
            normalize=False,
            coalesce=False,
            compensate=False,
            warn_negative=warn_negative,
            warn_invalid=warn_invalid)

    def put(self, pos: mi.Point3f, wavelengths: mi.UnpolarizedSpectrum,
            value: mi.Spectrum, alpha: mi.Float,
            weight: mi.Float, active: bool = True):
        spec = mi.unpolarized_spectrum(value)
        spec = spec.x
        pos2 = mi.Point2f(pos.x, pos.y)
        opl = pos.z

        values = []
        for freq in self.frequencies:
            phase = -2 * dr.pi * freq * opl
            values.append(spec * dr.cos(phase))
            values.append(spec * dr.sin(phase))

        values += [alpha, weight]
        self.put_(pos, values, active)

    # def put_(self, pos: mi.Point3f, values: Sequence[mi.Float], active: bool = True):
    #     # Check if all sample values are valid
    #     if self.warn_negative or self.warn_invalid:
    #         is_valid = True

    #         if self.warn_negative:
    #             for k in range(self.channel_count):
    #                 is_valid &= values[k] >= -1e-5

    #         if self.warn_invalid:
    #             for k in range(self.channel_count):
    #                 is_valid &= dr.isfinite(values[k])

    #         if dr.any(active and not is_valid):
    #             log_str = "Invalid sample value: ["
    #             for k in range(self.channel_count):
    #                 log_str += values[k]
    #                 if k + 1 < self.channel_count:
    #                     log_str += ", "
    #             log_str += "]"
    #             mi.Log(mi.LogLevel.Warn, log_str)

    #     # ====================================
    #     # Fast special case for the box filter
    #     # ====================================
    #     if not self.rfilter:
    #         p = mi.Point3u(dr.floor(pos) - self.offset_xyt)

    #         index = dr.fma(p.y, self.size_xyt.x, p.x)
    #         index = dr.fma(index, self.size_xyt.z, p.z) * self.channel_count

    #         active &= dr.all((0 <= p) & (p < self.size_xyt))

    #         for k in range(self.channel_count):
    #             self.accum(values[k], index + k, active)
    #     else:
    #         mi.Log(mi.LogLevel.Error, "TransientImageBlock::put_(): using a rfilter but it is not supported. If you need this, please open an issue on GitHub.")
