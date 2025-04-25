# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from pdkmaster.technology import (
    property_ as _prp, primitive as _prm, technology_ as _tch
)
from pdkmaster.design import circuit as _ckt, layout as _lay


class Tech(_tch.Technology):
    @property
    def name(self) -> str:
        return "Dummy"
    @property
    def grid(self) -> float:
        return 0.005
    
    def __init__(self):
        prims = _prm.Primitives(_prm.Base(type_=_prm.nBase))

        substrate = _prm.SubstrateMarker(name="substrate")
        prims += substrate

        nwell = _prm.Well(type_=_prm.nImpl, name="nwell", min_width=1.5, min_space=1.5)
        deepwell = _prm.DeepWell(
            name="deepwell", min_width=3.0, min_space=3.0,
            well=nwell, min_well_overlap=0.8, min_well_enclosure=0.8,
        )
        pwell = _prm.Well(type_=_prm.pImpl, name="pwell", min_width=1.5, min_space=1.5)
        nplus = _prm.Implant(type_=_prm.nImpl, name="nplus", min_width=1.0, min_space=1.0)
        pplus = _prm.Implant(type_=_prm.pImpl, name="pplus", min_width=1.0, min_space=1.0)
        hvox = _prm.Insulator(name="hvox", min_width=0.5, min_space=0.5)
        active = _prm.WaferWire(
            name="active", min_width=0.3, min_space=0.2,
            allow_in_substrate=True,
            implant=(nplus, pplus), min_implant_enclosure=_prp.Enclosure(0.2),
            min_implant_enclosure_same_type=(_prp.Enclosure(0.1), None),
            implant_abut="none", allow_contactless_implant=False,
            well=(nwell, pwell),
            min_well_enclosure=_prp.Enclosure(1.0),
            min_well_enclosure4oxide={hvox: _prp.Enclosure(1.0)},
            min_substrate_enclosure=_prp.Enclosure(1.0),
            min_substrate_enclosure4oxide={hvox: _prp.Enclosure(1.0)},
            oxide=hvox, min_oxide_enclosure=_prp.Enclosure(0.2),
            allow_well_crossing=False,
        )
        active2 = _prm.WaferWire(
            name="active2", min_width=0.3, min_space=0.2,
            allow_in_substrate=True,
            implant=(nplus, pplus), min_implant_enclosure=_prp.Enclosure(0.2),
            min_implant_enclosure_same_type=(None, _prp.Enclosure(0.1)),
            implant_abut="none", allow_contactless_implant=False,
            well=(nwell, pwell),
            min_well_enclosure=_prp.Enclosure(1.0),
            min_well_enclosure4oxide={hvox: _prp.Enclosure(1.0)},
            min_substrate_enclosure=_prp.Enclosure(1.0),
            min_substrate_enclosure4oxide={hvox: _prp.Enclosure(1.0)},
            oxide=hvox, min_oxide_enclosure=_prp.Enclosure(0.2),
            allow_well_crossing=False,
        )
        poly = _prm.GateWire(name="poly", min_width=0.25, min_space=0.25)
        prims += (nwell, deepwell, pwell, nplus, pplus, hvox, active, active2, poly)

        metalpin = _prm.Marker(name="metalpin")
        metal = _prm.MetalWire(
            name="metal",
            min_width=0.1, min_space=0.1, space_table=((0.2, 0.5), ((1.0, 1.0), 1.0)),
            min_area=0.05, min_density=0.20,
            pin=metalpin,
        )
        contact = _prm.Via(
            name="contact", width=0.35, min_space=0.35, bottom=(active, active2, poly), top=metal,
            min_bottom_enclosure=_prp.Enclosure(0.2), min_top_enclosure=_prp.Enclosure(0.15),
        )
        prims += (contact, metalpin, metal)

        mimtop = _prm.MIMTop(
            name="MIMTop", min_width=0.2, min_space=0.2,
        )
        prims += mimtop

        metal2pin = _prm.Marker(name="metal2pin")
        metal2block = _prm.Marker(name="metal2block")
        metal2 = _prm.TopMetalWire(
            name="metal2", min_width=0.1, min_space=0.1,
            pin=metal2pin, blockage=metal2block,
        )
        metal2mark = _prm.Marker(name="metal2mark")
        metal2res = _prm.Resistor(
            name="metal2res", wire=metal2, min_length=0.5,
            indicator=metal2mark, min_indicator_extension=0.4,
            contact=None,
        )
        via = _prm.Via(
            name="via", width=0.35, min_space=0.35,
            bottom=(metal, mimtop), top=(metal2, metal2res),
            min_bottom_enclosure=_prp.Enclosure(0.2), min_top_enclosure=_prp.Enclosure(0.15),
        )
        prims += (via, metal2pin, metal2block, metal2, metal2mark, metal2res)

        silblock = _prm.ExtraProcess(
            name="silblock", min_width=0.4, min_space=0.4, grid=0.010,
        )
        resistor = _prm.Resistor(
            name="resistor", wire=active,
            implant=nplus, min_implant_enclosure=active.min_implant_enclosure[0],
            contact=contact, min_contact_space=0.2,
            indicator=silblock, min_indicator_extension=0.4,
        )
        polyres = _prm.Resistor(
            name="polyres", wire=poly, implant=pplus, contact=contact,
            min_implant_enclosure=_prp.Enclosure(0.3), min_contact_space=0.2,
            indicator=silblock, min_indicator_extension=0.4,
        )
        prims += (silblock, resistor, polyres)

        diodemark = _prm.Marker(name="diodemark")
        ndiode = _prm.Diode(
            name="ndiode", wire=active,
            indicator=diodemark, min_indicator_enclosure=_prp.Enclosure(0.2),
            implant=nplus, min_implant_enclosure=_prp.Enclosure(0.2),
        )
        pdiode = _prm.Diode(
            name="pdiode", wire=active,
            indicator=diodemark, min_indicator_enclosure=_prp.Enclosure(0.2),
            implant=pplus, min_implant_enclosure=_prp.Enclosure(0.2),
            well=nwell, min_well_enclosure=_prp.Enclosure(2.0),
        )
        prims += (diodemark, ndiode, pdiode)

        esd = _prm.Marker(name="esd")
        mosgate = _prm.MOSFETGate(
            name="mosgate", active=active, min_sd_width=0.35,
            max_l=10.0, max_w=50.0,
            poly=poly, min_polyactive_extension=0.45,
            contact=contact, min_contactgate_space=0.15,
        )
        hvgate = _prm.MOSFETGate(
            name="hvgate", active=active, oxide=hvox,
            min_sd_width=0.35, min_gate_space=0.5,
            poly=poly, min_polyactive_extension=0.45,
            contact=contact, min_contactgate_space=0.25,
            min_l=0.5, min_w=0.5,
        )
        esdgate = _prm.MOSFETGate(
            name="esdgate", active=active,
            oxide=hvox, min_gateoxide_enclosure=_prp.Enclosure(0.4),
            inside=esd, min_gateinside_enclosure=_prp.Enclosure(0.4),
            min_sd_width=0.35,
            poly=poly, min_polyactive_extension=0.45,
            min_l=0.5, min_w=0.5,
        )
        nmos = _prm.MOSFET(
            name="nmos", gate=mosgate,
            implant=nplus, min_gateimplant_enclosure=_prp.Enclosure(0.25),
        )
        pmos = _prm.MOSFET(
            name="pmos", gate=mosgate,
            implant=pplus, min_gateimplant_enclosure=_prp.Enclosure(0.25),
            well=nwell,
        )
        hvnmos = _prm.MOSFET(
            name="hvnmos", gate=hvgate,
            implant=nplus, min_gateimplant_enclosure=_prp.Enclosure(0.4),
        )
        hvpmos = _prm.MOSFET(
            name="hvpmos", gate=hvgate,
            min_l=0.8, max_l=20.0, min_w=0.8, max_w=30.0,
            implant=pplus, min_gateimplant_enclosure=_prp.Enclosure(0.4),
            well=nwell,
        )
        esdnmos = _prm.MOSFET(
            name="esdnmos", gate=esdgate, min_gate_space=2.0,
            min_polyactive_extension=0.4,
            implant=nplus, min_gateimplant_enclosure=_prp.Enclosure((0.4, 0.6)),
            contact=contact, min_contactgate_space=0.75,
            min_sd_width=0.8,
        )
        prims += (mosgate, hvgate, esdgate, nmos, pmos, esd, hvnmos, hvpmos, esdnmos)

        bip = _prm.Marker(name="bip")
        npn = _prm.Bipolar(name="npn", type_=_prm.npnBipolar, indicator=bip)
        pnp = _prm.Bipolar(
            name="pnp", type_=_prm.pnpBipolar, indicator=bip,
        )
        prims += (bip, npn, pnp)

        mimcap = _prm.MIMCapacitor(
            name="MIMCap", bottom=metal, top=mimtop, via=via,
            min_bottom_top_enclosure=_prp.Enclosure(0.2),
            min_bottomvia_top_space=0.25,
            min_top_via_enclosure=_prp.Enclosure(0.25),
            min_bottom_space=None, min_top2bottom_space=None,
        )
        mimcap2 = _prm.MIMCapacitor(
            name="MIMCap2", bottom=metal, top=mimtop, via=via,
            min_bottom_top_enclosure=_prp.Enclosure(0.2),
            min_bottomvia_top_space=0.25,
            min_top_via_enclosure=_prp.Enclosure(0.25),
            min_bottom_space=None, min_top2bottom_space=None,
        )
        prims += (mimcap, mimcap2)

        aux = _prm.Auxiliary(name="anything_goes")
        prims += aux

        prims += (
            _prm.Spacing(
                primitives1=(nplus, pplus), primitives2=mosgate, min_space=0.25,
            ),
            _prm.Spacing(
                primitives1=active, primitives2=hvox, min_space=0.2,
            ),
            _prm.Spacing(
                primitives1=(nwell, pplus), min_space=2.0,
            ),
            _prm.MinWidth(prim=active.in_(hvox), min_width=0.5),
            _prm.Enclosure(prim=active, by=esd, min_enclosure=_prp.Enclosure(0.1)),
            _prm.NoOverlap(prim1=nplus, prim2=pplus),
        )

        super().__init__(primitives=prims)
tech = Tech()
cktfab = _ckt.CircuitFactory(tech=tech)
layoutfab = _lay.LayoutFactory(tech=tech)
