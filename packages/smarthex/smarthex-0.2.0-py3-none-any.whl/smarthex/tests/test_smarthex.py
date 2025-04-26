import unittest
from smarthex import SmartHex, SmartHexID

class TestSmartHex(unittest.TestCase):
    def setUp(self):
        self.smarthex = SmartHex()

    def test_generate_length(self):
        """Test that generated IDs are 16 characters long"""
        id_hex = self.smarthex.generate()
        self.assertEqual(len(id_hex), 16)

    def test_generate_format(self):
        """Test that generated IDs are valid hex strings"""
        id_hex = self.smarthex.generate()
        self.assertTrue(all(c in '0123456789ABCDEF' for c in id_hex))

    def test_validate_generated(self):
        """Test that generated IDs pass validation"""
        id_hex = self.smarthex.generate()
        self.assertTrue(self.smarthex.validate(id_hex))

    def test_validate_invalid_length(self):
        """Test that IDs of wrong length fail validation"""
        self.assertFalse(self.smarthex.validate('1234'))
        self.assertFalse(self.smarthex.validate('1' * 15))
        self.assertFalse(self.smarthex.validate('1' * 17))

    def test_validate_invalid_checksum(self):
        """Test that IDs with wrong checksum fail validation"""
        id_hex = str(self.smarthex.generate())
        corrupted = id_hex[:-2] + '00'  # Replace checksum with '00'
        self.assertFalse(self.smarthex.validate(corrupted))

    def test_smarthexid_type(self):
        """Test that generate returns a SmartHexID instance"""
        id_hex = self.smarthex.generate()
        self.assertIsInstance(id_hex, SmartHexID)

if __name__ == '__main__':
    unittest.main() 