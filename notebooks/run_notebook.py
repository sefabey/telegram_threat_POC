import papermill as pm
from nbconvert import HTMLExporter
import nbformat

# Execute the notebook
pm.execute_notebook("demo_POC.ipynb", "demo_POC_executed.ipynb")


# Convert the notebook to HTML
with open("demo_POC_executed.ipynb", "r") as f:
    nb = nbformat.read(f, as_version=4)

html_exporter = HTMLExporter()
(body, resources) = html_exporter.from_notebook_node(nb)

with open("demo_POC_executed.html", "w") as f:
    f.write(body)
