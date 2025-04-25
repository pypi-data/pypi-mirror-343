# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import cast

from pdkmaster.technology import geometry as _geo, primitive as _prm
from pdkmaster.design import library as _lbry, factory as _fab

from .tech import tech, cktfab, layoutfab


lib = _lbry.Library(name="dummy_lib", tech=tech)
fab = _fab.BaseCellFactory(lib=lib, cktfab=cktfab, layoutfab=layoutfab)
def _lib_init():
    # The dummy_lib will be initialized with different shapes to maximize
    # code coverage when being used for example in export code etc.
    prims = tech.primitives
    metal = cast(_prm.TopMetalWire, prims["metal"])

    rect1 = _geo.Rect(left=0.0, bottom=0.0, right=1.0, top=1.0)
    rect2 = _geo.Rect(left=1.0, bottom=0.0, right=2.0, top=1.0)
    rect12 = _geo.Rect(left=0.0, bottom=0.0, right=2.0, top=1.0)
    lshape = _geo.Polygon.from_floats(points=(
        (0.0, 0.0), (0.0, 3.0), (1.0, 3.0), (1.0, 1.0), (2.0, 1.0), (2.0, 0.0), (0.0, 0.0),
    ))

    # cell1: rect shape
    cell1 = fab.new_cell(name="cell1")
    ckt = cell1.new_circuit()
    layouter = cell1.new_circuitlayouter()
    layout = layouter.layout

    i = ckt.new_net(name="i", external=True)
    layouter.add_wire(net=i, wire=metal, pin=prims["metalpin"], shape=rect1)
    layouter.layout.boundary = rect1

    # cell2: cell instance
    cell2 = fab.new_cell(name="cell2")
    ckt = cell2.new_circuit()
    layouter = cell2.new_circuitlayouter()

    inst = ckt.instantiate(cell1, name="inst")
    i = ckt.new_net(name="i", external=True, childports=inst.ports["i"])

    layouter.place(object_=inst, origin=_geo.Point(x=1.0, y=0.0))
    layouter.layout.boundary = rect1

    # cell3: polygon
    cell3 = fab.new_cell(name="cell3")
    ckt = cell3.new_circuit()
    layouter = cell3.new_circuitlayouter()

    i = ckt.new_net(name="i", external=True)
    layouter.add_wire(net=i, wire=metal, pin=prims["metalpin"], shape=lshape)
    layouter.layout.boundary = lshape.bounds

    # cell4: multipartshape
    cell4 = fab.new_cell(name="cell4")
    ckt = cell4.new_circuit()
    layouter = cell4.new_circuitlayouter()
    layout = layouter.layout

    mps = _geo.MultiPartShape(fullshape=rect12, parts=(rect1, rect2))
    
    i1 = ckt.new_net(name="i1", external=False)
    i2 = ckt.new_net(name="i2", external=False)

    layout.add_shape(layer=metal, net=i1, shape=mps.parts[0])
    layout.add_shape(layer=metal, net=i2, shape=mps.parts[1])

    # cell5: primitive instance
    cell5 = fab.new_cell(name="cell5")
    ckt = cell5.new_circuit()
    layouter = cell5.new_circuitlayouter()
    layout = layouter.layout

    res = ckt.instantiate(
        cast(_prm.Resistor, prims["resistor"]), name="res",
        width=1.0, height=5.0,
    )

    ckt.new_net(name="p1", external=True, childports=res.ports["port1"])
    ckt.new_net(name="p2", external=True, childports=res.ports["port2"])

    layouter.place(res)
_lib_init()
