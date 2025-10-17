"""
Utility functions for RoK Rally Bot.
Handles device connection, screenshot capture, and image analysis.
"""

import os
import time
from datetime import datetime
from ppadb.client import Client as AdbClient
import cv2
import numpy as np
from PIL import Image
import pytesseract


class Rally:
    """Class to represent a rally with its details."""
    
    def __init__(self, player_name, target, status):
        """
        Initialize a Rally object.
        
        Args:
            player_name (str): Name of the player initiating the rally
            target (str): Target name/type (e.g., "Lvl 3 Barbarian Fort")
            status (str): Rally status (e.g., "Preparing..." or "Battling")
        """
        self.player_name = player_name
        self.target = target
        self.status = status
        self.timestamp = datetime.now()
    
    def __repr__(self):
        return f"Rally(player='{self.player_name}', target='{self.target}', status='{self.status}')"
    
    def __eq__(self, other):
        """Two rallies are equal if they have the same player name."""
        if isinstance(other, Rally):
            return self.player_name == other.player_name
        return False
    
    def __hash__(self):
        """Hash based on player name for use in sets/dicts."""
        return hash(self.player_name)


def connect_to_device(host='127.0.0.1', port=5037):
    """
    Connect to ADB server and return the first available device.
    
    Args:
        host (str): ADB server host (default: '127.0.0.1')
        port (int): ADB server port (default: 5037)
    
    Returns:
        Device: The first available ADB device, or None if no device found
    """
    try:
        adb = AdbClient(host=host, port=port)
        devices = adb.devices()
        
        if not devices:
            print("No devices connected. Please ensure your emulator is running.")
            return None
        
        device = devices[0]
        print(f"Connected to device: {device.serial}")
        return device
    except Exception as e:
        print(f"Error connecting to ADB: {e}")
        print("Make sure ADB server is running. Try running 'adb start-server' in your terminal.")
        return None


def capture_screenshot(device, output_dir='screenshots'):
    """
    Capture a screenshot from the connected device.
    
    Args:
        device: ADB device object
        output_dir (str): Directory to save screenshots (default: 'screenshots')
    
    Returns:
        str: Path to the saved screenshot, or None if failed
    """
    if device is None:
        print("No device connected. Cannot capture screenshot.")
        return None
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"rally_screen_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        # Capture screenshot using ADB
        screenshot = device.screencap()
        
        # Save screenshot
        with open(filepath, 'wb') as f:
            f.write(screenshot)
        
        print(f"Screenshot saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None


def process_rally_image(image_path):
    """
    Process a rally screenshot to extract rally information.
    
    Based on the user-provided image, we define coordinates for three rally slots.
    These coordinates should be adjusted based on your actual screen resolution.
    
    Args:
        image_path (str): Path to the screenshot image
    
    Returns:
        list: List of Rally objects extracted from the image
    """
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return []
    
    try:
        # Load the image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to load image: {image_path}")
            return []
        
        height, width = img.shape[:2]
        print(f"Image dimensions: {width}x{height}")
        
        rallies = []
        
        # Define ROI coordinates for three rally slots
        # These are example coordinates and should be adjusted based on actual screen layout
        # Format: (x, y, width, height) for each rally slot
        # Assuming rallies are stacked vertically in the "War" screen
        
        # Rally slot 1 (top)
        rally_slots = [
            {'y_start': int(height * 0.15), 'y_end': int(height * 0.35)},  # Top rally
            {'y_start': int(height * 0.40), 'y_end': int(height * 0.60)},  # Middle rally
            {'y_start': int(height * 0.65), 'y_end': int(height * 0.85)},  # Bottom rally
        ]
        
        for idx, slot in enumerate(rally_slots):
            # Extract the rally region
            rally_region = img[slot['y_start']:slot['y_end'], :]
            
            # Convert to grayscale for better OCR
            gray = cv2.cvtColor(rally_region, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding to improve OCR accuracy
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Perform OCR
            text = pytesseract.image_to_string(thresh, config='--psm 6')
            
            # Parse the extracted text
            rally = parse_rally_text(text)
            
            if rally:
                rallies.append(rally)
                print(f"Rally {idx + 1} detected: {rally}")
        
        return rallies
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return []


def parse_rally_text(text):
    """
    Parse OCR text to extract rally information.
    
    This is a basic parser that looks for common patterns.
    You may need to adjust this based on the actual OCR output.
    
    Args:
        text (str): OCR text output
    
    Returns:
        Rally: Rally object if valid rally data found, None otherwise
    """
    if not text or len(text.strip()) < 5:
        return None
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if len(lines) < 2:
        return None
    
    # Try to identify player name, target, and status
    # This is a simplified parser - adjust based on actual OCR output
    player_name = None
    target = None
    status = None
    
    for line in lines:
        # Look for player name (usually contains brackets like [D08K])
        if '[' in line and ']' in line:
            player_name = line
        # Look for target (usually contains "Lvl" or "Barbarian")
        elif 'Lvl' in line or 'Barbarian' in line or 'Fort' in line:
            target = line
        # Look for status
        elif 'Preparing' in line or 'Battling' in line or 'Marching' in line:
            status = line
    
    # If we found at least a player name, create a Rally object
    if player_name:
        target = target or "Unknown Target"
        status = status or "Unknown Status"
        return Rally(player_name, target, status)
    
    return None


def preprocess_image_for_ocr(image):
    """
    Preprocess image to improve OCR accuracy.
    
    Args:
        image: OpenCV image (numpy array)
    
    Returns:
        Preprocessed image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply denoising
    denoised = cv2.fastNlMeansDenoising(gray)
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    return thresh
