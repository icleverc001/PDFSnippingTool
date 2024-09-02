from pathlib import Path
import fitz
import cutPage

WIDTH = 793
HEIGHT = 1121

def main(source_path: str, output_path: str, start_num: int, stop_num: int):
    # PDFファイルを開く
    doc: fitz.Document = cutPage.get_cut_doc(source_path, start_num - 1, stop_num)
    for ip, page in enumerate(doc):
        print('page', ip + 1)
        for ih in range(7):
            page.draw_line(fitz.Point(100 * ih, 0), fitz.Point(100 * ih, HEIGHT), color=(1.0, 0.0, 0.0), width=1)
            page.draw_line(fitz.Point(100 * ih + 50, 0), fitz.Point(100 * ih + 50, HEIGHT), color=(1.0, 0.0, 0.0), width=1, dashes='[2] 0')
        for iv in range(11):
            page.draw_line(fitz.Point(0, 100 * iv), fitz.Point(WIDTH, 100 * iv), color=(1.0, 0.0, 0.0), width=1)
            page.draw_line(fitz.Point(0, 100 * iv + 50), fitz.Point(WIDTH, 100 * iv + 50), color=(1.0, 0.0, 0.0), width=1, dashes='[2] 0')
            

    output = fitz.open()
    output.insert_pdf(doc)
    output.save(output_path)
    
    

if __name__ == '__main__':
    source_path = './sample/origin.pdf'
    output_path = './sample/cut_101_line.pdf'
    main(source_path, output_path, 1, 101)