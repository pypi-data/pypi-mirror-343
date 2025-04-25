# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from pdkmaster.typing import GDSLayerSpecDict

from .tech import tech


gdslayers: GDSLayerSpecDict = {
    mask.name: (i + 1) if i%2 == 0 else (i + 1, 1)
    for i, mask in enumerate(tech.designmasks)
}
gdslayers["anything_goes"] = None
textgdslayers: GDSLayerSpecDict = {
    "metalpin": (10, 10),
}
