class Item:
    def __init__(self, name, description, item_type, value=0, effect=None):
        self.name = name
        self.description = description
        self.item_type = item_type  # 'weapon', 'potion', 'key', 'tool', 'data'
        self.value = value
        self.effect = effect  # Fungsi yang dijalankan saat item digunakan
        
    def use(self, player):
        """Menggunakan item pada player"""
        if self.effect:
            return self.effect(player)
        return f"Anda menggunakan {self.name}, tetapi tidak terjadi apa-apa."
    
    def __str__(self):
        return f"{self.name}: {self.description}"