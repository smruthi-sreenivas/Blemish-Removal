# Blemish-Removal
Blemishes or dark spots are parts of the skin region which have high roughness relative to the neighboring region. We can detect these regions by finding the region with high gradients. For doing so, we convolve the given image with the Sobel Filter or Laplacian filter kernels.
Here is the problem statement in steps

1.Display an image with blemishes on it.

2.The user clicks on the blemish and the blemish is magically gone!

An example image with blemishes is shown below.
![image](https://github.com/user-attachments/assets/81053d38-bcf7-4067-a81f-ac9eeccff3e3)

Blemish removal can be accomplished in two steps.

1.Find an image patch for replacing the blemish region. The best potential patches are in the neighborhood of the blemish region because lighting and texture in this region is likely to be consistent with the blemish region.

2.Blend the patch over the blemish region.
