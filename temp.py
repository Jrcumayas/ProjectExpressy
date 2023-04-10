import cv2
import os
import tkinter as tk
from PIL import Image, ImageTk

# Create a tkinter window
root = tk.Tk()
root.title("Camera")

# Create a label widget to display the video stream
label = tk.Label(root)
label.pack()

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)

# Initialize the camera
cap = cv2.VideoCapture(0)

def isSameImageName(filename):
    counter = 0
    name = filename.replace('.png','')
    while os.path.exists(filename):
        counter += 1
        filename = name + f"{counter}.png"
    return filename

def show_frame():
    ret, frame = cap.read()

    if ret:
        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Convert the image from BGR to RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a PIL image object from the NumPy array
        img = Image.fromarray(img)

        # Create a PhotoImage object from the PIL image object
        img_tk = ImageTk.PhotoImage(image=img)

        # Update the label widget with the new image
        label.img_tk = img_tk
        label.config(image=img_tk)

    # Call this function again after 15 milliseconds
    root.after(15, show_frame)

def take_picture():
    ret, frame = cap.read()
    filename = 'picture.png'

    if ret:
        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Save the image to a file
        cv2.imwrite(isSameImageName(filename), frame)

# Create the buttons
take_picture_button = tk.Button(button_frame, text='Take Picture', command=take_picture)
take_picture_button.pack(side=tk.LEFT, padx=10)

# Call the show_frame function for the first time
recording = False
show_frame()

# Run the tkinter event loop
root.mainloop()

# Release the camera
cap.release()
