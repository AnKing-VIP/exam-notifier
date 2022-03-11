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


from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from anki.consts import QUEUE_TYPE_REV
from aqt.qt import QObject, pyqtSlot
from aqt.utils import showWarning

from .consts import ADDON
from .deck_config import DeckConfigService
from .errors import AnkiObjectError
from .notifications import ExamNotificationContent, NotificationServiceAdapter

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.collection import Collection
    from aqt.main import AnkiQt
    from aqt.reviewer import Reviewer


class ReviewService(QObject):
    def __init__(
        self,
        main_window: "AnkiQt",
        deck_config_service: DeckConfigService,
        notification_service_adapter: NotificationServiceAdapter,
    ):
        super().__init__(main_window)
        self._main_window = main_window
        self._deck_config_service = deck_config_service
        self._notification_service_adapter = notification_service_adapter

    def on_reviewer_did_show_answer(self, card: "Card"):
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
        days_until_exam = (datetime_exam - datetime_now).days

        notification_content = ExamNotificationContent(
            days_past_exam=days_past_exam,
            days_until_exam=days_until_exam,
            exam_settings=exam_settings,
            card_id=int(card.id),
        )

        self._notification_service_adapter.notify(
            notification_content=notification_content
        )

    def on_reviewer_did_show_question(self, *args, **kwargs):
        self._notification_service_adapter.close_current_notification()

    def on_main_window_state_will_change(self, new_state: str, old_state: str):
        if old_state == "review" and new_state != "review":
            self._notification_service_adapter.close_current_notification()

    @pyqtSlot("qint64")
    def interactively_reschedule_card(self, card_id: int):
        # TODO: File a PR to allow specifying custom default text for
        # set_due_date_dialog, prefilling a sensible time before the exam
        if self._reviewer.card and self._reviewer.card.id == card_id:
            self._reviewer.on_set_due()
        else:
            showWarning(
                text="Rescheduling prevented as Reviewer has moved to different card",
                title=ADDON.NAME,
            )

        # from anki.collection import Config
        #
        # try:
        #     from aqt.operations.scheduling import set_due_date_dialog
        # except (ImportError, ModuleNotFoundError):
        #     from aqt.scheduling import set_due_date_dialog  # type: ignore
        #
        #     if op := set_due_date_dialog(
        #         parent=self._main_window,
        #         card_ids=[card_id],  # type: ignore[list-item]
        #         config_key=Config.String.SET_DUE_REVIEWER,
        #     ):
        #         op.run_in_background()

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
        from aqt.gui_hooks import (
            reviewer_did_show_answer,
            reviewer_did_show_question,
            state_will_change,
        )

        reviewer_did_show_answer.append(
            self._review_service.on_reviewer_did_show_answer
        )
        reviewer_did_show_question.append(
            self._review_service.on_reviewer_did_show_question
        )
        state_will_change.append(self._review_service.on_main_window_state_will_change)
