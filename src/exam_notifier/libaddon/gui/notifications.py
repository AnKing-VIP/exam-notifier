# -*- coding: utf-8 -*-

# Libaddon for Anki
#
# Copyright (C) 2018-2021  Aristotelis P. <https//glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

"""
Customizable notification pop-up
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Callable, Optional

from PyQt5.QtCore import QObject, QPoint, Qt, QTimer
from PyQt5.QtGui import QColor, QMouseEvent, QPalette, QResizeEvent
from PyQt5.QtWidgets import QFrame, QLabel, QWidget

if TYPE_CHECKING:
    from aqt.progress import ProgressManager


class NotificationHAlignment(Enum):
    left = "left"
    center = "center"
    right = "right"


class NotificationVAlignment(Enum):
    top = "top"
    center = "center"
    bottom = "bottom"


@dataclass
class NotificationSettings:
    """Notification settings

    Args:
        duration: Time in ms the notification should be shown for. Set to None or 0
                  for a persistent tooltip that has to be dismissed manually
    """

    duration: Optional[int] = 3000
    align_horizontal: NotificationHAlignment = NotificationHAlignment.left
    align_vertical: NotificationVAlignment = NotificationVAlignment.bottom
    space_horizontal: int = 0
    space_vertical: int = 0
    fg_color: str = "#000000"
    bg_color: str = "#FFFFFF"
    dismiss_on_click: bool = True


class NotificationService(QObject):
    def __init__(
        self,
        progress_manager: "ProgressManager",
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent=parent)
        self._parent = parent
        self._progress_manager = progress_manager

        self._current_timer: Optional[QTimer] = None
        self._current_instance: Optional["Notification"] = None

    def notify(
        self,
        message: str,
        settings: NotificationSettings,
        link_handler: Optional[Callable[[str], None]] = None,
        pre_show_callback: Optional[Callable[["Notification"], None]] = None,
    ):
        self.close_current_notification()

        notification = Notification(
            text=message, settings=settings, parent=self._parent
        )
        if link_handler:
            notification.setOpenExternalLinks(False)
            notification.linkActivated.connect(link_handler)

        if pre_show_callback:
            pre_show_callback(notification)

        notification.show()

        self._current_instance = notification

        if settings.duration:
            self._current_timer = self._progress_manager.timer(
                3000, self.close_current_notification, False
            )

    def close_current_notification(self):
        if self._current_instance:
            try:
                self._current_instance.deleteLater()
            except:  # noqa: E722
                # already deleted as parent window closed
                pass
            self._current_instance = None
        if self._current_timer:
            self._current_timer.stop()
            self._current_timer = None


class Notification(QLabel):

    # Anki dialog manager support
    silentlyClose = True

    def __init__(
        self,
        text: str,
        settings: NotificationSettings = NotificationSettings(),
        parent: Optional[QWidget] = None,
        **kwargs,
    ):
        super().__init__(text, parent=parent, **kwargs)
        self._settings = settings

        self.setFrameStyle(QFrame.Panel)
        self.setLineWidth(2)
        self.setWindowFlags(Qt.ToolTip)
        self.setContentsMargins(10, 10, 10, 10)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(self._settings.bg_color))
        palette.setColor(QPalette.WindowText, QColor(self._settings.fg_color))
        self.setPalette(palette)

    def mousePressEvent(self, event: QMouseEvent):
        if (
            not self._settings.dismiss_on_click
            or self.cursor().shape() == Qt.PointingHandCursor
        ):
            # Do not ignore mouse press event if configured that way and/or
            # currently hovering link (as signaled by cursor shape)
            return super().mousePressEvent(event)
        event.accept()
        self.hide()

    def resizeEvent(self, event: QResizeEvent) -> None:
        # true geometry is only known once resizeEvent fires
        self._setPosition()
        super().resizeEvent(event)

    def _setPosition(self):
        align_horizontal = self._settings.align_horizontal
        align_vertical = self._settings.align_vertical

        if align_horizontal == NotificationHAlignment.left:
            x = 0 + self._settings.space_horizontal
        elif align_horizontal == NotificationHAlignment.right:
            x = self.parent().width() - self.width() - self._settings.space_horizontal
        elif align_horizontal == NotificationHAlignment.center:
            x = (self.parent().width() - self.width()) / 2
        else:
            raise ValueError(f"Alignment value {align_horizontal} is not supported")

        if align_vertical == NotificationVAlignment.top:
            y = 0 + self._settings.space_vertical
        elif align_vertical == NotificationVAlignment.bottom:
            y = self.parent().height() - self.height() - self._settings.space_vertical
        elif align_vertical == NotificationVAlignment.center:
            y = (self.parent().height() - self.height()) / 2
        else:
            raise ValueError(f"Alignment value {align_vertical} is not supported")

        self.move(
            self.parent().mapToGlobal(QPoint(x, y))  # type:ignore
        )
