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


from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from anki.consts import QUEUE_TYPE_REV

from .deck_config import DeckConfigService
from .errors import AnkiObjectError
from .notifications import ExamNotification, NotificationService

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.collection import Collection
    from aqt.main import AnkiQt
    from aqt.reviewer import Reviewer


class ReviewService:
    def __init__(
        self,
        main_window: "AnkiQt",
        deck_config_service: DeckConfigService,
        notification_service: NotificationService,
    ):
        self._main_window = main_window
        self._deck_config_service = deck_config_service
        self._notification_service = notification_service

    def on_reviewer_did_show_question(self, card: "Card"):
        if card.queue != QUEUE_TYPE_REV:  # not a review
            return

        exam_settings = self._deck_config_service.get_settings_for_did(
            card.odid or card.did
        )
        if not exam_settings.enabled or not exam_settings.exam_date:
            return

        datetime_now = datetime.now()
        datetime_exam = datetime.fromtimestamp(exam_settings.exam_date)

        if datetime_now > datetime_exam:
            return

        # TODO: Unstable API, find alternative or file PR
        ease_good = self._reviewer._defaultEase()

        days_till_next_review = self._collection.sched.nextIvl(card, ease_good) / 86400

        datetime_next_review = datetime_now + timedelta(days=days_till_next_review)

        if datetime_next_review < datetime_exam:
            return

        days_past_exam = (datetime_next_review - datetime_exam).days

        notification = ExamNotification(
            days_past_exam=days_past_exam, exam_settings=exam_settings
        )

        self._notification_service.notify(
            notification=notification, parent=self._main_window
        )

    @property
    def _reviewer(self) -> "Reviewer":
        return self._main_window.reviewer

    @property
    def _collection(self) -> "Collection":
        if (collection := self._main_window.col) is None:
            raise AnkiObjectError("Collection is not loaded or not ready")
        return collection


class ReviewerSubscriber:
    def __init__(self, review_service: ReviewService):
        self._review_service = review_service

    def subscribe(self):
        from aqt.gui_hooks import reviewer_did_show_question

        reviewer_did_show_question.append(
            self._review_service.on_reviewer_did_show_question
        )
