class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.energy = 50
        self.max_energy = 100
        self.inventory = []
        self.current_location = "digital_forest"
        self.unlocked_locations = ["digital_forest"]
        self.knowledge = 0
        self.completed_quests = []
        
    def add_item(self, item):
        """Menambahkan item ke inventory"""
        self.inventory.append(item)
        print(f"\n[+] {item.name} telah ditambahkan ke inventory!")
        
    def remove_item(self, item_name):
        """Menghapus item dari inventory"""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                self.inventory.remove(item)
                return True
        return False
    
    def has_item(self, item_name):
        """Memeriksa apakah player memiliki item"""
        return any(item.name.lower() == item_name.lower() for item in self.inventory)
    
    def take_damage(self, amount):
        """Mengurangi health player"""
        self.health -= amount
        if self.health < 0:
            self.health = 0
            
    def heal(self, amount):
        """Memulihkan health player"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
            
    def use_energy(self, amount):
        """Menggunakan energi player"""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
    
    def restore_energy(self, amount):
        """Memulihkan energi player"""
        self.energy += amount
        if self.energy > self.max_energy:
            self.energy = self.max_energy
            
    def add_knowledge(self, amount):
        """Menambah pengetahuan player"""
        self.knowledge += amount
        
    def complete_quest(self, quest_name):
        """Menandai quest sebagai selesai"""
        if quest_name not in self.completed_quests:
            self.completed_quests.append(quest_name)
            
    def get_status(self):
        """Mengembalikan status player dalam bentuk string"""
        return (f"=== STATUS {self.name.upper()} ===\n"
                f"Health: {self.health}/{self.max_health}\n"
                f"Energy: {self.energy}/{self.max_energy}\n"
                f"Knowledge: {self.knowledge}\n"
                f"Location: {self.current_location.replace('_', ' ').title()}\n"
                f"Quests Completed: {len(self.completed_quests)}")