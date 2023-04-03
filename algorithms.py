import numpy as np
from scipy import ndimage as ndi
from skimage import (exposure, feature, filters, io, measure,
                     morphology, restoration, segmentation, transform,
                     util)


class Segmentation():

    def __init__(self, debug=True, img=None):
        self.debug = debug

        if self.debug:
            import napari

        self.viewer = napari.view_image(
            img, name='raw image', visible=False) if self.debug else None
        return

    def rescale_intensity(self, img=None, **kwargs):
        min_quantile = kwargs.get('min_quantile', 0.05)
        max_quantile = kwargs.get('max_quantile', 0.95)
        vmin, vmax = np.quantile(
            img, q=(min_quantile, max_quantile))
        img = exposure.rescale_intensity(
            img, in_range=(vmin, vmax), out_range=np.float32)

        if self.debug:
            self.viewer.add_image(img, name='rescale_intensity', visible=False)
        return img

    def subtract_background_noise(self, img=None, **kwargs):
        radius = kwargs.get('radius', 5)
        background = restoration.rolling_ball(img, radius=radius)
        img = img - background
        if self.debug:
            self.viewer.add_image(background, name='background', visible=False)
            self.viewer.add_image(
                img, name='subtract_background_noise', visible=False)
        return img

    def deconvolution(self, img=None, **kwargs):
        psf_size = kwargs.get('psf_size', 5)
        num_iter = kwargs.get('num_iter', 30)
        psf = np.ones((psf_size, psf_size, psf_size)) / 25
        img = restoration.richardson_lucy(img, psf, num_iter=num_iter)

        if self.debug:
            self.viewer.add_image(img, name='deconvolution', visible=False)
        return img

    def edges(self, img=None, **kwargs):
        method = kwargs.get('method', 'add')
        erosion_size = kwargs.get('erosion_size', 5)
        erosion = kwargs.get('erosion', False)

        edges = filters.sobel(img)
        if method == 'add':
            img = img + edges
        else:
            if erosion:
                edges = morphology.erosion(edges)
            img = img - edges

        if self.debug:
            self.viewer.add_image(edges, name='nuclei edges', visible=False)
            self.viewer.add_image(img, name=f'{method}_edges', visible=False)
        return img

    def _erosion(self, img=None, **kwargs):

        if self.debug:
            self.viewer.add_image(img, name='erosion', visible=False)
        return img

    def median_filter(self, img=None, **kwargs):
        ball_size = kwargs.get('ball_size', 5)
        img = filters.median(img, morphology.ball(ball_size))

        if self.debug:
            self.viewer.add_image(img, name='median_filter', visible=False)
        return img

    def binarize(self, img=None, **kwargs):
        block_size = kwargs.get('block_size', 101)
        img = img > filters.threshold_local(img, block_size)
        # img = img > filters.threshold_otsu(img)
        # threshold = kwargs.get('threshold', 0.5)
        # img = img > threshold

        if self.debug:
            self.viewer.add_image(img, name='binarize', visible=False)
        return img

    def binary_remove_small_objects(self, img=None, **kwargs):
        width = kwargs.get('width', 20)
        img = morphology.remove_small_objects(img, min_size=width ** 3)
        if self.debug:
            self.viewer.add_image(
                img, name='binary_remove_small_objects', visible=False)
        return img

    def binary_remove_small_holes(self, img=None, **kwargs):
        width = kwargs.get('width', 20)
        img = morphology.remove_small_holes(img, area_threshold=width ** 3)

        if self.debug:
            self.viewer.add_image(
                img, name='binary_remove_small_holes', visible=False)
        return img

    def binary_fill_holes(self, img=None, **kwargs):
        for idx in range(0, img.shape[0]):
            img[idx, :, :] = ndi.binary_fill_holes(img[idx, :, :])
        # img = ndi.binary_fill_holes(img)

        if self.debug:
            self.viewer.add_image(img, name='binary_fill_holes', visible=False)
        return img

    def watershed_segmentation(self, img=None, **kwargs):
        ball_size = kwargs.get('ball_size', 5)
        min_distance = kwargs.get('min_distance', 8)
        compactness = kwargs.get('compactness', 0.1)

        distance = ndi.distance_transform_edt(img)
        # erode the image to get rid of the overlapping nucleus and divide them
        # img_eroded = morphology.binary_erosion(img)
        # img_eroded = morphology.binary_erosion(img_eroded)
        # distance = distance * img_eroded

        local_max_coords = feature.peak_local_max(distance, indices=False, min_distance=min_distance, footprint=morphology.ball(
            ball_size), exclude_border=False)  # , labels=labels
        markers = measure.label(morphology.dilation(
            local_max_coords, footprint=morphology.ball(5)))
        img = segmentation.watershed(-distance, markers, mask=img,
                                     watershed_line=True, compactness=compactness)

        if self.debug:
            self.viewer.add_image(-distance, blending='additive',
                                  colormap='gray_r', name=f'-distance', visible=False)
            self.viewer.add_image(
                markers, blending='additive', colormap='red', name=f'markers', visible=False)
            self.viewer.add_labels(
                img, name=f'watershed_compactness:{compactness}_min_distance:{min_distance}', visible=False)
        return img

    def your_new_algorithm(self, img=None, **kwargs):
        param_1 = kwargs.get('param_1', 'default value here')
        param_2 = kwargs.get('param_2', 'default value here')

        #
        # write your own algorithm here
        #
        if self.debug:
            self.viewer.add_image(
                img, name='your_new_algorithm', visible=False)
        return img
