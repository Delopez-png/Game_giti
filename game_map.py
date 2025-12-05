# game_map.py
def show_map(player_locations):
    """Menampilkan peta Algoria"""
    map_text = """
                         [CODEmANTLE DOMINION]
                                  |
                                  v
                        [THE LOGIC KERNEL SPIRE]
                         /                  \\
                        /                    \\
        [BINARYHEART WOODS] <--> [DIGITAL FOREST] <--> [PACKETFLOW DEEP]
               |                       |                       |
               v                       v                       v
        [FIREWALL CASTLE]     [SEGFAULT ABYSS]        [ALGOLANE SQUARE]
               |                       |                       |
               v                       v                       v
          [SERVER CORE]        [MEMORY GAP]             [STORMBYTE EXPANSE]
               |                       |
               v                       v
          [MALVEX THRONE] <--> [HEARTLINE NODE] <--> [FRAGMENT HIVE]
    
    Legend:
    [ ] = Location      <--> = Two-way connection
    --> = One-way       | = Connection
    """
    print(map_text)