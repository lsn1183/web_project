from search.es_manager import EsManager


def update_anyplace_bugs():
    es_manager = EsManager.instance()
    try:
        es_manager.update_anyplace_index()
    except Exception as e:
        print(e)

