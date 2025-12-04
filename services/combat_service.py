import random
from colorama import Fore

class CombatService:
    @staticmethod
    def calculate_damage(attacker_power, defender_defense, critical_chance=0.1):
        """Menghitung damage dengan kemungkinan critical hit"""
        base_damage = max(1, attacker_power - defender_defense // 2)
        
        # Critical hit chance
        if random.random() < critical_chance:
            base_damage *= 2
            return base_damage, True
        
        return base_damage, False
    
    @staticmethod
    def calculate_dodge(agility):
        """Menghitung kemungkinan menghindar"""
        return random.random() < (agility / 100)
    
    @staticmethod
    def battle(player, enemy):
        """Melakukan pertempuran antara player dan enemy"""
        print(f"\n{Fore.RED}=== PERTEMPURAN vs {enemy['name'].upper()} ==={Fore.RESET}")
        
        player_health = player.health
        enemy_health = enemy['health']
        
        turn = 0
        
        while player_health > 0 and enemy_health > 0:
            turn += 1
            print(f"\n{Fore.CYAN}--- Turn {turn} ---{Fore.RESET}")
            
            # Player turn
            print(f"{Fore.GREEN}Giliran Anda:{Fore.RESET}")
            action = input("Pilih aksi (attack/use item/run): ").lower()
            
            if action == 'attack':
                damage, is_critical = CombatService.calculate_damage(
                    20, enemy['defense'], 0.15
                )
                
                if is_critical:
                    print(f"{Fore.YELLOW}CRITICAL HIT!{Fore.RESET}")
                
                enemy_health -= damage
                print(f"Anda memberikan {damage} damage ke {enemy['name']}!")
                print(f"{enemy['name']} health: {max(0, enemy_health)}/{enemy['health']}")
                
            elif action == 'use item':
                # Implement item use in combat
                print("Menggunakan item...")
                # This would need access to player's inventory
                continue
                
            elif action == 'run':
                if random.random() < 0.5:
                    print("Anda berhasil melarikan diri!")
                    return "escaped"
                else:
                    print("Gagal melarikan diri!")
            
            # Check if enemy is defeated
            if enemy_health <= 0:
                print(f"\n{Fore.GREEN}Anda mengalahkan {enemy['name']}!{Fore.RESET}")
                return "player_win"
            
            # Enemy turn
            print(f"\n{Fore.RED}Giliran {enemy['name']}:{Fore.RESET}")
            
            # Enemy attack
            damage, is_critical = CombatService.calculate_damage(
                enemy['attack'], 5, 0.05
            )
            
            if is_critical:
                print(f"{Fore.RED}CRITICAL HIT dari musuh!{Fore.RESET}")
            
            player_health -= damage
            print(f"{enemy['name']} memberikan {damage} damage ke Anda!")
            print(f"Health Anda: {max(0, player_health)}/{player.max_health}")
            
            # Check if player is defeated
            if player_health <= 0:
                print(f"\n{Fore.RED}Anda dikalahkan oleh {enemy['name']}!{Fore.RESET}")
                return "enemy_win"
        
        return "unknown"