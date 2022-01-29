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

if TYPE_CHECKING:
    from aqt.main import AnkiQt


class WebContentInjector:

    _html_placeholder = "HTML_CONTENT"

    def __init__(self, source_folder: Path, web_files_name_stem: str):
        html_path = source_folder / f"{web_files_name_stem}.html"
        js_path = source_folder / f"{web_files_name_stem}.js"

        with html_path.open() as html_file:
            html = html_file.read()
        with js_path.open() as js_file:
            js = js_file.read()

        self._js = js.replace(self._html_placeholder, json.dumps(html))

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
        self._web_content_injector.inject(deck_options_dialog.web)

    def on_webview_did_receive_js_message(
        self, handled: Tuple[bool, Any], message: str, context: Any
    ):
        """Major hack: Invoke old options dialog and navigate to Exams tab"""
        if not message.startswith(self._pycmd_identifier):
            return handled

        identifier, context, command = message.split(":")

        if context != self._context or command != "old_options":
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

        deck_legacy = self._main_window.col.decks.get(DeckId(deck["id"]))

        if deck_legacy is None:
            return handled

        deck_options_dialog.close()
        self._deck_options_dialog_reference = None

        def on_deck_conf_dialog_will_show(deck_conf: DeckConf):
            tab_widget = deck_conf.form.tabWidget

            exams_tab_index = None

            for index in range(tab_widget.count()):
                tab_name = tab_widget.tabText(index)
                if tab_name == "Exams":
                    exams_tab_index = index
                    break

            if exams_tab_index is None:
                return

            tab_widget.setCurrentIndex(exams_tab_index)

        gui_hooks.deck_conf_will_show.append(on_deck_conf_dialog_will_show)

        DeckConf(self._main_window, deck_legacy)

        gui_hooks.deck_conf_will_show.remove(on_deck_conf_dialog_will_show)

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
