# Cocktail
ML and Knowledge engineering project 

The “Cocktail” project was about building an AI system that uses computer vision and a graphical database to suggest and give recipes for cocktails that can be made with the house bar. Python was used for the project. In the first approach, a consistent git link was dispensed with, as the aim was to try out many different things and iteratively find a possible solution with the help of ChatGPT and co. This was structured as follows: YOLOv8 for bottle recognition (pre-trained COCO- class-id 39), then bottle tracking, forwarding the objects to the OCR function for reading the etiquette, then outputting all OCR texts of a bottle as a list per bottle. the last step, the comparison of the OCR text lists with a database of possible texts per predefined bottle categories (Whiskey Rum, Campari,...) was not yet implemented due to the very poor performance of the OCR. This could still be done as a basis for comparative work. After 12 attempts, the object recognition was basically usable, but not optimal. The Python code generated by ChatGPT was also of a very low quality - it worked, but was very complicated. Therefore, the approach was changed and the bottle labels are now trained directly via YOLOv8 (6 classes, 2514 labeled images, after processing: rotation, exposure, distortion total 6034 labeled images). This resulted in very high instance recognition. Problem: changes in bottle design require new training, upscaling to many classes is very time-consuming, recognition only of the original bottles, a self-filled beverage cannot be recognized.