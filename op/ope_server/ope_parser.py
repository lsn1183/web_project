import os
import json
MAX_CHAPTER_NUM = 9


class OpeParser(object):
    def __init__(self):
        self.screen_list = []
        pass

    def parse(self, path):
        if not path:
            raise Exception("Please indicate JSON file.")
        if not os.path.exists(path):
            raise Exception("Dose not exist file. path[%s]" % path)
        if not path.endswith(".json"):
            raise Exception("File name must be xxx.json. path[%s]" % path)
        with open(path) as fp:
            ope = json.load(fp)
            for d in ope.values():
                screen = ScreenParser()
                screen.parse(d)
                self.screen_list.append(screen)
        return self.screen_list


class ScreenParser(object):
    def __init__(self):
        self.chapter_list = []
        self.attr = dict()

    def parse(self, d):
        self.chapter_list = [[], [], [], [],
                             [], [], [], [],
                             []]
        item1_list = self.chapter_list[1]
        item2_list = self.chapter_list[2]
        item3_list = self.chapter_list[3]
        for key, val in d.items():
            if key == 'ScreenDispRect':
                self.attr[key] = val
            elif isinstance(val, dict) or isinstance(val, list):
                if "Display" in val and val["Display"].get("DisplayChapter") == '1':  # display/chapter1:
                    item1 = dict()
                    item1.update(val)
                    item1_list.append(item1)
                else:
                    if "Active" in val and val["Active"].get("ActiveChapter") == '2':
                        item2 = dict()
                        item2.update(val.get("Active"))
                        item2_list.append(item2)
                    if "Action" in val and val["Action"].get("ActionChapter") == '3':
                        item3 = dict()
                        item3.update(val.get("Action"))
                        item3_list.append(item3)
            else:
                self.attr[key] = val
        array_names = ["AvailableModelUUIDArray", "HKUUIDArray", "InitUUIDArray",
                       "StatusChangeUUIDArray", "TransitionUUIDArray", "TrigUUIDArray"]
        chapter_idxs = [0, 4, 5, 6, 7, 8]
        for array_name, chapter_idx in zip(array_names, chapter_idxs):
            item_list = self._parse_chapter(d, array_name)
            self.chapter_list[chapter_idx] = item_list
        return self.attr, self.chapter_list

    def _parse_chapter(self, d, array_name):
        item_list = []
        for uuid in d.get(array_name):
            chapter = d.get(uuid)
            item_list.append(chapter)
        return item_list


class ChapterParser():
    def __init__(self):
        pass


if __name__ == '__main__':
    obj = OpeParser()
    path = r'C:\Users\yuyin\Desktop\OPE\export\___exportspecs___\Page 1.json'
    screen_list = obj.parse(path)
    path
