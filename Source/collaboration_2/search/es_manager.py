from search.es_anyplace import EsAnyplace
from elasticsearch import Elasticsearch


class EsManager(object):
    pass

    """
        """
    __instance = None

    @staticmethod
    def instance():
        """create a instance"""
        if EsManager.__instance is None:
            EsManager.__instance = EsManager()
        return EsManager.__instance

    def __init__(self):
        self.ip = None
        self.port = 9200
        self.lastest_history_dir = ''
        self.curr_anyplace_index = None
        self.new_anyplace_index = None

    def set_ip(self, ip, port=9200):
        self.ip = ip
        self.port = port

    def set_lastest_history_dir(self, dir):
        self.lastest_history_dir = dir

    def get_curr_anyplace_index(self):
        if not self.curr_anyplace_index:
            self.curr_anyplace_index = EsAnyplace(index_name='anyplace', index_type="bugs", ip=self.ip, port=self.port)
            self.curr_anyplace_index.create_index()
        return self.curr_anyplace_index

    def update_anyplace_index(self, dir_path=''):
        if not dir_path:
            dir_path = self.lastest_history_dir
        self.new_anyplace_index = EsAnyplace(index_name='anyplace_new', index_type="bugs", ip=self.ip, port=self.port)
        if self.new_anyplace_index:
            # self.new_anyplace_index.delete_index()
            # self.new_anyplace_index.create_index()
            self.new_anyplace_index.import_anyplace_csv_dir(dir_path)
            print('new_anyplace total', self.new_anyplace_index.total())
            # 比较新旧的bug数目
            if self.cmp_anyplace_bugs(self.curr_anyplace_index, self.new_anyplace_index):
                # self.curr_anyplace_index.delete_index()
                self.reindex()
                if not self.curr_anyplace_index:
                    self.get_curr_anyplace_index()
                print('curr_anyplace total', self.curr_anyplace_index.total())
            else:
                raise Exception("新的Bug数【%s】比旧的少【%s】" %
                                (self.new_anyplace_index.total(),
                                 self.curr_anyplace_index.total()))

    def reindex(self):
        # self.curr_anyplace_index.delete_index()
        # self.curr_anyplace_index.create_index()
        body = {
            "source": {
                "index": 'anyplace_new'  # self.new_anyplace_index.index_name
            },
            "dest": {
                "index": 'anyplace',  # self.curr_anyplace_index.index_name,
                "version_type": "internal"  # 替换旧的
            }
        }
        # es = Elasticsearch([self.ip], port=self.port)
        # es.reindex(body, timeout='10m', wait_for_completion=False)
        self.new_anyplace_index.es.reindex(body, timeout='10m', wait_for_completion=False)

    def cmp_anyplace_bugs(self, anyplace_index1, anyplace_index2):
        if not anyplace_index1:
            return True
        if anyplace_index2.total() >= anyplace_index1.total():
            return True
        return False


if __name__ == "__main__":
    obj = EsAnyplace(ip="192.168.64.172")
    # obj.delete_all_index()
    # obj.create_index()
    es_manager = EsManager.instance()
    es_anyplace = es_manager.get_curr_anyplace_index()
    es_manager.set_ip("192.168.64.172")
    es_manager.get_curr_anyplace_index()

    print('Current bug number [%s]' % es_anyplace.total())
    # es_anyplace = None
    # es_manager.reindex()
    try:
        es_manager.update_anyplace_index(r'Y:')
    except Exception as e:
        print(e)
    print(es_manager.curr_anyplace_index.total())
    pass
