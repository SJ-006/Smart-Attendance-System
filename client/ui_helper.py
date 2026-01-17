import cv2

def draw_ui(frame, message, color=(255, 255, 255), name=None, status=None):
    h, w, _ = frame.shape
    # Top Bar
    cv2.rectangle(frame, (0, 0), (w, 50), (0, 0, 0), -1)
    cv2.putText(frame, message, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    # Target Box
    cv2.rectangle(frame, (int(w*0.3), int(h*0.2)), (int(w*0.7), int(h*0.8)), color, 2)
    
    if name:
        label = f"{name.upper()} - {status}"
        cv2.rectangle(frame, (int(w*0.3), int(h*0.8)-35), (int(w*0.7), int(h*0.8)), color, -1)
        cv2.putText(frame, label, (int(w*0.3)+10, int(h*0.8)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)