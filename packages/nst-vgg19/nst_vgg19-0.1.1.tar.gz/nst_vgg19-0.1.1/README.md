# NST_VGG19

Neural Style Transfer using VGG19.

## Installation

```bash
pip install nst_vgg19
```

## Usage
```
import numpy as np
from nst_vgg19 import NST_VGG19

style_image = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
content_image = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)

nst = NST_VGG19(style_image)
result = nst(content_image)
```
