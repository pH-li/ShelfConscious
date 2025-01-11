"""
All the data associated with identifying what the user is uploading.
"""

# Import statements
import cv2
import streamlit as st


class IdentifyFood:
    """
    This class is intended to allow a user to upload or take a picture,
    which will be identified by our program.
    """

    def __init__(self, *args, **kwargs) -> None:
        st.title('My First Streamlit App')
        st.write('Hello, World!')

    def takePicture(self) -> None:
        """
        This method is responsible just for taking the image.
        """
        # Initialize the camera
        cap = cv2.VideoCapture(0)

        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera.")
            exit()

        # Capture a single frame
        ret, frame = cap.read()

        if ret:
            # Save the captured frame as an image
            cv2.imwrite('captured_image.jpg', frame)
            print("Image captured successfully!")
        else:
            print("Error: Could not capture image.")

        # Release the camera
        cap.release()


if __name__ == '__main__':
    temp = IdentifyFood()
