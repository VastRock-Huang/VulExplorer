import json
import os.path

import global_config
from utils.log import pwarn


class DatasetHandler:
    def add_to_dataset(self, CVE_id: str, file_paths: list,
                       vul_func: str, sensitive_line: int, keywords: list,
                       vul_wfdg: str, vul_wfdg_no_sen: str, fixed_wfdg: str,
                       affected_vers=None, fixed_vers=None, vul_type: str = ""):
        pass

    def finish_dataset(self):
        pass

    def show_dataset(self):
        pass


class JsonDatasetHandler(DatasetHandler):
    _FILE_PATH = os.path.join(global_config.DATASET_DIR, global_config.DATASET_FILE_NAME)

    def __init__(self):
        self._json_list = []
        self._index = 0
        self._file_path = ''

    def add_to_dataset(self, CVE_id: str, file_paths: list,
                       vul_func: str, sensitive_line: int, keywords: list,
                       vul_wfdg: str, vul_wfdg_no_sen: str, fixed_wfdg: str,
                       affected_vers=None, fixed_vers=None, vul_type: str = ""):
        if not affected_vers:
            affected_vers = []
        if not fixed_vers:
            fixed_vers = []
        json_obj = {
            'id': self._index,
            'checked': False,
            'CVE_id': CVE_id,
            'file_paths': file_paths,
            'vul_func': vul_func,
            'sensitive_line': sensitive_line,
            'keywords': keywords,
            'vul_wfdg': vul_wfdg,
            'vul_wfdg_no_sen': vul_wfdg_no_sen,
            'fixed_wfdg': fixed_wfdg,
            'affected_vers': affected_vers,
            'fixed_vers': fixed_vers,
            'vul_type': vul_type
        }
        self._json_list.append(json_obj)
        self._index += 1

    def finish_dataset(self):
        with open(self._FILE_PATH, 'w') as wf:
            json.dump(self._json_list, wf)

    def show_dataset(self):
        try:
            with open(self._FILE_PATH, 'r') as rf:
                json_obj = json.load(rf)
        except:
            pwarn('dataset not found, path: %s', self._FILE_PATH)
            return

        print(' %-3s | %-7s | %-12s | %-25s | %-30s | %-30s | %-9s | %-15s | %-50s | %-50s'
              % ('id', 'checked', 'CVE id', 'vul type', 'file paths', 'vul func', 'sensitive',
                 'keywords', 'affected versions', 'fixed versions'))
        for vul in json_obj:
            print(' %-3s  ' % vul['id'], end='')
            checked = '√' if vul['checked'] else ' '
            print(' %-7s  ' % checked, end='')
            print(' %-12s  ' % vul['CVE_id'], end='')
            print(' %-25s  ' % vul['vul_type'], end='')
            print(' %-30s  ' % vul['file_paths'], end='')
            print(' %-30s  ' % vul['vul_func'], end='')
            print(' %-9s  ' % vul['sensitive_line'], end='')
            print(' %-15s  ' % vul['keywords'], end='')
            print(' %-50s  ' % vul['affected_vers'], end='')
            print(' %-50s  ' % vul['fixed_vers'], end='')
            print('')


class DataHandlerFactory:
    JSON_TYPE = 'JSON'
    MYSQL_TYPE = 'MySQL'

    @classmethod
    def create_handler(cls, data_type: str):
        if data_type == cls.JSON_TYPE:
            return JsonDatasetHandler()
        return None