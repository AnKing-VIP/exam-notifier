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

from typing import TYPE_CHECKING, NamedTuple, Optional, Type

if TYPE_CHECKING:
    from aqt.main import AnkiQt
    from anki.decks import DeckConfig

class ExamSettings(NamedTuple):
    enabled: bool = False  # exam notifications enabled
    exam_name: str = ""
    exam_date: Optional[int] = None  # secs since epoch


class DeckConfigService:
    def __init__(self, main_window: "AnkiQt", settings_key: str):
        self._main_window = main_window
        self._settings_key = settings_key
    
    def get_settings_for_did(self, deck_id: int) -> ExamSettings:
        deck_config: "DeckConfig" = self._main_window.col.decks.confForDid(deck_id)

        return self.get_settings(deck_config)
    
    def get_settings(self, deck_config: "DeckConfig") -> ExamSettings:
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
    
    def set_settings(self, deck_id: int, settings: ExamSettings):
        deck_config: "DeckConfig" = self._main_window.col.decks.confForDid(deck_id)
        
        