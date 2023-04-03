import json
from datetime import datetime
import copy


import os
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage import exposure, feature, filters, io, measure, morphology, restoration, segmentation, transform, util
from tqdm import tqdm

# from aicsimageio import AICSImage
from algorithms import Segmentation


ALL_PROPERTIES = [
    "area",
    "area_bbox",
    "area_convex",
    "area_filled",
    "axis_major_length",
    "axis_minor_length",
    "bbox",
    "centroid",
    "centroid_local",
    "coords",
    "equivalent_diameter_area",
    "euler_number",
    "extent",
    "feret_diameter_max",
    "image",
    "image_convex",
    "image_filled",
    "inertia_tensor",
    "inertia_tensor_eigvals",
    "label",
    "moments",
    "moments_central",
    "moments_normalized",
    "slice",
    "solidity",
]


class Nucleus3DSegmentation:
    def __init__(self, settings={}):
        self.img_path = settings["img_path"]
        self.debug = settings["debug"]
        self.properties = settings["properties"]
        self.raw_settings = copy.deepcopy(settings)
        self.settings = settings
        self.img = None
        self.actin_img = None
        self.segmented_img = None
        self.segmentation = None
        self.stats = None

        self.output_dir = f"{settings['output_dir']}/{settings['img_path'].split('/')[-1].split('.')[0]}"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.load_img(self.img_path)
        return

    def load_img(self, img_path):
        print(f"Loading the image...")

        if not self.settings.get("multichannel", False):
            self.img = io.imread(img_path)
            # self.img = AICSImage(img_path).get_image_data("ZYX", C=1, S=0, T=0)

        else:
            from aicsimageio import AICSImage

            nuclei_channel = self.settings.get("nuclei_channel", 2)
            # self.img = io.imread(img_path)[:, :, nuclei_channel]
            self.img = AICSImage(img_path).get_image_data("ZYX", C=nuclei_channel - 1, S=0, T=0, B=0, V=0)

            try:
                actin_channel = self.settings.get("actin_channel", 1)
                self.actin_img = io.imread(img_path)
                # self.actin_img = AICSImage(img_path).get_image_data("ZYX", C=actin_channel-1, S=0, T=0, B=0, V=0)
            except:
                self.actin_img = None

        if not self.settings["use_all"]:
            start_slice = self.settings["start_slice"]
            end_slice = self.settings["end_slice"]
            self.img = self.img[start_slice:end_slice, :, :]

        self.segmentation = Segmentation(debug=self.debug, img=self.img)
        self.assign_functions()
        print(f"nuclei image shape: {self.img.shape}")
        print(f"actin image shape: {self.actin_img.shape if self.actin_img is not None else None}")
        return

    def assign_functions(self):
        for each in self.settings["schedule"]:
            try:
                each["func"] = eval(f'self.segmentation.{each["method"]}')
            except:
                raise ValueError(f"Method not found: {each['method']}. Check your spelling and available methods.")

        return

    def run(self):
        self.segmented_img = self.img
        for each in tqdm(self.settings["schedule"]):
            print(f'{each["method"]}: {each["params"]}')
            self.segmented_img = each["func"](img=self.segmented_img, **each["params"])

        self.save()

        if self.debug:
            import napari

            napari.run()
        return

    def analysis(self):
        self.stats = measure.regionprops_table(self.segmented_img, properties=self.properties)
        vertices, faces, _, _ = measure.marching_cubes(self.segmented_img)
        surface_area = measure.mesh_surface_area(vertices, faces)
        self.stats["surface_area"] = surface_area
        return

    def save(self):
        if self.settings.get("save", True):
            print(f"Saving the results...")
            current_time = datetime.today().strftime("%Y%m%d_%H%M%S")

            """analysis"""
            if self.settings["analysis"]:
                print(f"Analyzing the segmented image...")
                self.analysis()
                df = pd.DataFrame(self.stats)
                df.to_pickle(os.path.join(self.output_dir, f"{current_time}_results.pkl"))
                df.to_csv(os.path.join(self.output_dir, f"{current_time}_results.csv"))

            """save segmented image as numpy array"""
            with open(os.path.join(self.output_dir, f"{current_time}_results.npy"), "wb") as f:
                np.save(f, self.segmented_img)
            # io.imsave(self.output_dir +
            #           f'/{current_time}_segmented.tif', self.segmented_img)

            """save settings used in this run"""
            with open(os.path.join(self.output_dir, f"{current_time}_settings.json"), "w") as f:
                json.dump(self.raw_settings, f, indent=4, ensure_ascii=False)

        print(f"Finished.")
        return
