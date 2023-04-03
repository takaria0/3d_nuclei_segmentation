from scipy import ndimage as ndi
from skimage.measure import marching_cubes, mesh_surface_area
from skimage.segmentation import find_boundaries


def surface_area(img):
    verts, faces, _, _ = marching_cubes(img, 0)
    area = mesh_surface_area(verts, faces)
    return area
