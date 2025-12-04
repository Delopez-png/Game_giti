import os
import random
from colorama import Fore, Style
from models.player import Player
from models.location import Location
from models.item import Item
from utils import formatters, validators, constants
from templates import load_template  # Import tambahan

class GameService:
    def __init__(self):
        self.player = None
        self.locations = {}
        self.is_running = False
        self.game_state = "menu"
        self.setup_game()
    
    def setup_game(self):
        """Menyiapkan game dengan lokasi, item, dan musuh"""
        self.create_items()
        self.create_locations()
        self.create_enemies()
        self.create_puzzles()
    
    def create_items(self):
        """Membuat item-item dalam game"""
        self.items = {
            'debug_tool': Item(
                name="Debug Tool", 
                description="Alat untuk debugging bug di Algoria", 
                item_type="tool",
                value=15
            ),
            'health_potion': Item(
                name="Health Potion", 
                description="Memulihkan 30 health", 
                item_type="potion",
                effect=constants.heal_effect
            ),
            'energy_drink': Item(
                name="Energy Drink", 
                description="Memulihkan 40 energy", 
                item_type="potion",
                effect=constants.energy_effect
            ),
            'firewall_key': Item(
                name="Firewall Key", 
                description="Kunci untuk membuka Firewall Castle", 
                item_type="key",
                value=1
            ),
            'encrypted_data': Item(
                name="Encrypted Data", 
                description="Data terenkripsi dari Server Core", 
                item_type="data",
                value=50
            ),
            'logic_sword': Item(
                name="Logic Sword", 
                description="Senjata untuk melawan Bug Monster", 
                item_type="weapon",
                value=25
            )
        }
    
    def create_locations(self):
        """Membuat lokasi-lokasi dalam game"""
        # Digital Forest
        digital_forest = Location(
            location_id="digital_forest",
            name="Digital Forest",
            description=(
                "Anda berada di Hutan Digital. Pohon-pohon data tumbuh di sekeliling.\n"
                "Suara binary berdesir di angin. Ada jalan ke utara menuju Firewall Castle."
            ),
            items=[self.items['debug_tool'], self.items['health_potion']]
        )
        digital_forest.add_connection("north", "firewall_castle")
        
        # Firewall Castle
        firewall_castle = Location(
            location_id="firewall_castle",
            name="Firewall Castle",
            description=(
                "Sebuah kastil firewall yang megah berdiri di depan Anda.\n"
                "Pintu gerbang terkunci dengan kunci enkripsi. Anda membutuhkan Firewall Key."
            ),
            is_locked=True,
            required_item="firewall_key"
        )
        firewall_castle.add_connection("south", "digital_forest")
        firewall_castle.add_connection("east", "server_core")
        
        # Server Core
        server_core = Location(
            location_id="server_core",
            name="Server Core",
            description=(
                "Anda berada di inti server Algoria. Kode-kode berkedip di dinding.\n"
                "Di tengah ruangan, terdapat terminal dengan data terenkripsi."
            ),
            items=[self.items['encrypted_data']]
        )
        server_core.add_connection("west", "firewall_castle")
        
        # Simpan semua lokasi
        self.locations = {
            "digital_forest": digital_forest,
            "firewall_castle": firewall_castle,
            "server_core": server_core
        }
    
    def create_enemies(self):
        """Membuat musuh-musuh dalam game"""
        self.enemies = {
            "bug_monster": {
                "name": "Bug Monster",
                "health": 60,
                "attack": 15,
                "defense": 5,
                "description": "Makhluk mengerikan dari bug kode yang tidak teratasi.",
                "location": "digital_forest",
                "reward": {"knowledge": 20, "item": self.items['logic_sword']}
            },
            "firewall_guardian": {
                "name": "Firewall Guardian",
                "health": 80,
                "attack": 20,
                "defense": 10,
                "description": "Penjaga firewall yang mengamankan kastil.",
                "location": "firewall_castle",
                "reward": {"knowledge": 30, "item": self.items['firewall_key']}
            }
        }
        
        # Tambahkan musuh ke lokasi
        for enemy_id, enemy_data in self.enemies.items():
            location = self.locations.get(enemy_data["location"])
            if location:
                location.enemies.append(enemy_data)
    
    def create_puzzles(self):
        """Membuat puzzle-puzzle dalam game"""
        self.puzzles = {
            "binary_puzzle": {
                "puzzle_id": "binary_puzzle",
                "question": "Dalam sistem binary, berapakah hasil dari 1010 + 0110? (Jawab dalam decimal)",
                "answer": "16",
                "hint": "Ubah ke decimal dulu: 1010 = 10, 0110 = 6",
                "location": "digital_forest",
                "reward": {"knowledge": 15, "item": self.items['energy_drink']}
            },
            "encryption_puzzle": {
                "puzzle_id": "encryption_puzzle",
                "question": "Dalam Caesar Cipher dengan shift 3, 'khoor' artinya apa?",
                "answer": "hello",
                "hint": "Setiap huruf digeser 3 ke kiri",
                "location": "server_core",
                "reward": {"knowledge": 25}
            }
        }
        
        # Tambahkan puzzle ke lokasi
        for puzzle_id, puzzle_data in self.puzzles.items():
            location = self.locations.get(puzzle_data["location"])
            if location:
                location.puzzles.append(puzzle_data)
    
    def start_new_game(self):
        """Memulai game baru"""
        print(formatters.format_text("\n=== PENCIPTAAN KARAKTER ===", Fore.CYAN, Style.BRIGHT))
        player_name = validators.validate_name("Masukkan nama karakter Anda: ")
        
        self.player = Player(player_name)
        self.is_running = True
        self.game_state = "playing"
        
        print(formatters.format_text(f"\nSelamat datang, {player_name}!", Fore.GREEN, Style.BRIGHT))
        print(formatters.format_text("Anda adalah seorang Programmer yang terjebak di dunia digital Algoria.", Fore.WHITE))
        print(formatters.format_text("Tujuan Anda: menemukan The Lost Code untuk keluar dari dunia ini.\n", Fore.WHITE))
        
        self.show_location()
    
    def show_location(self):
        """Menampilkan lokasi saat ini dengan template"""
        location = self.locations.get(self.player.current_location)
        
        if not location:
            print("Lokasi tidak ditemukan!")
            return
        
        # Load template berdasarkan location
        template_file = ""
        if location.location_id == "digital_forest":
            template_file = "locations/digital_forest.txt"
        elif location.location_id == "firewall_castle":
            template_file = "locations/firewall_castle.txt"
        elif location.location_id == "server_core":
            template_file = "locations/server_core.txt"
        
        # Tampilkan template jika ada, atau tampilkan deskripsi default
        try:
            if template_file:
                template_content = load_template(template_file)
                print(template_content)
            else:
                print(formatters.format_text(f"\n=== {location.name.upper()} ===", Fore.YELLOW, Style.BRIGHT))
                print(location.description)
        except Exception as e:
            # Fallback ke deskripsi default jika template tidak ditemukan
            print(formatters.format_text(f"\n=== {location.name.upper()} ===", Fore.YELLOW, Style.BRIGHT))
            print(location.description)
        
        # Tampilkan item yang tersedia
        if location.items:
            print(formatters.format_text("\nItem yang terlihat:", Fore.GREEN))
            for item in location.items:
                print(f"  - {item.name}: {item.description}")
        
        # Tampilkan musuh yang ada
        if location.enemies:
            print(formatters.format_text("\nMusuh di area ini:", Fore.RED))
            for enemy in location.enemies:
                print(f"  - {enemy['name']}: {enemy['description']}")
        
        # Tampilkan puzzle yang ada
        if location.puzzles:
            print(formatters.format_text("\nPuzzle yang tersedia:", Fore.BLUE))
            for puzzle in location.puzzles:
                print(f"  - Puzzle: {puzzle['question'][:50]}...")
        
        # Tampilkan arah yang mungkin
        if location.connections:
            print(formatters.format_text("\nJalan yang tersedia:", Fore.CYAN))
            for direction, loc_id in location.connections.items():
                loc_name = self.locations[loc_id].name if loc_id in self.locations else loc_id
                # Tampilkan status terkunci
                target_loc = self.locations.get(loc_id)
                lock_status = " [TERKUNCI]" if target_loc and target_loc.is_locked else ""
                print(f"  - {direction.upper()}: menuju {loc_name}{lock_status}")
    
    def process_command(self, command):
        """Memproses perintah dari pemain"""
        cmd_parts = command.lower().split()
        
        if not cmd_parts:
            return False
        
        action = cmd_parts[0]
        
        # Handle berbagai perintah
        if action == 'go':
            self.handle_go(cmd_parts[1] if len(cmd_parts) > 1 else None)
        elif action == 'look':
            self.show_location()
        elif action == 'take':
            self.handle_take(cmd_parts[1:] if len(cmd_parts) > 1 else None)
        elif action == 'use':
            self.handle_use(cmd_parts[1:] if len(cmd_parts) > 1 else None)
        elif action == 'inventory':
            self.show_inventory()
        elif action == 'status':
            self.show_status()
        elif action == 'attack':
            self.handle_attack(cmd_parts[1] if len(cmd_parts) > 1 else None)
        elif action == 'solve':
            self.handle_solve()
        elif action == 'save':
            self.handle_save()
        elif action == 'load':
            self.handle_load()
        elif action == 'help':
            self.show_help()
        elif action == 'quit':
            self.handle_quit()
        else:
            print("Perintah tidak dikenali. Ketik 'help' untuk melihat daftar perintah.")
    
    def handle_go(self, direction):
        """Menangani perintah go"""
        if not direction:
            print("Go ke mana? Contoh: go north, go south")
            return
        
        current_location = self.locations.get(self.player.current_location)
        
        if not current_location:
            print("Lokasi saat ini tidak valid!")
            return
        
        if direction in current_location.connections:
            target_location_id = current_location.connections[direction]
            target_location = self.locations.get(target_location_id)
            
            if not target_location:
                print(f"Lokasi {target_location_id} tidak ditemukan!")
                return
            
            # Cek apakah lokasi terkunci
            if target_location.is_locked:
                if target_location.required_item:
                    if self.player.has_item(target_location.required_item):
                        print(f"\n{Fore.GREEN}Anda menggunakan {target_location.required_item} untuk membuka {target_location.name}!{Fore.RESET}")
                        target_location.is_locked = False
                    else:
                        print(f"\n{Fore.RED}{target_location.name} terkunci! Anda membutuhkan {target_location.required_item}.{Fore.RESET}")
                        return
                else:
                    print(f"\n{Fore.RED}{target_location.name} terkunci!{Fore.RESET}")
                    return
            
            # Pindah ke lokasi baru
            self.player.current_location = target_location_id
            if target_location_id not in self.player.unlocked_locations:
                self.player.unlocked_locations.append(target_location_id)
            
            print(f"\n{Fore.CYAN}Anda pergi ke {direction}.{Fore.RESET}")
            print(f"{Fore.CYAN}Anda sekarang di {target_location.name}.{Fore.RESET}")
            self.show_location()
        else:
            print(f"{Fore.RED}Tidak bisa pergi ke {direction} dari sini.{Fore.RESET}")
    
    def handle_take(self, item_names):
        """Menangani perintah take"""
        if not item_names:
            print("Ambil apa? Contoh: take sword, take potion")
            return
        
        item_name = " ".join(item_names)
        current_location = self.locations.get(self.player.current_location)
        
        if not current_location:
            print("Lokasi saat ini tidak valid!")
            return
        
        # Cari item di lokasi
        taken_item = current_location.remove_item(item_name)
        
        if taken_item:
            self.player.add_item(taken_item)
        else:
            print(f"{Fore.RED}Tidak ada {item_name} di sini.{Fore.RESET}")
    
    def handle_use(self, item_names):
        """Menangani perintah use"""
        if not item_names:
            print("Gunakan apa? Contoh: use potion, use key")
            return
        
        item_name = " ".join(item_names)
        
        # Cari item di inventory
        for item in self.player.inventory:
            if item.name.lower() == item_name.lower():
                result = item.use(self.player)
                print(f"\n{Fore.GREEN}{result}{Fore.RESET}")
                
                # Jika item adalah consumable, hapus dari inventory setelah digunakan
                if item.item_type == "potion":
                    self.player.remove_item(item_name)
                return
        
        print(f"{Fore.RED}Anda tidak memiliki {item_name}.{Fore.RESET}")
    
    def handle_attack(self, enemy_name):
        """Menangani perintah attack"""
        if not enemy_name:
            print("Serang siapa? Contoh: attack monster")
            return
        
        current_location = self.locations.get(self.player.current_location)
        
        if not current_location:
            print("Lokasi saat ini tidak valid!")
            return
        
        # Cari musuh di lokasi
        enemy = None
        for e in current_location.enemies:
            if e['name'].lower() == enemy_name.lower():
                enemy = e
                break
        
        if not enemy:
            print(f"{Fore.RED}Tidak ada {enemy_name} di sini.{Fore.RESET}")
            return
        
        print(f"\n{Fore.YELLOW}Anda menyerang {enemy['name']}!{Fore.RESET}")
        
        # Simple combat logic
        damage = random.randint(10, 25)  # Player damage
        enemy_damage = random.randint(5, enemy['attack'])
        
        enemy['health'] -= damage
        self.player.take_damage(enemy_damage)
        
        print(f"{Fore.GREEN}Anda memberikan {damage} damage ke {enemy['name']}!{Fore.RESET}")
        print(f"{Fore.RED}{enemy['name']} memberikan {enemy_damage} damage ke Anda!{Fore.RESET}")
        
        if enemy['health'] <= 0:
            print(f"\n{Fore.GREEN}Anda mengalahkan {enemy['name']}!{Fore.RESET}")
            
            # Berikan reward
            if 'reward' in enemy:
                reward = enemy['reward']
                if 'knowledge' in reward:
                    self.player.add_knowledge(reward['knowledge'])
                    print(f"{Fore.BLUE}Anda mendapatkan {reward['knowledge']} knowledge!{Fore.RESET}")
                
                if 'item' in reward:
                    self.player.add_item(reward['item'])
            
            # Hapus musuh dari lokasi
            current_location.enemies.remove(enemy)
            
            # Cek apakah semua musuh sudah dikalahkan
            if not current_location.enemies:
                print(f"{Fore.CYAN}Area ini sekarang aman!{Fore.RESET}")
        
        # Cek apakah player mati
        if self.player.health <= 0:
            print(f"\n{Fore.RED}Anda kalah dalam pertarungan!{Fore.RESET}")
            self.game_over()
    
    def handle_solve(self):
        """Menangani perintah solve puzzle"""
        current_location = self.locations.get(self.player.current_location)
        
        if not current_location:
            print("Lokasi saat ini tidak valid!")
            return
        
        if not current_location.puzzles:
            print("Tidak ada puzzle untuk diselesaikan di sini.")
            return
        
        # Tampilkan puzzle pertama di lokasi
        puzzle = current_location.puzzles[0]
        print(f"\n{Fore.BLUE}=== PUZZLE ==={Fore.RESET}")
        print(f"{Fore.CYAN}{puzzle['question']}{Fore.RESET}")
        
        if 'hint' in puzzle:
            hint_choice = input(f"\n{Fore.YELLOW}Ingin petunjuk? (ya/tidak): {Fore.RESET}").lower()
            if hint_choice == 'ya':
                print(f"{Fore.YELLOW}Petunjuk: {puzzle['hint']}{Fore.RESET}")
        
        answer = input(f"\n{Fore.GREEN}Jawaban Anda: {Fore.RESET}").strip().lower()
        
        if answer == puzzle['answer'].lower():
            print(f"\n{Fore.GREEN}Benar! Puzzle terpecahkan!{Fore.RESET}")
            
            # Berikan reward
            if 'reward' in puzzle:
                reward = puzzle['reward']
                if 'knowledge' in reward:
                    self.player.add_knowledge(reward['knowledge'])
                    print(f"{Fore.BLUE}Anda mendapatkan {reward['knowledge']} knowledge!{Fore.RESET}")
                
                if 'item' in reward:
                    self.player.add_item(reward['item'])
            
            # Hapus puzzle dari lokasi
            current_location.puzzles.remove(puzzle)
            
            # Cek apakah semua puzzle sudah diselesaikan
            if not current_location.puzzles and not current_location.enemies:
                print(f"{Fore.CYAN}Anda telah menyelesaikan semua tantangan di area ini!{Fore.RESET}")
        else:
            print(f"\n{Fore.RED}Salah! Coba lagi nanti.{Fore.RESET}")
            self.player.use_energy(10)
    
    def show_inventory(self):
        """Menampilkan inventory player"""
        print(formatters.format_inventory(self.player))
    
    def show_status(self):
        """Menampilkan status player"""
        print(formatters.format_status(self.player))
    
    def handle_save(self):
        """Menangani penyimpanan game"""
        print("Fitur save akan diimplementasikan di versi mendatang.")
    
    def handle_load(self):
        """Menangani pemuatan game"""
        print("Fitur load akan diimplementasikan di versi mendatang.")
    
    def show_help(self):
        """Menampilkan bantuan"""
        help_text = f"""
{Fore.CYAN}=== DAFTAR PERINTAH ==={Fore.RESET}
{Fore.YELLOW}go [arah]{Fore.RESET}          - Bergerak ke arah tertentu (north, south, east, west)
{Fore.YELLOW}look{Fore.RESET}              - Melihat sekeliling
{Fore.YELLOW}take [item]{Fore.RESET}        - Mengambil item
{Fore.YELLOW}use [item]{Fore.RESET}         - Menggunakan item
{Fore.YELLOW}inventory{Fore.RESET}          - Menampilkan inventory
{Fore.YELLOW}status{Fore.RESET}             - Menampilkan status karakter
{Fore.YELLOW}attack [musuh]{Fore.RESET}     - Menyerang musuh
{Fore.YELLOW}solve{Fore.RESET}              - Memecahkan puzzle
{Fore.YELLOW}save{Fore.RESET}               - Menyimpan game
{Fore.YELLOW}load{Fore.RESET}               - Memuat game
{Fore.YELLOW}help{Fore.RESET}               - Menampilkan bantuan ini
{Fore.YELLOW}quit{Fore.RESET}               - Keluar dari game

{Fore.GREEN}Tujuan Game:{Fore.RESET}
Temukan The Lost Code di Server Core dan keluar dari dunia Algoria!

{Fore.MAGENTA}Hint:{Fore.RESET}
- Kumpulkan knowledge dengan mengalahkan musuh dan memecahkan puzzle
- Gunakan item yang tepat di lokasi yang tepat
- Periksa status dan inventory secara berkala
"""
        print(help_text)
    
    def handle_quit(self):
        """Menangani perintah quit"""
        confirm = input(f"\n{Fore.YELLOW}Apakah Anda yakin ingin keluar? (ya/tidak): {Fore.RESET}").lower()
        if confirm == 'ya':
            print(f"{Fore.CYAN}Terima kasih telah bermain!{Fore.RESET}")
            self.is_running = False
    
    def game_over(self):
        """Menangani game over"""
        try:
            bad_ending = load_template("endings/bad_ending.txt")
            print(f"\n{Fore.RED}{bad_ending}{Fore.RESET}")
        except:
            print(f"\n{Fore.RED}=== GAME OVER ==={Fore.RESET}")
            print(f"{Fore.RED}Karakter Anda telah kalah.{Fore.RESET}")
        
        play_again = input(f"\n{Fore.YELLOW}Main lagi? (ya/tidak): {Fore.RESET}").lower()
        if play_again == 'ya':
            self.start_new_game()
        else:
            self.is_running = False
    
    def check_win_condition(self):
        """Memeriksa apakah player menang"""
        # Ubah kondisi kemenangan menjadi lebih realistis (dari 100 ke 70 knowledge)
        if (self.player.has_item("Encrypted Data") and 
            self.player.knowledge >= 70 and
            self.player.current_location == "server_core"):
            
            try:
                good_ending = load_template("endings/good_ending.txt")
                print(f"\n{Fore.GREEN}{good_ending}{Fore.RESET}")
            except:
                print(f"\n{Fore.GREEN}=== SELAMAT! ==={Fore.RESET}")
                print(f"{Fore.GREEN}Anda berhasil menemukan The Lost Code of Algoria!{Fore.RESET}")
                print(f"{Fore.GREEN}Dengan pengetahuan yang cukup, Anda berhasil mendekripsi data.{Fore.RESET}")
                print(f"{Fore.GREEN}Anda menemukan kode yang membuka portal kembali ke dunia nyata!{Fore.RESET}")
                print(f"\n{Fore.CYAN}Terima kasih telah bermain, {self.player.name}!{Fore.RESET}")
            
            # Tampilkan statistik akhir
            print(f"\n{Fore.YELLOW}=== STATISTIK AKHIR ===")
            print(f"Total Knowledge: {self.player.knowledge}")
            print(f"Health tersisa: {self.player.health}/{self.player.max_health}")
            print(f"Energy tersisa: {self.player.energy}/{self.player.max_energy}")
            print(f"Item yang dikumpulkan: {len(self.player.inventory)}")
            print(f"Lokasi yang dijelajahi: {len(self.player.unlocked_locations)}{Fore.RESET}")
            
            return True
        
        return False