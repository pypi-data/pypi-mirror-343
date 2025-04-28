import argparse
import sys
import os
import re
from pathlib import Path

import lxml.etree
import lxml.objectify


def remove_ext(path):
    return path.parent / os.path.splitext(path.name)[0]

def load_extensions():
    extensions = {}
    for mime_base in  [Path("/usr/share/mime"), Path.home() / ".local" / "share" / "mime"]:
        for base, _dirs, names in mime_base.walk():
            for name in names:
                path = base / name
                mime_type = str(remove_ext(path).relative_to(mime_base))
                _, ext = os.path.splitext(path)

                if ext == ".xml":
                    mime_extensions = []
                    globs = read_globs(path)
                    for glob in globs:
                        pattern = glob.attrib.get("pattern")
                        if pattern:
                            m = re.match(r'\*(\.[^.]*)$', pattern)
                            if m:
                                mime_extensions.append(m.group(1))

                    extensions[mime_type] = mime_extensions
    return extensions



PARSER = argparse.ArgumentParser(description='Find the extensions for a mime type')
PARSER.add_argument('mimetype')
PARSER.add_argument('--list-types', action='store_true')



def main():
    extensions = load_extensions()
    if "--list-types" in sys.argv[1:] or "-l" in sys.argv[1:]:
        for k in extensions:
            print(k)
        return

    args = PARSER.parse_args()


    print("\n".join(extensions.get(args.mimetype, [])))


def read_globs(path):
    with path.open("rb") as s:
        data = s.read()
        # print(data.decode('utf8'))
        tree = lxml.etree.fromstring(data)
        dropns(tree)
        return tree.xpath("//glob")


def dropns(root):
    for elem in root.iter():
        if hasattr(elem.tag, 'func_name') and elem.tag.func_name == 'Comment':
            continue
        elem.tag = re.sub("{[^}]+}*", '', str(elem.tag))
