
from typing import *



from dataclasses import dataclass
import logging

from PySide6.QtWebEngineCore import QWebEngineSettings
import edifice as ed
from edifice.engine import (
    CommandType,
    Element,
    QtWidgetElement,
    _WidgetTree,
)
from edifice.qt import QT_VERSION
if QT_VERSION == "PyQt6" and not tp.TYPE_CHECKING:
    from PyQt6 import QtCore, QtGui, QtSvg, QtSvgWidgets, QtWidgets, QtWebEngineWidgets
else:
    from PySide6 import QtCore, QtGui, QtSvg, QtSvgWidgets, QtWidgets
    from PySide6 import QtWebEngineWidgets

class WebEngineView(QtWidgetElement[QtWebEngineWidgets.QWebEngineView]):
    """Widget to display a website.

    .. highlights::
        - Underlying Qt Widget
          `QWebEngineView <https://doc.qt.io/qtforpython-6/PySide6/QtWebEngineWidgets/QWebEngineView.html>`_

    .. rubric:: Props

    All **props** from :class:`QtWidgetElement` plus:

    Args:
        url: The address of the website to display.

    .. rubric:: Usage

    Render rich text with the
    `Qt supported HTML subset <https://doc.qt.io/qtforpython-6/overviews/richtext-html-subset.html>`_.

    .. code-block:: python

        WebEngineView(url="https://www.google.com/")
    """

    def __init__(
        self,
        url: str="",
        html: str="",
        # showScrollBars=True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._register_props(
            {
                "url": url,
                "html":html
            },
        )
        self._register_props(kwargs)

    def _initialize(self):
        self.underlying = QtWebEngineWidgets.QWebEngineView()
        self.underlying.setObjectName(str(id(self)))

    def _qt_update_commands(
        self,
        widget_trees: dict[Element, _WidgetTree],
        newprops,
    ):
        if self.underlying is None:
            self._initialize()
        assert self.underlying is not None

        # TODO None of this code is working.
        # > size = self.underlying.font().pointSize()
        # > self._set_size(size * len(self.props.text), size, lambda size: (size * len(str(self.props.text)), size))
        # https://github.com/pyedifice/pyedifice/issues/41

        commands = super()._qt_update_commands_super(widget_trees, newprops, self.underlying, None)
        if "url" in newprops:
            commands.append(CommandType(self.underlying.setUrl, newprops.url))
        if "html" in newprops:
            commands.append(CommandType(self.underlying.setHtml, newprops.html))
        # if "showScrollBars" in newprops:
        #     try:
        #         def setShowScrollbars(value, underlying=self.underlying):
        #             print("setShowScrollbars", value, underlying)
        #             settings = self.underlying.settings()
        #             settings.setAttribute(QWebEngineSettings.ShowScrollBars, value)
        #         commands.append(CommandType(setShowScrollbars, newprops.html))
        #     except Exception as err:
        #         print(err, flush=True)

        return commands