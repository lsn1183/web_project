import os
from xlsxwriter import Workbook, worksheet
from io import BytesIO
from PIL import Image
import urllib.request
from urllib.parse import quote
import string
import validators
DOS_BULLET = u'■'  # 项目符号
SEC_CELL_HEIGHT_POINT = 13.5  # 18像素
SEC_CELL_HEIGHT_PIXEL = SEC_CELL_HEIGHT_POINT / 0.75
SEC_CELL_WIDTH = 72  # 72像素


def write_body_title_format(ws, title,
                            row, start_col,
                            end_col=12, title_format=None):
    """
    :param ws: work sheet
    :param title: 标题
    :param row:
    :param start_col:
    :param end_col: 默认 'L'列
    :param title_format:
    :return:
    """
    if title_format:
        ws.write(row, start_col, title, title_format)
        for col in range(start_col + 1, end_col):
            ws.write_blank(row, col, None, title_format)
    else:
        ws.write(row, start_col, title)


class SectionWriter(object):
    """设计文档章节
    """
    def __init__(self, ws, title=None, sec_type=None,
                 comment=None, image_urls=None,
                 row=1, col=1, title_format=None):
        self.ws = ws
        self.ws.set_default_row(SEC_CELL_HEIGHT_POINT)
        # self.ws = ws
        self.title = title
        self.sec_type = sec_type
        self.comment = comment
        if image_urls:
            self.image_urls = image_urls
        else:
            self.image_urls = []
        self.row = row
        self.col = col
        self.title_format = title_format

    def write(self):
        self._write_title()
        self._write_images()
        self._write_comment()

    def _write_title(self):
        # self.ws.write(self.row, self.col,  DOS_BULLET + self.title)
        write_body_title_format(self.ws, DOS_BULLET + self.title,
                                self.row, self.col,
                                title_format=self.title_format)
        self.row += 1

    def _write_images(self):
        """图"""
        if not self.image_urls:
            self.ws.write(self.row, self.col, '无')
            self.row = 31
        for image_url in self.image_urls:
            # filename = 'python.png'
            _, file_type = os.path.splitext(image_url)
            if not file_type:
                self.ws.write(self.row, self.col, '写入图片类型出错！url=%s' % image_url)
                continue
            if file_type.lower()[1:] not in ('png', 'jpeg', 'jpg',
                                             'bmp', 'wmf', 'emf'):
                self.ws.write(self.row, self.col, '写入图片类型出错！url=%s' % image_url)
                continue
            try:
                image_url = image_url.replace(' ', '%20')
                if validators.url(image_url):
                    url = quote(image_url, safe=string.printable)  # safe表示可以忽略的字
                    image_data = BytesIO(urllib.request.urlopen(url).read())
                    # from urllib.parse import urlparse
                    # parse_result = urlparse(image_url)
                    # image_file = parse_result.path
                    # image_data = BytesIO(image_file.read())
                else:
                    image_url = quote(image_url, safe=string.printable)
                    image_file = open(image_url, 'rb')
                    image_data = BytesIO(image_file.read())
                    image_file.close()
                filename = image_url
                # Write the byte stream image to a cell.
                # The filename must be specified.
                self.ws.insert_image(self.row, self.col, filename,
                                     {'image_data': image_data,
                                      'x_offset': 3,
                                      'y_offset': 2,
                                      })
                image = Image.open(image_data)
                width, height = image.size
                # 图片覆盖的行数
                cover_row = int((height + SEC_CELL_HEIGHT_PIXEL - 1) / SEC_CELL_HEIGHT_PIXEL)
                self.row += cover_row + 2
            except Exception as e:
                self.ws.write(self.row, self. col,
                              '写入图片出错！url=%s' % image_url)
                self.row += 2

    def _write_comment(self):
        """说明"""
        self.ws.write(self.row, self.col, DOS_BULLET + u'说明')
        # write_body_title_format(self.ws, DOS_BULLET + u'说明', self.row,
        #                         self.col, title_format=self.title_format)
        self.row += 1
        for cm in self.comment:
            cm = cm.replace('<br>', '\n')
            for s in cm.split('\n'):
                self.ws.write(self.row, self.col, s)
                self.row += 1


def add_to_format(existing_format, dict_of_properties, workbook):
    """Give a format you want to extend and a dict of the properties you want to
    extend it with, and you get them returned in a single format"""
    new_dict = {}
    for key, value in existing_format.__dict__.items():
        if value:
            new_dict[key] = value
    del new_dict['escapes']
    new_dict.update(dict_of_properties)
    return workbook.add_format(new_dict)


def my_box(workbook, ws,
           row_start, col_start,
           row_stop, col_stop,
           border_index=6):
    """Makes an RxC box. Use integers, not the 'A1' format"""
    rows = row_stop - row_start + 1
    cols = col_stop - col_start + 1
    for x in range(rows * cols):   # Total number of cells in the rectangle
        box_form = workbook.add_format()   # The format resets each loop
        row = row_start + (x // cols)
        column = col_start + (x % cols)
        if x < cols:  # If it's on the top row
            box_form = add_to_format(box_form, {'top': border_index}, workbook)
        if x >= ((rows * cols) - cols):    # If it's on the bottom row
            box_form = add_to_format(box_form, {'bottom': border_index}, workbook)
        if x % cols == 0:                  # If it's on the left column
            box_form = add_to_format(box_form, {'left': border_index}, workbook)
        if x % cols == (cols - 1):         # If it's on the right column
            box_form = add_to_format(box_form, {'right': border_index}, workbook)
        ws.write(row, column, "", box_form)


if __name__ == "__main__":
    wb = Workbook(r'test.xlsx')
    image_urls = [r'E:\17Cy\basic_design\20180601145042.png',
                  r'E:\17Cy\basic_design\Usecase.png',
                  ]
    # for i in range(0, 6):
    #     image_urls += image_urls
    # print(len(image_urls))
    ws = wb.add_worksheet('section')
    # sec_wt = SectionWriter(ws=ws, title="图",
    #                        comment='说明', image_urls=image_urls)
    # sec_wt.write()
    my_box(wb, ws, 1, 1, 5, 5, border_index=6)
    # wb.add_format()
    wb.close()
    s = 'aa DetailDesign CrossPointDisplay'
    import re
    for doc_type_s in ["DetailDesign", "BasicDesign"]:
        r = r"[\s|\-|_]*%s[\s|\-|_]*" % doc_type_s
        p = re.compile(r, re.I)
        m = p.findall(s)
        if m:
            print(m[0])
            s = s.replace(m[0], ' ')
    print(s)
