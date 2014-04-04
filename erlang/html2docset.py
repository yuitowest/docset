# -*- encoding: utf-8 -*-

import os
import re
import sqlite3

from pyquery import PyQuery


path = os.path.dirname(os.path.abspath(__file__))
documents_path = path + '/erlang.docset/Contents/Resources/Documents'
database_path = path + "/erlang.docset/Contents/Resources/docSet.dsidx"
create_table_sql = "CREATE TABLE IF NOT EXISTS searchIndex( \
    id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);"
create_index_sql = "CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);"
insert_record_sql = "INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)"


def get_file_list():
    file_list = []
    for root, dirs, files in os.walk(documents_path):
        for f in files:
            if re.search(r"\.html$", f):
                prefix_path = root.replace(documents_path + '/', '')
                file_list.append(os.path.join(prefix_path, f))

    return file_list


def is_module_doc(query):
    h3 = query.find("h3")
    return (
        2 <= len(h3) and h3[0].text == "MODULE" and h3[1].text == "MODULE SUMMARY")


def create_searchindex():
    db = sqlite3.connect(database_path)
    cursor = db.cursor()
    cursor.execute(create_table_sql)
    cursor.execute(create_index_sql)
    files = get_file_list()
    for f in files:
        html = open(os.path.join(documents_path, f)).read().decode("utf-8")
        query = PyQuery(html)

        if not is_module_doc(query):
            continue

        module_name = query.find("h3:first").next().text()
        cursor.execute(insert_record_sql, (module_name, 'Module', f))

        for x in query.find("#content>.innertube>p>a"):
            function_name = re.sub("'", '', PyQuery(x).attr("name"))
            params = (
                module_name + ":" + re.sub("-", "/", function_name),
                'func',
                f + "#" + function_name)
            cursor.execute(insert_record_sql, params)

    db.commit()
    db.close()


def main():
    create_searchindex()

if __name__ == "__main__":
    main()
