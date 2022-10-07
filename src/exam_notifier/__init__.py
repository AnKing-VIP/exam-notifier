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
Initializes add-on components.
"""

from typing import TYPE_CHECKING, Final
from pathlib import Path

from aqt import mw

from ._version import __version__  # noqa: F401
from .consts import ADDON
from .deck_config import DeckConfigService
from .deck_options_legacy import (
    DeckConfigDialogSubscriber,
    DeckConfigDialogService,
    ExamConfigTab,
)
from .libaddon.consts import set_addon_properties
from .notifications import ExamNotificationLinkhandler, NotificationServiceAdapter
from .reviewer import ReviewerSubscriber, ReviewService

from .libaddon.gui.notifications import NotificationService
from .libaddon.platform import is_anki_version_in_range

if TYPE_CHECKING:
    assert mw is not None

# Constants ####

EXAM_SETTINGS_KEY: Final = "exam_settings"

set_addon_properties(ADDON)

# Deck config access ####

deck_config_service = DeckConfigService(main_window=mw, settings_key=EXAM_SETTINGS_KEY)

# Deck options dialog ####

# Qt (Anki <= 2.1.44 and any Anki with V1 scheduler)

deck_config_dialog_service = DeckConfigDialogService(
    settings_key=EXAM_SETTINGS_KEY,
    deck_config_service=deck_config_service,
    deck_config_tab_factory=ExamConfigTab,
)
deck_config_dialog_subscriber = DeckConfigDialogSubscriber(deck_config_dialog_service)
deck_config_dialog_subscriber.subscribe()

# Web (new)

if is_anki_version_in_range("2.1.45"):
    from .deck_options import (
        WebContentInjector,
        DeckOptionsPatcher,
        DeckOptionsSubscriber,
    )

    web_folder_path = web_folder_path = Path(__file__).parent / "web"

    web_content_injector = WebContentInjector(
        source_folder=web_folder_path, web_files_name_stem="deck_options"
    )
    deck_options_patcher = DeckOptionsPatcher(
        main_window=mw, web_content_injector=web_content_injector, deck_config_service=deck_config_service
    )
    deck_options_subscriber = DeckOptionsSubscriber(
        deck_options_patcher=deck_options_patcher
    )
    deck_options_subscriber.subscribe()

# Notifications ####

notification_link_handler = ExamNotificationLinkhandler()
notification_service = NotificationService(progress_manager=mw.progress, parent=mw)
notification_service_adapter = NotificationServiceAdapter(
    notification_service=notification_service, link_handler=notification_link_handler
)
notification_link_handler.close_requested.connect(
    notification_service.close_current_notification
)

# Reviewer ####

review_service = ReviewService(
    main_window=mw,
    deck_config_service=deck_config_service,
    notification_service_adapter=notification_service_adapter,
)

notification_link_handler.reschedule_requested.connect(
    review_service.interactively_reschedule_card
)

reviewer_subscriber = ReviewerSubscriber(review_service=review_service)
reviewer_subscriber.subscribe()
