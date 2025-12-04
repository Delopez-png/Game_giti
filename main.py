#!/usr/bin/env python3
"""
Game Story: The Lost Code of Algoria
Game petualangan teks di dunia digital Algoria
"""

import os
import sys
from colorama import init, Fore, Style
from pyfiglet import Figlet

# Tambahkan path ke modul kita
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.game_service import GameService
from templates import load_template

# Inisialisasi colorama
init(autoreset=True)

def clear_screen():
    """Membersihkan layar"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_title():
    """Menampilkan judul game"""
    clear_screen()
    
    # Gunakan pyfiglet untuk judul yang menarik
    try:
        f = Figlet(font='slant')
        title = f.renderText('ALGORIA')
        print(Fore.CYAN + title)
    except:
        # Fallback jika pyfiglet tidak tersedia
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "              THE LOST CODE OF ALGORIA")
        print(Fore.CYAN + "=" * 60)
    
    print(Fore.YELLOW + "          Sebuah Game Story Petualangan Teks")
    print(Fore.YELLOW + "=" * 60 + "\n")

def main_menu():
    """Menampilkan menu utama"""
    while True:
        show_title()
        
        print(Fore.GREEN + "\n=== MENU UTAMA ===")
        print(Fore.WHITE + "1. Mulai Game Baru")
        print(Fore.WHITE + "2. Muat Game")
        print(Fore.WHITE + "3. Baca Cerita")
        print(Fore.WHITE + "4. Petunjuk")
        print(Fore.WHITE + "5. Keluar")
        
        choice = input(Fore.CYAN + "\nPilih menu (1-5): ").strip()
        
        if choice == '1':
            return 'new_game'
        elif choice == '2':
            return 'load_game'
        elif choice == '3':
            show_story()
        elif choice == '4':
            show_instructions()
        elif choice == '5':
            print(Fore.YELLOW + "\nTerima kasih telah bermain!")
            sys.exit(0)
        else:
            print(Fore.RED + "Pilihan tidak valid. Coba lagi.")
            input(Fore.WHITE + "Tekan Enter untuk melanjutkan...")

def show_story():
    """Menampilkan cerita game"""
    clear_screen()
    show_title()
    
    print(load_template('intro.txt'))
    
    input(Fore.WHITE + "\nTekan Enter untuk kembali ke menu...")

def show_instructions():
    """Menampilkan petunjuk permainan"""
    clear_screen()
    show_title()
    
    print(Fore.CYAN + "=== PETUNJUK PERMAINAN ===\n")
    print(Fore.WHITE + "PERINTAH DASAR:")
    print("  go [arah]     - Bergerak ke arah (north, south, east, west)")
    print("  look          - Melihat sekeliling")
    print("  take [item]   - Mengambil item")
    print("  use [item]    - Menggunakan item")
    print("  inventory     - Menampilkan barang yang dimiliki")
    print("  status        - Menampilkan status karakter")
    print("  attack [musuh]- Menyerang musuh")
    print("  solve         - Memecahkan puzzle")
    print("  save          - Menyimpan permainan")
    print("  load          - Memuat permainan")
    print("  help          - Menampilkan bantuan")
    print("  quit          - Keluar dari game\n")
    
    print(Fore.YELLOW + "TUJUAN PERMAINAN:")
    print("  Temukan 'The Lost Code' di Server Core untuk memenangkan game!")
    print("  Kumpulkan pengetahuan dengan mengalahkan musuh dan memecahkan puzzle.")
    print("  Gunakan item yang tepat untuk membuka area yang terkunci.\n")
    
    input(Fore.WHITE + "Tekan Enter untuk kembali ke menu...")

def main():
    """Fungsi utama untuk menjalankan game"""
    game_service = GameService()
    
    while True:
        menu_choice = main_menu()
        
        if menu_choice == 'new_game':
            clear_screen()
            show_title()
            
            # Tampilkan intro
            print(load_template('intro.txt'))
            input(Fore.WHITE + "\nTekan Enter untuk memulai petualangan...")
            
            # Mulai game baru
            game_service.start_new_game()
            
            # Game loop
            while game_service.is_running:
                # Cek kondisi menang
                if game_service.check_win_condition():
                    play_again = input(Fore.CYAN + "\nMain lagi? (ya/tidak): ").lower()
                    if play_again == 'ya':
                        game_service.start_new_game()
                        continue
                    else:
                        break
                
                # Tampilkan prompt
                print(Fore.CYAN + "\n" + "=" * 60)
                command = input(Fore.GREEN + "\nApa yang ingin Anda lakukan? ").strip()
                
                # Proses perintah
                game_service.process_command(command)
            
            print(Fore.YELLOW + "\nKembali ke menu utama...")
            input(Fore.WHITE + "Tekan Enter untuk melanjutkan...")
            
        elif menu_choice == 'load_game':
            print(Fore.YELLOW + "\nFitur load game akan tersedia di versi mendatang.")
            input(Fore.WHITE + "Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\nGame dihentikan.")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\nTerjadi error: {e}")
        sys.exit(1)