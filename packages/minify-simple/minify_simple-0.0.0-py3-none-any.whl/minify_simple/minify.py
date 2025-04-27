import os
import minify_html

from enum import Enum

from .exceptions import MinifiedError


class Language(Enum):
    JS = 'js'
    CSS = 'css'
    HTML = 'html'


def minify(code: str, language: Language) -> str:
    """ Minificar codigo

    Args:
        code (str): Codigo
        language (Language): Lenguaje del codigo

    Returns:
        str: Codigo minificado
    """
    kwargs = {
        "remove_processing_instructions": True
    }
    if language == Language.JS:
        minified = minify_html.minify(code, minify_js=True, **kwargs)
    elif language == Language.CSS:
        minified = minify_html.minify(code, minify_css=True, **kwargs)
    else:
        minified = minify_html.minify(code, minify_doctype=True, **kwargs)
    return minified


def minify_file(
    in_filename: str,
    out_filename: str | None = None,
    language: Language | None = None,
    suffix: str | None = None,
    check_suffix: bool = True
) -> str:
    """ Minificar archivo

    Args:
        in_filename (str): Ruta de archivo entrada
        out_filename (str | None, optional): Ruta de archivo salida. Por defecto None
        language (Language | None, optional): Lenguaje del codigo. Por defecto None
        suffix (str | None, optional): Sufijo para el nombre del archivo. Por defecto None
        check_suffix (bool, optional): Agregar sufijo si es necesario. Por defecto True

    Returns
        str: Nombre de archivo minificado
    """
    _language = language
    if _language is None:
        _language = _lang_from_filename(in_filename)

    _output_path = in_filename if out_filename is None else out_filename
    if suffix is not None:
        _output_path, has_suffix = _filename_with_sufix(_output_path, suffix)
        if check_suffix and has_suffix:
            raise MinifiedError("Minified input file")

    with open(in_filename, "r") as f:
        code = f.read()

    minified = minify(code, _language)

    with open(_output_path, "w") as f:
        f.write(minified)

    return _output_path


def _lang_from_filename(filename: str) -> Language:
    filename = os.path.basename(filename)
    name, ext = os.path.splitext(filename)
    lang = ext[1:]
    try:
        return Language(lang)
    except ValueError:
        raise ValueError("Language not set. File extension not supported.")


def _filename_with_sufix(filename: str, suffix: str) -> tuple[str, bool]:
    dirname = os.path.dirname(filename)
    _filename = os.path.basename(filename)
    name, ext = os.path.splitext(_filename)
    has_suffix = name[-len(suffix):] == suffix
    new_filename = f"{name}{suffix}{ext}" # if not has_suffix else _filename
    _output_path = os.path.join(dirname, new_filename)
    return _output_path, has_suffix
