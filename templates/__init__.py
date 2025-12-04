import os

def load_template(template_name):
    """Memuat template dari file"""
    template_path = os.path.join(os.path.dirname(__file__), template_name)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Template {template_name} tidak ditemukan."