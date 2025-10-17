"""
RoK Rally Bot - Main Application
Automates rally monitoring for Rise of Kingdoms game.
"""

import time
from collections import defaultdict
from datetime import datetime
from utils import connect_to_device, capture_screenshot, process_rally_image


# Configuration
SCAN_INTERVAL = 30  # seconds between scans
SCREENSHOT_DIR = 'screenshots'


class RallyMonitor:
    """Main class to monitor and track rallies."""
    
    def __init__(self, scan_interval=SCAN_INTERVAL):
        """
        Initialize the Rally Monitor.
        
        Args:
            scan_interval (int): Time in seconds between scans
        """
        self.scan_interval = scan_interval
        self.active_rallies = {}  # Dictionary to track active rallies (key: player_name)
        self.player_stats = defaultdict(int)  # Count of rallies per player
        self.device = None
    
    def connect(self):
        """Connect to the Android device."""
        print("=" * 60)
        print("RoK Rally Bot - Starting Up")
        print("=" * 60)
        self.device = connect_to_device()
        return self.device is not None
    
    def update_rally_state(self, new_rallies):
        """
        Update the state of active rallies.
        
        Args:
            new_rallies (list): List of Rally objects from latest scan
        """
        # Create a set of new rally player names
        new_rally_players = {rally.player_name for rally in new_rallies}
        
        # Check for new rallies
        for rally in new_rallies:
            if rally.player_name not in self.active_rallies:
                # New rally detected
                print(f"\n[NEW RALLY DETECTED]")
                print(f"  Player: {rally.player_name}")
                print(f"  Target: {rally.target}")
                print(f"  Status: {rally.status}")
                print(f"  Time: {rally.timestamp.strftime('%H:%M:%S')}")
                
                self.active_rallies[rally.player_name] = rally
                self.player_stats[rally.player_name] += 1
            else:
                # Rally already exists, check if status changed
                existing_rally = self.active_rallies[rally.player_name]
                if existing_rally.status != rally.status:
                    print(f"\n[RALLY STATUS UPDATE]")
                    print(f"  Player: {rally.player_name}")
                    print(f"  Old Status: {existing_rally.status}")
                    print(f"  New Status: {rally.status}")
                    
                    # Update the rally
                    self.active_rallies[rally.player_name] = rally
        
        # Check for completed/removed rallies
        current_rally_players = set(self.active_rallies.keys())
        removed_players = current_rally_players - new_rally_players
        
        for player in removed_players:
            removed_rally = self.active_rallies.pop(player)
            print(f"\n[RALLY COMPLETED/REMOVED]")
            print(f"  Player: {removed_rally.player_name}")
            print(f"  Target: {removed_rally.target}")
    
    def display_stats(self):
        """Display current rally statistics."""
        print("\n" + "=" * 60)
        print("RALLY STATISTICS")
        print("=" * 60)
        print(f"Active Rallies: {len(self.active_rallies)}")
        
        if self.player_stats:
            print("\nRallies Initiated by Player:")
            # Sort by count (descending)
            sorted_stats = sorted(
                self.player_stats.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            for player, count in sorted_stats:
                print(f"  {player}: {count}")
        
        print("=" * 60)
    
    def run(self):
        """Main application loop."""
        if not self.connect():
            print("Failed to connect to device. Exiting.")
            return
        
        print(f"\nMonitoring rallies every {self.scan_interval} seconds...")
        print("Press Ctrl+C to stop.\n")
        
        try:
            iteration = 0
            while True:
                iteration += 1
                print(f"\n[Scan #{iteration}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Capture screenshot
                screenshot_path = capture_screenshot(self.device, SCREENSHOT_DIR)
                
                if screenshot_path:
                    # Analyze screenshot
                    print("Analyzing screenshot...")
                    rallies = process_rally_image(screenshot_path)
                    
                    print(f"Found {len(rallies)} rally/rallies in the screenshot")
                    
                    # Update state
                    self.update_rally_state(rallies)
                    
                    # Display stats every 5 iterations
                    if iteration % 5 == 0:
                        self.display_stats()
                else:
                    print("Failed to capture screenshot. Retrying next cycle...")
                
                # Wait for next scan
                print(f"\nWaiting {self.scan_interval} seconds until next scan...")
                time.sleep(self.scan_interval)
        
        except KeyboardInterrupt:
            print("\n\nStopping RoK Rally Bot...")
            self.display_stats()
            print("\nGoodbye!")


def main():
    """Entry point of the application."""
    monitor = RallyMonitor(scan_interval=SCAN_INTERVAL)
    monitor.run()


if __name__ == "__main__":
    main()
