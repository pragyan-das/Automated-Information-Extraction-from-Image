# Automated-PDF-Extraction
This code automatically extracts the information from an image with the help of a configuration file.

How to run the code:

Step1: First Prepare the config file related to the image you want to extract which shall contain the keywords and its value features. The value features specifically contain height and width multipliers that help to extract the exact position in an image. It is nothing but the total coverage area in ratio to the whole image width or height(Ex. if width multiplier is 0.30 , it means the width covers around 30% of total width in an image). Refer to sample config file attached to this repository.

Step2: Create a pickle file that shall contain few important words that can help in spell correction

Step3: Go and run the hocr_main.py file to see your results.
