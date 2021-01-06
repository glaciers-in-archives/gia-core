from urllib.parse import quote

from IPython.display import HTML, Markdown


def render_code(code: str, format='xml'):
    return Markdown('```{}\n{}```'.format(format, code))

def set_download(data: str, filename: str ):
    blob = quote(data, safe='~()*!.\'') # matches encodeURIComponent()
    HTML('<a download="{}" href="data:text/plain;charset=utf-8,{}">Download</a>'.format(filename, blob))
