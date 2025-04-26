#!/usr/bin/env python3
"""
Comprehensive test script for SmartHex package.
"""
from smarthex import SmartHex, SmartHexID
from smarthex.main import SmartHexError, InvalidLengthError

def test_generation():
    """Test ID generation."""
    print("\nTesting ID Generation:")
    sh = SmartHex()
    for i in range(3):
        hex_id = sh.generate()
        print(f"{i+1}. Generated: {hex_id}")
        print(f"   Length: {len(hex_id)}")
        print(f"   Valid: {sh.validate(hex_id)}")
        print(f"   Base: {hex_id.base}")
        print(f"   Checksum: {hex_id.checksum}")

def test_validation():
    """Test ID validation."""
    print("\nTesting ID Validation:")
    sh = SmartHex()
    
    # Test valid ID
    valid_id = "FBA6C40FCF5FD611"
    print(f"1. Valid ID: {valid_id}")
    print(f"   Result: {sh.validate(valid_id)}")
    
    # Test invalid length
    invalid_length = "1234"
    print(f"2. Invalid length: {invalid_length}")
    print(f"   Result: {sh.validate(invalid_length)}")
    
    # Test invalid characters
    invalid_chars = "FBA6C40FCF5FD61G"
    print(f"3. Invalid chars: {invalid_chars}")
    print(f"   Result: {sh.validate(invalid_chars)}")

def test_smarthexid():
    """Test SmartHexID class."""
    print("\nTesting SmartHexID Class:")
    
    # Test valid ID
    try:
        valid_id = SmartHexID("FBA6C40FCF5FD611")
        print(f"1. Valid ID: {valid_id}")
        print(f"   Base: {valid_id.base}")
        print(f"   Checksum: {valid_id.checksum}")
    except SmartHexError:
        print("1. Valid ID: Failed")
    
    # Test invalid length
    try:
        SmartHexID("1234")
        print("2. Invalid length: Failed")
    except InvalidLengthError:
        print("2. Invalid length: Passed")
    
    # Test invalid characters
    try:
        SmartHexID("FBA6C40FCF5FD61G")
        print("3. Invalid chars: Failed")
    except ValueError:
        print("3. Invalid chars: Passed")

def main():
    """Run all tests."""
    print("Starting SmartHex Tests...")
    test_generation()
    test_validation()
    test_smarthexid()
    print("\nAll tests completed.")

if __name__ == "__main__":
    main() 