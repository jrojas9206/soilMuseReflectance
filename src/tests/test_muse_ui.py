import os 
from pathlib import Path
from srmouse.ui.muse_ui import SimpleUI

root = Path(__file__).parent.absolute()
path2spectralCube = Path(os.path.join(root, '../../', 'data', 'Sk_1_15_11_2024', 'Spectral_Cube')).resolve()

objSimpleUI = SimpleUI(path2spectralCube)
objSimpleUI.startUI()