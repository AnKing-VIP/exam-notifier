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

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from anki.hooks import addHook
from aqt import mw
from aqt.utils import tooltip
from anki.utils import convertSecondsTo
from datetime import datetime, timedelta

from .config import config

def onQuestionShown():
    try:
        sched = mw.col.sched
        card = mw.reviewer.card
    except:
        return
    
    if card.queue != 2:
        # not a review card
        return
    
    try:
        exam_date_str = config["local"]["exam_date"]
    except:
        return

    if not exam_date_str:
        return
    
    
    nextIvl = convertSecondsTo(sched.nextIvl(card, 2), "days")  # next ivl for "good"
    
    try:
        date_obj_exam = datetime.strptime(exam_date_str, "%Y/%m/%d")
    except:
        return
    
    date_obj_next = datetime.now() + timedelta(days=nextIvl)
    
    if date_obj_next < date_obj_exam:
        return
    
    days_after = (date_obj_next - date_obj_exam).days
    
    tooltip(
        f"Warning: If you answer this card with good you will see it "
        f"{days_after} days after the exam")


def initializeTooltip():
    try:  # >=2.1.20
        from aqt import gui_hooks
        gui_hooks.reviewer_did_show_question.append(onQuestionShown)
    except (ImportError, AttributeError):
        addHook("showQuestion", onQuestionShown)
