# NST_VGG19

Neural Style Transfer using VGG19.
Original paper https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf
VGG19 weights from `torchvision`.

## Installation

```bash
pip install nst_vgg19
```

## Usage

```
from nst_vgg19 import NST_VGG19
import cv2

def load_image(path):
  img = cv2.imread(path)
  return cv.cvtColor(style_image, cv2.COLOR_BGR2RGB) # cv2 loads BGR by default so we convert

style_image = load_image('style.png')
content_image_1 = load_image('img1.jpg')
content_image_2 = load_image('img2.png')

nst = NST_VGG19(style_image)

result_1 = nst(content_image_1)
result_2 = nst(content_image_2)

cv2.imwrite('result1.png', cv2.cvtColor(result_1, cv2.COLOR_RGB2BGR))
cv2.imwrite('result2.png', cv2.cvtColor(result_2, cv2.COLOR_RGB2BGR))
```

## NST_VGG19 constructor options

* style_image_numpy: Numpy array of the style image in format (Heght, Width, Channels). This is a default Numpy image array.
* content_layers_weights: Dictionary of weights for content losses.
* style_layers_weights: Dictionary of weights for style losses.
* quality_loss_weight: Weight for quality loss.
* delta_loss_threshold: Loss change threshold for stopping optimization.

If you do not specify weights of loss, the folowing parameters will be used:

```
DEFAULT_CONTENT_WEIGHTS = {
    'conv_1': 35000,  # Shape?
    'conv_2': 28000,
    'conv_4': 30000,
}
DEFAULT_STYLE_WEIGHTS = {
    'conv_2': 0.000001,  # Light/shadow?
    'conv_4': 0.000009,  # Contrast?
    'conv_5': 0.000006,  # Volume?
    'conv_7': 0.000003,
    'conv_8': 0.000002,  # Dents?
    'conv_9': 0.000003
}
quality_loss_weight=2e-4
delta_loss_threshold=1
```
