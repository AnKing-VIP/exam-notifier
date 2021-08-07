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

from typing import TYPE_CHECKING, NamedTuple, Optional, Union

if TYPE_CHECKING:
    from anki.decks import DeckConfigDict, DeckId, DeckManager
    from aqt.main import AnkiQt

DeckIdType = Union["DeckId", int]


class ExamSettings(NamedTuple):
    enabled: bool = False  # exam notifications enabled
    exam_name: str = ""
    exam_date: Optional[int] = None  # secs since epoch


class DeckConfigError(Exception):
    pass


class DeckConfigService:
    def __init__(self, main_window: "AnkiQt", settings_key: str):
        self._main_window = main_window
        self._settings_key = settings_key

    def get_settings_for_did(self, deck_id: DeckIdType) -> ExamSettings:
        deck_config = self._config_dict_for_deck_id(deck_id)
        return self.get_settings(deck_config=deck_config)

    def get_settings(self, deck_config: "DeckConfigDict") -> ExamSettings:
        """
        Gets add-on settings from deck configuration, mutates configuration
        with default settings if not existing
        """
        if not deck_config.get(self._settings_key):
            default_settings = ExamSettings()
            deck_config[self._settings_key] = default_settings._asdict()
            return default_settings

        exam_settings_dict = deck_config[self._settings_key]

        return ExamSettings(**exam_settings_dict)

    def set_settings_for_did(self, deck_id: DeckIdType, settings: ExamSettings):
        deck_config = self._config_dict_for_deck_id(deck_id)
        self.set_settings(deck_config=deck_config, settings=settings)

    def set_settings(self, deck_config: "DeckConfigDict", settings: ExamSettings):
        try:
            self._deck_manager.update_config(deck_config)
        except AttributeError:
            self._deck_manager.updateConf(deck_config)  # type: ignore[attr-defined]

    def _config_dict_for_deck_id(self, deck_id: DeckIdType) -> "DeckConfigDict":
        try:  # 2.1.45+
            return self._deck_manager.config_dict_for_deck_id(
                deck_id  # type: ignore[arg-type]
            )
        except AttributeError:
            return self._deck_manager.confForDid(deck_id)  # type: ignore[attr-defined]

    @property
    def _deck_manager(self) -> "DeckManager":
        if (collection := self._main_window.col) is None:
            raise DeckConfigError("User collection is not loaded")

        return collection.decks
