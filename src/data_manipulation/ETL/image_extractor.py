"""
Image Extractor Module
----------------
This module defines the `image_extractor` class, responsible create an 
image object from the given image path.

Supported Image Types:
    - BeamProfileCheck.xim
"""

import logging

import numpy as np
import matplotlib.pyplot as plt

from pylinac.field_analysis import FieldAnalysis
from pylinac.core.image import XIM, ArrayImage

# Set up logger for this module
logger = logging.getLogger(__name__)

class image_extractor:
    def process_image(self,imageModel, is_test=False):
        # Load images (you may need to convert XIM to a format pylinac accepts)
        clinicalPath = imageModel.get_path()
        darkPath = imageModel.get_dark_image_path()
        floodPath = imageModel.get_flood_image_path()
        #Load images as numpy arrays
        clinical = np.array(XIM(clinicalPath))
        dark = np.array(XIM(darkPath))
        flood = np.array(XIM(floodPath))
        
        # Apply corrections
        corrected_flood = flood - dark
        corrected_clinical = clinical - dark
        
        # Avoid division by zero
        threshold = 1e-6
        corrected_flood[corrected_flood < threshold] = threshold
        
        # Normalize
        #normalized = corrected_clinical / corrected_flood
        normalized = np.divide(
        corrected_clinical,
        corrected_flood,
        out=np.zeros_like(corrected_clinical, dtype=np.float32),
        where=corrected_flood > threshold
        )

        img = ArrayImage(normalized, dpi = 280)
        analysis = FieldAnalysis(img)
        analysis.analyze()
        r = analysis.results_data()
        
        h = analysis.horiz_profile
        plt.figure()
        plt.plot(h.values)
        plt.title("Horizontal Profile")
        plt.xlabel("Pixel")
        plt.ylabel("Intensity")
        plt.grid(True)

        plt.savefig("horizontal_profile.png", dpi=280, bbox_inches="tight")
        plt.close()

        v = analysis.vert_profile
        plt.figure()
        plt.plot(v.values)
        plt.title("Vertical Profile")
        plt.xlabel("Pixel")
        plt.ylabel("Intensity")
        plt.grid(True)

        plt.savefig("vertical_profile.png", dpi=280, bbox_inches="tight")
        plt.close()

        imageModel.set_symmetry_horizontal(r.protocol_results['symmetry_horizontal'])
        imageModel.set_symmetry_vertical(r.protocol_results['symmetry_vertical'])
        imageModel.set_flatness_horizontal(r.protocol_results['flatness_horizontal'])
        imageModel.set_flatness_vertical(r.protocol_results['flatness_vertical'])
        if is_test:
            # Print numerical analysis results to the console
            logger.info(f"Flatness (Horizontal): {imageModel.get_flatness_horizontal()}")
            logger.info(f"Flatness (Vertical):   {imageModel.get_flatness_vertical()}")
            logger.info(f"Symmetry (Horizontal): {imageModel.get_symmetry_horizontal()}")
            logger.info(f"Symmetry (Vertical):   {imageModel.get_symmetry_vertical()}")
            # Display Flatness and Symmetry Profiles
            h = analysis.horiz_profile
            plt.figure()
            plt.plot(h.values)
            plt.title("Horizontal Profile")
            plt.xlabel("Pixel")
            plt.ylabel("Intensity")
            plt.grid(True)
            plt.show()

            v = analysis.vert_profile
            plt.figure()
            plt.plot(v.values)
            plt.title("Vertical Profile")
            plt.xlabel("Pixel")
            plt.ylabel("Intensity")
            plt.grid(True)
            plt.show()
    # def process_image(self,clinical_path, dark_path, flood_path, is_test=False):
    #     # Load images (you may need to convert XIM to a format pylinac accepts)
    #     logger.info(f"Clinical path: {clinical_path}")
    #     logger.info(f"Dark path: {dark_path}")
    #     logger.info(f"Flood path: {flood_path}")
    #     clinical = XIM(clinical_path)
    #     clinical = np.array(clinical)
    #     dark = XIM(dark_path)
    #     dark = np.array(dark)
    #     flood = XIM(flood_path)
    #     flood = np.array(flood)
        
    #     # Apply corrections
    #     corrected_flood = flood - dark
    #     corrected_clinical = clinical - dark
        
    #     # Avoid division by zero
    #     threshold = 1e-6
    #     corrected_flood[corrected_flood < threshold] = threshold
        
    #     # Normalize
    #     #normalized = corrected_clinical / corrected_flood
    #     normalized = np.divide(
    #     corrected_clinical,
    #     corrected_flood,
    #     out=np.zeros_like(corrected_clinical, dtype=np.float32),
    #     where=corrected_flood > threshold
    #     )

    #     img = ArrayImage(normalized, dpi = 280)
    #     analysis = FieldAnalysis(img)
        
    #     print(analysis)
    #     analysis.analyze()
    #     r = analysis.results()
    #     print(r)
    #     r = analysis.results_data()
    #     print(r)
        
    #     h = analysis.horiz_profile
    #     plt.figure()
    #     plt.plot(h.values)
    #     plt.title("Horizontal Profile")
    #     plt.xlabel("Pixel")
    #     plt.ylabel("Intensity")
    #     plt.grid(True)

    #     plt.savefig("horizontal_profile.png", dpi=300, bbox_inches="tight")
    #     plt.close()

    #     v = analysis.vert_profile
    #     plt.figure()
    #     plt.plot(v.values)
    #     plt.title("Vertical Profile")
    #     plt.xlabel("Pixel")
    #     plt.ylabel("Intensity")
    #     plt.grid(True)

    #     plt.savefig("vertical_profile.png", dpi=300, bbox_inches="tight")
    #     plt.close()

    #     return {
    #         'flatness_x': r.protocol_results['flatness_horizontal'],
    #         'flatness_y': r.protocol_results['flatness_vertical'],
    #         'symmetry_x': r.protocol_results['symmetry_horizontal'],
    #         'symmetry_y': r.protocol_results['symmetry_vertical']
    #     }


