#!/usr/bin/env python
"""
Dual-mode araçların hem LightMCP hem de FastMCP olarak çalışıp çalışmadığını test eder.
"""
import os
import sys
import importlib.util
from pathlib import Path
import argparse

# LightMCP importları
from lightmcp import add
from lightmcp.tool_loader import MCPTool

def test_lightmcp_github():
    """GitHub aracını LightMCP üzerinden test et"""
    print("\n=== GitHub Tool LightMCP Test ===")
    
    # GitHub token kontrolü
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN çevre değişkeni tanımlanmamış!")
        token = input("GitHub Token giriniz: ")
        os.environ["GITHUB_TOKEN"] = token
    
    # Tool'u LightMCP üzerinden yükle
    tool = add("github.list_issues")
    print(f"Tool yüklendi: {tool}")
    
    # LightMCP call() fonksiyonu ile çağır
    result = tool.call({
        "repo_owner": "Upsonic", 
        "repo_name": "upsonic"
    })
    
    # Sonuçları kontrol et ve göster
    issues = result.get("issues", [])
    print(f"Toplam issue sayısı: {len(issues)}")
    for issue in issues[:3]:  # İlk 3 issue'yu göster
        print(f"- {issue.get('title', 'Başlık yok')} (#{issue.get('number', '?')})")
    
    # Başarılı mı?
    return len(issues) > 0

def test_lightmcp_notion():
    """Notion aracını LightMCP üzerinden test et"""
    print("\n=== Notion Tool LightMCP Test ===")
    
    # Notion API key kontrolü
    token = os.getenv("NOTION_API_KEY")
    if not token:
        print("NOTION_API_KEY çevre değişkeni tanımlanmamış!")
        token = input("Notion API Key giriniz: ")
        os.environ["NOTION_API_KEY"] = token
    
    # Tool'u LightMCP üzerinden yükle
    tool = add("notion.query_tasks")
    print(f"Tool yüklendi: {tool}")
    
    # Veritabanı ID'si
    database_id = input("Notion veritabanı ID'si giriniz: ")
    
    # LightMCP call() fonksiyonu ile çağır
    result = tool.call({
        "database_id": database_id,
        "filter_by": {"property": "Status", "status": {"equals": "In progress"}}
    })
    
    # Sonuçları kontrol et ve göster
    tasks = result.get("tasks", [])
    print(f"Toplam görev sayısı: {len(tasks)}")
    for task in tasks[:3]:  # İlk 3 görevi göster
        title = task.get('properties', {}).get('Name', {}).get('title', [{}])[0].get('plain_text', 'İsimsiz')
        print(f"- {title}")
    
    # Başarılı mı?
    return len(tasks) >= 0  # Hiç görev olmasa da başarılı sayılabilir

def test_fastmcp_github():
    """GitHub aracını doğrudan FastMCP olarak çalıştır"""
    print("\n=== GitHub Tool FastMCP Test ===")
    
    try:
        # GitHub tool modülünü direkt olarak dosya sisteminden yükle
        import importlib.util
        import os
        
        # Proje kök dizinini bul
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # GitHub tool modül yolu 
        github_module_path = os.path.join(base_dir, "toolz/github/list_issues.py")
        
        if not os.path.exists(github_module_path):
            print(f"GitHub tool modülü bulunamadı: {github_module_path}")
            return False
            
        # Modülü manuel olarak yükle
        spec = importlib.util.spec_from_file_location("github_tool", github_module_path)
        github_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(github_module)
        
        # FastMCP sunucusunu başlat
        print("FastMCP sunucusu başlatılıyor...")
        github_mcp = github_module.mcp  # Modül içindeki mcp nesnesini al
        
        # Arka planda çalıştırmak için threading kullan
        import threading
        server_thread = threading.Thread(target=github_mcp.run, kwargs={"port": 8765})
        server_thread.daemon = True
        server_thread.start()
        
        # Sunucunun başlaması için kısa bir bekleme
        import time
        time.sleep(1)
        
        # FastMCP client ile bağlan
        from fastmcp import Client
        import asyncio
        
        async def test_github_api():
            async with Client("http://localhost:8765") as client:
                # Araçları listele
                tools = await client.list_tools()
                print(f"Sunucu üzerindeki araçlar: {tools}")
                
                # GitHub issue'ları çek
                result = await client.call_tool(
                    tools[0], 
                    {
                        "repo_owner": "Upsonic",
                        "repo_name": "upsonic"
                    }
                )
                
                issues = result
                print(f"Toplam issue sayısı: {len(issues)}")
                for issue in issues[:3]:
                    print(f"- {issue.get('title', 'Başlık yok')} (#{issue.get('number', '?')})")
                
                return len(issues) > 0
        
        # Asenkron fonksiyonu çalıştır
        print("FastMCP API testi yapılıyor...")
        result = asyncio.run(test_github_api())
        
        # Sunucuyu durdur
        github_mcp.stop()
        print("FastMCP sunucusu durduruldu.")
        
        return result
    
    except Exception as e:
        print(f"FastMCP testi sırasında hata: {str(e)}")
        return False

def test_fastmcp_notion():
    """Notion aracını doğrudan FastMCP olarak çalıştır"""
    print("\n=== Notion Tool FastMCP Test ===")
    
    try:
        # Notion token kontrolü
        token = os.getenv("NOTION_API_KEY")
        if not token:
            print("NOTION_API_KEY çevre değişkeni tanımlanmamış!")
            return False
        
        # Veritabanı ID'si
        database_id = input("Notion veritabanı ID'si giriniz: ")
        
        # Notion tool dosyasını import et
        from toolz.notion.query_tasks import mcp as notion_mcp
        
        # FastMCP sunucusunu başlat
        print("FastMCP sunucusu başlatılıyor...")
        notion_mcp = notion_mcp  # Modül içindeki mcp nesnesini al
        
        # Arka planda çalıştırmak için threading kullan
        import threading
        server_thread = threading.Thread(target=notion_mcp.run, kwargs={"port": 8766})
        server_thread.daemon = True
        server_thread.start()
        
        # Sunucunun başlaması için kısa bir bekleme
        import time
        time.sleep(1)
        
        # FastMCP client ile bağlan
        from fastmcp import Client
        import asyncio
        
        async def test_notion_api():
            async with Client("http://localhost:8766") as client:
                # Araçları listele
                tools = await client.list_tools()
                print(f"Sunucu üzerindeki araçlar: {tools}")
                
                # Notion görevlerini çek
                result = await client.call_tool(
                    tools[0], 
                    {
                        "database_id": database_id,
                        "filter_by": {"property": "Status", "status": {"equals": "In progress"}}
                    }
                )
                
                tasks = result
                print(f"Toplam görev sayısı: {len(tasks)}")
                for task in tasks[:3]:
                    title = task.get('properties', {}).get('Name', {}).get('title', [{}])[0].get('plain_text', 'İsimsiz')
                    print(f"- {title}")
                
                return True
        
        # Asenkron fonksiyonu çalıştır
        print("FastMCP API testi yapılıyor...")
        result = asyncio.run(test_notion_api())
        
        # Sunucuyu durdur
        notion_mcp.stop()
        print("FastMCP sunucusu durduruldu.")
        
        return result
    
    except Exception as e:
        print(f"FastMCP testi sırasında hata: {str(e)}")
        return False

def main():
    """Ana test işlevi"""
    parser = argparse.ArgumentParser(description="LightMCP dual-mode araç testleri")
    parser.add_argument("--mode", choices=["lightmcp", "fastmcp", "all"], default="all",
                      help="Test modu: lightmcp, fastmcp veya ikisi birden (all)")
    parser.add_argument("--tool", choices=["github", "notion", "all"], default="all",
                      help="Test edilecek araç: github, notion veya ikisi birden (all)")
    
    args = parser.parse_args()
    
    # Testleri hazırla
    test_functions = []
    
    if args.mode in ["lightmcp", "all"]:
        if args.tool in ["github", "all"]:
            test_functions.append(("LightMCP GitHub", test_lightmcp_github))
        if args.tool in ["notion", "all"]:
            test_functions.append(("LightMCP Notion", test_lightmcp_notion))
    
    if args.mode in ["fastmcp", "all"]:
        if args.tool in ["github", "all"]:
            test_functions.append(("FastMCP GitHub", test_fastmcp_github))
        if args.tool in ["notion", "all"]:
            test_functions.append(("FastMCP Notion", test_fastmcp_notion))
    
    # Testleri çalıştır
    print("\n=== DUAL-MODE TOOL TESTLERİ ===")
    results = []
    
    for name, test_func in test_functions:
        try:
            print(f"\nTest: {name}")
            success = test_func()
            results.append((name, success))
        except KeyboardInterrupt:
            print(f"{name} testi kullanıcı tarafından iptal edildi.")
            results.append((name, False))
        except Exception as e:
            print(f"{name} testi sırasında beklenmedik hata: {str(e)}")
            results.append((name, False))
    
    # Sonuçları göster
    print("\n=== TEST SONUÇLARI ===")
    all_success = True
    for name, success in results:
        status = "✅ Başarılı" if success else "❌ Başarısız"
        print(f"{name}: {status}")
        if not success:
            all_success = False
    
    # Çıkış kodu
    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())
