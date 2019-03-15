# -*- coding: UTF-8 -*-
from app import create_app
import os
import logging
from flask_apscheduler import APScheduler
import logging.handlers
from search.es_manager import EsManager


app = create_app('default')

info_log = os.path.join('log', 'weblog.log')
info_file_handler = logging.handlers.RotatingFileHandler(
    info_log, maxBytes=1048576, backupCount=20)
info_file_handler.setLevel(logging.INFO)
info_file_handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                      '[in %(pathname)s:%(lineno)d]')
)
app.logger.addHandler(info_file_handler)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
es_manager = EsManager.instance()
ip = app.config['ES_SERVER_IP']
port = app.config['ES_SERVER_PORT']
es_manager.set_ip(ip, port)
es_manager.set_lastest_history_dir(app.config['LASTEST_HISTORY_DIR'])
app.run(debug=False, host='', port=5000, threaded=True)

