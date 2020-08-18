import json
import markdown


STUDENT_NOTEBOOK_PATH = "Jupyter Notebooks/Programming_Tutorial.ipynb"


def parse_jupyter_json(file_path=STUDENT_NOTEBOOK_PATH):
    """
    parse_jupyter_json(file_path=STUDENT_NOTEBOOK_PATH) is the cleaned 
    and parsed jupyter notebook source file
    """
    fp = open(file_path, "r")
    jupyter_json = json.load(fp)
    fp.close()

    cells = jupyter_json["cells"]

    cleaned_cells = []

    md = markdown.Markdown()

    for cell in cells:
        cell_typ = cell["cell_type"]
        source = cell["source"]
        if cell_typ == "markdown":
            source = "\n".join(source)
            source = md.convert(source)
        cleaned_cells.append((cell_typ, source))

    return cleaned_cells


if __name__ == "__main__":
    print(parse_jupyter_json(file_path=STUDENT_NOTEBOOK_PATH))
