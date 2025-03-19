import string
import bcrypt  # Ensure bcrypt is installed

class TextSecurity:
    """Class to encrypt and decrypt text using an improved Caesar cipher and bcrypt hashing."""

    def __init__(self, shift):
        """Constructor to initialize the shift value"""
        self.shifter = shift
        self.s = self.shifter % 26  # Ensures shift stays within bounds

    def _convert(self, text, shift):
        """Encrypt or decrypt the input text while preserving special characters."""
        result = ""
        for ch in text:
            if ch.isupper():
                result += chr((ord(ch) - 65 + shift) % 26 + 65)  # Uppercase A-Z
            elif ch.islower():
                result += chr((ord(ch) - 97 + shift) % 26 + 97)  # Lowercase a-z
            elif ch.isdigit():
                result += chr((ord(ch) - 48 + shift) % 10 + 48)  # Numbers 0-9
            else:
                result += ch  # Keep special characters unchanged
        return result

    def encrypt(self, text):
        """Encrypts the text using the Caesar cipher"""
        return self._convert(text, self.shifter)

    def decrypt(self, text):
        """Decrypts the text using the inverse shift"""
        return self._convert(text, -self.shifter)

    def hash_password(self, password):
        """Hashes a password using bcrypt"""
        salt = bcrypt.gensalt()  # Generate a random salt
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash password
        return hashed.decode('utf-8')  # Return hashed password as string

    def verify_password(self, password, hashed_password):
        """Verifies a password against a stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Example Usage
if __name__ == "__main__":
    cipher = TextSecurity(4)

    # Test encryption
    message = "SecureMessage123!"
    coded = cipher.encrypt(message)
    print('Encrypted Message:', coded)
    print('Decrypted Message:', cipher.decrypt(coded))

    # Test password hashing
    password = "SecurePass123"
    hashed_password = cipher.hash_password(password)
    print("Hashed Password:", hashed_password)
    print("Password Valid:", cipher.verify_password(password, hashed_password))

