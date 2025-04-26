#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SmartHex16 - A 16-character hexadecimal identifier system with checksum.
#
# Author: Victor Matos (@spacemany2k38, @vvrmatos)
# Email: contact@byteram.co
# Date: 2025-04-25
# Title: Applied Mathematician
#

import secrets

class SmartHexID(str):
    """Represents a validated 16-character hex identifier with checksum."""
    def __new__(cls, value: str):
        if len(value) != 16:
            raise ValueError("SmartHexID must be 16 characters long")
        return super().__new__(cls, value)

class SmartHex:
    def generate(self) -> SmartHexID:
        """Returns a new SmartHex identifier with checksum."""
        raw_bytes = secrets.token_bytes(7)
        base_hex = raw_bytes.hex().upper()
        return SmartHexID(base_hex + self._compute_checksum(base_hex))

    def validate(self, id_hex: str) -> bool:
        """Verifies if the given hex string is a valid SmartHex identifier."""
        if len(id_hex) != 16:
            return False
        base, check = id_hex[:14], id_hex[14:]
        return self._compute_checksum(base) == check.upper()

    def _compute_checksum(self, base_hex: str) -> str:
        """Computes a 2-character hex checksum using polynomial weighting."""
        digits = [int(c, 16) for c in base_hex]
        checksum = sum(d * (i + 1) for i, d in enumerate(digits))
        return f"{(checksum & 0xFF):02X}" 
