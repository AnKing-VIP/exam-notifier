/*
# -*- coding: utf-8 -*-

# Exam Notifier Add-on for Anki
#
# Copyright (C) 2019-2022  Aristotelis P. <https://glutanimate.com/>
# Copyright (C) 2021  Ankitects Pty Ltd and contributors
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
*/

$deckOptions.then((options) => {
  options.addHtmlAddon(HTML_CONTENT, () => {
    const examEnabledInput = document.getElementById("en-exam-enabled");
    const examNameInput = document.getElementById("en-exam-name");
    const examDateInput = document.getElementById("en-exam-date");
    const mainInputsDiv = document.getElementById("en-main-inputs");
    const glutanimateBtn = document.getElementById("en-btn-glutanimate");
    const ankingBtn = document.getElementById("en-btn-anking");

    const setInputEnabled = (enable) => {
      examNameInput.disabled = !enable;
      examDateInput.disabled = !enable;
      if (enable) {
        mainInputsDiv.classList.remove("disabled");
      } else {
        mainInputsDiv.classList.add("disabled");
      }
    };
    examEnabledInput.addEventListener("change", (event) => {
      const checked = event.target.checked;
      setInputEnabled(checked);
      const value = checked ? "true" : "false";
      pycmd(`exam_notifier:deck_options:exam_enabled:${value}`);
    });
    examNameInput.addEventListener("change", (event) => {
      const value = event.target.value;
      pycmd(`exam_notifier:deck_options:exam_name:${value}`);
    });
    examDateInput.addEventListener("change", (event) => {
      const date = event.target.valueAsDate;
      const value = Math.round(date.getTime() / 1000); // to epoch seconds
      pycmd(`exam_notifier:deck_options:exam_date:${value}`);
    });
    glutanimateBtn.addEventListener("click", (_) => {
      pycmd(`exam_notifier:deck_options:open_link:glutanimate`);
    });
    ankingBtn.addEventListener("click", (_) => {
      pycmd(`exam_notifier:deck_options:open_link:anking`);
    });

    // set input value
    examEnabledInput.checked = EXAM_ENABLED;
    examNameInput.value = EXAM_NAME;
    const examDateEpoch = EXAM_DATE;
    examDateInput.valueAsDate = new Date(examDateEpoch * 1000); // s to ms

    setInputEnabled(examEnabledInput.checked);
  });
});
