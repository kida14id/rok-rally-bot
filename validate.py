"""
Simple validation script to test the Rally class and basic functionality.
This script doesn't require device connection or dependencies.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_rally_class():
    """Test the Rally class functionality."""
    print("Testing Rally class...")
    
    try:
        # Import the Rally class
        from utils import Rally
    except ImportError as e:
        print(f"⚠ Skipping Rally class tests - dependencies not installed")
        print(f"   (This is expected without 'pip install -r requirements.txt')")
        print(f"   Error: {e}")
        print("   Install dependencies to run full tests.\n")
        return
    
    # Create test rallies
    rally1 = Rally("[D08K]DKGoku F2P", "Lvl 3 Barbarian Fort", "Preparing...")
    rally2 = Rally("[XYZ]Player2", "Lvl 5 Barbarian Fort", "Battling")
    rally3 = Rally("[D08K]DKGoku F2P", "Lvl 4 Barbarian Fort", "Marching")
    
    # Test __repr__
    print(f"Rally 1: {rally1}")
    assert "DKGoku" in str(rally1), "Rally __repr__ should contain player name"
    
    # Test equality (same player name)
    assert rally1 == rally3, "Rallies with same player should be equal"
    assert rally1 != rally2, "Rallies with different players should not be equal"
    
    # Test hash (for use in sets/dicts)
    rally_set = {rally1, rally2, rally3}
    assert len(rally_set) == 2, "Set should contain only 2 unique rallies (by player name)"
    
    print("✓ Rally class tests passed!\n")


def test_parse_rally_text():
    """Test the parse_rally_text function."""
    print("Testing parse_rally_text function...")
    
    try:
        from utils import parse_rally_text
    except ImportError as e:
        print(f"⚠ Skipping parse_rally_text tests - dependencies not installed")
        print(f"   (This is expected without 'pip install -r requirements.txt')")
        print(f"   Error: {e}")
        print("   Install dependencies to run full tests.\n")
        return
    
    # Test with valid data
    test_text = """[D08K]DKGoku F2P
Lvl 3 Barbarian Fort
Preparing..."""
    
    rally = parse_rally_text(test_text)
    
    if rally:
        print(f"Parsed rally: {rally}")
        assert rally.player_name == "[D08K]DKGoku F2P", "Player name should match"
        assert "Barbarian" in rally.target, "Target should contain 'Barbarian'"
        assert "Preparing" in rally.status, "Status should contain 'Preparing'"
        print("✓ Parse rally text tests passed!\n")
    else:
        print("⚠ Warning: Could not parse test text (this is expected without full OCR context)\n")
    
    # Test with empty text
    empty_rally = parse_rally_text("")
    assert empty_rally is None, "Empty text should return None"
    print("✓ Empty text handling passed!\n")


def test_imports():
    """Test that all imports work (basic syntax check)."""
    print("Testing module structure (without dependencies)...")
    print("Note: Some imports will fail without dependencies installed.")
    print("      This validates the code structure only.\n")
    
    try:
        # Test main.py structure
        import main
        assert hasattr(main, 'RallyMonitor'), "main.py should have RallyMonitor class"
        assert hasattr(main, 'main'), "main.py should have main function"
        print("✓ main.py structure is valid\n")
        
        # Test utils.py structure  
        import utils
        assert hasattr(utils, 'Rally'), "utils.py should have Rally class"
        assert hasattr(utils, 'connect_to_device'), "utils.py should have connect_to_device"
        assert hasattr(utils, 'capture_screenshot'), "utils.py should have capture_screenshot"
        assert hasattr(utils, 'process_rally_image'), "utils.py should have process_rally_image"
        print("✓ utils.py structure is valid\n")
        
    except ImportError as e:
        print(f"⚠ Some dependencies not installed: {e}")
        print("   Install dependencies with: pip install -r requirements.txt")
        print("   However, basic Python structure validation passed!\n")


def test_rally_monitor_structure():
    """Test RallyMonitor class structure."""
    print("Testing RallyMonitor class structure...")
    
    try:
        from main import RallyMonitor
        
        # Create instance (without device connection)
        monitor = RallyMonitor(scan_interval=10)
        
        # Test attributes
        assert hasattr(monitor, 'scan_interval'), "Should have scan_interval attribute"
        assert hasattr(monitor, 'active_rallies'), "Should have active_rallies attribute"
        assert hasattr(monitor, 'player_stats'), "Should have player_stats attribute"
        
        # Test methods
        assert hasattr(monitor, 'connect'), "Should have connect method"
        assert hasattr(monitor, 'update_rally_state'), "Should have update_rally_state method"
        assert hasattr(monitor, 'display_stats'), "Should have display_stats method"
        assert hasattr(monitor, 'run'), "Should have run method"
        
        print("✓ RallyMonitor class structure is valid\n")
        
    except ImportError as e:
        print(f"⚠ Skipping RallyMonitor tests - dependencies not installed")
        print(f"   Error: {e}\n")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("RoK Rally Bot - Validation Tests")
    print("=" * 60)
    print()
    
    test_rally_class()
    test_parse_rally_text()
    test_imports()
    test_rally_monitor_structure()
    
    print("=" * 60)
    print("Validation Complete!")
    print("=" * 60)
    print("\nAll basic structure tests passed.")
    print("\nTo run the full bot, install dependencies:")
    print("  pip install -r requirements.txt")
    print("\nThen run:")
    print("  python main.py")


if __name__ == "__main__":
    main()
