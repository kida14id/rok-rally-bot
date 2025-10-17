"""
Example demonstration of the Rally data structure and workflow.
This script shows how the bot processes rally data without requiring actual dependencies.
"""


class Rally:
    """Example Rally class (simplified for demo)."""
    
    def __init__(self, player_name, target, status):
        self.player_name = player_name
        self.target = target
        self.status = status
    
    def __repr__(self):
        return f"Rally(player='{self.player_name}', target='{self.target}', status='{self.status}')"


def demo_rally_detection():
    """Demonstrate rally detection and tracking."""
    print("=" * 60)
    print("RoK Rally Bot - Demo Workflow")
    print("=" * 60)
    print()
    
    # Simulate detected rallies from screenshot analysis
    print("Simulating screenshot capture and analysis...")
    print()
    
    # First scan
    print("[Scan #1] Detected rallies:")
    scan1_rallies = [
        Rally("[D08K]DKGoku F2P", "Lvl 3 Barbarian Fort", "Preparing..."),
        Rally("[XYZ]PlayerTwo", "Lvl 5 Barbarian Fort", "Marching"),
    ]
    
    active_rallies = {}
    player_stats = {}
    
    for rally in scan1_rallies:
        print(f"  [NEW RALLY DETECTED]")
        print(f"    Player: {rally.player_name}")
        print(f"    Target: {rally.target}")
        print(f"    Status: {rally.status}")
        print()
        
        active_rallies[rally.player_name] = rally
        player_stats[rally.player_name] = player_stats.get(rally.player_name, 0) + 1
    
    print(f"Active rallies: {len(active_rallies)}")
    print()
    
    # Second scan - status update
    print("-" * 60)
    print("[Scan #2] Detected rallies:")
    scan2_rallies = [
        Rally("[D08K]DKGoku F2P", "Lvl 3 Barbarian Fort", "Battling"),  # Status changed
        Rally("[XYZ]PlayerTwo", "Lvl 5 Barbarian Fort", "Marching"),  # No change
        Rally("[ABC]NewPlayer", "Lvl 4 Barbarian Fort", "Preparing..."),  # New rally
    ]
    
    new_rally_players = {rally.player_name for rally in scan2_rallies}
    
    for rally in scan2_rallies:
        if rally.player_name not in active_rallies:
            print(f"  [NEW RALLY DETECTED]")
            print(f"    Player: {rally.player_name}")
            print(f"    Target: {rally.target}")
            print(f"    Status: {rally.status}")
            print()
            
            active_rallies[rally.player_name] = rally
            player_stats[rally.player_name] = player_stats.get(rally.player_name, 0) + 1
        else:
            existing = active_rallies[rally.player_name]
            if existing.status != rally.status:
                print(f"  [RALLY STATUS UPDATE]")
                print(f"    Player: {rally.player_name}")
                print(f"    Old Status: {existing.status}")
                print(f"    New Status: {rally.status}")
                print()
                active_rallies[rally.player_name] = rally
    
    print(f"Active rallies: {len(active_rallies)}")
    print()
    
    # Third scan - rally completed
    print("-" * 60)
    print("[Scan #3] Detected rallies:")
    scan3_rallies = [
        Rally("[XYZ]PlayerTwo", "Lvl 5 Barbarian Fort", "Marching"),
        Rally("[ABC]NewPlayer", "Lvl 4 Barbarian Fort", "Battling"),
    ]
    
    new_rally_players = {rally.player_name for rally in scan3_rallies}
    removed_players = set(active_rallies.keys()) - new_rally_players
    
    for rally in scan3_rallies:
        if rally.player_name in active_rallies:
            existing = active_rallies[rally.player_name]
            if existing.status != rally.status:
                print(f"  [RALLY STATUS UPDATE]")
                print(f"    Player: {rally.player_name}")
                print(f"    Old Status: {existing.status}")
                print(f"    New Status: {rally.status}")
                print()
                active_rallies[rally.player_name] = rally
    
    for player in removed_players:
        removed_rally = active_rallies.pop(player)
        print(f"  [RALLY COMPLETED/REMOVED]")
        print(f"    Player: {removed_rally.player_name}")
        print(f"    Target: {removed_rally.target}")
        print()
    
    print(f"Active rallies: {len(active_rallies)}")
    print()
    
    # Display statistics
    print("=" * 60)
    print("RALLY STATISTICS")
    print("=" * 60)
    print(f"Active Rallies: {len(active_rallies)}")
    print()
    print("Rallies Initiated by Player:")
    for player, count in sorted(player_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {player}: {count}")
    print("=" * 60)


def demo_ocr_workflow():
    """Demonstrate OCR processing workflow."""
    print("\n\n")
    print("=" * 60)
    print("OCR Processing Workflow Demo")
    print("=" * 60)
    print()
    
    # Simulated OCR output
    sample_ocr_text = """[D08K]DKGoku F2P
Lvl 3 Barbarian Fort
Preparing..."""
    
    print("Simulated OCR text from rally slot:")
    print("-" * 40)
    print(sample_ocr_text)
    print("-" * 40)
    print()
    
    # Parse the text
    lines = [line.strip() for line in sample_ocr_text.split('\n') if line.strip()]
    
    player_name = None
    target = None
    status = None
    
    for line in lines:
        if '[' in line and ']' in line:
            player_name = line
        elif 'Lvl' in line or 'Barbarian' in line:
            target = line
        elif 'Preparing' in line or 'Battling' in line:
            status = line
    
    print("Extracted data:")
    print(f"  Player Name: {player_name}")
    print(f"  Target: {target}")
    print(f"  Status: {status}")
    print()
    
    if player_name:
        rally = Rally(player_name, target or "Unknown", status or "Unknown")
        print(f"Created rally object: {rally}")
    
    print("=" * 60)


if __name__ == "__main__":
    demo_rally_detection()
    demo_ocr_workflow()
    
    print("\n\nThis demo shows the expected behavior of the RoK Rally Bot.")
    print("To run the actual bot with device connection and OCR:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Start your LDP9 emulator")
    print("  3. Run: python main.py")
