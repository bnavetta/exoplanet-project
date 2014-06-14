#!/usr/bin/env python

import os
import shutil
import subprocess
import sys

documents_dir = os.path.realpath(os.path.dirname(__file__))
root_dir = os.path.normpath(os.path.join(documents_dir, '..'))

build_dir = os.path.join(root_dir, 'build')
gen_dir = os.path.join(build_dir, 'gen')

sys.path.append(root_dir)

from exo.documents import *

mkdir_p(build_dir)
mkdir_p(gen_dir)

jinja_env = create_latex_env(documents_dir)

context = make(gen_dir)

for document in ('report', 'presentation'):
    input_dir = os.path.join(documents_dir, document)
    template = jinja_env.get_template('{0}/{0}.tex'.format(document))
    output_dir = os.path.join(build_dir, document)
    shutil.rmtree(output_dir)
    mkdir_p(output_dir)
    with open(os.path.join(output_dir, document + '.tex'), 'w') as generated_document:
        generated_document.write(template.render(context))

    environment = {
        'PATH': os.environ.get('PATH', os.defpath),
        'TEXINPUTS': '.' + os.pathsep + input_dir + os.pathsep + documents_dir + os.pathsep + os.environ.get('TEXINPUTS', ''),
        'BIBINPUTS': '.' + os.pathsep + documents_dir + os.pathsep + os.environ.get('BIBINPUTS', '')
    }

    subprocess.check_call(["xelatex", document], cwd=output_dir, env=environment)
    subprocess.check_call(["biber", document], cwd=output_dir, env=environment)
    subprocess.check_call(["xelatex", document], cwd=output_dir, env=environment)
    # subprocess.check_call(["biber"])
