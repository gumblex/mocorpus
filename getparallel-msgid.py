#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import sqlite3

def main(filename, tgt):
    db = sqlite3.connect(filename)
    cur = db.cursor()
    with open('msgid-%s.msgid.txt' % tgt, 'w', encoding='utf-8') as w1, \
         open('msgid-%s.%s.txt' % (tgt, tgt), 'w', encoding='utf-8') as w2:
        for s, t in cur.execute(
            'SELECT m.msgid, t.msgstr FROM msgids m'
            ' INNER JOIN msgstrs t ON t.msgid = m.id'
            ' WHERE t.locale = ?', (tgt,)):
            w1.write(s.replace('\n', ' ').strip() + '\n')
            w2.write(t.replace('\n', ' ').strip() + '\n')

if __name__ == '__main__':
    main(*sys.argv[1:])
