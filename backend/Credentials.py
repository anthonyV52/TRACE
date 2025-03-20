from typing import List

class Credentials(DBEnumerator):
    min_length = 6
    
    def __init__(self):
        self.password_store: List[str] = []
        self.username_store: List[str] = []
    
    def store_password(self, password: str):
        if password and len(password) >= self.min_length:
            self.password_store.append(password)
    
    def store_username(self, username: str):
        if username and len(username) >= self.min_length:
            self.username_store.append(username)
    
    def calc_pass_strength(self, password: str) -> int:
        if not password or len(password) < self.min_length:
            return 1
        
        strength = 1
        if any(char.isdigit() for char in password):
            strength += 1
        if any(char.islower() for char in password) and any(char.isupper() for char in password):
            strength += 1
        if any(char in "!@#$%^&*()-_=+[]{}|;:'",.<>?/" for char in password):
            strength += 1
        if len(password) >= 12:
            strength += 1
        
        return min(strength, 5)
    
    def calc_user_strength(self, username: str) -> int:
        if not username or len(username) < self.min_length:
            return 1
        
        strength = 1
        if any(char.isdigit() for char in username):
            strength += 1
        if any(char in "-_" for char in username):
            strength += 1
        if len(username) >= 10:
            strength += 1
        if len(username) >= 15:
            strength += 1
        
        return min(strength, 5)
