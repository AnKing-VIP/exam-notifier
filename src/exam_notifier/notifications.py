# -*- coding: utf-8 -*-

# Exam Notifier Add-on for Anki
#
# Copyright (C) 2019-2021  Aristotelis P. <https://glutanimate.com/>
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

from __future__ import annotations

from abc import ABC, abstractproperty
from dataclasses import dataclass
from typing import Optional

from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from aqt.utils import openLink, GetTextDialog

from .deck_config import ExamSettings
from .libaddon.gui.notifications import (
    Notification,
    NotificationHAlignment,
    NotificationService,
    NotificationSettings,
    FocusBehavior,
)

from .consts import ADDON


def maybe_pluralize(count: float, term: str) -> str:
    return term + "s" if abs(count) > 1 else term


class NotificationContent(ABC):
    """Class describing notification content"""

    @abstractproperty
    def message(self) -> str:
        ...


@dataclass
class ExamNotificationContent(NotificationContent):
    days_past_exam: int
    days_until_exam: int
    card_id: int
    exam_settings: ExamSettings

    @property
    def message(self) -> str:
        exam_name = self.exam_settings.exam_name
        exam_name_str = f" {exam_name}" if exam_name else ""
        return f"""\
            
<div style="text-align: right; margin-bottom: 5px;">
<a style="text-decoration: none;" href="#close"><span style="font-size: medium; font-weight: bold; color: #785959;">x</span></a>
</div>
<b>Exam Notifier</b>: Card due past{exam_name_str} exam<br><br>

Next review (<span style="color:green;">Good</span>): <b>{self.days_past_exam}</b>
 {maybe_pluralize(self.days_past_exam, 'day')} after exam
<br>
<center><a style="color: #780000" href="#reschedule:{self.card_id}">Change due date...</a><br>
<span>(<i>{self.days_until_exam}</i> {maybe_pluralize(self.days_until_exam, 'day')}
 until exam)</span></center>
<p style="font-size: small">&nbsp;</p>
<table cellpadding=0 style="margin: 0; padding: 0;" width="100%">
    <td width="50%" align="left">
        <span style="font-size: small; color: #785959;">By Glutanimate & AnKing</span>
    </td>
    <td width="50%" align="right"><a style="text-decoration: underline;" href="#contribute">
        <span style="font-size: small; color: #785959;">♥ Support our Work</span>
    </a></td>
</table>
"""


from .libaddon.gui.dialog_contrib import ContribDialog
from aqt import mw

from .gui.forms import contrib
from .gui import initialize_qt_resources

initialize_qt_resources()


class CollabContributionDialog(ContribDialog):
    def _setupEvents(self):
        self.form.btnGlutanimate.clicked.connect(
            lambda: openLink(ADDON.LINKS["bepatron"])
        )
        self.form.btnAnKing.clicked.connect(
            lambda: openLink("https://patreon.com/ankingmed")
        )


class ExamNotificationLinkhandler(QObject):

    reschedule_requested = pyqtSignal("qint64")
    close_requested = pyqtSignal()

    @pyqtSlot(str)
    def __call__(self, link: str):
        if link.startswith("http"):
            openLink(link)
            return

        command, *data_list = link[1:].split(":", 1)
        data = data_list[0] if data_list else None

        if command == "reschedule" and data is not None:
            card_id = int(data)
            self.reschedule_requested.emit(card_id)
        elif command == "contribute":
            dialog = CollabContributionDialog(contrib, parent=mw)
            dialog.show()
        elif command == "close":
            self.close_requested.emit()

        else:
            print(f"Unrecognized link command {command}")


class NotificationServiceAdapter:
    def __init__(
        self,
        notification_service: NotificationService,
        link_handler: ExamNotificationLinkhandler,
    ):
        self._notification_service = notification_service
        self._link_handler = link_handler

    def notify(
        self,
        notification_content: NotificationContent,
        notification_settings: Optional[NotificationSettings] = None,
    ):
        if not notification_settings:
            notification_settings = NotificationSettings(
                align_horizontal=NotificationHAlignment.center,
                space_vertical=100,
                bg_color="#fdf0d5",
                fg_color="#003049",
                duration=None,
                dismiss_on_click=False,
                focus_behavior=FocusBehavior.close_on_window_focus_lost,
                focus_behavior_exceptions=[GetTextDialog],
            )
            # ^ add exception to keep notification open for reschedule dialog

        self._notification_service.notify(
            message=notification_content.message,
            link_handler=self._link_handler,
            settings=notification_settings,
            pre_show_callback=self.on_notification_will_show,
        )

    def close_current_notification(self):
        self._notification_service.close_current_notification()

    def on_notification_will_show(self, notification: Notification):
        notification.setFrameStyle(QFrame.NoFrame)
        notification.setContentsMargins(10, 3, 5, 5)
