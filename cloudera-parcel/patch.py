import os
import re
from optparse import OptionParser


def fix_binaries(prefix):
    """
    Fix the binaries under the prefix
    """
    bin_dir = os.path.join(prefix, "bin")
    for fname in os.listdir(bin_dir):
        filepath = os.path.join(bin_dir, fname)
        if not is_elf(filepath):
            fix_shebang(filepath)


def is_elf(filepath):
    if not os.path.isfile(filepath):
        return False
    with open(filepath, "rb") as file:
        head = file.read(4)
    return head == b"\x7fELF"


def fix_shebang(filepath):
    """
    Change the shebang to #!/usr/bin/env python
    """
    with open(filepath, "r") as f:
        script = f.read()

    shebang_pat = re.compile(r"^#!.+$", re.M)
    match = shebang_pat.match(script)
    if match and "python" in match.group():
        # If `python` its on the shebang, change it it the generic one
        new_script = shebang_pat.sub("#!/usr/bin/env python", script, count=1)
        if new_script == script:
            return
        print("Updating shebang on:", filepath)
        with open(filepath, "w") as file:
            file.write(new_script)
        os.chmod(filepath, 0o0755)


if __name__ == "__main__":
    params = OptionParser(
        usage="usage: %prog [options] PREFIX",
        description="Fix an conda installation to make it relocatable")

    opts, args = params.parse_args()
    if len(args) != 1:
        params.error("Exactly 1 argument expected")

    prefix = args[0]
    
    fix_binaries(prefix)
