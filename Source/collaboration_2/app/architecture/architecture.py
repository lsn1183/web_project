"""
Architecture
---------
注意
框架的layer相当于我们平台说的模块
框架的Module是文件, 如: xx.so, packages.db, state-router.lua, UcsBig5-H-HeiW5.ttf
"""
import json
import pandas as pd
from requests import get, put, post, delete
# from flask import current_app
MAX_LAYER_NUM = 5
SKIP_LAYES = ['', 'build', 'project', 'nutshell', 'src']


class Architecture(object):
    def __init__(self, host):
        self.host = host  # current_app.config["ARCHITECTURE_SRV"]
        # self.host = 'http://192.168.8.152/'

    def get_projects(self, proj_name=""):
        # host = current_app.config["ARCHITECTURE_SRV"]
        url = self.host + "a/projects"
        r = get(url)
        if r.status_code == 200:
            projects = json.loads(r.content)
            if proj_name:
                for proj in projects:
                    if proj.get("name").lower() == proj_name.lower():
                        return proj
        return None

    def get_devices(self, proj_id):
        """ DCU/MEU
        :param proj_id:
        :return:
        """
        url = self.host + "a/project/%s" % proj_id
        r = get(url)
        if r.status_code == 200:
            project = json.loads(r.content)
            if project:
                devices = project.get("devices")
                return devices
        return []

    def get_layers(self, proj_id, device_id):
        """
        :param proj_id:
        :param device_id:
        :return: layer
        """
        url = self.host + "a/project/%s/%s" % (proj_id, device_id)
        r = get(url)
        if r.status_code == 200:
            device = json.loads(r.content)
            if device:
                layers = device.get("layers")
                return layers
        return []

    def get_all_layers(self, proj_name):
        """获取项目下所有layer
        :param proj_id:
        :param device_id:
        :return: layer
        """
        layers = []
        if not proj_name:
            return layers
        project = self.get_projects(proj_name)
        if project:
            proj_id = project.get("id")
            devices = self.get_devices(proj_id)
            for dev in devices:
                device_id = dev.get("id")
                layers += self.get_layers(proj_id, device_id)
        return layers

    def layer2df(self, layers):
        data = []
        columns = []
        for i in range(1, MAX_LAYER_NUM + 1):
            columns.append('Layer_id%s' % i)
            columns.append('Layer%s' % i)
        for layer_names, layer_ids, modules in self._deep_search(layers):
            # print(layer_ids)
            if layer_names == ['externals', 'wayland', 'wayland']:
                # 模块名称重复(两个wayland)，并且没法处理
                continue
            if layer_names[0] == 'xxx':
                continue
            new_names, new_ids = self.delete_skip_layer(layer_names, layer_ids,
                                                        skip_layers=SKIP_LAYES)
            new_names, new_ids = self.delete_repeat_model(new_names, new_ids)
            print(new_names)
            row = []
            for layer_id, name in zip(new_ids, new_names):
                row.append(layer_id)
                row.append(name)
            row += [None] * (MAX_LAYER_NUM * 2 - len(row))
            data.append(row)
        df = pd.DataFrame(data=data, columns=columns)
        return df

    def layername2df(self, layers):
        columns = []
        for i in range(1, MAX_LAYER_NUM + 1):
            columns.append('layer%s' % i)
        data = []
        for layer_names, layer_ids, modules in self._deep_search(layers):
            new_names, new_ids = self.delete_skip_layer(layer_names, layer_ids,
                                                        skip_layers=SKIP_LAYES)
            # print(layer_names)
            # print(new_names)
            row = []
            row += new_names + [None] * (12 - len(new_names))
            data.append(row)
        df = pd.DataFrame(data=data, columns=columns)
        return df

    def delete_skip_layer(self, names, ids, skip_layers):
        new_names, new_ids = [], []
        for name, layer_id in zip(names, ids):
            if name not in skip_layers:
                new_names.append(name)
                new_ids.append(layer_id)
            else:
                if layer_id == ids[-1] and name != '':
                    new_names.append(name)
                    new_ids.append(layer_id)
        return new_names, new_ids

    def delete_repeat_model(self, layer_names, layer_ids):
        """模块名称重复
        :return:
        """
        unique_names, unique_ids = layer_names[-1:], layer_ids[-1:]
        for i in range(len(layer_names) - 2, -1, -1):
            if layer_names[i] in unique_names:
                print("Module Name repeat! %s" % layer_names)
                continue
            else:
                if layer_names[i].lower() == 'platfrom':
                    unique_names.insert(0, 'Platform')
                else:
                    unique_names.insert(0, layer_names[i])
                unique_ids.insert(0, layer_ids[i])
        return unique_names, unique_ids

    def _deep_search(self, layers):
        names = []
        ids = []
        stack = [iter(layers)]
        while stack:
            children = stack[-1]
            child = next(children, None)
            if child is None:
                stack.pop()
                if names:
                    names.pop()
                    ids.pop()
            else:
                sub = child.get("layers")
                # TODO@hcz
                # if not isinstance(sub, list):
                #     print(names)
                #     print(sub)
                if not sub or not isinstance(sub, list):
                    # print(visited + [child.get("model_name")])
                    yield (names + [child.get("name")],
                           ids + [child.get("id")],
                           child.get("modules")
                           )
                else:
                    names.append(child.get("name"))
                    ids.append(child.get("id"))
                    stack.append(iter(sub))

    def to_sql(self, name, proj_name, df, db):
        """
        :param name:
        :param proj_name:
        :param df:
        :param db:
        :return:
        """
        # 删除旧的
        # pd.DataFrame().to_sql()
        df["proj_name"] = [proj_name] * len(df)
        df.to_sql(name, con=db.session.bind, schema='architecture')

if __name__ == "__main__":
    arcitecture_obj = Architecture(host='http://192.168.8.152/')
    layers = arcitecture_obj.get_all_layers(proj_name='17cy')
    # arcitecture_obj.layer2df(layers)
    print(arcitecture_obj.layer2df(layers))
