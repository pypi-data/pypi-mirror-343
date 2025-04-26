"""
Sampling methods for image conversion operations

This module provides different sampling methods for use in equirectangular and perspective image conversions.
"""

import numpy as np
from numba import jit, cuda
from ..utils.projection_utils import check_cuda_support

# Check for CUDA support
HAS_CUDA = check_cuda_support()

# CPU sampling methods
@jit(nopython=True)
def nearest_neighbor_sampling(img, y, x):
    """
    Sample image using nearest neighbor interpolation
    
    Parameters:
    - img: Source image
    - y: Y coordinate
    - x: X coordinate
    
    Returns:
    - RGB pixel value
    """
    h, w = img.shape[:2]
    
    # Convert to float, clip, then round to nearest integer
    x_int = int(round(min(max(0.0, float(x)), w - 1)))
    y_int = int(round(min(max(0.0, float(y)), h - 1)))
    
    return img[y_int, x_int]

@jit(nopython=True)
def bilinear_sampling(img, y, x):
    """
    Sample image using bilinear interpolation
    
    Parameters:
    - img: Source image
    - y: Y coordinate
    - x: X coordinate
    
    Returns:
    - RGB pixel value
    """
    h, w = img.shape[:2]
    
    # Convert to float and clip in one step
    x = min(max(0.0, float(x)), w - 1.001)  # Small epsilon to avoid edge overflow
    y = min(max(0.0, float(y)), h - 1.001)
    
    # Get integer and fractional parts
    x0 = int(np.floor(x))
    y0 = int(np.floor(y))
    x1 = min(x0 + 1, w - 1)
    y1 = min(y0 + 1, h - 1)
    
    # Calculate interpolation weights
    wx = x - x0
    wy = y - y0
    
    # Perform bilinear interpolation for each channel
    result = np.zeros(3, dtype=np.uint8)
    for c in range(3):
        top = img[y0, x0, c] * (1.0 - wx) + img[y0, x1, c] * wx
        bottom = img[y1, x0, c] * (1.0 - wx) + img[y1, x1, c] * wx
        result[c] = np.uint8(top * (1.0 - wy) + bottom * wy)
    
    return result

@jit(nopython=True)
def sample_image(img, y, x, method):
    """
    Sample a pixel from an image using the specified filtering method.
    
    Parameters:
        img (numpy.ndarray): Source image array
        y (float): Y coordinate in the source image
        x (float): X coordinate in the source image
        method (str): Filtering method ('nearest', 'bilinear')
        
    Returns:
        numpy.ndarray: RGB values of the sampled pixel
    """
    if method == "bilinear":
        return bilinear_sampling(img, y, x)
    else:  # Default to nearest neighbor
        return nearest_neighbor_sampling(img, y, x)

# GPU sampling methods (only defined if CUDA is available)
if HAS_CUDA:
    @cuda.jit(device=True)
    def nearest_neighbor_sampling_gpu(img, y, x, w, h):
        """
        Device function for nearest neighbor sampling on GPU
        
        Parameters:
        - img: Source image
        - y, x: Coordinates
        - w, h: Image dimensions
        
        Returns:
        - RGB pixel values as tuple
        """
        # Round and clip coordinates
        px = int(round(min(max(0, x), w-1)))
        py = int(round(min(max(0, y), h-1)))
        
        # Return pixel values as tuple (CUDA can't return arrays from device functions)
        return img[py, px, 0], img[py, px, 1], img[py, px, 2]
    
    @cuda.jit(device=True)
    def bilinear_sampling_gpu(img, y, x, w, h):
        """
        Device function for bilinear sampling on GPU
        
        Parameters:
        - img: Source image
        - y, x: Coordinates
        - w, h: Image dimensions
        
        Returns:
        - RGB pixel values as tuple
        """
        # Ensure coordinates are within bounds
        x = min(max(0, x), w - 1.001)
        y = min(max(0, y), h - 1.001)
        
        # Get integer and fractional parts
        x0 = int(x)
        y0 = int(y)
        x1 = min(x0 + 1, w - 1)
        y1 = min(y0 + 1, h - 1)
        
        # Calculate interpolation weights
        wx = x - x0
        wy = y - y0
        
        # Results for each channel
        r = 0
        g = 0
        b = 0
        
        # Calculate interpolation for each channel
        top_r = img[y0, x0, 0] * (1 - wx) + img[y0, x1, 0] * wx
        bottom_r = img[y1, x0, 0] * (1 - wx) + img[y1, x1, 0] * wx
        r = int(top_r * (1 - wy) + bottom_r * wy)
        
        top_g = img[y0, x0, 1] * (1 - wx) + img[y0, x1, 1] * wx
        bottom_g = img[y1, x0, 1] * (1 - wx) + img[y1, x1, 1] * wx
        g = int(top_g * (1 - wy) + bottom_g * wy)
        
        top_b = img[y0, x0, 2] * (1 - wx) + img[y0, x1, 2] * wx
        bottom_b = img[y1, x0, 2] * (1 - wx) + img[y1, x1, 2] * wx
        b = int(top_b * (1 - wy) + bottom_b * wy)
        
        return r, g, b
