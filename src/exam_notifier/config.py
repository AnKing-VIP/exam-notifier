# TODO: use https://github.com/glutanimate/anki-libaddon/blob/master/src/libaddon/anki/config/storages/local.py

from aqt import mw

config = mw.addonManager.getConfig(__name__)

from .libaddon.gui.notifications import (
    NotificationHAlignment,
    NotificationVAlignment,
)

def horizontal_alignment_from_config() -> NotificationHAlignment:
    value = config.get("notification_horizontal_alignment", "center")
    if value == "left":
        return NotificationHAlignment.left
    elif value == "right":
        return NotificationHAlignment.right
    else:
        return NotificationHAlignment.center

def vertical_alignment_from_config() -> NotificationVAlignment:
    value = config.get("notification_vertical_alignment", "bottom")
    if value == "top":
        return NotificationVAlignment.top
    elif value == "center":
        return NotificationVAlignment.center
    else:
        return NotificationVAlignment.bottom
