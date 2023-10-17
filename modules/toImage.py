from pdf2image import convert_from_path
import os
from datetime import date


class toImgClass:
    def fromPDF(self, pdf_path):

        # Get today's date in YYYYMMDD format
        today_date = date.today().strftime("%Y-%m-%d")

        # Create a directory to store the images with today's date
        output_directory = os.path.join("imagesUploaded", today_date)
        os.makedirs(output_directory, exist_ok=True)

        # Convert PDF to images
        images = convert_from_path(pdf_path)

        # Get the base name of the PDF (without extension)
        pdf_base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Save the image with the same name as the PDF
        images[0].save(os.path.join(output_directory,
                       f"{pdf_base_name}.png"), "PNG")

        return output_directory
