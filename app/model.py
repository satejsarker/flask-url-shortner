import os
from datetime import datetime

from tinydb import TinyDB, Query

current_dir = os.path.dirname(os.path.abspath(__file__))
print(os.path.join(current_dir, 'db', 'database.json'))


class Database:
    """database query and import """
    def __init__(self):
        self.db = TinyDB(os.path.join(current_dir, 'db', 'database.json'))

    def search_url(self, table_name, title):
        Url = Query()
        current_table = self.db.table(table_name)
        print(current_table.search(Url.title.matches(str(title))))
        return current_table.search(Url.title.matches(str(title)))

    def search_url_title(self, table_name, title):
        Url = Query()
        current_table = self.db.table(table_name)
        return current_table.get(Url.title == str(title))

    def url_by_id(self, table_name, id):
        Url = Query()
        current_table = self.db.table(table_name)
        res = current_table.get(Url.id == str(id))
        return res.doc_id, res

    def update_url(self, table_name, id):
        doc_id, res = self.url_by_id(table_name=table_name, id=id)
        if doc_id is not None:
            hit = res['hits']
            print(res['hit_times'])
            hit_times = [el for el in res['hit_times']]
            hit_times.append(str(datetime.now()))
            current_table = self.db.table(table_name)
            current_table.update({"hits": hit + 1, "hit_times": hit_times}, doc_ids=[doc_id])
            return True, res
        return None

    def insert_data(self, data_obj, table_name):
        current_table = self.db.table(table_name)
        value_search = self.search_url_title(table_name=table_name, title=data_obj['title'])

        if value_search is not None:
            print("insert not possible ")
            return None

        else:
            return current_table.insert(data_obj)
