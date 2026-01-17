import cv2
import time
import numpy as np

# Modern Color Palette
COLOR_CYAN = (255, 255, 0)
COLOR_NEON_GREEN = (50, 255, 50)
COLOR_NEON_RED = (50, 50, 255)
COLOR_DARK_GRAY = (20, 20, 20)

def draw_futuristic_hud(frame, status_text, color=COLOR_CYAN):
    h, w, _ = frame.shape
    
    # 1. Add a semi-transparent dark overlay for a "cinematic" look
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)

    # 2. Draw Corner Brackets (Modern Scanner Look)
    length = 40
    thickness = 2
    # Top-Left
    cv2.line(frame, (50, 50), (50 + length, 50), color, thickness)
    cv2.line(frame, (50, 50), (50, 50 + length), color, thickness)
    # Top-Right
    cv2.line(frame, (w-50, 50), (w-50-length, 50), color, thickness)
    cv2.line(frame, (w-50, 50), (w-50, 50 + length), color, thickness)
    # Bottom-Left
    cv2.line(frame, (50, h-50), (50 + length, h-50), color, thickness)
    cv2.line(frame, (50, h-50), (50, h-50 - length), color, thickness)
    # Bottom-Right
    cv2.line(frame, (w-50, h-50), (w-50-length, h-50), color, thickness)
    cv2.line(frame, (w-50, h-50), (w-50, h-50 - length), color, thickness)

    # 3. Status Sidebar (Left side)
    cv2.rectangle(frame, (0, 0), (220, h), (10, 10, 10), -1)
    cv2.line(frame, (220, 0), (220, h), color, 1)
    
    cv2.putText(frame, "CORE SYSTEM", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 0.6, color, 1)
    cv2.putText(frame, "STATUS:", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
    cv2.putText(frame, status_text.upper(), (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

def draw_scanning_line(frame, color=COLOR_CYAN):
    """Draws a moving horizontal line to simulate a laser scan."""
    h, w, _ = frame.shape
    # Use time to calculate the line position
    t = time.time() % 2  # 2-second loop
    y_pos = int((t / 2) * (h - 100)) + 50
    
    # Draw the main laser line
    cv2.line(frame, (220, y_pos), (w-50, y_pos), color, 1)
    # Add a slight glow effect
    overlay = frame.copy()
    cv2.line(overlay, (220, y_pos), (w-50, y_pos), color, 5)
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

def draw_attendance_card(frame, name, status, color=COLOR_NEON_GREEN):
    """A sleek card that pops up when someone is recognized."""
    # Centered Card
    h, w, _ = frame.shape
    cw, ch = 300, 120
    x, y = 240, h - 150
    
    cv2.rectangle(frame, (x, y), (x + cw, y + ch), (0, 0, 0), -1)
    cv2.rectangle(frame, (x, y), (x + cw, y + ch), color, 1)
    
    cv2.putText(frame, "STUDENT VERIFIED", (x + 20, y + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color, 1)
    cv2.putText(frame, name.upper(), (x + 20, y + 75), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, f"STATUS: {status}", (x + 20, y + 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)