"""
Bu test, dual-mode yapısının hem doğrudan FastMCP hem de fallback ile çalıştığını kontrol eder.
"""
import os
import sys
import importlib.util
from pathlib import Path
from lightmcp import add
from lightmcp.tool_loader import ToolRegistry, MCPTool

# Test dosyalarının yolları
CURRENT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = CURRENT_DIR.parent

# Önce yeni araçları register et ve doğrudan kullan
def register_test_tools():
    """Test araçlarını registry'e kaydet"""
    registry = ToolRegistry()
    print("Mevcut araçlar:", registry.list_tools())
    
    # Yeni araçları ekle
    github_tool_path = str(CURRENT_DIR / "fastmcp_v2_example/github_tool.py")
    notion_tool_path = str(CURRENT_DIR / "fastmcp_v2_example/notion_tool.py")
    
    # LightMCP registry'sine ekleyelim (bu işe yaramayabilir direkt kurulu paket)
    registry.add_tool("github_tool", f"tests/fastmcp_v2_example/github_tool.py")
    registry.add_tool("notion_tool", f"tests/fastmcp_v2_example/notion_tool.py")
    print("Registry güncellendi. Yeni araçlar:", registry.list_tools())
    
    return github_tool_path, notion_tool_path

# Test başlamadan önce araçları register et
github_path, notion_path = register_test_tools()

def test_github_tool():
    """GitHub aracını test et"""
    # Önce token olduğundan emin ol
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN çevre değişkeni tanımlanmamış!")
        token = input("GitHub Token giriniz: ")
        os.environ["GITHUB_TOKEN"] = token
    
    # Aracı yükle
    print("\n=== GitHub Tool Testi ===")
    # Direkt MCPTool oluştur (registry'yi bypass et)
    tool = MCPTool("github_tool", github_path)
    print("Tool yüklendi:", tool)
    
    # Aracı çalıştır
    result = tool.call({
        "repo_owner": "gokborayilmaz", 
        "repo_name": "lightmcp1"
    })
    print("Sonuç:")
    for issue in result:
        print(f"- {issue.get('title', 'Başlık yok')} ({issue.get('number', '?')})")
    
    return True

def test_notion_tool():
    """Notion aracını test et"""
    # Önce token olduğundan emin ol
    token = os.getenv("NOTION_API_KEY")
    if not token:
        print("NOTION_API_KEY çevre değişkeni tanımlanmamış!")
        token = input("Notion API Key giriniz: ")
        os.environ["NOTION_API_KEY"] = token
    
    # Aracı yükle
    print("\n=== Notion Tool Testi ===")
    # Direkt MCPTool oluştur (registry'yi bypass et)
    tool = MCPTool("notion_tool", notion_path)
    print("Tool yüklendi:", tool)
    
    # Aracı çalıştır
    # Not: Notion veritabanı ID'si girilmeli
    database_id = input("Notion veritabanı ID'si giriniz: ")
    result = tool.call({
        "database_id": database_id,
        "filter_by": "In progress"
    })
    print("Sonuç:")
    for task in result:
        print(f"- {task.get('properties', {}).get('Name', {}).get('title', [{}])[0].get('plain_text', 'İsimsiz')}")
    
    return True

if __name__ == "__main__":
    print("=== Dual Mode Test ===")
    
    # Her bir aracı test et
    tests = [test_github_tool, test_notion_tool]
    success = []
    
    for test in tests:
        try:
            result = test()
            if result:
                success.append(test.__name__)
            print(f"{test.__name__}: {'✅ Başarılı' if result else '❌ Başarısız'}")
        except Exception as e:
            print(f"{test.__name__}: ❌ Hata - {str(e)}")
    
    print(f"\nSonuç: {len(success)}/{len(tests)} test başarılı")
    
    if len(success) != len(tests):
        sys.exit(1)
