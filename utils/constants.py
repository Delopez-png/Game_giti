# Konstanta game
GAME_TITLE = "THE LOST CODE OF ALGORIA"

# Arah yang valid
DIRECTIONS = ['north', 'south', 'east', 'west', 'up', 'down']

# Perintah yang valid
COMMANDS = [
    'go', 'look', 'take', 'use', 'inventory', 'status', 
    'talk', 'attack', 'solve', 'save', 'load', 'quit', 'help'
]

# Item efek khusus
def heal_effect(player):
    if player.health < player.max_health:
        player.heal(30)
        return f"Anda menggunakan Health Potion! Health +30 (Sekarang: {player.health}/{player.max_health})"
    return "Health Anda sudah penuh!"

def energy_effect(player):
    if player.energy < player.max_energy:
        player.restore_energy(40)
        return f"Anda menggunakan Energy Drink! Energy +40 (Sekarang: {player.energy}/{player.max_energy})"
    return "Energy Anda sudah penuh!"