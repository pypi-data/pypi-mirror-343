# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
import abc
from typing import Iterable, Optional

from .. import _util
from ..technology import geometry as _geo, technology_ as _tch
from . import layout as _lay, circuit as _ckt

__all__ = ["Cell", "OnDemandCell", "CellsT"]


class Cell:
    """A cell is an element from a `Library` and represents the building blocks
    of a circuit. A cell may contain one or more circuits and one or more layouts.

    API Notes:
        User supported ways for creating cells is not fixed. Backwards incompatible
        changes are still expected.
    """
    def __init__(self, *,
        name: str,
        tech: _tch.Technology, cktfab: _ckt.CircuitFactory, layoutfab: _lay.LayoutFactory,
    ):
        self._name = name
        self._tech = tech
        self._cktfab = cktfab
        self._layoutfab = layoutfab

        self._circuit: Optional[_ckt.CircuitT] = None
        self._layout: Optional[_lay.LayoutT] = None

    @property
    def name(self) -> str:
        return self._name
    @property
    def tech(self) -> _tch.Technology:
        return self._tech
    @property
    def cktfab(self) -> _ckt.CircuitFactory:
        return self._cktfab
    @property
    def layoutfab(self) -> _lay.LayoutFactory:
        return self._layoutfab

    @property
    def circuit(self) -> _ckt.CircuitT:
        if self._circuit is None:
            raise AttributeError(f"Cell '{self.name}' has no circuit")
        return self._circuit

    @property
    def layout(self) -> _lay.LayoutT:
        if self._layout is None:
            raise AttributeError(f"Cell '{self.name}' has no layout")
        return self._layout

    def new_circuit(self, *, name: Optional[str]=None) -> _ckt.CircuitT:
        """Create a new empty circuit for the cell.

        Arguments:
            name: the name of the circuit. If not specified the same name as the
                cell will be used.
        """
        if name is None:
            name = self.name

        self._circuit = circuit = self.cktfab.new_circuit(name=name)
        return circuit

    def new_layout(self, *,
        name: Optional[str]=None, boundary: Optional[_geo._Rectangular]=None,
    ) -> "_lay.LayoutT":
        """Create a new empty layout for the cell.

        Arguments:
            name: the name of the circuit. If not specified the same name as the
                cell will be used.
            boundary: optional boundary for the layout
        """
        if name is None:
            name = self.name

        self._layout = layout = self.layoutfab.new_layout(boundary=boundary)
        return layout

    def new_circuitlayouter(self, *,
        boundary: Optional[_geo._Rectangular]=None,
    ) -> "_lay.CircuitLayouterT":
        """Create a circuit layouter for a circuit of the cell.

        API Notes:
            _CircuitLayouter API is not fixed.
                see: https://gitlab.com/Chips4Makers/PDKMaster/-/issues/25
        """
        if self._circuit is None:
            raise ValueError(f"Cell '{self.name}' has no circuit to layout")
        if self._layout is not None:
            raise ValueError(f"Cell '{self.name}' already has a layout")

        layouter = self.layoutfab.new_circuitlayouter(
            circuit=self._circuit, boundary=boundary,
        )
        self._layout = layouter.layout
        return layouter

    @property
    def subcells_sorted(self) -> Iterable["Cell"]:
        if self._circuit is None:
            # If the cell has no circuit is has no subcells
            return
        cells = set()
        for cell in self._circuit.subcells_sorted:
            if cell not in cells:
                yield cell
                cells.add(cell)
CellsT = _util.ExtendedListStrMapping[Cell]


class OnDemandCell(Cell, abc.ABC):
    """_Cell with on demand circuit and layout creation

    The circuit and layout will only be generated the first time it is accessed.
    """
    @property
    def circuit(self) -> _ckt.CircuitT:
        if self._circuit is None:
            self._create_circuit_()
        if self._circuit is None:
            raise AttributeError(
                f"Calling _create_circuit_() for cell '{self.name}' did not create a cirvcuit",
            )
        return self._circuit

    @property
    def layout(self) -> _lay.LayoutT:
        if self._layout is None:
            self._create_layout_()
        if self._layout is None:
            raise AttributeError(
                f"Calling _create_layout_() for cell '{self.name}' did not create a layout",
            )
        return self._layout

    @abc.abstractmethod
    def _create_circuit_(self):
        """The _create_circuit_() abstract method needs to be implemented by child classes
        to generate the cell circuit on demand. After this method has been called the
        cell needs to have a circuit.
        """
        ... # pragma: no cover

    @abc.abstractmethod
    def _create_layout_(self):
        """The _create_layout_() abstract method needs to be implemented by child classes
        to generate the cell layout on demand. After this method has been called the
        cell needs to have a layout.
        """
        ... # pragma: no cover
