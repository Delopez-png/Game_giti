#!/usr/bin/env python3
"""
Test Runner untuk Game The Lost Code of Algoria
Menjalankan berbagai skenario testing secara otomatis
"""

import os
import sys
import time
from colorama import Fore, Style, init

# Tambahkan path ke modul kita
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.game_service import GameService
from models.player import Player
from models.item import Item

# Inisialisasi colorama
init(autoreset=True)

class GameTester:
    def __init__(self):
        self.game_service = GameService()
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def print_test_header(self, test_name):
        """Menampilkan header test"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"TEST: {test_name}")
        print(f"{'='*60}{Fore.RESET}")
    
    def print_test_result(self, test_name, success, message=""):
        """Menampilkan hasil test"""
        self.total_tests += 1
        
        if success:
            self.passed_tests += 1
            status = f"{Fore.GREEN}PASS{Fore.RESET}"
        else:
            self.failed_tests += 1
            status = f"{Fore.RED}FAIL{Fore.RESET}"
        
        result = {
            "test": test_name,
            "status": "PASS" if success else "FAIL",
            "message": message
        }
        self.test_results.append(result)
        
        print(f"{status} - {test_name}")
        if message:
            print(f"   {Fore.YELLOW}{message}{Fore.RESET}")
    
    def test_player_creation(self):
        """Test pembuatan player"""
        self.print_test_header("Player Creation Test")
        
        try:
            player = Player("TestPlayer")
            
            # Test atribut dasar
            assert player.name == "TestPlayer", "Nama player salah"
            assert player.health == 100, "Health awal salah"
            assert player.energy == 50, "Energy awal salah"
            assert player.knowledge == 0, "Knowledge awal salah"
            assert player.current_location == "digital_forest", "Lokasi awal salah"
            
            # Test inventory
            assert len(player.inventory) == 0, "Inventory harus kosong"
            
            # Test metode add_item
            test_item = Item("Test Item", "Item untuk testing", "tool", 10)
            player.add_item(test_item)
            assert len(player.inventory) == 1, "Item tidak ditambahkan"
            assert player.has_item("Test Item"), "has_item tidak berfungsi"
            
            # Test metode remove_item
            player.remove_item("Test Item")
            assert len(player.inventory) == 0, "Item tidak dihapus"
            
            # Test damage dan healing
            player.take_damage(30)
            assert player.health == 70, "Damage tidak bekerja"
            
            player.heal(20)
            assert player.health == 90, "Heal tidak bekerja"
            
            self.print_test_result("Player Creation", True, "Semua test player berhasil")
            return True
            
        except AssertionError as e:
            self.print_test_result("Player Creation", False, str(e))
            return False
        except Exception as e:
            self.print_test_result("Player Creation", False, f"Error: {str(e)}")
            return False
    
    def test_item_system(self):
        """Test sistem item"""
        self.print_test_header("Item System Test")
        
        try:
            # Test item creation
            item = Item("Health Potion", "Memulihkan 30 health", "potion", 30)
            
            assert item.name == "Health Potion", "Nama item salah"
            assert item.description == "Memulihkan 30 health", "Deskripsi item salah"
            assert item.item_type == "potion", "Tipe item salah"
            assert item.value == 30, "Value item salah"
            
            # Test efek item
            player = Player("TestPlayer")
            player.take_damage(40)
            health_before = player.health
            
            # Tambahkan efek healing sederhana
            def heal_effect(p):
                p.heal(30)
                return "Healed!"
            
            item.effect = heal_effect
            result = item.use(player)
            
            assert player.health == health_before + 30, "Efek item tidak bekerja"
            assert result == "Healed!", "Return value item.use salah"
            
            self.print_test_result("Item System", True, "Semua test item berhasil")
            return True
            
        except AssertionError as e:
            self.print_test_result("Item System", False, str(e))
            return False
        except Exception as e:
            self.print_test_result("Item System", False, f"Error: {str(e)}")
            return False
    
    def test_location_system(self):
        """Test sistem lokasi"""
        self.print_test_header("Location System Test")
        
        try:
            # Setup game service untuk mendapatkan lokasi
            self.game_service.setup_game()
            
            # Test lokasi ada
            assert "digital_forest" in self.game_service.locations, "Digital Forest tidak ada"
            assert "firewall_castle" in self.game_service.locations, "Firewall Castle tidak ada"
            assert "server_core" in self.game_service.locations, "Server Core tidak ada"
            
            # Test Digital Forest
            df = self.game_service.locations["digital_forest"]
            assert df.name == "Digital Forest", "Nama lokasi salah"
            assert len(df.items) == 2, "Item di Digital Forest salah"
            assert "north" in df.connections, "Koneksi north tidak ada"
            
            # Test Firewall Castle terkunci
            fc = self.game_service.locations["firewall_castle"]
            assert fc.is_locked == True, "Firewall Castle harus terkunci"
            assert fc.required_item == "firewall_key", "Required item salah"
            
            # Test koneksi antar lokasi
            assert df.connections["north"] == "firewall_castle", "Koneksi north salah"
            assert fc.connections["south"] == "digital_forest", "Koneksi south salah"
            assert fc.connections["east"] == "server_core", "Koneksi east salah"
            
            self.print_test_result("Location System", True, "Semua test lokasi berhasil")
            return True
            
        except AssertionError as e:
            self.print_test_result("Location System", False, str(e))
            return False
        except Exception as e:
            self.print_test_result("Location System", False, f"Error: {str(e)}")
            return False
    
    def test_puzzle_system(self):
        """Test sistem puzzle"""
        self.print_test_header("Puzzle System Test")
        
        try:
            self.game_service.setup_game()
            
            # Test puzzle ada di lokasi
            df = self.game_service.locations["digital_forest"]
            assert len(df.puzzles) > 0, "Tidak ada puzzle di Digital Forest"
            
            # Test puzzle data
            puzzle = df.puzzles[0]
            assert "question" in puzzle, "Puzzle tidak punya question"
            assert "answer" in puzzle, "Puzzle tidak punya answer"
            assert "hint" in puzzle, "Puzzle tidak punya hint"
            assert "reward" in puzzle, "Puzzle tidak punya reward"
            
            # Test jawaban puzzle (harusnya 20 untuk 1010 + 1010)
            # Atau 16 untuk 1010 + 0110, tergantung perbaikan
            expected_answer = "20"  # Ganti dengan "16" jika sudah diperbaiki
            assert puzzle["answer"] == expected_answer, f"Jawaban puzzle salah. Harusnya: {expected_answer}"
            
            self.print_test_result("Puzzle System", True, f"Puzzle test berhasil (answer: {puzzle['answer']})")
            return True
            
        except AssertionError as e:
            self.print_test_result("Puzzle System", False, str(e))
            return False
        except Exception as e:
            self.print_test_result("Puzzle System", False, f"Error: {str(e)}")
            return False
    
    def test_combat_system(self):
        """Test sistem combat"""
        self.print_test_header("Combat System Test")
        
        try:
            self.game_service.setup_game()
            
            # Setup player
            player = Player("CombatTest")
            
            # Test damage calculation
            initial_health = player.health
            player.take_damage(25)
            assert player.health == initial_health - 25, "Damage calculation salah"
            
            # Test health bounds
            player.take_damage(100)
            assert player.health == 0, "Health tidak boleh negatif"
            
            # Test healing bounds
            player.heal(150)
            assert player.health == player.max_health, "Health tidak boleh lebih dari max"
            
            self.print_test_result("Combat System", True, "Semua test combat berhasil")
            return True
            
        except AssertionError as e:
            self.print_test_result("Combat System", False, str(e))
            return False
        except Exception as e:
            self.print_test_result("Combat System", False, f"Error: {str(e)}")
            return False
    
    def test_game_flow(self):
        """Test alur game dasar"""
        self.print_test_header("Game Flow Test")
        
        try:
            # Start new game
            self.game_service.start_new_game()
            
            # Test player dibuat
            assert self.game_service.player is not None, "Player tidak dibuat"
            assert self.game_service.is_running == True, "Game tidak running"
            assert self.game_service.game_state == "playing", "Game state salah"
            
            # Test command processing
            result = self.game_service.process_command("help")
            assert result is None or result is not False, "Command help gagal"
            
            # Test status command
            result = self.game_service.process_command("status")
            assert result is None or result is not False, "Command status gagal"
            
            # Test inventory command (harusnya kosong)
            result = self.game_service.process_command("inventory")
            assert result is None or result is not False, "Command inventory gagal"
            
            self.print_test_result("Game Flow", True, "Alur game berjalan normal")
            return True
            
        except AssertionError as e:
            self.print_test_result("Game Flow", False, str(e))
            return False
        except Exception as e:
            self.print_test_result("Game Flow", False, f"Error: {str(e)}")
            return False
    
    def test_binary_puzzle_correction(self):
        """Test khusus untuk perbaikan binary puzzle"""
        self.print_test_header("Binary Puzzle Correction Test")
        
        try:
            self.game_service.setup_game()
            
            # Get the binary puzzle
            df = self.game_service.locations["digital_forest"]
            puzzle = None
            
            for p in df.puzzles:
                if "binary" in p.get("puzzle_id", ""):
                    puzzle = p
                    break
            
            assert puzzle is not None, "Binary puzzle tidak ditemukan"
            
            question = puzzle["question"]
            answer = puzzle["answer"]
            
            print(f"{Fore.YELLOW}Pertanyaan: {question}{Fore.RESET}")
            print(f"{Fore.YELLOW}Jawaban: {answer}{Fore.RESET}")
            
            # Cek apakah puzzle sudah diperbaiki
            if "1010 + 1010" in question and answer == "20":
                self.print_test_result("Binary Puzzle", True, "✓ Puzzle sudah BENAR: 1010 + 1010 = 20")
                return True
            elif "1010 + 0110" in question and answer == "16":
                self.print_test_result("Binary Puzzle", True, "✓ Puzzle sudah BENAR: 1010 + 0110 = 16")
                return True
            else:
                error_msg = f"✗ Puzzle MASIH SALAH! Question: '{question}', Answer: '{answer}'"
                error_msg += "\n   Harusnya: '1010 + 1010' dengan answer '20'"
                error_msg += "\n   ATAU: '1010 + 0110' dengan answer '16'"
                self.print_test_result("Binary Puzzle", False, error_msg)
                return False
                
        except Exception as e:
            self.print_test_result("Binary Puzzle", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Menjalankan semua test"""
        print(f"{Fore.MAGENTA}{'='*60}")
        print("   TEST SUITE: THE LOST CODE OF ALGORIA")
        print(f"{'='*60}{Fore.RESET}")
        
        # Jalankan semua test
        tests = [
            self.test_player_creation,
            self.test_item_system,
            self.test_location_system,
            self.test_puzzle_system,
            self.test_combat_system,
            self.test_game_flow,
            self.test_binary_puzzle_correction
        ]
        
        for test in tests:
            test()
        
        # Tampilkan summary
        self.print_summary()
    
    def print_summary(self):
        """Menampilkan summary test"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}{Fore.RESET}")
        
        print(f"\nTotal Tests: {self.total_tests}")
        print(f"{Fore.GREEN}Passed: {self.passed_tests}{Fore.RESET}")
        print(f"{Fore.RED}Failed: {self.failed_tests}{Fore.RESET}")
        
        pass_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        color = Fore.GREEN if pass_rate >= 80 else Fore.YELLOW if pass_rate >= 60 else Fore.RED
        print(f"{color}Pass Rate: {pass_rate:.1f}%{Fore.RESET}")
        
        # Tampilkan detail test yang gagal
        if self.failed_tests > 0:
            print(f"\n{Fore.YELLOW}Failed Tests:{Fore.RESET}")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['message']}")
        
        # Rekomendasi
        print(f"\n{Fore.MAGENTA}Rekomendasi:{Fore.RESET}")
        if pass_rate == 100:
            print("✓ Semua test berhasil! Game siap dimainkan.")
        elif pass_rate >= 80:
            print("✓ Game hampir siap. Perbaiki beberapa test yang gagal.")
        else:
            print("✗ Game butuh perbaikan signifikan.")

def main():
    """Fungsi utama test runner"""
    tester = GameTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()