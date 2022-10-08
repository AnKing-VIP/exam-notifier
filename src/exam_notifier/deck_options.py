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


"""
Support for new deck options
"""

import json
import weakref
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Tuple
from weakref import ReferenceType

from aqt import gui_hooks

from anki.decks import DeckId
from aqt.deckconf import DeckConf
from aqt.deckoptions import DeckOptionsDialog
from aqt.webview import AnkiWebView
from aqt.utils import openLink

if TYPE_CHECKING:
    from aqt.main import AnkiQt

from .deck_config import DeckConfigService, ExamSettings


class WebContentInjector:
    def __init__(self, source_folder: Path, web_files_name_stem: str):
        svelte_path = source_folder / f"{web_files_name_stem}.js"

        with svelte_path.open() as js_file:
            js = js_file.read()
        self._js = js
        
    def inject(self, web_view: AnkiWebView):
        web_view.eval(self._js)


class DeckOptionsPatcher:

    _pycmd_identifier = "exam_notifier"
    _context = "deck_options"

    def __init__(self, main_window: "AnkiQt", web_content_injector: WebContentInjector):
        self._main_window = main_window
        self._web_content_injector = web_content_injector
        self._deck_options_dialog_reference: Optional[
            ReferenceType[DeckOptionsDialog]
        ] = None

    def on_deck_options_did_load(self, deck_options_dialog: DeckOptionsDialog):
        self._deck_options_dialog_reference = weakref.ref(deck_options_dialog)
        col = self._main_window.col
        if col is None:
            return
        self._web_content_injector.inject(deck_options_dialog.web)

    def on_webview_did_receive_js_message(
        self, handled: Tuple[bool, Any], message: str, context: Any
    ):
        """Major hack: Invoke old options dialog and navigate to Exams tab"""
        if not message.startswith(self._pycmd_identifier):
            return handled

        identifier, context, command, value = message.split(":")

        if context != self._context:
            return handled

        if self._deck_options_dialog_reference is None:
            return handled

        deck_options_dialog: Optional[
            DeckOptionsDialog
        ] = self._deck_options_dialog_reference()

        if deck_options_dialog is None:
            return handled

        if self._main_window.col is None:
            return handled

        deck = getattr(deck_options_dialog, "_deck", None)

        if deck is None:
            print("Could not access deck attribute in DeckOptions")
            return handled

        if command == "open_link":
            if value == "glutanimate":
                openLink("https://www.patreon.com/glutanimate")
            elif value == "anking":
                openLink("https://www.patreon.com/ankingmed")
            return (True, None)
        return handled

class DeckOptionsSubscriber:
    def __init__(self, deck_options_patcher: DeckOptionsPatcher):
        self._deck_options_patcher = deck_options_patcher

    def subscribe(self):
        gui_hooks.deck_options_did_load.append(
            self._deck_options_patcher.on_deck_options_did_load
        )

        gui_hooks.webview_did_receive_js_message.append(
            self._deck_options_patcher.on_webview_did_receive_js_message
        )
