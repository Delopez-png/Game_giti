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

PUZZLE_QUESTIONS = {
    "stack_trace": {
        "question": "Dalam stack trace: 'Segmentation fault at 0x7ffd4a2b' - "
                   "Apa arti 0x7ffd4a2b?",
        "answer": "memory address",
        "options": ["memory address", "line number", "function name", "error code"]
    },
    "network": {
        "question": "TCP handshake punya 3 langkah: SYN, _____, ACK",
        "answer": "syn-ack",
        "options": ["syn-ack", "ack-syn", "syn-syn", "fin-ack"]
    },
    "boolean": {
        "question": "Jika A=True, B=False, maka (A AND B) OR (NOT A) = ?",
        "answer": "false",
        "options": ["true", "false", "null", "undefined"]
    },
    "array": {
        "question": "Array: [5, 8, 3, 1, 9]. Setelah sort ascending, elemen ke-3 adalah?",
        "answer": "5",
        "options": ["3", "5", "8", "9"]
    },
    "os": {
        "question": "Dalam OS, proses child yang selesai tapi belum di-reap disebut?",
        "answer": "zombie",
        "options": ["zombie", "orphan", "daemon", "ghost"]
    },
    "pointer": {
        "question": "int x = 5; int *p = &x; *p = 10; Berapa nilai x sekarang?",
        "answer": "10",
        "options": ["5", "10", "15", "pointer error"]
    },
    "tree": {
        "question": "Binary tree dengan inorder: D B E A F C. Preorder: A B D E C F. Postorder traversal-nya?",
        "answer": "d e b f c a",
        "options": ["d e b f c a", "a b d e c f", "d b e a f c", "f c a e b d"]
    },
    "merchant": {
        "question": "Anda punya 100 bitcoins. Debug Tool (15), Health Potion (30), Logic Sword (25). Berapa sisa jika beli semua?",
        "answer": "30",
        "options": ["20", "30", "40", "50"]
    },
    "heartbeat": {
        "question": "Detak jantung biner: 01001000 01100101 01101100 01101100 01101111. Decode ke ASCII",
        "answer": "hello",
        "options": ["hello", "world", "code", "algoria"]
    },
    "bitwise": {
        "question": "1010 (10) AND 0110 (6) = ? (dalam binary 4-bit)",
        "answer": "0010",
        "options": ["0010", "1100", "1110", "0000"]
    },
    "syntax": {
        "question": "Apa output: for i in range(3): print(i*2) ?",
        "answer": "0 2 4",
        "options": ["0 1 2", "0 2 4", "2 4 6", "error"]
    },
    "final": {
        "question": "Decrypt: Gur pxevpx vf rapelcgrq. (Caesar cipher ROT13)",
        "answer": "the check is encrypted",
        "options": ["the check is encrypted", "this is a secret message", "hello world", "decrypt me"]
    }
}

LOCATION_DESCRIPTIONS = {
    "digital_forest": "Hutan Digital tempat data tumbuh seperti pohon.",
    "firewall_castle": "Kastil firewall yang terkunci rapat.",
    "server_core": "Inti server Algoria tempat The Lost Code disimpan.",
    "segfault_abyss": "Jurang crash algorithm yang dalam.",
    "packetflow_deep": "Lautan packet data yang mengalir cepat.",
    "logic_horizon": "Padang luas tempat logika mengalir bebas.",
    "algolane_square": "Pasar digital tempat avatar dan bot berdagang.",
    "fragment_hive": "Sarang bug data yang tidak lengkap.",
    "kernel_spire": "Menara tinggi yang berfungsi sebagai otak utama Algoria.",
    "memory_gap": "Ruang kosong tempat memori-memori hilang berkumpul.",
    "heartline_node": "Jantung dunia berupa kristal data raksasa.",
    "codemantle": "Kerajaan megah dari block-syntax dan rune algoritma.",
    "malvex_throne": "Takhta Raja Virus penguasa Nullwave.",
    "stormbyte": "Wilayah dengan hujan data tak henti.",
    "binaryheart": "Hutan kuno dengan 'detak angka' seperti jantung digital."
}

# Warna untuk berbagai tipe item
ITEM_COLORS = {
    'weapon': 'RED',
    'potion': 'GREEN', 
    'key': 'YELLOW',
    'tool': 'BLUE',
    'data': 'MAGENTA',
    'armor': 'CYAN',
    'artifact': 'WHITE',
    'special': 'YELLOW'
}

# Statistik musuh default
ENEMY_STATS = {
    'easy': {'health': 50, 'attack': 10, 'defense': 5, 'knowledge': 15},
    'medium': {'health': 80, 'attack': 20, 'defense': 10, 'knowledge': 30},
    'hard': {'health': 120, 'attack': 30, 'defense': 20, 'knowledge': 50},
    'boss': {'health': 300, 'attack': 60, 'defense': 50, 'knowledge': 100}
}

# Requirement untuk kemenangan
WIN_REQUIREMENTS = {
    'min_knowledge': 200,
    'required_item': 'Encrypted Data',
    'final_location': 'server_core',
    'must_defeat_boss': True
}

# Quest utama
MAIN_QUESTS = [
    "Temukan Debug Tool di Digital Forest",
    "Kalahkan Bug Monster untuk mendapatkan Logic Sword",
    "Pecahkan Binary Puzzle untuk mendapatkan Energy Drink",
    "Kumpulkan Firewall Key untuk membuka Firewall Castle",
    "Jelajahi semua 15 lokasi di Algoria",
    "Kalahkan Malvex, Sovereign of the Nullwave",
    "Temukan Encrypted Data di Server Core",
    "Dapatkan 200 Knowledge Points"
]

# Pesan bantuan tambahan
HELP_MESSAGES = {
    'combat': "Gunakan 'attack [nama_musuh]' untuk menyerang. Pastikan health dan energy cukup!",
    'puzzle': "Gunakan 'solve' untuk memecahkan puzzle. Dapatkan hint dengan jawab 'ya' saat ditanya.",
    'exploration': "Gunakan 'look' untuk melihat sekeliling dan 'go [arah]' untuk berpindah.",
    'inventory': "Gunakan 'use [nama_item]' untuk menggunakan item dari inventory.",
    'keys': "Beberapa lokasi terkunci. Butuh item khusus seperti Firewall Key, Logic Key, dll."
}