from html2pdf.workers.convert import SOURCE_TYPE, convert_html_to_pdf
from pathlib import Path

def test_convert_html_to_pdf_by_url(tmp_dir):
    url = "http://google.com"
    path = convert_html_to_pdf(
        source_type=SOURCE_TYPE.url, source=url, target_dir=tmp_dir
    )
    assert path.suffix == ".pdf"
    assert path.parent == tmp_dir


def test_convert_html_to_pdf_by_file(tmp_dir):
    file_content = """
    <!DOCTYPE html>
        <html>
        <body>

        <div style="position:relative;">
        <div style="opacity:0.5;position:absolute;left:50px;top:-30px;width:300px;height:150px;background-color:#40B3DF"></div>
        <div style="opacity:0.3;position:absolute;left:120px;top:20px;width:100px;height:170px;background-color:#73AD21"></div>
        <div style="margin-top:30px;width:360px;height:130px;padding:20px;border-radius:10px;border:10px solid #EE872A;font-size:120%;">
            <h1>CSS = Styles and Colors</h1>
            <div style="letter-spacing:12px;font-size:15px;position:relative;left:25px;top:25px;">Manipulate Text</div>
            <div style="color:#40B3DF;letter-spacing:12px;font-size:15px;position:relative;left:25px;top:30px;">Colors,
            <span style="background-color:#B4009E;color:#ffffff;"> Boxes</span></div>
        </div>
        </div>

        </body>
        </html>
    """
    tmp_html_path: Path = tmp_dir / "test.html"
    with tmp_html_path.open('w') as file:
        file.write(file_content)
    path = convert_html_to_pdf(
        source_type=SOURCE_TYPE.file, source=tmp_html_path, target_dir=tmp_dir
    )
    assert path.suffix == ".pdf"
    assert path.parent == tmp_dir
