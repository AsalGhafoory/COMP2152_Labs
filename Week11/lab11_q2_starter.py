class PasswordChecker:

    def __init__(self):
        self.common_passwords = [
            "admin", "password", "123456",
            "root", "guest", "letmein", "welcome"
        ]
        self.history = []

    def check_common(self, password):
        return password.lower() in self.common_passwords

    def check_strength(self, password):
        has_length = len(password) >= 8
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*" for c in password)

        return {
            "length": has_length,
            "digit": has_digit,
            "special": has_special
        }

    def evaluate(self, password):
        if self.check_common(password):
            result = "WEAK (common password)"
        else:
            strength = self.check_strength(password)
            score = sum(strength.values())

            if score <= 1:
                result = "WEAK"
            elif score == 2:
                result = "MEDIUM"
            else:
                result = "STRONG"

        self.history.append((password, result))
        return result