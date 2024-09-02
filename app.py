import sys, pymupdf
from pathlib import Path
import fitz
import yaml

# 一般操作
def delete_files(dire: Path):
    for file in dire.iterdir():  # check_dir内をlsして1ファイルずつファイル名を取得
        if file.is_file():
            file.unlink()
def get_dict_value(dic, key):
    return dic[key] if key in dic else None

# Methods
def get_page_type_list(config, listsize: int):
    types = [None for _ in range(listsize)]
    for page_data in config['page_data_list']['pages']:
        key = page_data['key']
        for pNum in range(page_data['page_range']['start'], page_data['page_range']['end'] + 1):
            if pNum > len(types):
                break
            types[pNum - 1] = {'key': key, 'offset_dats': []}
    if config['page_data_list']['options']['offsets']:
        for offset in config['page_data_list']['options']['offsets']:
            types[offset['target']['page_number'] - 1]['offset_dats'].append(offset)
    
    return types

def get_point(yaml_rect):
    p0 = pymupdf.Point(yaml_rect['pointTL']['x'], yaml_rect['pointTL']['y'])
    p1 = pymupdf.Point(yaml_rect['pointBR']['x'], yaml_rect['pointBR']['y'])
    return p0, p1

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
    defs = [def_dic[key] for key in offset['keys']]
    return defs

# 実行部
def main(config):
    pdf_path = Path(config['pdf_path'])

    # 出力Directoryを用意
    output_dir = pdf_path.parent / pdf_path.stem
    output_dir.mkdir(exist_ok=True)
    delete_files(output_dir)
    
    # PDFファイルを開く
    doc = fitz.open(pdf_path)
    print('Open:', pdf_path)
    
    types = get_page_type_list(config, len(doc)) # [{'key': None, 'offsetkey': None}, {'key': 'type1', 'offsetkey': None}, {'key': 'type1', 'offsetkey': ''}]
    
    # 1ページずつ処理
    for iPage, page in enumerate(doc.pages(stop=101)):
        page_type = types[iPage]
        if page_type == None:
            print('skip:', iPage + 1)
            continue
        
        # Page内の画像矩形リスト
        page_def_image_rects = config['page_type_definitions']['types'][page_type['key']]['image_rects']
        # 画像でloop
        for imgidx, image_rect in enumerate(page_def_image_rects):
            offset_data = get_target_offset_data(page_type['offset_dats'] , iPage + 1, imgidx + 1)
            offset_def_dic = config['page_type_definitions']['options']['offsets']
            offset_defs = get_target_offset_defs(offset_data, offset_def_dic)
            rect = get_image_rect(image_rect, offset_defs)
            
            page.draw_rect(rect, color=(1.0, 0.0, 0.0), width=1, dashes='[4] 0')
            
            if config['outputfile']['image']:
                pix = page.get_pixmap(dpi=300, clip=rect)
                name = f'Page{str(iPage + 1).zfill(4)}_Img{str(imgidx + 1).zfill(1)}_{page_type['key']}.png'
                pix.save(output_dir / name)
            
    if config['outputfile']['cutlinePDF']:
        doc.save(output_dir / 'cutline.pdf')


def config_load(config_path):
    with open(config_path, 'r', encoding='utf-8') as yml:
        config = yaml.safe_load(yml)
        return config


if __name__ == '__main__':
    config_path = './config.yaml'
    config = config_load(config_path)

    main(config)