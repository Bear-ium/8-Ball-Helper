import cv2
import numpy as np
import mss
import keyboard

# Region to capture
x1, y1, x2, y2 = 135, 235, 520, 990
monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}

# Refresh rate
refresh_rate = 75  # Frames per second

# Points for drawing lines
points = []
lines_layer = None  # Separate layer for drawings

# Flag to keep the app running
running = True

def capture_screen():
    """Capture the defined screen region using mss."""
    with mss.mss() as sct:
        frame = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # Convert to BGR for OpenCV
        return frame

def draw_line(event, x, y, flags, param):
    """Handle mouse clicks to capture points and draw straight lines."""
    global points, lines_layer
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button click
        points.append((x, y))
        if len(points) == 2:
            # Draw the line on the lines layer
            cv2.line(lines_layer, points[0], points[1], (0, 0, 255), 2)
            points = []  # Reset points after drawing

# OpenCV window setup
cv2.namedWindow("Screen Capture")
cv2.setMouseCallback("Screen Capture", draw_line)

while running:
    # Capture the defined screen region
    screen = capture_screen()

    # Initialize the drawing layer if not already done
    if lines_layer is None:
        lines_layer = np.zeros_like(screen)

    # Combine the screen with the lines layer
    output = cv2.addWeighted(screen, 1.0, lines_layer, 1.0, 0)

    # Display the captured frame
    cv2.imshow("Screen Capture", output)

    # Check for keyboard inputs
    if keyboard.is_pressed('q'):  # Quit the application
        running = False
    elif keyboard.is_pressed('e'):  # Erase all drawings
        lines_layer = np.zeros_like(screen)  # Reset the drawing layer

    # Refresh at the specified rate
    if cv2.waitKey(int(1000 / refresh_rate)) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
