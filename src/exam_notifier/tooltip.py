# -*- coding: utf-8 -*-

# Exam Notifier Add-on for Anki
#
# Copyright (C) 2019-2020  Aristotelis P. <https://glutanimate.com/>
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
Module template.
"""


from anki.hooks import addHook
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from datetime import datetime, timedelta

from .config import config

try:  # >= 2.1.21
    from anki.consts import QUEUE_TYPE_REV
except (ImportError, ModuleNotFoundError, AttributeError):
    QUEUE_TYPE_REV = 2


def onQuestionShown(*args, **kwargs):
    reviewer: Reviewer = mw.reviewer

    try:
        sched = mw.col.sched
        card = reviewer.card
    except AttributeError:
        raise

    if card.queue != QUEUE_TYPE_REV:
        # not a review card
        return

    try:
        exam_date_str = config["local"]["exam_date"]
    except KeyError:
        return

    if not exam_date_str:
        return

    ease_good = reviewer._defaultEase()

    # next ivl for "good"
    nextIvl = sched.nextIvl(card, ease_good) / 86400

    try:
        date_obj_exam = datetime.strptime(exam_date_str, "%Y/%m/%d")
    except ValueError:
        return

    date_obj_next = datetime.now() + timedelta(days=nextIvl)

    if date_obj_next < date_obj_exam:
        return

    days_after = (date_obj_next - date_obj_exam).days

    # TODO: use mw.col.sched.answerButtons(card) to check for hard and easy

    tooltip(
        f"""
<b>Exam Notifier</b><br>
If you answer this card with <span style="color:green;">Good</span><br>you will
see it {days_after} days after your exam.
"""
    )


def initializeTooltip():
    try:  # >=2.1.20
        from aqt import gui_hooks

        gui_hooks.reviewer_did_show_question.append(onQuestionShown)
    except (ImportError, ModuleNotFoundError, AttributeError):
        addHook("showQuestion", onQuestionShown)
