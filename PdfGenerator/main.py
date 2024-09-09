import markdown
import pdfkit
import os
import base64

_default_relative_path = "TahaMertGokdemirCV.md"
_default_output_file_name = "TahaMertGokdemirCV"
_wkhtmltopdf_path = "D:\\Lib\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
_image_file_name = "Portrait.png"
_template_file_name = "pdfcvtemplate.html"

def convert_image_to_base64():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    image_path = os.path.join(parent_dir, "Media", _image_file_name)
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string

def embed_into_template(content, style):
    with open(_template_file_name,'r', encoding='utf-8') as template_file:
        file = template_file.read()
        file = file.replace('{{ style }}', style)
        file = file.replace('{{ content }}', content)
        return file


def convert_md_to_pdf(md_file_path, pdf_file_path):
    # Read Markdown file
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_text = md_file.read()

    image_tag = f'<p align="center">\n  <img src="data:image/png;base64,{convert_image_to_base64()}" width="200px"/>\n</p>'

    style_tag = '''
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
            body {
                font-family: 'Roboto', sans-serif;
            }
        </style>
        '''


    md_content = f'{image_tag}</br></br>\n{md_text}'

    # Convert Markdown to HTML
    html_text = markdown.markdown(md_content, extensions=['extra', 'smarty'])

    final_text = embed_into_template(html_text, style_tag)

    # Convert HTML to PDF
    pdfkit.from_string(final_text, pdf_file_path,
                       configuration=pdfkit.configuration(wkhtmltopdf=_wkhtmltopdf_path),
                       options={'encoding': 'UTF-8', "enable-local-file-access": True})

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

    md_file_path = os.path.join(parent_dir, _default_relative_path)
    print(md_file_path)
    pdf_output_dir = parent_dir
    pdf_file_path = os.path.join(pdf_output_dir, f"{_default_output_file_name}.pdf")

    # Convert Markdown to PDF
    convert_md_to_pdf(md_file_path, pdf_file_path)





