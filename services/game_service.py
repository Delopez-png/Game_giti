import os
import random
from colorama import Fore, Style, init
init(autoreset=True)

from models.player import Player
from models.location import Location
from models.item import Item
from templates import load_template
from utils.constants import (
    GAME_TITLE, DIRECTIONS, COMMANDS, 
    heal_effect, energy_effect,
    PUZZLE_QUESTIONS, LOCATION_DESCRIPTIONS,
    ITEM_COLORS, ENEMY_STATS, WIN_REQUIREMENTS
)
from utils import formatters, validators

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
        """Membuat item-item dalam game - FIXED HEALING"""
        # Helper functions untuk item effects
        def health_potion_effect(player):
            """Effect untuk health potion"""
            old_health = player.health
            max_health = getattr(player, 'max_health', 100)
            player.health = min(player.health + 30, max_health)
            heal_amount = player.health - old_health
            return f"Health +{heal_amount}! Sekarang: {player.health}/{max_health}"
        
        def energy_drink_effect(player):
            """Effect untuk energy drink"""
            old_energy = player.energy
            max_energy = getattr(player, 'max_energy', 100)
            player.energy = min(player.energy + 40, max_energy)
            energy_amount = player.energy - old_energy
            return f"Energy +{energy_amount}! Sekarang: {player.energy}/{max_energy}"
        
        def logic_potion_effect(player):
            """Effect untuk logic potion"""
            old_knowledge = player.knowledge
            player.knowledge += 50
            return f"Knowledge +50! Sekarang: {player.knowledge}"
        
        def data_potion_effect(player):
            """Effect untuk data potion"""
            max_energy = getattr(player, 'max_energy', 100)
            player.energy = max_energy
            return f"Energy dipulihkan 100%! Sekarang: {player.energy}/{max_energy}"
        
        def quantum_potion_effect(player):
            """Effect untuk quantum potion"""
            old_health = player.health
            old_energy = player.energy
            max_health = getattr(player, 'max_health', 100)
            max_energy = getattr(player, 'max_energy', 100)
            
            player.health = min(player.health + 50, max_health)
            player.energy = min(player.energy + 50, max_energy)
            
            health_heal = player.health - old_health
            energy_restore = player.energy - old_energy
            
            return f"Health +{health_heal} dan Energy +{energy_restore}! Sekarang: {player.health}/{max_health} HP, {player.energy}/{max_energy} Energy"
        
        # Existing items dengan effects yang benar
        self.items = {
            'debug_tool': Item("Debug Tool", "Alat debugging (+15 attack)", "tool", 15),
            'health_potion': Item("Health Potion", "+30 health", "potion", health_potion_effect),
            'energy_drink': Item("Energy Drink", "+40 energy", "potion", energy_drink_effect),
            'firewall_key': Item("Firewall Key", "Buka Firewall Castle", "key", 1),
            'encrypted_data': Item("Encrypted Data", "Data terenkripsi", "data", 50),
            'logic_sword': Item("Logic Sword", "Senjata vs Bug (+25 attack)", "weapon", 25),
        }
        
        # NEW ITEMS untuk lokasi baru
        new_items = {
            # Item untuk puzzle dan lokasi terkunci
            'logic_key': Item("Logic Key", "Membuka Logic Horizon", "key", 10),
            'defrag_tool': Item("Defrag Tool", "Membersihkan fragment data (+20 attack)", "tool", 20),
            'kernel_access': Item("Kernel Access Card", "Akses ke Logic Kernel", "key", 30),
            'heart_key': Item("Heart Key", "Membuka Heartline Node", "key", 40),
            'royal_syntax': Item("Royal Syntax Token", "Masuk Codemantle", "key", 50),
            'antivirus_sword': Item("Antivirus Sword", "Senjata vs Malvex (+60 attack)", "weapon", 60),
            
            # Item khusus
            'packet_sniffer': Item("Packet Sniffer", "Menangkap packet di Packetflow Deep", "tool", 25),
            'memory_shard': Item("Memory Shard", "Fragment memori dari Memory Gap", "data", 35),
            'binary_seed': Item("Binary Seed", "Bibit dari Binaryheart Woods", "special", 15),
            'storm_cape': Item("Storm Cape", "Melindungi dari hujan data (+10 defense)", "armor", 45),
            'nullwave_orb': Item("Nullwave Orb", "Bola energi gelap Malvex", "artifact", 100),
            
            # Potion baru dengan efek yang benar
            'logic_potion': Item("Logic Potion", "+50 knowledge", "potion", logic_potion_effect),
            'data_potion': Item("Data Potion", "Memulihkan semua energy", "potion", data_potion_effect),
            'quantum_potion': Item("Quantum Potion", "+50 health dan +50 energy", "potion", quantum_potion_effect),
        }
        
        self.items.update(new_items)
    
    def create_locations(self):
        """Membuat lokasi-lokasi dalam game"""
        
        # ========================
        # 1. DEFINISI SEMUA LOKASI
        # ========================
        
        # Digital Forest (Starting Location)
        digital_forest = Location(
            location_id="digital_forest",
            name="Digital Forest",
            description=(
                "Anda berada di Hutan Digital. Pohon-pohon data tumbuh di sekeliling.\n"
                "Suara binary berdesir di angin."
            ),
            items=[self.items['debug_tool'], self.items['health_potion']]
        )
        
        # Segfault Abyss
        segfault_abyss = Location(
            location_id="segfault_abyss",
            name="Segfault Abyss",
            description=(
                "Jurang dalam yang muncul setelah crash besar algoritma. "
                "Dinding jurang berisi stack trace yang berkedip. Suara 'segmentation fault' "
                "bergema dari kedalaman."
            ),
            is_locked=False
        )
        
        # Packetflow Deep
        packetflow_deep = Location(
            location_id="packetflow_deep",
            name="Packetflow Deep",
            description=(
                "Lautan data dengan arus packet yang sangat cepat. "
                "Anda melihat packet TCP/IP berenang seperti ikan. "
                "Cahaya dari router-coral menyinari dasar lautan."
            ),
            is_locked=False
        )
        
        # Logic Horizon Plains
        logic_horizon = Location(
            location_id="logic_horizon",
            name="Logic Horizon Plains",
            description=(
                "Padang luas tempat logika mengalir bebas. "
                "Rumput-rumput boolean (true/false) bergoyang tertiup angin. "
                "Di kejauhan, kawanan algoritma bermigrasi."
            ),
            is_locked=True,
            required_item="logic_key"
        )
        
        # Algolane Merchant Square
        algolane_square = Location(
            location_id="algolane_square",
            name="Algolane Merchant Square",
            description=(
                "Pasar digital tempat avatar dan bot berdagang. "
                "Kios-kios menjual memory chips, quantum bits, dan algoritma langka. "
                "Suara tawar-menawar dalam berbagai bahasa programming."
            ),
            is_locked=False
        )
        
        # Fragment Hive
        fragment_hive = Location(
            location_id="fragment_hive",
            name="Fragment Hive",
            description=(
                "Sarang bug data yang tidak lengkap. Dinding-dinding hexagonal "
                "berisi fragment code yang bergerak-gerak. Suara dengung byte "
                "yang terkorupsi memenuhi udara."
            ),
            is_locked=True,
            required_item="defrag_tool"
        )
        
        # The Logic Kernel Spire
        kernel_spire = Location(
            location_id="kernel_spire",
            name="The Logic Kernel Spire",
            description=(
                "Menara tinggi yang berfungsi sebagai otak utama Algoria. "
                "Processor core berputar di puncak, memancarkan gelombang logika. "
                "Tangga spiral terbuat dari assembly code."
            ),
            is_locked=True,
            required_item="kernel_access"
        )
        
        # The Shattered Memory Gap
        memory_gap = Location(
            location_id="memory_gap",
            name="The Shattered Memory Gap",
            description=(
                "Ruang kosong tempat memori-memori hilang berkumpul. "
                "Fragment memori melayang seperti awan. Terkadang flashback "
                "dari program yang sudah dihapus muncul tiba-tiba."
            ),
            is_locked=False
        )
        
        # Central Heartline Node
        heartline_node = Location(
            location_id="heartline_node",
            name="Central Heartline Node",
            description=(
                "Jantung dunia berupa kristal data raksasa. "
                "Cahaya biner (0/1) berdenyut seperti detak jantung, "
                "mengalirkan energi ke seluruh Algoria."
            ),
            is_locked=True,
            required_item="heart_key"
        )
        
        # Codemantle Dominion
        codemantle = Location(
            location_id="codemantle",
            name="Codemantle Dominion",
            description=(
                "Kerajaan megah dari block-syntax dan rune algoritma. "
                "Pilar data menjulang tinggi, dihiasi dengan comment emas. "
                "Function-call banners berkibar di angin digital."
            ),
            is_locked=True,
            required_item="royal_syntax"
        )
        
        # Malvex's Throne (Nullwave Domain)
        malvex_throne = Location(
            location_id="malvex_throne",
            name="Malvex, Sovereign of the Nullwave",
            description=(
                "Takhta Raja Virus yang mampu menelan kode. "
                "Segala sesuatu di sini tampak terdistorsi. "
                "Malvex sendiri adalah entitas data hitam dengan mata merah menyala."
            ),
            is_locked=True,
            required_item="antivirus_sword"
        )
        
        # Stormbyte Expanse
        stormbyte = Location(
            location_id="stormbyte",
            name="Stormbyte Expanse",
            description=(
                "Wilayah dengan hujan data tak henti. "
                "Setiap tetes hujan adalah bit informasi bersinar. "
                "Petir berupa error messages menyambar sesekali."
            ),
            is_locked=False
        )
        
        # Binaryheart Woods
        binaryheart = Location(
            location_id="binaryheart",
            name="Binaryheart Woods",
            description=(
                "Hutan kuno dengan 'detak angka' seperti jantung digital. "
                "Pohon-pohon berakar dalam binary soil. "
                "Daun-daun berubah warna antara 0 (hijau) dan 1 (biru)."
            ),
            is_locked=False
        )
        
        # Firewall Castle
        firewall_castle = Location(
            location_id="firewall_castle",
            name="Firewall Castle",
            description=(
                "Sebuah kastil firewall yang megah berdiri di depan Anda.\n"
                "Pintu gerbang terkunci dengan kunci enkripsi."
            ),
            is_locked=True,
            required_item="firewall_key"
        )
        
        # Server Core (Final Location)
        server_core = Location(
            location_id="server_core",
            name="Server Core",
            description=(
                "Anda berada di inti server Algoria. Kode-kode berkedip di dinding.\n"
                "Di tengah ruangan, terdapat terminal dengan data terenkripsi."
            ),
            items=[self.items['encrypted_data']]
        )
        
        # ========================
        # 2. KONEKSI ANTAR LOKASI
        # ========================
        
        # Digital Forest connections (Center Hub)
        digital_forest.add_connection("north", "segfault_abyss")
        digital_forest.add_connection("east", "packetflow_deep")
        digital_forest.add_connection("west", "binaryheart")
        digital_forest.add_connection("northeast", "algolane_square")
        
        # Segfault Abyss connections
        segfault_abyss.add_connection("south", "digital_forest")
        segfault_abyss.add_connection("down", "memory_gap")
        segfault_abyss.add_connection("east", "logic_horizon")
        
        # Packetflow Deep connections
        packetflow_deep.add_connection("west", "digital_forest")
        packetflow_deep.add_connection("south", "algolane_square")
        packetflow_deep.add_connection("down", "fragment_hive")
        
        # Logic Horizon connections
        logic_horizon.add_connection("west", "segfault_abyss")
        logic_horizon.add_connection("north", "kernel_spire")
        
        # Algolane Merchant Square connections
        algolane_square.add_connection("north", "packetflow_deep")
        algolane_square.add_connection("west", "digital_forest")
        algolane_square.add_connection("east", "stormbyte")
        
        # Fragment Hive connections
        fragment_hive.add_connection("up", "packetflow_deep")
        fragment_hive.add_connection("north", "heartline_node")
        
        # Kernel Spire connections
        kernel_spire.add_connection("south", "logic_horizon")
        kernel_spire.add_connection("up", "codemantle")
        
        # Memory Gap connections
        memory_gap.add_connection("up", "segfault_abyss")
        memory_gap.add_connection("east", "heartline_node")
        
        # Heartline Node connections
        heartline_node.add_connection("south", "fragment_hive")
        heartline_node.add_connection("west", "memory_gap")
        heartline_node.add_connection("east", "malvex_throne")
        
        # Codemantle connections
        codemantle.add_connection("down", "kernel_spire")
        codemantle.add_connection("north", "server_core")
        
        # Malvex Throne connections
        malvex_throne.add_connection("west", "heartline_node")
        
        # Stormbyte connections
        stormbyte.add_connection("west", "algolane_square")
        stormbyte.add_connection("north", "server_core")
        
        # Binaryheart Woods connections
        binaryheart.add_connection("east", "digital_forest")
        binaryheart.add_connection("north", "firewall_castle")
        
        # Firewall Castle connections
        firewall_castle.add_connection("south", "binaryheart")
        firewall_castle.add_connection("east", "server_core")
        
        # Server Core connections
        server_core.add_connection("west", "firewall_castle")
        server_core.add_connection("south", "stormbyte")
        server_core.add_connection("down", "codemantle")
        
        # ========================
        # 3. SIMPAN SEMUA LOKASI
        # ========================
        
        self.locations = {
            "digital_forest": digital_forest,
            "binaryheart": binaryheart,
            "segfault_abyss": segfault_abyss,
            "packetflow_deep": packetflow_deep,
            "algolane_square": algolane_square,
            "logic_horizon": logic_horizon,
            "fragment_hive": fragment_hive,
            "memory_gap": memory_gap,
            "stormbyte": stormbyte,
            "firewall_castle": firewall_castle,
            "kernel_spire": kernel_spire,
            "heartline_node": heartline_node,
            "codemantle": codemantle,
            "malvex_throne": malvex_throne,
            "server_core": server_core,
        }
        
        self.starting_location = "digital_forest"
    
    def create_enemies(self):
        """Membuat musuh-musuh dalam game"""
        for location in self.locations.values():
            location.enemies = []
        
        enemies_data = {
            "bug_monster": {
                "id": "bug_monster",
                "name": "Bug Monster",
                "health": 60,
                "max_health": 60,
                "attack": 15,
                "defense": 5,
                "description": "Bug kode yang tidak teratasi.",
                "location": "digital_forest",
                "reward": {"knowledge": 20, "item": self.items['logic_sword']}
            },
            "firewall_guardian": {
                "id": "firewall_guardian",
                "name": "Firewall Guardian",
                "health": 80,
                "max_health": 80,
                "attack": 20,
                "defense": 10,
                "description": "Penjaga firewall yang mengamankan kastil.",
                "location": "firewall_castle",
                "reward": {"knowledge": 30, "item": self.items['firewall_key']}
            },
            "segfault_specter": {
                "id": "segfault_specter",
                "name": "Segfault Specter",
                "health": 80,
                "max_health": 80,
                "attack": 25,
                "defense": 10,
                "description": "Hantu dari crash algorithm yang fatal.",
                "location": "segfault_abyss",
                "reward": {"knowledge": 30, "item": self.items['defrag_tool']}
            },
            "packet_shark": {
                "id": "packet_shark",
                "name": "Packet Shark",
                "health": 70,
                "max_health": 70,
                "attack": 20,
                "defense": 15,
                "description": "Predator yang memakan packet data.",
                "location": "packetflow_deep",
                "reward": {"knowledge": 25, "item": self.items['packet_sniffer']}
            },
            "fragment_drone": {
                "id": "fragment_drone",
                "name": "Fragment Drone",
                "health": 90,
                "max_health": 90,
                "attack": 30,
                "defense": 20,
                "description": "Bug drone penjaga Fragment Hive.",
                "location": "fragment_hive",
                "reward": {"knowledge": 40, "item": self.items['logic_key']}
            },
            "memory_phantom": {
                "id": "memory_phantom",
                "name": "Memory Phantom",
                "health": 100,
                "max_health": 100,
                "attack": 35,
                "defense": 25,
                "description": "Hantu dari memori yang terhapus.",
                "location": "memory_gap",
                "reward": {"knowledge": 45, "item": self.items['memory_shard']}
            },
            "binary_wolf": {
                "id": "binary_wolf",
                "name": "Binary Wolf",
                "health": 75,
                "max_health": 75,
                "attack": 22,
                "defense": 18,
                "description": "Serigala dengan pola bulu 0 dan 1.",
                "location": "binaryheart",
                "reward": {"knowledge": 28, "item": self.items['binary_seed']}
            },
            "storm_golem": {
                "id": "storm_golem",
                "name": "Storm Golem",
                "health": 120,
                "max_health": 120,
                "attack": 40,
                "defense": 30,
                "description": "Golem dari bit-bit hujan data.",
                "location": "stormbyte",
                "reward": {"knowledge": 50, "item": self.items['storm_cape']}
            },
            "malvex_boss": {
                "id": "malvex_boss",
                "name": "Malvex, Sovereign of the Nullwave",
                "health": 300,
                "max_health": 300,
                "attack": 60,
                "defense": 50,
                "description": "Raja virus penguasa Nullwave.",
                "location": "malvex_throne",
                "reward": {"knowledge": 100, "item": self.items['nullwave_orb']}
            },
        }
        
        for enemy_id, enemy_data in enemies_data.items():
            location_id = enemy_data["location"]
            location = self.locations.get(location_id)
            
            if location:
                enemy_copy = enemy_data.copy()
                location.enemies.append(enemy_copy)
        
        self.enemies = enemies_data
    
    def create_puzzles(self):
        """Membuat puzzle-puzzle dalam game"""
        for location in self.locations.values():
            location.puzzles = []
        
        self.puzzles = {
            "binary_puzzle": {
                "puzzle_id": "binary_puzzle",
                "question": "Dalam sistem binary, berapakah hasil dari 1010 + 1010? (decimal)",
                "answer": "20",
                "hint": "1010 binary = 10 decimal",
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
            },
            "stack_trace_puzzle": {
                "puzzle_id": "stack_trace",
                "question": "Dalam stack trace: 'Segmentation fault at 0x7ffd4a2b' - "
                           "Apa arti 0x7ffd4a2b? (jawab: memory address / line number / function name)",
                "answer": "memory address",
                "hint": "0x menandakan hexadecimal address",
                "location": "segfault_abyss",
                "reward": {"knowledge": 25, "item": self.items['health_potion']}
            },
            "network_puzzle": {
                "puzzle_id": "network_puzzle",
                "question": "TCP handshake punya 3 langkah: SYN, _____, ACK",
                "answer": "syn-ack",
                "hint": "Langkah kedua adalah SYN-ACK",
                "location": "packetflow_deep",
                "reward": {"knowledge": 30, "item": self.items['data_potion']}
            },
            "boolean_puzzle": {
                "puzzle_id": "boolean_puzzle",
                "question": "Jika A=True, B=False, maka (A AND B) OR (NOT A) = ?",
                "answer": "false",
                "hint": "A AND B = False, NOT A = False, False OR False = False",
                "location": "logic_horizon",
                "reward": {"knowledge": 35, "item": self.items['logic_key']}
            },
            "array_puzzle": {
                "puzzle_id": "array_puzzle",
                "question": "Array: [5, 8, 3, 1, 9]. Setelah sort ascending, elemen ke-3 adalah?",
                "answer": "5",
                "hint": "Sorted: [1, 3, 5, 8, 9]. Elemen ke-3 (index 2) = 5",
                "location": "fragment_hive",
                "reward": {"knowledge": 40, "item": self.items['defrag_tool']}
            },
            "os_puzzle": {
                "puzzle_id": "os_puzzle",
                "question": "Dalam OS, proses child yang selesai tapi belum di-reap disebut? "
                           "(zombie / orphan / daemon)",
                "answer": "zombie",
                "hint": "Proses yang sudah mati tapi masih ada di process table",
                "location": "kernel_spire",
                "reward": {"knowledge": 45, "item": self.items['kernel_access']}
            },
            "pointer_puzzle": {
                "puzzle_id": "pointer_puzzle",
                "question": "int x = 5; int *p = &x; *p = 10; Berapa nilai x sekarang?",
                "answer": "10",
                "hint": "Pointer p menunjuk ke x, mengubah *p mengubah x",
                "location": "memory_gap",
                "reward": {"knowledge": 50, "item": self.items['memory_shard']}
            },
            "tree_puzzle": {
                "puzzle_id": "tree_puzzle",
                "question": "Binary tree dengan inorder: D B E A F C. Preorder: A B D E C F. "
                           "Postorder traversal-nya?",
                "answer": "d e b f c a",
                "hint": "Postorder: kiri-kanan-akar",
                "location": "binaryheart",
                "reward": {"knowledge": 55, "item": self.items['logic_potion']}
            },
            "merchant_puzzle": {
                "puzzle_id": "merchant_puzzle",
                "question": "Anda punya 100 bitcoins. Debug Tool (15), Health Potion (30), "
                           "Logic Sword (25). Berapa sisa jika beli semua?",
                "answer": "30",
                "hint": "Total: 15+30+25 = 70. Sisa: 100-70 = 30",
                "location": "algolane_square",
                "reward": {"knowledge": 20, "item": self.items['quantum_potion']}
            },
            "heartbeat_puzzle": {
                "puzzle_id": "heartbeat_puzzle",
                "question": "Detak jantung biner: 01001000 01100101 01101100 01101100 01101111. "
                           "Decode ke ASCII (string pendek).",
                "answer": "hello",
                "hint": "Setiap 8 bit = 1 karakter ASCII",
                "location": "heartline_node",
                "reward": {"knowledge": 60, "item": self.items['heart_key']}
            },
            "bitwise_puzzle": {
                "puzzle_id": "bitwise_puzzle",
                "question": "1010 (10) AND 0110 (6) = ? (dalam binary 4-bit)",
                "answer": "0010",
                "hint": "Bitwise AND: 1&0=0, 0&1=0, 1&1=1, 0&0=0",
                "location": "stormbyte",
                "reward": {"knowledge": 65, "item": self.items['storm_cape']}
            },
            "syntax_puzzle": {
                "puzzle_id": "syntax_puzzle",
                "question": "Apa output: for i in range(3): print(i*2) ?",
                "answer": "0 2 4",
                "hint": "i = 0,1,2 → i*2 = 0,2,4",
                "location": "codemantle",
                "reward": {"knowledge": 70, "item": self.items['royal_syntax']}
            },
            "final_puzzle": {
                "puzzle_id": "final_puzzle",
                "question": "Decrypt: Gur pxevpx vf rapelcgrq. (Caesar cipher ROT13)",
                "answer": "the check is encrypted",
                "hint": "ROT13: g→t, u→h, r→e, dll.",
                "location": "malvex_throne",
                "reward": {"knowledge": 100, "item": self.items['antivirus_sword']}
            },
        }
        
        for puzzle_id, puzzle_data in self.puzzles.items():
            location = self.locations.get(puzzle_data["location"])
            if location:
                location.puzzles.append(puzzle_data)
    
    def start_new_game(self):
        """Memulai game baru"""
        print(formatters.format_text("\n=== PENCIPTAAN KARAKTER ===", Fore.CYAN, Style.BRIGHT))
        player_name = validators.validate_name("Masukkan nama karakter Anda: ")
        
        self.player = Player(player_name)
        self.player.current_location = self.starting_location
        self.is_running = True
        self.game_state = "playing"
        
        print(formatters.format_text(f"\nSelamat datang, {player_name}!", Fore.GREEN, Style.BRIGHT))
        print(formatters.format_text("Anda adalah seorang Programmer yang terjebak di dunia digital Algoria.", Fore.WHITE))
        print(formatters.format_text("Tujuan Anda: menemukan The Lost Code untuk keluar dari dunia ini.\n", Fore.WHITE))
        
        self.show_location()
    
    def show_location(self):
        """Menampilkan lokasi saat ini"""
        location = self.locations.get(self.player.current_location)
        
        if not location:
            print("Lokasi tidak ditemukan!")
            return
        
        template_file = ""
        if location.location_id == "digital_forest":
            template_file = "locations/digital_forest.txt"
        elif location.location_id == "firewall_castle":
            template_file = "locations/firewall_castle.txt"
        elif location.location_id == "server_core":
            template_file = "locations/server_core.txt"
        elif location.location_id == "segfault_abyss":
            template_file = "locations/segfault_abyss.txt"
        elif location.location_id == "packetflow_deep":
            template_file = "locations/packetflow_deep.txt"
        elif location.location_id == "logic_horizon":
            template_file = "locations/logic_horizon.txt"
        elif location.location_id == "algolane_square":
            template_file = "locations/algolane_square.txt"
        elif location.location_id == "fragment_hive":
            template_file = "locations/fragment_hive.txt"
        elif location.location_id == "kernel_spire":
            template_file = "locations/kernel_spire.txt"
        elif location.location_id == "memory_gap":
            template_file = "locations/memory_gap.txt"
        elif location.location_id == "heartline_node":
            template_file = "locations/heartline_node.txt"
        elif location.location_id == "codemantle":
            template_file = "locations/codemantle.txt"
        elif location.location_id == "malvex_throne":
            template_file = "locations/malvex_throne.txt"
        elif location.location_id == "stormbyte":
            template_file = "locations/stormbyte.txt"
        elif location.location_id == "binaryheart":
            template_file = "locations/binaryheart.txt"
        
        try:
            if template_file:
                template_content = load_template(template_file)
                print(template_content)
            else:
                print(formatters.format_text(f"\n=== {location.name.upper()} ===", Fore.YELLOW, Style.BRIGHT))
                print(location.description)
        except:
            print(formatters.format_text(f"\n=== {location.name.upper()} ===", Fore.YELLOW, Style.BRIGHT))
            print(location.description)
        
        if location.items:
            print(formatters.format_text("\n📦 Item yang terlihat:", Fore.GREEN))
            for item in location.items:
                print(f"  - {item.name}: {item.description}")
        
        if location.enemies:
            print(formatters.format_text("\n👹 Musuh di area ini:", Fore.RED))
            for enemy in location.enemies:
                print(f"  - {enemy['name']}: {enemy['description']}")
                print(f"    HP: {enemy['health']}/{enemy.get('max_health', enemy['health'])}")
        
        if location.puzzles:
            print(formatters.format_text("\n🧩 Puzzle yang tersedia:", Fore.BLUE))
            for puzzle in location.puzzles:
                short_q = puzzle['question'][:60] + "..." if len(puzzle['question']) > 60 else puzzle['question']
                print(f"  - {short_q}")
        
        if location.connections:
            print(formatters.format_text("\n🗺️  Jalan yang tersedia:", Fore.CYAN))
            for direction, loc_id in location.connections.items():
                loc_name = self.locations[loc_id].name if loc_id in self.locations else loc_id
                target_loc = self.locations.get(loc_id)
                lock_status = " [TERKUNCI]" if target_loc and target_loc.is_locked else ""
                print(f"  - {direction.upper()}: menuju {loc_name}{lock_status}")
    
    def process_command(self, command):
        """Memproses perintah dari pemain"""
        cmd_parts = command.lower().split()
        
        if not cmd_parts:
            print("Masukkan perintah! Ketik 'help' untuk bantuan.")
            return False
        
        action = cmd_parts[0]
        
        print(f"[DEBUG] Processing: '{command}' -> action: '{action}'")
        
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
            self.handle_attack(cmd_parts[1:] if len(cmd_parts) > 1 else None)
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
        elif action == 'debug':
            self.handle_debug(cmd_parts[1:] if len(cmd_parts) > 1 else None)
        else:
            print("Perintah tidak dikenali. Ketik 'help' untuk melihat daftar perintah.")
    
    def handle_go(self, direction):
        """Menangani perintah go"""
        if not direction:
            print("Go ke mana? Contoh: go north, go south, go east, go west")
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
            
            if target_location.is_locked:
                if target_location.required_item:
                    has_item = False
                    required_item_name = target_location.required_item
                    
                    for item in self.player.inventory:
                        if item.name.lower() == required_item_name.lower():
                            has_item = True
                            break
                    
                    if has_item:
                        print(f"\n{Fore.GREEN}🔓 Anda menggunakan {required_item_name} untuk membuka {target_location.name}!{Fore.RESET}")
                        target_location.is_locked = False
                    else:
                        print(f"\n{Fore.RED}🔒 {target_location.name} terkunci!{Fore.RESET}")
                        print(f"{Fore.YELLOW}Anda membutuhkan: {required_item_name}{Fore.RESET}")
                        return
                else:
                    print(f"\n{Fore.RED}🔒 {target_location.name} terkunci!{Fore.RESET}")
                    return
            
            self.player.current_location = target_location_id
            if target_location_id not in self.player.unlocked_locations:
                self.player.unlocked_locations.append(target_location_id)
            
            print(f"\n{Fore.CYAN}🚶 Anda pergi ke {direction}.{Fore.RESET}")
            print(f"{Fore.CYAN}📍 Anda sekarang di {target_location.name}.{Fore.RESET}")
            self.show_location()
        else:
            print(f"{Fore.RED}Tidak bisa pergi ke '{direction}' dari sini.{Fore.RESET}")
            print(f"{Fore.YELLOW}Arah yang tersedia: {list(current_location.connections.keys())}{Fore.RESET}")
    
    def handle_take(self, item_names):
        """Menangani perintah take"""
        if not item_names:
            print("Ambil apa? Contoh: take sword, take potion, take 'debug tool'")
            return
        
        item_name = " ".join(item_names)
        current_location = self.locations.get(self.player.current_location)
        
        if not current_location:
            print("Lokasi saat ini tidak valid!")
            return
        
        taken_item = None
        for item in current_location.items:
            if item_name.lower() in item.name.lower():
                taken_item = item
                break
        
        if taken_item:
            current_location.items = [item for item in current_location.items if item != taken_item]
            self.player.add_item(taken_item)
            print(f"{Fore.GREEN}✅ Anda mengambil: {taken_item.name}{Fore.RESET}")
        else:
            print(f"{Fore.RED}❌ Tidak ada '{item_name}' di sini.{Fore.RESET}")
            if current_location.items:
                print(f"{Fore.YELLOW}Item yang tersedia: {[item.name for item in current_location.items]}{Fore.RESET}")
    
    def handle_use(self, item_names):
        """Menangani perintah use - FIXED HEALING"""
        if not item_names:
            print("Gunakan apa? Contoh: use potion, use key, use 'debug tool'")
            return
        
        item_name = " ".join(item_names)
        
        used_item = None
        for item in self.player.inventory:
            if item_name.lower() in item.name.lower():
                used_item = item
                break
        
        if used_item:
            try:
                print(f"[DEBUG] Using item: {used_item.name}")
                print(f"[DEBUG] Item effect: {used_item.effect}")
                
                # Panggil effect function jika callable
                if callable(used_item.effect):
                    result = used_item.effect(self.player)
                    print(f"\n{Fore.GREEN}✅ {result}{Fore.RESET}")
                else:
                    # Jika effect bukan function, coba sebagai string
                    print(f"\n{Fore.GREEN}✅ Anda menggunakan {used_item.name}.{Fore.RESET}")
                    print(f"{Fore.YELLOW}Effect: {used_item.effect}{Fore.RESET}")
                
                # Jika item adalah potion, hapus setelah digunakan
                if used_item.item_type == "potion":
                    self.player.remove_item(used_item.name)
                    print(f"{Fore.YELLOW}🧴 {used_item.name} telah digunakan dan dihapus dari inventory{Fore.RESET}")
                    
            except Exception as e:
                print(f"{Fore.RED}❌ Error menggunakan item: {str(e)}{Fore.RESET}")
                import traceback
                traceback.print_exc()
        else:
            print(f"{Fore.RED}❌ Anda tidak memiliki '{item_name}'.{Fore.RESET}")
    
    def handle_attack(self, enemy_names):
        """Menangani perintah attack"""
        if not enemy_names:
            print("Serang siapa? Contoh: attack monster, attack bug, attack 'bug monster'")
            return
        
        enemy_name = " ".join(enemy_names)
        current_location = self.locations.get(self.player.current_location)
        
        if not current_location:
            print("Lokasi saat ini tidak valid!")
            return
        
        enemy = None
        enemy_index = -1
        
        for i, e in enumerate(current_location.enemies):
            if enemy_name.lower() in e['name'].lower():
                enemy = e
                enemy_index = i
                break
        
        if not enemy:
            print(f"{Fore.RED}❌ Tidak menemukan '{enemy_name}' di sini!{Fore.RESET}")
            if current_location.enemies:
                print(f"{Fore.YELLOW}Musuh yang tersedia: {[e['name'] for e in current_location.enemies]}{Fore.RESET}")
            return
        
        print(f"\n{Fore.YELLOW}⚔️  ANDA MENYERANG {enemy['name'].upper()}! ⚔️{Fore.RESET}")
        
        base_damage = random.randint(10, 25)
        
        weapon_bonus = 0
        weapon_name = "Tangan kosong"
        for item in self.player.inventory:
            if item.item_type in ["weapon", "tool"] and hasattr(item, 'value'):
                weapon_bonus = item.value
                weapon_name = item.name
                print(f"{Fore.CYAN}🗡️  {weapon_name} memberikan bonus +{weapon_bonus} damage!{Fore.RESET}")
                break
        
        player_damage = base_damage + weapon_bonus
        
        enemy_damage = random.randint(5, enemy['attack'])
        
        player_defense = getattr(self.player, 'defense', 0)
        actual_enemy_damage = max(1, enemy_damage - player_defense)
        
        enemy_defense = enemy.get('defense', 0)
        actual_player_damage = max(1, player_damage - enemy_defense)
        
        enemy['health'] -= actual_player_damage
        self.player.take_damage(actual_enemy_damage)
        
        print(f"\n{Fore.GREEN}✅ Anda memberikan {actual_player_damage} damage ke {enemy['name']}!{Fore.RESET}")
        print(f"{Fore.RED}⚠️  {enemy['name']} memberikan {actual_enemy_damage} damage ke Anda!{Fore.RESET}")
        print(f"{Fore.YELLOW}❤️  HP {enemy['name']}: {max(0, enemy['health'])}/{enemy.get('max_health', enemy['health'])}{Fore.RESET}")
        print(f"{Fore.YELLOW}❤️  HP Anda: {self.player.health}/{self.player.max_health}{Fore.RESET}")
        
        if enemy['health'] <= 0:
            print(f"\n{Fore.GREEN}🎉 ANDA MENGALAHKAN {enemy['name'].upper()}! 🎉{Fore.RESET}")
            
            if 'reward' in enemy:
                reward = enemy['reward']
                
                if 'knowledge' in reward:
                    knowledge_gain = reward['knowledge']
                    self.player.add_knowledge(knowledge_gain)
                    print(f"{Fore.BLUE}📚 +{knowledge_gain} Knowledge! Total: {self.player.knowledge}{Fore.RESET}")
                
                if 'item' in reward and reward['item']:
                    reward_item = reward['item']
                    self.player.add_item(reward_item)
                    print(f"{Fore.GREEN}🎁 Anda mendapatkan: {reward_item.name}!{Fore.RESET}")
            
            if enemy_index != -1 and enemy_index < len(current_location.enemies):
                current_location.enemies.pop(enemy_index)
            
            if not current_location.enemies:
                print(f"{Fore.CYAN}✨ Area ini sekarang aman! ✨{Fore.RESET}")
        
        if self.player.health <= 0:
            print(f"\n{Fore.RED}💀 ANDA KALAH DALAM PERTEMPURAN! 💀{Fore.RESET}")
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
        
        puzzle = current_location.puzzles[0]
        print(f"\n{Fore.BLUE}=== 🧩 PUZZLE ==={Fore.RESET}")
        print(f"{Fore.CYAN}{puzzle['question']}{Fore.RESET}")
        
        if 'hint' in puzzle:
            hint_choice = input(f"\n{Fore.YELLOW}Ingin petunjuk? (ya/tidak): {Fore.RESET}").lower()
            if hint_choice == 'ya' or hint_choice == 'y':
                print(f"{Fore.YELLOW}💡 Petunjuk: {puzzle['hint']}{Fore.RESET}")
        
        answer = input(f"\n{Fore.GREEN}🤔 Jawaban Anda: {Fore.RESET}").strip().lower()
        
        if answer == puzzle['answer'].lower():
            print(f"\n{Fore.GREEN}✅ Benar! Puzzle terpecahkan!{Fore.RESET}")
            
            if 'reward' in puzzle:
                reward = puzzle['reward']
                if 'knowledge' in reward:
                    self.player.add_knowledge(reward['knowledge'])
                    print(f"{Fore.BLUE}📚 +{reward['knowledge']} Knowledge! Total: {self.player.knowledge}{Fore.RESET}")
                
                if 'item' in reward:
                    self.player.add_item(reward['item'])
                    print(f"{Fore.GREEN}🎁 Anda mendapatkan: {reward['item'].name}!{Fore.RESET}")
            
            current_location.puzzles.remove(puzzle)
            
            if not current_location.puzzles and not current_location.enemies:
                print(f"{Fore.CYAN}✨ Anda telah menyelesaikan semua tantangan di area ini!{Fore.RESET}")
        else:
            print(f"\n{Fore.RED}❌ Salah! Coba lagi nanti.{Fore.RESET}")
            print(f"{Fore.YELLOW}Jawaban yang benar: {puzzle['answer']}{Fore.RESET}")
            if hasattr(self.player, 'use_energy'):
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
    
    def handle_debug(self, args):
        """Debug command untuk testing"""
        if not args:
            print(f"\n{Fore.CYAN}=== DEBUG INFO ==={Fore.RESET}")
            print(f"Player Location: {self.player.current_location}")
            print(f"Player Health: {self.player.health}/{self.player.max_health}")
            print(f"Player Knowledge: {self.player.knowledge}")
            print(f"Game State: {self.game_state}")
            print(f"Locations: {len(self.locations)}")
            return
        
        command = args[0].lower()
        
        if command == 'enemies':
            current_location = self.locations.get(self.player.current_location)
            print(f"\nEnemies at {self.player.current_location}:")
            for i, enemy in enumerate(current_location.enemies):
                print(f"  {i+1}. {enemy['name']} - HP: {enemy['health']}")
        
        elif command == 'items':
            print(f"\nAll game items:")
            for key, item in self.items.items():
                print(f"  {key}: {item.name}")
        
        elif command == 'heal':
            self.player.health = self.player.max_health
            print(f"{Fore.GREEN}Player healed to full health!{Fore.RESET}")
        
        elif command == 'damage':
            if len(args) > 1:
                try:
                    damage = int(args[1])
                    self.player.health = max(0, self.player.health - damage)
                    print(f"{Fore.YELLOW}Player damaged {damage}. Health: {self.player.health}/{self.player.max_health}{Fore.RESET}")
                except:
                    print(f"{Fore.RED}Invalid damage amount!{Fore.RESET}")
        
        elif command == 'teleport':
            if len(args) > 1:
                location_id = args[1]
                if location_id in self.locations:
                    self.player.current_location = location_id
                    print(f"{Fore.GREEN}Teleported to {location_id}!{Fore.RESET}")
                    self.show_location()
                else:
                    print(f"{Fore.RED}Location {location_id} not found!{Fore.RESET}")
        
        elif command == 'spawn':
            current_location = self.locations.get(self.player.current_location)
            current_location.enemies.append({
                "id": "debug_bug",
                "name": "Bug Monster",
                "health": 60,
                "max_health": 60,
                "attack": 15,
                "defense": 5,
                "description": "Bug kode untuk testing.",
                "reward": {"knowledge": 20, "item": self.items['logic_sword']}
            })
            print(f"{Fore.GREEN}Spawned Bug Monster!{Fore.RESET}")
        
        elif command == 'give':
            if len(args) > 1:
                item_name = args[1]
                found_item = None
                for key, item in self.items.items():
                    if item_name.lower() in key.lower() or item_name.lower() in item.name.lower():
                        found_item = item
                        break
                
                if found_item:
                    self.player.add_item(found_item)
                    print(f"{Fore.GREEN}Given {found_item.name} to player!{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Item {item_name} not found!{Fore.RESET}")
    
    def show_help(self):
        """Menampilkan bantuan"""
        help_text = f"""
{Fore.CYAN}=== 🎮 DAFTAR PERINTAH ==={Fore.RESET}
{Fore.YELLOW}go [arah]{Fore.RESET}          - Bergerak ke arah tertentu
{Fore.YELLOW}look{Fore.RESET}              - Melihat sekeliling lokasi saat ini
{Fore.YELLOW}take [item]{Fore.RESET}        - Mengambil item dari lokasi
{Fore.YELLOW}use [item]{Fore.RESET}         - Menggunakan item dari inventory
{Fore.YELLOW}inventory{Fore.RESET}          - Menampilkan semua item di inventory
{Fore.YELLOW}status{Fore.RESET}             - Menampilkan status karakter
{Fore.YELLOW}attack [musuh]{Fore.RESET}     - Menyerang musuh
{Fore.YELLOW}solve{Fore.RESET}              - Memecahkan puzzle di lokasi saat ini
{Fore.YELLOW}save{Fore.RESET}               - Menyimpan progress game
{Fore.YELLOW}load{Fore.RESET}               - Memuat game yang tersimpan
{Fore.YELLOW}help{Fore.RESET}               - Menampilkan bantuan ini
{Fore.YELLOW}debug [command]{Fore.RESET}    - Debug commands
{Fore.YELLOW}quit{Fore.RESET}               - Keluar dari game

{Fore.GREEN}🎯 Tujuan Game:{Fore.RESET}
Temukan The Lost Code di Server Core dan keluar dari dunia Algoria!

{Fore.MAGENTA}💡 Tips:{Fore.RESET}
- Gunakan potion saat health rendah
- Kumpulkan senjata untuk bonus damage
- Pecahkan puzzle untuk mendapatkan item kunci
"""
        print(help_text)
    
    def handle_quit(self):
        """Menangani perintah quit"""
        confirm = input(f"\n{Fore.YELLOW}⚠️  Apakah Anda yakin ingin keluar? (ya/tidak): {Fore.RESET}").lower()
        if confirm == 'ya' or confirm == 'y':
            print(f"{Fore.CYAN}👋 Terima kasih telah bermain Algoria!{Fore.RESET}")
            self.is_running = False
            self.game_state = "menu"
    
    def game_over(self):
        """Menangani game over"""
        try:
            bad_ending = load_template("endings/bad_ending.txt")
            print(f"\n{Fore.RED}{bad_ending}{Fore.RESET}")
        except:
            print(f"\n{Fore.RED}=== 💀 GAME OVER ==={Fore.RESET}")
            print(f"{Fore.RED}Karakter Anda telah kalah dalam pertempuran.{Fore.RESET}")
        
        play_again = input(f"\n{Fore.YELLOW}🔄 Main lagi? (ya/tidak): {Fore.RESET}").lower()
        if play_again == 'ya' or play_again == 'y':
            print(f"{Fore.GREEN}Memulai game baru...{Fore.RESET}")
            self.setup_game()
            self.start_new_game()
        else:
            self.is_running = False
            self.game_state = "menu"
    
    def check_win_condition(self):
        """Memeriksa apakah player menang"""
        if (self.player.current_location == "server_core" and 
            self.player.has_item("Encrypted Data") and
            self.player.knowledge >= 100):
            
            malvex_location = self.locations.get("malvex_throne")
            malvex_defeated = True
            
            if malvex_location:
                for enemy in malvex_location.enemies:
                    if "malvex" in enemy['name'].lower():
                        malvex_defeated = False
                        break
            
            if malvex_defeated:
                try:
                    good_ending = load_template("endings/good_ending.txt")
                    print(f"\n{Fore.GREEN}{good_ending}{Fore.RESET}")
                except:
                    print(f"\n{Fore.GREEN}=== 🏆 VICTORY! ==={Fore.RESET}")
                    print(f"🎉 Anda berhasil mengalahkan Malvex dan menemukan The Lost Code!")
                
                print(f"\n{Fore.CYAN}=== 📊 FINAL STATISTICS ===")
                print(f"👤 Player: {self.player.name}")
                print(f"🧠 Final Knowledge: {self.player.knowledge}")
                print(f"❤️  Health: {self.player.health}/{self.player.max_health}")
                print(f"📍 Locations Explored: {len(self.player.unlocked_locations)}/{len(self.locations)}")
                print(f"🎒 Items Collected: {len(self.player.inventory)}")
                print(f"================================{Fore.RESET}")
                
                return True
        
        return False

    def run_game_loop(self):
        """Menjalankan game loop utama"""
        print(f"\n{Fore.CYAN}{'='*50}{Fore.RESET}")
        print(f"{Fore.GREEN}{GAME_TITLE}{Fore.RESET}")
        print(f"{Fore.CYAN}{'='*50}{Fore.RESET}")
        
        while True:
            if self.game_state == "menu":
                print(f"\n{Fore.YELLOW}=== MENU UTAMA ==={Fore.RESET}")
                print("1. Mulai Game Baru")
                print("2. Petunjuk")
                print("3. Keluar")
                
                choice = input(f"\n{Fore.GREEN}Pilih opsi (1-3): {Fore.RESET}").strip()
                
                if choice == "1":
                    self.start_new_game()
                elif choice == "2":
                    self.show_help()
                elif choice == "3":
                    print(f"{Fore.CYAN}Terima kasih! Sampai jumpa!{Fore.RESET}")
                    break
                else:
                    print(f"{Fore.RED}Pilihan tidak valid!{Fore.RESET}")
            
            elif self.game_state == "playing" and self.is_running:
                command = input(f"\n{Fore.YELLOW}>>> {Fore.RESET}").strip()
                
                if command.lower() == 'quit':
                    self.handle_quit()
                    if not self.is_running:
                        self.game_state = "menu"
                    continue
                
                self.process_command(command)
                
                if self.check_win_condition():
                    play_again = input(f"\n{Fore.YELLOW}🎮 Main lagi? (ya/tidak): {Fore.RESET}").lower()
                    if play_again == 'ya' or play_again == 'y':
                        self.setup_game()
                        self.start_new_game()
                    else:
                        self.game_state = "menu"
                        self.is_running = False

if __name__ == "__main__":
    game = GameService()
    game.run_game_loop()