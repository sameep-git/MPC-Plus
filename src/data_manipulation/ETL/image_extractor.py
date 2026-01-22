"""
Image Extractor Module
----------------
This module defines the `image_extractor` class, responsible create an 
image object from the given image path.

Supported Image Types:
    - BeamProfileCheck.xim
"""

#import pylinac as pl
from pylinac import FieldAnalysis
from pylinac import image as imgPylinac
from pylinac.core.image import XIM
import numpy as np

class image_extractor:
    def process_image(self, image, is_test=False):
        #baseline_img_png = XIM(r"data/csv_data/NDS-WKS-SN6543-2025-09-18-08-06-01-0004-BeamCheckTemplate6e/BeamProfileCheck.xim")
        #baseline_img = XIM(image.get_path())
        #baseline_img_png = baseline_img = XIM(image.get_path()).array.astype(np.float32)
        #baseline_img_png = np.asarray(baseline_img)
        #raw_img_png = XIM(image.get_path())
        #raw_img_png = raw_img.array.astype(np.float32)
        #raw_img_png = np.asarray(raw_img)
        
        baseline_img = XIM(r"data/csv_data/NDS-WKS-SN6543-2025-09-18-08-06-01-0004-BeamCheckTemplate6e/BeamProfileCheck.xim")
        baseline_img_png = np.asarray(baseline_img)
        raw_img_png = image.get_path()

        # -------------------------------------------------------------------------
        # Small value added to avoid division by zero.
        # Some baseline pixels may be zero or extremely small (dead pixels, edges).
        # This keeps the math stable without affecting real image values.
        # -------------------------------------------------------------------------
        eps = 1e-8

        # -------------------------------------------------------------------------
        # Load the BASELINE image (reference detector response)
        # This image represents the expected or "normal" pixel intensities.
        # -------------------------------------------------------------------------
        # baseline_img = image.load(
        #     "src/image-experimentation/brae/get-damons-working/images-and-reports/10raw.png"
        # )

        # Convert the baseline image to a NumPy array for pixel-wise math
        # baseline_array = np.asarray(baseline_img)

        # -------------------------------------------------------------------------
        # Load the RAW image (image being compared against the baseline)
        # -------------------------------------------------------------------------
        # raw_img = image.load(
        #     "src/image-experimentation/brae/get-damons-working/images-and-reports/10raw_0207.png"
        # )

        # Convert the raw image to a NumPy array
        # raw_array = np.asarray(raw_img)

        # -------------------------------------------------------------------------
        # Compute the mean intensity of the baseline image.
        # This is used to re-scale the corrected image so overall brightness
        # stays consistent with the baseline.
        # -------------------------------------------------------------------------
        mean_baseline = float(np.mean(baseline_img_png))

        # -------------------------------------------------------------------------
        # Perform pixel-by-pixel normalization:
        #   1. Divide the raw image by the baseline image
        #   2. Add eps to prevent divide-by-zero
        #   3. Multiply by the baseline mean to preserve intensity scale
        #
        # This corrects detector non-uniformity while keeping physics intact.
        # -------------------------------------------------------------------------
        corrected = (raw_img_png / (baseline_img_png + eps)) * mean_baseline
        corrected = raw_img_png.astype(np.float32)

        # -------------------------------------------------------------------------
        # Convert the corrected NumPy array back into a DICOM image.
        # Geometry metadata (SID, gantry, collimator, couch) is required
        # so pylinac can properly analyze the image.
        # -------------------------------------------------------------------------
        print("Corrected stats:")
        print("  min:", np.min(corrected))
        print("  max:", np.max(corrected))
        print("  mean:", np.mean(corrected))
        print("  NaNs:", np.isnan(corrected).any())
        print("  Infs:", np.isinf(corrected).any())

        corrected_dicom = imgPylinac.array_to_dicom(
            corrected,
            sid=1000,
            gantry=0,
            coll=0,
            couch=0,
            dpi=280
        )

        # Save the corrected DICOM image to disk
        corrected_dicom.save_as(
            "src/image-experimentation/brae/get-damons-working/images-and-reports/Baseline0201vsRaw0207.dcm"
        )

        # -------------------------------------------------------------------------
        # Run pylinac Field Analysis on the corrected DICOM image
        # -------------------------------------------------------------------------
        corrected_data = (
            "src/image-experimentation/brae/get-damons-working/images-and-reports/"
            "Baseline0201vsRaw0207.dcm"
        )

        # Initialize field analysis
        # my_img = FieldAnalysis(corrected_data)
        my_img = FieldAnalysis(corrected_data)
        # Perform flatness, symmetry, and other field metrics
        my_img.analyze()
        r = my_img.results_data()

        
        image.set_symmetry_horizontal(r.protocol_results['symmetry_horizontal'])
        image.set_symmetry_vertical(r.protocol_results['symmetry_vertical'])
        image.set_flatness_horizontal(r.protocol_results['flatness_horizontal'])
        image.set_flatness_vertical(r.protocol_results['flatness_vertical'])
        if is_test:

            # Print numerical analysis results to the console

            
            print(f"Flatness (Horizontal): {image.get_flatness_horizontal()}")
            print(f"Flatness (Vertical):   {image.get_flatness_vertical()}")
            print(f"Symmetry (Horizontal): {image.get_symmetry_horizontal()}")
            print(f"Symmetry (Vertical):   {image.get_symmetry_vertical()}")

            # Must Close PDF for program to complete         
            # Display the analyzed image with pylinac overlays
            my_img.plot_analyzed_image()

            # Generate a PDF report with results and annotated images
            my_img.publish_pdf(
                filename="src/image-experimentation/brae/get-damons-working/images-and-reports/Baseline0201vsRaw0207.pdf"
            )