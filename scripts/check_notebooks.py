"""Execute every notebook, failing if a cell raises an exception."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

root=Path(__file__).resolve().parents[1]
for path in sorted((root/'notebooks').glob('*.ipynb')):
    notebook=nbformat.read(path,as_version=4)
    print('Executing',path.name,flush=True)
    NotebookClient(notebook,timeout=60,kernel_name='python3',allow_errors=False,
                   resources={'metadata':{'path':str(root)}}).execute()
print('All notebooks executed cleanly.')
