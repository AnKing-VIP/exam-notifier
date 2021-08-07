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

from abc import ABC, abstractproperty
from dataclasses import dataclass
from typing import Optional

from aqt.utils import tooltip
from PyQt5.QtWidgets import QWidget

from .deck_config import ExamSettings

@dataclass  # type: ignore[misc]  # https://github.com/python/mypy/issues/5374
class _AbstractNotification(ABC):
    @abstractproperty
    def message(self) -> str:
        ...


@dataclass  # type: ignore[misc]
class ExamNotification(_AbstractNotification):
    days_past_exam: int
    exam_settings: ExamSettings

    @property
    def message(self) -> str:
        exam_name = self.exam_settings.exam_name
        exam_name_str = f" <b>{exam_name}</b>" if exam_name else ""
        return f"""
<b>Exam Notifier</b><br>
If you answer this card with <span style="color:green;">Good</span> you will<br>
see it <b>{self.days_past_exam}</b> days after your{exam_name_str} exam.
"""


class NotificationService:
    def notify(
        self,
        notification: _AbstractNotification,
        period: int = 3000,
        parent: Optional[QWidget] = None,
    ):
        # TODO: custom notification system
        tooltip(msg=notification.message, period=period, parent=parent)
