#!/usr/bin/env python3

import os
import sys
import subprocess
import pathlib
from collections import defaultdict

HEADER = """
<html>
<head>
    <title>{title}</title>
    <style>
        a {{
            color: #0000ee !important;
        }}

        body {{
            padding: 15px;
            margin: 10px;
            border: 2px solid #333333;
            border-radius: 4px;


            position:absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }}

        .entry:hover {{
            border: 1px solid #ababab;
            border-radius: 3px;
        }}

        .entry {{
            border: 1px solid rgba(0,0,0,0);
        }}


    </style>
</head>
<body>

"""

FOOTER = """

</body>
</html>
"""


def main(args):
    files = defaultdict(list)


    if len(args) > 0:
        directory = args[0]
        os.chdir(directory)
    result = subprocess.run(["git", "ls-tree", "-r", "master", "--name-only"], stdout=subprocess.PIPE)
    if result.returncode == 0:
        for line in result.stdout.decode("utf-8").split('\n'):
            path = pathlib.Path(line)
            files[path.parent].append(path.name)
    else:
        print("Git error (are you in a git repository?)")
        exit(1)



    for path, names in files.items():
        with open(path / "index.html", "w") as f:
            f.write(HEADER.format(title=str(path)))

            f.write("<h1>Files:</h1>")

            for name in names:
                f.write(f"<a href=\"{name}\"><div class=\"fileentry entry\">{name}</div></a>")

            f.write("<h1>Directories:</h1>")

            cwd = os.getcwd()
            os.chdir(path)
            for name in next(os.walk('.'))[1]:
                if not name.starts_with(".") and not os.path.islink(name):
                    f.write(f"<a href=\"{name}/index.html\"><div class=\"direntry entry\">{name}</div></a>")
            os.chdir(cwd)

            f.write(FOOTER)




if __name__ == "__main__":
    main(sys.argv[1:])



