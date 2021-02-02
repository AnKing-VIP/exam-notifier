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

"""
Reviewer tooltip
"""


from datetime import datetime, timedelta

from anki.hooks import addHook
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import tooltip

try:  # >= 2.1.21
    from anki.consts import QUEUE_TYPE_REV
except (ImportError, ModuleNotFoundError, AttributeError):
    QUEUE_TYPE_REV = 2


def on_question_shown(*args, **kwargs):
    reviewer: Reviewer = mw.reviewer

    try:
        sched = mw.col.sched
        card = reviewer.card
    except AttributeError:
        raise

    if card.queue != QUEUE_TYPE_REV:
        # not a review card
        return

    deck_options = mw.col.decks.confForDid(card.odid or card.did)

    try:
        options = deck_options["examNotifier"]
    except KeyError:
        return

    if not options["enable"] or not options["date"]:
        return

    datetime_now = datetime.now()
    datetime_exam = datetime.fromtimestamp(options["date"])

    if datetime_now > datetime_exam:
        return

    ease_good = reviewer._defaultEase()

    # next ivl for "good"
    next_ivl = sched.nextIvl(card, ease_good) / 86400

    datetime_next_review = datetime.now() + timedelta(days=next_ivl)

    if datetime_next_review < datetime_exam:
        return

    days_after = (datetime_next_review - datetime_exam).days

    # TODO: use mw.col.sched.answerButtons(card) to check for hard and easy

    name_str = f" <b>{options['name']}</b>" if options["name"] else ""

    tooltip(
        f"""
<b>Exam Notifier</b><br>
If you answer this card with <span style="color:green;">Good</span> you will<br>
see it <b>{days_after}</b> days after your{name_str} exam.
""",
        period=3000,
    )


def initialize_tooltip():
    try:  # >=2.1.20
        from aqt import gui_hooks

        gui_hooks.reviewer_did_show_question.append(on_question_shown)
    except (ImportError, ModuleNotFoundError, AttributeError):
        addHook("showQuestion", on_question_shown)
