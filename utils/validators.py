def validate_input(prompt, valid_options=None, input_type=str):
    """
    Memvalidasi input pengguna dengan opsi yang valid
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input:
                print("Input tidak boleh kosong. Coba lagi.")
                continue
                
            if valid_options:
                if user_input.lower() in [opt.lower() for opt in valid_options]:
                    return user_input
                else:
                    print(f"Input tidak valid. Pilihan: {', '.join(valid_options)}")
            else:
                return input_type(user_input)
                
        except ValueError:
            print(f"Input harus berupa {input_type.__name__}. Coba lagi.")
        except KeyboardInterrupt:
            print("\n\nGame dihentikan.")
            exit(0)

def validate_name(prompt):
    """Memvalidasi nama player"""
    while True:
        name = input(prompt).strip()
        
        if not name:
            print("Nama tidak boleh kosong.")
        elif len(name) < 2:
            print("Nama terlalu pendek (minimal 2 karakter).")
        elif len(name) > 20:
            print("Nama terlalu panjang (maksimal 20 karakter).")
        elif not name.isalnum():
            print("Nama hanya boleh berisi huruf dan angka (tanpa spasi).")
        else:
            return name