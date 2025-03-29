from crewai_tools import DirectorySearchTool
import inspect

def show_directory_search_attributes():
    # Créer une instance de DirectorySearchTool
    tool = DirectorySearchTool(directory=".")
    
    # Obtenir tous les attributs et méthodes
    attributes = inspect.getmembers(tool)
    
    print("\n=== Attributs de DirectorySearchTool ===\n")
    
    for name, value in attributes:
        # Ignorer les attributs privés (commençant par _)
        if not name.startswith('_'):
            print(f"{name}: {value}")

if __name__ == "__main__":
    show_directory_search_attributes() 