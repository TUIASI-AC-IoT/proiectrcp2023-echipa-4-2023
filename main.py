from server import Server
from gui_manager import GUIManager

if __name__ == '__main__':
    server = Server()
    gui_manager = GUIManager(server)
    server.run()
    gui_manager.run()
