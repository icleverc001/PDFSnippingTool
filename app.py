import sys, pymupdf
from pathlib import Path
import fitz
import yaml
sys.path.append('./pdf_snipping_tool/models')
from pdf_snipping_tool.models.config import Config
from pdf_snipping_tool.models.page_data import PageData
from pdf_snipping_tool.models.definitions import Definitions

# 一般操作
def delete_files(dire: Path):
    for file in dire.iterdir():  # check_dir内をlsして1ファイルずつファイル名を取得
        if file.is_file():
            file.unlink()
def get_dict_value(dic, id):
    return dic[id] if id in dic else None

# Methods
def get_page_type_list(config: Config, listsize: int):
    data: PageData = config.data
    
    types = [None for _ in range(listsize)]
    for page_data in data.pages:
        id = page_data['id']
        for pNum in range(page_data['range']['start'], page_data['range']['end'] + 1):
            if pNum > len(types):
                break
            types[pNum - 1] = {'id': id, 'offset_dats': []}
    if data.options['offsets']:
        for offset in data.options['offsets']:
            types[offset['target']['page_number'] - 1]['offset_dats'].append(offset)
    
    return types

def get_point(yaml_rect):
    p0 = pymupdf.Point(yaml_rect['pointTL']['x'], yaml_rect['pointTL']['y'])
    p1 = pymupdf.Point(yaml_rect['pointBR']['x'], yaml_rect['pointBR']['y'])
    return p0, p1

def get_color(list: list[object], index: int):
    ir: int = index % len(list)
    colordict: dict[str, float] = list[ir]
    return (colordict['r'], colordict['g'], colordict['b'])

def get_image_rect(img, offsets) -> pymupdf.Rect:
    p0, p1 = get_point(img)
    for offset in offsets:
        offset_p0, offset_p1 = get_point(offset)
        p0 += offset_p0
        p1 += offset_p1
    return pymupdf.Rect(p0=p0, p1=p1)


def get_target_offset_data(offset_data_list, pagenum, imgnum):
    """指定Page,指定図番号のoffset dataを取得する

    Args:
        offset_data_list (_type_): _description_
        pagenum (_type_): _description_
        imgnum (_type_): _description_

    Returns:
        _type_: _description_
    """
    offsets = [data for data in offset_data_list if data['target']['page_number'] == pagenum and data['target']['image_number'] == imgnum]
    if len(offsets) == 0:
        return []
    if len(offsets) > 1:
        raise "offsetsが重複"
    return offsets[0]


def get_target_offset_defs(offset, def_dic):
    """offset dataで指定のoffset定義を取得する

    Args:
        offset (_type_): 対象のoffset data
        def_dic (_type_): 定義辞書

    Returns:
        _type_: 対象のoffset定義リスト
    """
    # offset = get_target_offset_data(offset_data_list, pagenum, imgnum)
    if not offset:
        return []
    defs = [def_dic[id] for id in offset['ids']]
    return defs

# 実行部
def main(config: Config) -> None:
    pdf_file = Path(config.pdf_path)
    
    if not pdf_file.is_file():
        return

    # 出力Directoryを用意
    output_dir: Path = pdf_file.parent / pdf_file.stem
    output_dir.mkdir(exist_ok=True)
    delete_files(output_dir)
    
    # PDFファイルを開く
    doc: fitz.Document = fitz.open(pdf_file)
    print('Open:', pdf_file)
    
    types = get_page_type_list(config, len(doc)) # [{'id': None, 'offsetid': None}, {'id': 'type1', 'offsetid': None}, {'id': 'type1', 'offsetid': ''}]
    
    # 1ページずつ処理
    for iPage, page in enumerate(doc.pages(stop=101)):
        page_type = types[iPage]
        if page_type == None:
            print('skip:', iPage + 1)
            continue
        
        definitions: Definitions = config.definitions
        # Page内の画像矩形リスト
        page_def_image_rects = definitions.rectangles[page_type['id']]['image_rects']
        # 画像でloop
        for imgidx, image_rect in enumerate(page_def_image_rects):
            offset_data = get_target_offset_data(page_type['offset_dats'] , iPage + 1, imgidx + 1)
            offset_def_dic = definitions.options['offsets']
            offset_defs = get_target_offset_defs(offset_data, offset_def_dic)
            rect = get_image_rect(image_rect, offset_defs)
            
            color = get_color(config.colors['cut_lines'], imgidx)
            page.draw_rect(rect, color=color, width=1, dashes='[4] 0')
            
            if config.outputfile['image']:
                pix = page.get_pixmap(dpi=300, clip=rect)
                name = f'Page{str(iPage + 1).zfill(4)}_Img{str(imgidx + 1).zfill(1)}_{page_type['id']}.png'
                pix.save(output_dir / name)
            
    if config.outputfile['cutlinePDF']:
        doc.save(output_dir / 'cutline.pdf')


def config_load(config_path: str) -> Config:
    config: Config = Config()
    config.load(config_path)
    return config
    with open(config_path, 'r', encoding='utf-8') as yml:
        config = yaml.safe_load(yml)
        return config


if __name__ == '__main__':
    config_path: str = './config.yaml'
    if Path(config_path).exists():
        config: Config = config_load(config_path)
        main(config)