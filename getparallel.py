#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import sqlite3

def main(filename, src, tgt):
    db = sqlite3.connect(filename)
    cur = db.cursor()
    print(src, tgt)
    with open('%s-%s.%s.txt' % (src, tgt, src), 'w', encoding='utf-8') as w1, \
         open('%s-%s.%s.txt' % (src, tgt, tgt), 'w', encoding='utf-8') as w2:
        for s, t in cur.execute(
            'SELECT s.msgstr, t.msgstr FROM msgstrs s'
            ' INNER JOIN msgstrs t ON t.msgid = s.msgid'
            ' WHERE s.locale = ? AND t.locale = ?', (src, tgt)):
            w1.write(s.replace('\n', ' ').strip() + '\n')
            w2.write(t.replace('\n', ' ').strip() + '\n')

if __name__ == '__main__':
    main(*sys.argv[1:])
