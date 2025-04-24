#!/usr/bin/env python
"""
Basit bir FastMCP v2 testi - modülü doğrudan çağırır
"""
import sys
import os
import importlib.util
from pathlib import Path

def main():
    """Ana test fonksiyonu"""
    print("=== FastMCP v2 Basit Test ===")
    
    # GitHub token kontrolü
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN çevre değişkeni tanımlanmamış!")
        token = input("GitHub Token giriniz: ")
        os.environ["GITHUB_TOKEN"] = token
    
    # Proje kök dizinini bul
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # GitHub tool modül yolu 
    github_module_path = os.path.join(base_dir, "toolz/github/list_issues.py")
    
    if not os.path.exists(github_module_path):
        print(f"GitHub tool modülü bulunamadı: {github_module_path}")
        return 1
    
    print(f"Modül yükleniyor: {github_module_path}")
    
    # Modülü manuel olarak yükle
    spec = importlib.util.spec_from_file_location("github_tool", github_module_path)
    github_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(github_module)
    
    print("Modül başarıyla yüklendi")
    
    # Modülü direkt olarak çağır (FastMCP olmadan)
    print("\n[Doğrudan Modül Çağrısı]")
    params = {
        "repo_owner": "Upsonic",
        "repo_name": "upsonic"
    }
    
    # run() fonksiyonunu çağır
    print("run() fonksiyonu çağrılıyor...")
    try:
        result = github_module.run(params)
        issues = result.get("issues", [])
        print(f"Toplam issue sayısı: {len(issues)}")
        for issue in issues[:3]:
            print(f"- {issue.get('title', 'Başlık yok')} (#{issue.get('number', '?')})")
        
        print("\nDual-mode yapı başarıyla çalışıyor! ✅")
        return 0
    except Exception as e:
        print(f"Hata: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
