# Copyright (C) 2021  Peter van Heusden <pvh@sanbi.ac.za>
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from .farhat_rlc import FarhatLab_RLC_Regions
from .farhat_rlc_lowmap import FarhatLab_RLC_LowMap_Regions
from .mtbseq import MTBseqRegions
from .pe_ppe import PE_PPE_Regions
from .tbprofiler import TBProfilerRegions
from .uvp import UVPRegions

__all__ = [
    "FarhatLab_RLC_Regions",
    "FarhatLab_RLC_LowMap_Regions",
    "MTBseqRegions",
    "PE_PPE_Regions",
    "TBProfilerRegions",
    "UVPRegions",
]
