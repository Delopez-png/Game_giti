class Location:
    def __init__(self, location_id, name, description, connections=None, items=None, 
                 enemies=None, puzzles=None, is_locked=False, required_item=None):
        self.location_id = location_id
        self.name = name
        self.description = description
        self.connections = connections or {}
        self.items = items or []
        self.enemies = enemies or []
        self.puzzles = puzzles or []
        self.is_locked = is_locked
        self.required_item = required_item
        
    def add_connection(self, direction, location_id):
        """Menambahkan koneksi ke lokasi lain"""
        self.connections[direction] = location_id
        
    def remove_item(self, item_name):
        """Menghapus item dari lokasi"""
        for i, item in enumerate(self.items):
            if item.name.lower() == item_name.lower():
                return self.items.pop(i)
        return None
    
    def get_enemy(self, enemy_name):
        """Mendapatkan enemy berdasarkan nama"""
        for enemy in self.enemies:
            if enemy.name.lower() == enemy_name.lower():
                return enemy
        return None
    
    def get_puzzle(self, puzzle_id):
        """Mendapatkan puzzle berdasarkan ID"""
        for puzzle in self.puzzles:
            if puzzle.puzzle_id == puzzle_id:
                return puzzle
        return None