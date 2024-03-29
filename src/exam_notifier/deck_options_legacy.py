# -*- coding: utf-8 -*-

# Exam Notifier Add-on for Anki
#
# Copyright (C) 2019-2022  Aristotelis P. <https://glutanimate.com/>
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
Additions to Anki's deck options dialog
"""

from dataclasses import asdict
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Type

from aqt.deckconf import DeckConf
from aqt.qt import QDateTime, QIcon, QPixmap, QSize, QWidget

from .gui import asset_provider
from .gui.forms import deckconf_exam_tab

if TYPE_CHECKING:
    from anki.decks import DeckConfigDict

from aqt.utils import openLink

from .consts import ADDON
from .deck_config import DeckConfigService, ExamSettings


class ExamConfigTab(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.form = deckconf_exam_tab.Ui_Form()
        self.form.setupUi(self)
        unix_time_now = int(round(datetime.now().timestamp()))
        self.form.exam_date.setMinimumDateTime(
            self._qdatetime_from_epoch(unix_time_now)
        )
        self.form.btnGlutanimate.clicked.connect(
            lambda: openLink("https://patreon.com/glutanimate")
        )
        self.form.btnAnKing.clicked.connect(
            lambda: openLink("https://www.theanking.com/anking-memberships")
        )
        for button in (self.form.btnGlutanimate, self.form.btnAnKing):
            icon = asset_provider.get_icon("icons/patreon.svg")
            button.setIcon(icon)
            button.setIconSize(QSize(32, 32))

    def set_settings(self, settings: ExamSettings):
        self.form.exam_group_box.setChecked(settings.enabled)
        self.form.exam_name.setText(settings.exam_name)
        if settings.exam_date is not None:
            self.form.exam_date.setDateTime(
                self._qdatetime_from_epoch(settings.exam_date)
            )

    def get_settings(self) -> ExamSettings:
        enabled = self.form.exam_group_box.isChecked()
        exam_name = self.form.exam_name.text()
        exam_date = self._epoch_from_qdatetime(self.form.exam_date.dateTime())
        return ExamSettings(enabled=enabled, exam_name=exam_name, exam_date=exam_date)

    @staticmethod
    def _qdatetime_from_epoch(unix_epoch: int) -> QDateTime:
        qdatetime = QDateTime.fromSecsSinceEpoch(unix_epoch)
        return qdatetime

    @staticmethod
    def _epoch_from_qdatetime(qdatetime: QDateTime) -> int:
        return int(round(qdatetime.toSecsSinceEpoch()))


class DeckConfigDialogService:
    def __init__(
        self,
        settings_key: str,
        deck_config_service: DeckConfigService,
        deck_config_tab_factory: Type[ExamConfigTab],
    ):
        self._settings_key = settings_key
        self._deck_config_service = deck_config_service
        self._factory = deck_config_tab_factory

    def on_deck_config_gui_loaded(self, deck_conf_dialog: DeckConf, *args):
        deck_config_tab = self._factory(parent=deck_conf_dialog)
        deck_conf_dialog.form.tabWidget.insertTab(
            3, deck_config_tab, deck_config_tab.windowTitle()
        )
        setattr(deck_conf_dialog, self._settings_key, deck_config_tab)

    def on_deck_config_loaded(self, deck_conf_dialog: DeckConf, *args):
        exam_settings_page: Optional[ExamConfigTab] = getattr(
            deck_conf_dialog, self._settings_key, None
        )
        if not exam_settings_page:
            return

        if not hasattr(deck_conf_dialog, self._settings_key):
            return

        deck_config: Optional["DeckConfigDict"] = deck_conf_dialog.conf
        if not deck_config:
            return

        exam_settings = self._deck_config_service.get_settings(deck_config=deck_config)
        exam_settings_page.set_settings(exam_settings)

    def on_deck_config_will_save(self, deck_conf_dialog: DeckConf, *args):
        exam_settings_page: Optional[ExamConfigTab] = getattr(
            deck_conf_dialog, self._settings_key, None
        )
        if not exam_settings_page:
            return

        deck_config: Optional["DeckConfigDict"] = deck_conf_dialog.conf
        if not deck_config:
            return

        exam_deck_settings = exam_settings_page.get_settings()
        deck_config[self._settings_key] = asdict(exam_deck_settings)
        # deck config dialog handles updating


class DeckConfigDialogSubscriber:
    def __init__(self, deck_config_service: DeckConfigDialogService):
        self._deck_config_service = deck_config_service

    def subscribe(self):
        from aqt.gui_hooks import (
            deck_conf_did_load_config,
            deck_conf_did_setup_ui_form,
            deck_conf_will_save_config,
        )

        deck_conf_did_setup_ui_form.append(
            self._deck_config_service.on_deck_config_gui_loaded
        )
        deck_conf_did_load_config.append(
            self._deck_config_service.on_deck_config_loaded
        )
        deck_conf_will_save_config.append(
            self._deck_config_service.on_deck_config_will_save
        )
