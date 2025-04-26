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

"""
SmartHex16 - A 16-character hexadecimal identifier system with checksum.

This module provides functionality for generating and validating hexadecimal identifiers
with built-in error detection through checksums.
"""
from __future__ import annotations

import secrets
from typing import Final

IDENTIFIER_LENGTH: Final[int] = 16
BASE_LENGTH: Final[int] = 14
CHECKSUM_LENGTH: Final[int] = 2

class SmartHexError(Exception):
    """Base exception for SmartHex-related errors."""
    pass

class InvalidLengthError(SmartHexError):
    """Raised when identifier length is invalid."""
    pass

class SmartHexID(str):
    """Represents a validated 16-character hex identifier with checksum."""
    def __new__(cls, value: str) -> SmartHexID:
        if len(value) != IDENTIFIER_LENGTH:
            raise InvalidLengthError(
                f"SmartHexID must be {IDENTIFIER_LENGTH} characters long"
            )
        if not all(c in '0123456789ABCDEF' for c in value.upper()):
            raise ValueError("SmartHexID must contain only hexadecimal characters")
        return super().__new__(cls, value.upper())

    @property
    def base(self) -> str:
        """Return the base identifier without checksum."""
        return self[:BASE_LENGTH]

    @property
    def checksum(self) -> str:
        """Return the checksum portion."""
        return self[BASE_LENGTH:]

class SmartHex:
    """Generator and validator for SmartHex identifiers."""
    
    def generate(self) -> SmartHexID:
        """Generate a new SmartHex identifier with checksum."""
        raw_bytes = secrets.token_bytes(7)  # 7 bytes = 14 hex chars
        base_hex = raw_bytes.hex().upper()
        return SmartHexID(base_hex + self._compute_checksum(base_hex))

    def validate(self, id_hex: str) -> bool:
        """Verify if the given hex string is a valid SmartHex identifier."""
        try:
            id_hex = id_hex.upper()
            if len(id_hex) != IDENTIFIER_LENGTH:
                return False
            base, check = id_hex[:BASE_LENGTH], id_hex[BASE_LENGTH:]
            return self._compute_checksum(base) == check
        except (ValueError, AttributeError):
            return False

    def _compute_checksum(self, base_hex: str) -> str:
        """Compute a 2-character hex checksum using polynomial weighting."""
        try:
            digits = [int(c, 16) for c in base_hex]
            checksum = sum(d * (i + 1) for i, d in enumerate(digits))
            return f"{(checksum & 0xFF):02X}"
        except (ValueError, TypeError) as e:
            raise SmartHexError("Invalid base identifier") from e 