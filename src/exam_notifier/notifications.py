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

from PyQt5.QtCore import QObject, pyqtSignal

from .deck_config import ExamSettings
from .libaddon.gui.notifications import (
    Notification,
    NotificationHAlignment,
    NotificationService,
    NotificationSettings,
)


class NotificationContent(ABC):
    """Class describing notification content"""

    @abstractproperty
    def message(self) -> str:
        ...


@dataclass
class ExamNotificationContent(NotificationContent):
    days_past_exam: int
    card_id: int
    exam_settings: ExamSettings

    @property
    def message(self) -> str:
        exam_name = self.exam_settings.exam_name
        exam_name_str = f" <b>{exam_name}</b>" if exam_name else ""
        return f"""
<b>Exam Notifier</b><br>
If you answer this card with <span style="color:green;">Good</span> you will<br>
see it <b>{self.days_past_exam}</b> days after your{exam_name_str} exam.<br>
<center><a href="#reschedule:{self.card_id}">Reschedule Now...</a></center>
"""


class ExamNotificationLinkhandler(QObject):

    reschedule_requested = pyqtSignal("qint64")

    def __call__(self, link: str):
        command, *data_list = link[1:].split(":", 1)
        data = data_list[0] if data_list else None

        if command == "reschedule" and data is not None:
            card_id = int(data)
            self.reschedule_requested.emit(card_id)

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
        settings = NotificationSettings(
            align_horizontal=NotificationHAlignment.center,
            space_vertical=100,
            bg_color="#e8ffa6",
            dismiss_on_click=False,
            duration=None,
        )

        self._notification_service.notify(
            message=notification_content.message,
            link_handler=self._link_handler,
            settings=settings,
            pre_show_callback=self.on_notification_will_show,
        )

    def close_current_notification(self):
        self._notification_service.close_current_notification()

    def on_notification_will_show(self, notification: Notification):
        notification.setFrameStyle(QFrame.NoFrame)
        # notification.setLineWidth(2)
        notification.setContentsMargins(10, 10, 10, 10)
        notification.setStyleSheet("QLabel{ border-radius: 25px; }")
