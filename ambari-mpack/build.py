import os
import re
import glob
import shutil
import subprocess
from optparse import OptionParser
from jinja2 import Environment, FileSystemLoader


args = {
    "name": "Hyperconda",  # This gets replaced on __main__ based on the construtor installer
    "version": "1.0.0.0",  # mpack version
    "constructor_version": "4.0.0",  # This gets replaced on __main__ based on the construtor installer
    "conda_service_name": "conda",
    "conda_service_version": "1.0.0",
    "min_ambari_version": "2.4.0.0",
    "hdp_min_version": "2.0.*",
    "min_stack_name": "HDP",
    "min_stack_version": "2.5.*",
}


def parse_path(path):
    """
    Get name and version of the installer
    """
    pat = re.compile(r"([\w.]+)-([\w.]+)-Linux-x86_64\.sh$")
    fn = os.path.basename(path)
    m = pat.match(fn)
    name = m.group(1)
    version = m.group(2)
    return name, version


def render_templates(output_dir="./output"):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    templates_dir = os.path.join(this_dir, "templates")

    # Cleanup: Remove output dir and create empty one
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    files = glob.iglob(os.path.join(templates_dir, "**/*"), recursive=True)
    jinja2_env = Environment(loader=FileSystemLoader(templates_dir))

    # Iterate all the files under `templates` and render them
    for fname in list(files):
        template_path = fname[len(templates_dir) + 1:]  # remove `./templates/` prefix
        output_path = os.path.join(output_dir, template_path)
        if os.path.isdir(fname):
            # Render filename and create dir with that name
            output_path = Environment().from_string(output_path).render(**args)
            os.mkdir(output_path)
        else:
            # Render jinja template and save
            template = jinja2_env.get_template(template_path)
            output_from_parsed_template = template.render(**args)
            # Save file
            output_path = Environment().from_string(output_path).render(**args)
            with open(output_path, "w") as fh:
                fh.write(output_from_parsed_template)


def copy_constructor(installer_path, output_dir="./output"):
    """
    Move the constructor installer to the output directory under the files on the service
    """
    target_path = Environment().from_string("{{ name }}-mpack-{{ version }}/common-services/{{ conda_service_name | upper }}/{{ conda_service_version }}/package/files").render(**args)
    target_path = os.path.join(output_dir, target_path)
    shutil.copy(installer_path, target_path)


def pkg_extension(output_dir="./output"):
    """
    Pack the output directory into a tar.gz file
    """
    tar_file = Environment().from_string("{{ name | lower }}-mpack-{{ version }}.tar.gz").render(**args)
    target_dir = Environment().from_string("{{ name }}-mpack-{{ version }}").render(**args)
    process = subprocess.Popen(["tar", "-zcvf", tar_file, target_dir], cwd=output_dir)
    process.wait()


if __name__ == "__main__":
    output_dir = "./output"

    p = OptionParser(
        usage="usage: %prog [options] PATH",
        description="create a parcel from an Anaconda installer (located at "
                    "PATH).  The resulting will be placed in the current "
                    "working directory")

    opts, cli_args = p.parse_args()
    if len(cli_args) != 1:
        p.error("Exactly one argument expected")

    installer_path = cli_args[0]

    name, version = parse_path(installer_path)
    args['name'] = name
    args['constructor_version'] = version

    render_templates(output_dir=output_dir)
    copy_constructor(installer_path)
    pkg_extension(output_dir=output_dir)
