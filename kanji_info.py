#!/usr/bin/python
#-*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# This file is a plugin for anki flashcard application http://repose.cx/anki/
# ---------------------------------------------------------------------------
# File:        kanji_info.py
# Description: Add information about kanji for each card on the answer side.
#              This information is not meant to be learnt and remembered,
#              it's just there so you don't have to look up this information
#              elsewhere while studying.
#
#              Information that is displayed for each single kanji:
#              - kanji in a special font (stroke order, handwriting, ...)
#                stroke order font: http://nihilist.org.uk/
#              - extra kanji info (by mouseover)
#              - ...more to come (ideas?)
#
# Author:      Andreas Klauer (Andreas.Klauer@metamorpher.de)
# Version:     0.05 (2008-10-22)
# License:     GPL
# ---------------------------------------------------------------------------
# Changelog:
# ---- 0.05 -- 2008-10-22 -- Andreas Klauer ----
#   add some debug messages to help users
# ---- 0.04 -- 2007-08-17 -- Andreas Klauer ----
#   adapted for latest anki version
# ---- 0.03 -- 2007-06-16 -- Andreas Klauer ----
#   tidied the kanji info loop up a bit
# ---- 0.02 -- 2007-06-16 -- Andreas Klauer ----
#   appearance changes
# ---- 0.01 -- 2007-06-15 -- Andreas Klauer ----
#   initial release
# ---------------------------------------------------------------------------

# --- initialize kanji information database ---
from ankiqt import mw
from ankiqt import ui
import os
import codecs

kanji_info = {}
kanji_info_version = "v0.05"

def read_kanji_info(file):
    """Read kanji info from a 'kanji info' type of file.
       This file is simple, just <kanji> <single space> <whatever you want>,
       for example an UTF-8 encoded kanjidic without changes would work,
       but usually you'd strip all unneeded info from it first."""

    try:
        f = codecs.open(file, "rb", "utf8")

        for line in f.readlines():
            if line[0] != u"#":
                kanji_info[line[0]] = line[2:].strip()

        print "kanji_info", kanji_info_version, "read", file

    except:
        print "kanji_info", kanji_info_version, "error reading file", file


# --- hook ourselves into the anki drawAnswer system ---

def append_kanji_info(self, drawAnswer=ui.view.View.drawAnswer):
    """Append additional information about the kanji of the current card."""

    # Call the original drawAnswer function first
    drawAnswer(self)

    done = {}
    info = "<p></p>"

    for u in self.main.currentCard.question+self.main.currentCard.answer:
        # prevent showing same kanji twice:
        if u not in done:
            done[u] = 1

            if u in kanji_info:
                # FIXME:   I'd like to get rid of the kanji mouseover title,
                # FIXME::  but there does not seem to be a way to get a
                # FIXME::  furigana-alike formatting in simple HTML.
                info += """ <span style="%s" title="%s">%s</span> """ % \
                    ("color:#000000; font-family:KanjiStrokeOrders; font-size:128px;",
                     kanji_info[u], u)

    # if there is any info, add it to the buffer
    if len(info):
        self.buffer += "<center>%s</center>" % (info)

def initKanjiInfo():
    kanji_info_txt = os.path.join(mw.config.configPath, "plugins", "kanji_info.txt")
    read_kanji_info(kanji_info_txt)

    if not len(kanji_info):
        read_kanji_info(os.path.join(mw.config.configPath, "kanji_info.txt"))
        print "kanji_info", kanji_info_version, "please put kanji_info.txt in", kanji_info_txt

    print "kanji_info", kanji_info_version, "found", len(kanji_info), "entries"

    if len(kanji_info):
        ui.view.View.drawAnswer = append_kanji_info

mw.addHook("init", initKanjiInfo)
