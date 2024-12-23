"""
The following code is used to extract images from a video.
It was needed to create the training data for the CV-model.
(Video recording of bottles from different angles)
"""
import cv2
import os

# Paths for input video and output folder
input_video_path = r"C:\Users\padin\Documents\_Cocktail ML Wissb systeme\background noice\martini-b.mp4"
output_folder = r"C:\Users\padin\Documents\_Cocktail ML Wissb systeme\martini-b"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the video
video = cv2.VideoCapture(input_video_path)
fps = 15  # fps = Frames per second

count = 0
while True:
    # Read a frame
    success, frame = video.read()
    if not success:
        break

    # Save the frame every 'fps' frames
    if int(video.get(cv2.CAP_PROP_POS_FRAMES)) % int(video.get(cv2.CAP_PROP_FPS) / fps) == 0:
        frame_path = os.path.join(output_folder, f"martini-b_{count:04d}.png")
        cv2.imwrite(frame_path, frame)
        count += 1

video.release()

print("Done")
