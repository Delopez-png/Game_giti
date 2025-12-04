from colorama import Fore, Style, init

# Inisialisasi colorama untuk Windows
init(autoreset=True)

def format_text(text, color=Fore.WHITE, style=Style.NORMAL):
    """Memformat teks dengan warna dan gaya"""
    return f"{color}{style}{text}{Style.RESET_ALL}"

def format_status(player):
    """Memformat status player untuk ditampilkan"""
    health_color = Fore.GREEN if player.health > 50 else Fore.YELLOW if player.health > 20 else Fore.RED
    energy_color = Fore.CYAN if player.energy > 30 else Fore.YELLOW
    
    status = [
        format_text(f"\n=== STATUS {player.name.upper()} ===", Fore.MAGENTA, Style.BRIGHT),
        f"Health: {health_color}{player.health}/{player.max_health}",
        f"Energy: {energy_color}{player.energy}/{player.max_energy}",
        f"Knowledge: {Fore.BLUE}{player.knowledge}",
        f"Location: {Fore.YELLOW}{player.current_location.replace('_', ' ').title()}",
        f"Quests Completed: {Fore.GREEN}{len(player.completed_quests)}"
    ]
    
    return "\n".join(status)

def format_inventory(player):
    """Memformat inventory player untuk ditampilkan"""
    if not player.inventory:
        return format_text("\nInventory kosong.", Fore.YELLOW)
    
    items = [format_text(f"\n=== INVENTORY ===", Fore.CYAN, Style.BRIGHT)]
    
    for i, item in enumerate(player.inventory, 1):
        item_type_color = {
            'weapon': Fore.RED,
            'potion': Fore.GREEN,
            'key': Fore.YELLOW,
            'tool': Fore.BLUE,
            'data': Fore.MAGENTA
        }.get(item.item_type, Fore.WHITE)
        
        items.append(f"{i}. {item_type_color}{item.name}{Fore.WHITE}: {item.description}")
    
    return "\n".join(items)