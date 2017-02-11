#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3

import polib

def init_db(db):
    cur = db.cursor()
    cur.execute('PRAGMA journal_mode=WAL')
    cur.execute('CREATE TABLE IF NOT EXISTS msgids ('
        'id INTEGER PRIMARY KEY,'
        'domain TEXT,'
        'msgctxt TEXT,'
        'msgid TEXT,'
        'msgid_plural TEXT'
    ')')
    cur.execute('CREATE TABLE IF NOT EXISTS msgstrs ('
        'msgid INTEGER,'
        'locale TEXT,'
        'plural INTEGER,'
        'msgstr TEXT'
    ')')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_msgids'
                ' ON msgids (domain, msgid)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_msgstrs'
                ' ON msgstrs (msgid, locale, plural)')
    db.commit()

def process_mo(db, filename, locale):
    try:
        mo = polib.mofile(filename)
    except Exception as ex:
        print(filename, ex)
        return
    domain = os.path.splitext(os.path.basename(filename))[0]
    locale2 = mo.metadata.get('Language')
    if locale2 and len(locale2) < len(locale):
        locale = locale2
    cur = db.cursor()
    for entry in mo:
        res = cur.execute(
            'SELECT id FROM msgids WHERE domain=? AND msgctxt=? AND msgid=?',
            (domain, entry.msgctxt, entry.msgid)).fetchone()
        if res:
            msgid = res[0]
        else:
            cur.execute(
                'INSERT INTO msgids (domain, msgctxt, msgid, msgid_plural) VALUES (?,?,?,?)',
                (domain, entry.msgctxt, entry.msgid, entry.msgid_plural)
            )
            msgid = cur.lastrowid
        if entry.msgstr_plural:
            for plural, msgstr in entry.msgstr_plural.items():
                cur.execute(
                    'INSERT INTO msgstrs (msgid, locale, plural, msgstr) VALUES (?,?,?,?)',
                    (msgid, locale, plural, msgstr)
                )
        else:
            cur.execute(
                'INSERT INTO msgstrs (msgid, locale, plural, msgstr) VALUES (?,?,?,?)',
                (msgid, locale, None, entry.msgstr)
            )

def process_dir(db, path):
    for root, dirs, files in os.walk(path):
        locale = os.path.relpath(root, path).split('/', 1)[0].rsplit('.', 1)[0]
        print(root)
        for filename in files:
            if os.path.splitext(filename)[1] != '.mo':
                continue
            filepath = os.path.join(root, filename)
            try:
                process_mo(db, filepath, locale)
            except Exception as ex:
                print(filename)
                raise
        db.commit()

def main(args):
    db = sqlite3.connect(args[0])
    path = args[1]
    init_db(db)
    process_dir(db, path)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
