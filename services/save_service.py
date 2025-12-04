import json
import os
from datetime import datetime

class SaveService:
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
    
    def save_game(self, player, locations=None):
        """Menyimpan game ke file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_file = os.path.join(self.save_dir, f"save_{player.name}_{timestamp}.json")
        
        save_data = {
            "player": {
                "name": player.name,
                "health": player.health,
                "max_health": player.max_health,
                "energy": player.energy,
                "max_energy": player.max_energy,
                "inventory": [
                    {
                        "name": item.name,
                        "description": item.description,
                        "item_type": item.item_type,
                        "value": item.value
                    }
                    for item in player.inventory
                ],
                "current_location": player.current_location,
                "unlocked_locations": player.unlocked_locations,
                "knowledge": player.knowledge,
                "completed_quests": player.completed_quests
            },
            "timestamp": timestamp,
            "version": "1.0"
        }
        
        try:
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            return f"Game berhasil disimpan: {save_file}"
        except Exception as e:
            return f"Gagal menyimpan game: {str(e)}"
    
    def load_game(self, save_file):
        """Memuat game dari file"""
        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            return save_data
        except Exception as e:
            return f"Gagal memuat game: {str(e)}"
    
    def list_saves(self):
        """Mendapatkan daftar save file yang tersedia"""
        saves = []
        if os.path.exists(self.save_dir):
            for file in os.listdir(self.save_dir):
                if file.endswith('.json'):
                    saves.append(os.path.join(self.save_dir, file))
        return saves