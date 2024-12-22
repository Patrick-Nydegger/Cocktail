"""
The following file is the main file for the CV. It starts the camera, passes the frames to the CV model, initiates the
normalization of the detected objects (normalize_classes), and the DB interaction (db_interaktion), and finally outputs
the obtained results.A minimal GUI was also implemented
"""

import cv2
from db_interaktion import find_recipes_with_ingredients
from normalize_classes import normalize_classes
from bottle_classifier import BottleClassifier
from ocr_recognition import OCRRecognition
import tkinter as tk
from tkinter import simpledialog, ttk


# Creation of the list for detected classes
recognized_classes = []


# Function for managing the CV module
def cv_main(recognized_classes):
    bottle_classifier = BottleClassifier('best.pt')

    cap = cv2.VideoCapture(0)

    # Setting the confidence required for a label to be detected by bottle_classifications
    confidence_level = 0.5

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame could not be read")
            break

        # Bottle classification
        bottle_classification = bottle_classifier.classify_bottles(frame)

        # Drawing objects with recognized classes
        for x_min, y_min, x_max, y_max, confidence, class_id, class_name in bottle_classification:
            if confidence >= confidence_level:
                label = f"{class_name} ({confidence:.2f})"
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 255, 255), 4)
                cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)

                # Adding the recognized objects to the "recognized_classes" list
                recognized_classes.append(class_name)

        # Display the results in the camera window
        cv2.imshow('PRESS "Q" TO CLOSE WINDOW', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Ask the user for additional ingredients or essentials (everyday ingredients)
    available_essentials = get_available_essentials()

    recognized_classes.extend(available_essentials.split(","))
    recognized_classes = [item.strip() for item in recognized_classes if item.strip()]

    # Create normalized classes
    normalized_classes = normalize_classes(recognized_classes)

    # Find and display recipes
    recipes = find_recipes_with_ingredients(normalized_classes)
    display_recipes_gui(recipes)


# GUI to add additional ingredients or essentials (everyday ingredients)
def get_available_essentials():
    # Create the root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Set a dark theme for the input dialog
    root.configure(bg="#2e2e2e")  # Dark background for root window
    style = ttk.Style()
    style.configure("TButton", background="#4e4e4e", foreground="white")
    style.configure("TLabel", background="#2e2e2e", foreground="white")

    # Display input dialog with dark theme
    input_value = simpledialog.askstring(
        "Input",
        "Enter your available essentials or additional ingredients (like: lemon juice, sugar,...):",
        parent=root
    )

    # If the user clicks "Cancel", input_value will be None
    if input_value is None:
        input_value = ""  # Set to empty string or handle as needed

    # Destroy the root window after input
    root.destroy()
    return input_value


# GUI to display the found recipes
def display_recipes_gui(recipes):
    # Create the main window
    root = tk.Tk()
    root.title("Found Recipes")
    root.geometry("700x600")  # Window size
    root.configure(bg="#2e2e2e")  # Dark gray background

    # Create a scrollable area for recipes
    canvas = tk.Canvas(root, bg="#2e2e2e")
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the style for the frame and label
    style = ttk.Style()
    style.configure("Dark.TFrame", background="#2e2e2e")
    style.configure("NoRecipes.TLabel", background="#2e2e2e", foreground="white", font=("Arial", 14, "bold"))

    scrollable_frame.configure(style="Dark.TFrame")

    # Check if there are recipes
    if not recipes:
        # Display "No matching recipes found"
        no_recipes_label = ttk.Label(scrollable_frame, text="No matching recipes found", style="NoRecipes.TLabel")
        no_recipes_label.pack(pady=20)

    # Display recipes
    for idx, recipe in enumerate(recipes):
        bg_color = "#4e4e4e"

        # Frame for each recipe
        recipe_frame = tk.Frame(scrollable_frame, bg=bg_color, pady=10, padx=10, relief=tk.FLAT, bd=2)
        recipe_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

        # Recipe name
        name_label = tk.Label(recipe_frame, text=recipe['name'].upper(), bg=bg_color, fg="white",
                              font=("Arial", 16, "bold"))
        name_label.pack(anchor="w", pady=5)

        # Ingredients section
        ingredients_label = tk.Label(recipe_frame, text="Ingredients:", bg=bg_color, fg="white",
                                     font=("Arial", 12, "bold"))
        ingredients_label.pack(anchor="w")

        for ingredient in recipe['ingredients']:
            ingredient_label = tk.Label(recipe_frame, text=f"     {ingredient}", bg=bg_color, fg="white",
                                        font=("Arial", 11))
            ingredient_label.pack(anchor="w")

        # Method section
        method_label = tk.Label(recipe_frame, text="Method:", bg=bg_color, fg="white", font=("Arial", 12, "bold"))
        method_label.pack(anchor="w", pady=(10, 0))

        # Display the method with word wrapping
        method_text = tk.Label(
            recipe_frame,
            text=recipe['method'],
            bg=bg_color,
            fg="white",
            wraplength=650,  # Wrap text at 650 pixels
            justify="left",
            font=("Arial", 11)
        )
        method_text.pack(anchor="w", pady=5)

    # Start the main loop
    root.mainloop()



if __name__ == "__main__":
    cv_main(recognized_classes)
