import cv2
from pyzbar.pyzbar import decode
import numpy as np
import qrcode
import tkinter as tk

cap = cv2.VideoCapture(0)
window = tk.Tk()

# Create a label to display the QR code data as a clickable link
link_label = tk.Label(window, text="", fg="blue", cursor="hand2")
link_label.pack()

def open_link(event):
    # This function will be executed when the link_label is clicked
    import webbrowser
    webbrowser.open(link_label["text"])

# Bind the click event to the label
link_label.bind("<Button-1>", open_link)

while True:
    ret, frame = cap.read()
    decoded_objects = decode(frame)
    print(decoded_objects)

    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        link_label.config(text=data)
        # print(data)
        rect_points = obj.polygon

        if len(rect_points) > 4:
            hull = cv2.convexHull(np.array(rect_points), clockwise=False)
            cv2.polylines(frame, [hull], True, (0, 255, 0), 3)
        else:
            cv2.polylines(frame, [np.array(rect_points)], True, (0, 255, 0), 3)

        cv2.putText(
            frame,
            data,
            (rect_points[0][0], rect_points[0][1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    cv2.imshow("QR Code Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
window.mainloop()

qr = qrcode.QRCode(
    version=1,  # QR code version (adjust as needed)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Error correction level
    box_size=10,  # Size of each QR code block
    border=4,  # Border size around the QR code
)

qr.add_data(data)
qr.make(fit=True)

qr_image = qr.make_image(fill_color="black", back_color="white")

# qr_image.save("qr_code.png")

qr_image.show() 