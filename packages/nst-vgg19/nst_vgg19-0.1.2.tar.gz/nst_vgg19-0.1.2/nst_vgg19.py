import numpy as np
import torch
import torch.nn as nn
from torch.optim import LBFGS
import torch.nn.functional as F
from torchvision import models, transforms

class ContentLoss(nn.Module):
    def __init__(self, weight=1.0):
        super(ContentLoss, self).__init__()
        self.target = None
        self.weight = weight

    def forward(self, input):
        if self.target is not None:
            self.loss = self.weight * F.mse_loss(input, self.target) / input.numel()
        return input


class StyleLoss(nn.Module):
    def __init__(self, target_feature, weight=1.0):
        super(StyleLoss, self).__init__()
        self.target = self.gram_matrix(target_feature).detach()
        self.weight = weight

    def forward(self, input):
        G = self.gram_matrix(input)
        self.loss = self.weight * F.mse_loss(G, self.target)
        return input

    @staticmethod
    def gram_matrix(input):
        a, b, c, d = input.size()
        features = input.view(a * b, c * d)  # Flatten the feature map
        G = torch.mm(features, features.t())  # Compute Gram matrix
        return G.div((a * b * c * d) ** 0.5)  # Normalize the Gram matrix

class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        self.mean = mean.clone().detach().view(-1, 1, 1)
        self.std = std.clone().detach().view(-1, 1, 1)

    def forward(self, img):
        return (img - self.mean) / self.std  # Normalize the image

class NST_VGG19:
    def __init__(self, style_image_numpy, style_layers_weights=None, content_layers_weights=None, quality_loss_weight=2e-4, delta_loss_threshold=1):
        """
        Neural Style Transfer using VGG19.
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
        :param style_image_numpy: Numpy array of the style image (H, W, C).
        :param content_layers_weights: Dictionary of weights for content losses. 
        :param style_layers_weights: Dictionary of weights for style losses.
        :param quality_loss_weight: Weight for quality loss.
        :param delta_loss_threshold: Loss change threshold for stopping optimization.
        """
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

        # Use default weights if user doesn't provide custom ones
        self.content_layers_weights = content_layers_weights if content_layers_weights is not None else DEFAULT_CONTENT_WEIGHTS
        self.style_layers_weights = style_layers_weights if style_layers_weights is not None else DEFAULT_STYLE_WEIGHTS
        self.quality_loss_weight = quality_loss_weight
        self.delta_loss_threshold = delta_loss_threshold

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Use GPU if available

        self.style_image_tensor = self.get_style_tensor(style_image_numpy)  # Preprocess style image

        self.vgg19 = models.vgg19(weights=models.VGG19_Weights.IMAGENET1K_V1).features.to(self.device).eval()  # Load VGG19 model

        self.model, self.content_losses, self.style_losses = self.build_model()  # Build the NST model

    def get_style_tensor(self, style_image_numpy):
        style_image_tensor = torch.from_numpy(style_image_numpy).permute(2, 0, 1).float() / 255.0  # Convert (H, W, C) to (C, H, W)

        style_height, style_width = style_image_numpy.shape[:2]
        resize = transforms.Resize((style_height // 2, style_width // 2), interpolation=transforms.InterpolationMode.BICUBIC)

        # fix jipegs
        style_image_tensor = resize(style_image_tensor.unsqueeze(0)).to(self.device)

        return style_image_tensor

    def image_to_tensor(self, numpy_image):
        tensor = np.transpose(numpy_image, (2, 0, 1)).astype("float32") / 255.0
        tensor = np.expand_dims(tensor, axis=0)
        return torch.tensor(tensor).to(self.device, torch.float)

    def tensor_to_image(self, tensor):
        img = tensor.squeeze(0).cpu().detach().numpy()
        img = np.transpose(img, (1, 2, 0))
        img = (img * 255).clip(0, 255).astype("uint8")
        return img

    def quality_loss(self, x, sigma_s=0.1, sigma_r=0.05):
        """Sort of bilateral loss"""
        image_height = x.shape[1]
        image_width = x.shape[2]

        # Differences along horizontal and vertical axes (vector norms)
        dx = torch.norm(x[:, :image_height - 1, :image_width - 1, :] - x[:, 1:, :image_width - 1, :], dim=-1)
        dy = torch.norm(x[:, :image_height - 1, :image_width - 1, :] - x[:, :image_height - 1, 1:, :], dim=-1)

        # Gaussian weights for spatial proximity (sigma_s) and intensity similarity (sigma_r)
        spatial_weight = torch.exp(-((dx ** 2) / (2 * sigma_s ** 2)))
        intensity_weight = torch.exp(-((dy ** 2) / (2 * sigma_r ** 2)))

        # Weighted sum of differences
        loss = (spatial_weight * dx ** 2 + intensity_weight * dy ** 2).sum()

        # Additional penalty for RGB channel differences
        rgb_dx = x[:, :image_height - 1, :image_width - 1, :] - x[:, 1:, :image_width - 1, :]
        rgb_dy = x[:, :image_height - 1, :image_width - 1, :] - x[:, :image_height - 1, 1:, :]
        rgb_penalty = (rgb_dx ** 2).mean(dim=-1) + (rgb_dy ** 2).mean(dim=-1)
        loss += rgb_penalty.sum()

        # Local contrast
        local_contrast = torch.abs(dx) + torch.abs(dy)
        loss += local_contrast.mean()

        return loss / (image_width * image_height * x.shape[0])

    def build_model(self):
        normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(self.device)
        normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(self.device)

        model = nn.Sequential(Normalization(normalization_mean, normalization_std).to(self.device))
        content_losses = []
        style_losses = []
        i = 0

        for layer in self.vgg19.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = f'conv_{i}'
            elif isinstance(layer, nn.ReLU):
                name = f'relu_{i}'
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = f'pool_{i}'
            elif isinstance(layer, nn.BatchNorm2d):
                name = f'bn_{i}'
            else:
                raise RuntimeError(f'Unrecognized layer: {layer.__class__.__name__}')

            model.add_module(name, layer)

            # Model does N layers then calc loss for N layers, then does other M layers and calc loss to N+M layers...

            if name in self.content_layers_weights:
                content_loss = ContentLoss(self.content_layers_weights[name])
                model.add_module(f"content_loss_{i}", content_loss)
                content_losses.append(content_loss)

            if name in self.style_layers_weights:
                target_feature = model(self.style_image_tensor).detach()
                style_loss = StyleLoss(target_feature, self.style_layers_weights[name])
                model.add_module(f"style_loss_{i}", style_loss)
                style_losses.append(style_loss)

        for i in range(len(model) - 1, -1, -1):
            if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
                break

        model = model[:(i + 1)]

        return model, content_losses, style_losses

    def set_content_losses(self, content_image_tensor):
        temp_model = nn.Sequential()

        for module in self.model:
            if isinstance(module, ContentLoss):
                target = temp_model(content_image_tensor).detach()
                module.target = target
            else:
                temp_model.add_module(str(len(temp_model)), module)

    def __call__(self, content_image_np):
        """
        Perform style transfer on a content image.

        Args:
            content_image_np (np.ndarray): Content image as a numpy array (H, W, C).

        Returns:
            np.ndarray: Resulting styled image as a numpy array (H, W, C).
        """
        content_image_tensor = self.image_to_tensor(content_image_np)
        input_img = content_image_tensor.clone().contiguous()
        noise = torch.randn_like(input_img)
        input_img = input_img * 0.91 + noise * 0.01

        # Update content losses with the new content image
        self.set_content_losses(content_image_tensor)

        # Optimize
        optimizer = LBFGS([input_img.requires_grad_()], max_iter=2000, history_size=2000, tolerance_change=self.delta_loss_threshold * 0.00001)

        def closure():
            optimizer.zero_grad()

            # Compute total variation loss
            variation_score = self.quality_loss(input_img) * self.quality_loss_weight

            # Compute features through the model
            self.model(input_img)

            # Total loss
            loss = sum(sl.loss for sl in self.style_losses) ** 2 + sum(cl.loss for cl in self.content_losses) ** 2 + variation_score

            # Backpropagate gradients
            loss.backward()
            return loss

        optimizer.step(closure)

        return self.tensor_to_image(input_img)