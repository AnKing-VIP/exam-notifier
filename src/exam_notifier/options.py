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
Additions to Anki's deck options dialog
"""

from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDateTime

from anki.hooks import wrap
from aqt.deckconf import DeckConf
from aqt.forms import dconf

DEFAULT_CONFIG = {"enable": False, "name": "", "date": None}


def _qdatetime_from_epoch(unix_epoch: int) -> QDateTime:
    qdatetime = QDateTime()
    qdatetime.setTime_t(unix_epoch)
    return qdatetime


def on_deck_conf_did_load_config(deck_conf: DeckConf, *args, **kwargs):
    form = deck_conf.form
    conf = deck_conf.conf

    if not conf.get("examNotifier"):
        conf["examNotifier"] = DEFAULT_CONFIG

    config = conf["examNotifier"]

    form.examGroupBox.setChecked(config["enable"])
    form.examName.setText(config["name"])

    form.examDate.setMinimumDateTime(
        _qdatetime_from_epoch(int(round(datetime.now().timestamp())))
    )

    if config["date"]:
        form.examDate.setDateTime(_qdatetime_from_epoch(config["date"]))


def on_deck_conf_will_save_config(deck_conf: DeckConf, *args, **kwargs):
    form = deck_conf.form
    conf = deck_conf.conf

    if not conf.get("examNotifier"):
        conf["examNotifier"] = DEFAULT_CONFIG

    config = conf["examNotifier"]

    config["enable"] = form.examGroupBox.isChecked()
    config["name"] = form.examName.text()

    qdatetime = form.examDate.dateTime()
    timestamp = int(round(qdatetime.toSecsSinceEpoch()))

    config["date"] = timestamp


def on_setup_ui(form, dialog):
    form.examGroupBox = QtWidgets.QGroupBox(
        "Enable exam notifications", parent=form.tab_5
    )
    form.examGroupBox.setCheckable(True)
    form.examGroupBox.setObjectName("examGroupBox")
    form.examLayout = QtWidgets.QGridLayout(form.examGroupBox)
    form.examLayout.setObjectName("examLayout")
    form.examDate = QtWidgets.QDateEdit(form.examGroupBox)
    form.examDate.setCalendarPopup(True)
    form.examDate.setObjectName("examDate")
    form.examLayout.addWidget(form.examDate, 0, 5, 1, 1)
    form.labelExamName = QtWidgets.QLabel("Exam name", parent=form.examGroupBox)
    form.labelExamName.setObjectName("labelExamName")
    form.examLayout.addWidget(form.labelExamName, 0, 0, 1, 1)
    form.examName = QtWidgets.QLineEdit(form.examGroupBox)
    form.examName.setText("")
    form.examName.setObjectName("examName")
    form.examName.setPlaceholderText("(e.g. 'USMLE Step 1'")
    form.examLayout.addWidget(form.examName, 0, 2, 1, 1)
    form.labelExamDate = QtWidgets.QLabel("Exam date", parent=form.examGroupBox)
    form.labelExamDate.setObjectName("labelExamDate")
    form.examLayout.addWidget(form.labelExamDate, 0, 4, 1, 1)
    examSpacer = QtWidgets.QSpacerItem(
        10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
    )
    form.examLayout.addItem(examSpacer, 0, 3, 1, 1)
    form.verticalLayout_6.insertWidget(
        form.verticalLayout_6.count() - 1, form.examGroupBox
    )


def initializeOptions():
    dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, on_setup_ui)
    DeckConf.loadConf = wrap(DeckConf.loadConf, on_deck_conf_did_load_config)
    DeckConf.saveConf = wrap(DeckConf.saveConf, on_deck_conf_will_save_config, "before")
    # TODO: Use new-style hooks as soon as PR merged
    # https://github.com/ankitects/anki/pull/458
