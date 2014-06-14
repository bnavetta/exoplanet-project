import re

from jinja2 import Environment, FileSystemLoader

LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'""'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots')
)

def escape_tex(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

def create_latex_env(template_path):
    """
    Create a Jinja2 environment for LaTeX files. See http://flask.pocoo.org/snippets/55/
    """
    env = Environment(loader=FileSystemLoader(template_path))
    env.block_start_string = "((*"
    env.block_end_string = "*))"
    env.variable_start_string = "((("
    env.variable_end_string = ")))"
    env.comment_start_string = "((="
    env.comment_end_string = "=))"
    env.filters['escape_tex'] = escape_tex
    return env
