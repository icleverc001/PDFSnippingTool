from pathlib import Path
import fitz

def get_cut_doc(source_path, start_index: int, stop_num: int):
    pdf_path = Path(source_path)
    # PDFファイルを開く
    source = fitz.open(pdf_path)
    output = fitz.open()
    output.insert_pdf(source, from_page=start_index, to_page=stop_num - 1)
    return output

def main(source_path: str, output_path: str, start_num: int, stop_num: int) -> None:
    output = get_cut_doc(source_path, start_num - 1, stop_num)
    output.save(output_path)

if __name__ == '__main__':
    pdf_path: str = r'./sample/origin.pdf'
    output_path: str = r'./sample/cut_40.pdf'
    main(pdf_path, output_path, 1, 40)