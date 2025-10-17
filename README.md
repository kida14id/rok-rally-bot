# RoK Rally Bot

A Python-based automation tool for monitoring rallies in the mobile game "Rise of Kingdoms" (RoK). This bot connects to an Android emulator (LDP9), captures screenshots of the game's "War" rally screen, and uses OCR and computer vision to extract and track rally data.

## Features

- **Automatic Screenshot Capture**: Connects to LDP9 Android emulator via ADB and captures screenshots at configurable intervals
- **OCR & Image Analysis**: Uses Tesseract OCR and OpenCV to extract rally information from screenshots
- **Rally Tracking**: Maintains state of active rallies and detects new rallies, status changes, and completed rallies
- **Player Statistics**: Tracks the number of rallies initiated by each player
- **Duplicate Prevention**: Avoids re-processing unchanged rallies

## Extracted Data

For each rally, the bot extracts:
- **Initiating Player Name** (e.g., `[D08K]DKGoku F2P`)
- **Target Name/Type** (e.g., `Lvl 3 Barbarian Fort`)
- **Rally Status** (e.g., `Preparing...`, `Battling`, `Marching`)

## Prerequisites

### 1. Python Installation
- Install Python 3.7 or higher from [python.org](https://www.python.org/downloads/)
- During installation, make sure to check "Add Python to PATH"

### 2. Tesseract OCR Installation

**Windows:**
1. Download the Tesseract installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer and note the installation path (typically `C:\Program Files\Tesseract-OCR`)
3. Add Tesseract to your system PATH:
   - Open System Properties → Environment Variables
   - Under "System variables", find and edit "Path"
   - Add the Tesseract installation directory (e.g., `C:\Program Files\Tesseract-OCR`)
   - Click OK to save

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### 3. Android Debug Bridge (ADB) Installation

**Windows:**
1. Download Android Platform Tools from [Google](https://developer.android.com/studio/releases/platform-tools)
2. Extract the ZIP file to a folder (e.g., `C:\platform-tools`)
3. Add the folder to your system PATH (same process as Tesseract)

**macOS:**
```bash
brew install android-platform-tools
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install android-tools-adb
```

### 4. LDP9 Emulator Setup
1. Install and launch the LDP9 (LDPlayer) Android emulator
2. Start the emulator and ensure Rise of Kingdoms is installed
3. Enable ADB connection in LDPlayer settings:
   - Open LDPlayer
   - Go to Settings → Other settings
   - Enable "ADB debugging"
4. Verify the emulator is detectable:
   ```bash
   adb devices
   ```
   You should see your emulator listed (e.g., `emulator-5554`)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/kida14id/rok-rally-bot.git
   cd rok-rally-bot
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the ADB server (if not already running):
   ```bash
   adb start-server
   ```

4. Verify your emulator is connected:
   ```bash
   adb devices
   ```

## Configuration

You can modify the following settings in `main.py`:

- `SCAN_INTERVAL`: Time in seconds between screenshot captures (default: 30)
- `SCREENSHOT_DIR`: Directory where screenshots are saved (default: 'screenshots')

### Adjusting Rally Slot Coordinates

The rally slot coordinates in `utils.py` (function `process_rally_image`) may need adjustment based on your screen resolution. The default values are:
- Rally 1 (top): 15-35% of screen height
- Rally 2 (middle): 40-60% of screen height
- Rally 3 (bottom): 65-85% of screen height

To fine-tune these:
1. Capture a screenshot of your "War" rally screen
2. Open it in an image editor to measure the Y-coordinates of each rally slot
3. Update the `rally_slots` array in `utils.py` accordingly

## Usage

1. Launch your LDP9 emulator and open Rise of Kingdoms
2. Navigate to the "War" screen where rallies are displayed
3. Run the bot:
   ```bash
   python main.py
   ```

4. The bot will:
   - Connect to your emulator
   - Start capturing screenshots at regular intervals
   - Analyze each screenshot for rally information
   - Display detected rallies and track their status
   - Show statistics periodically

5. To stop the bot, press `Ctrl+C`

## Output Example

```
============================================================
RoK Rally Bot - Starting Up
============================================================
Connected to device: emulator-5554

Monitoring rallies every 30 seconds...
Press Ctrl+C to stop.

[Scan #1] 2025-10-17 14:21:30
Screenshot saved: screenshots/rally_screen_20251017_142130.png
Analyzing screenshot...
Found 2 rally/rallies in the screenshot

[NEW RALLY DETECTED]
  Player: [D08K]DKGoku F2P
  Target: Lvl 3 Barbarian Fort
  Status: Preparing...
  Time: 14:21:30

[NEW RALLY DETECTED]
  Player: [XYZ]PlayerTwo
  Target: Lvl 5 Barbarian Fort
  Status: Marching
  Time: 14:21:30

Waiting 30 seconds until next scan...
```

## Project Structure

```
rok-rally-bot/
├── main.py              # Main application loop and rally monitoring
├── utils.py             # Utility functions (ADB, screenshot, OCR)
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── screenshots/        # Directory for saved screenshots (auto-created)
```

## Troubleshooting

### "No devices connected"
- Ensure your emulator is running
- Check that ADB can see your device: `adb devices`
- Try restarting ADB server: `adb kill-server && adb start-server`

### "Tesseract not found"
- Verify Tesseract is installed: `tesseract --version`
- Ensure Tesseract is in your system PATH
- On Windows, you may need to set the path manually in `utils.py`:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### Poor OCR Accuracy
- Adjust the rally slot coordinates in `utils.py` to match your screen
- Ensure the game resolution is consistent
- The OCR works best with clear, high-contrast text
- You may need to tune the image preprocessing parameters

### Screenshots are blank or corrupted
- Verify you have permission to write to the screenshots directory
- Check that the emulator screen is visible (not minimized)
- Try capturing a manual screenshot: `adb shell screencap /sdcard/test.png`

## Future Enhancements

- Interactive UI for easier configuration
- Better OCR accuracy with custom training data
- Automatic clicking to gather more rally details
- Export data to CSV/Excel for analysis
- Discord/Telegram notifications for new rallies
- Multi-device support

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational purposes. Use responsibly and in accordance with the game's terms of service.

## Disclaimer

This tool is designed for educational purposes. Using automation tools may violate the terms of service of Rise of Kingdoms. Use at your own risk.
