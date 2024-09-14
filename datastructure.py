import json
import os

# Correct file path using raw string or double backslashes
FILE_PATH = r"C:\miracle intern\To-Do List Application with Data Structures\cricket_players.json"

# Helper function to read data from JSON file
def read_json_file():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Helper function to write data to JSON file
def write_json_file(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)


# Node class for Cricket Player Linked List
class PlayerNode:
    def __init__(self, player_id, player_name, player_country, player_role, player_team):
        self.player_id = player_id
        self.player_name = player_name
        self.player_country = player_country
        self.player_role = player_role
        self.player_team = player_team
        self.next = None

# Linked List class to manage players
class PlayerLinkedList:
    def __init__(self):
        self.head = None

    # Add a player to the linked list and JSON file
    def add_player(self, player_id, player_name, player_country, player_role, player_team):
        new_node = PlayerNode(player_id, player_name, player_country, player_role, player_team)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        print(f"Player added: {player_name}")

    # Get all players in list format
    def get_players(self):
        current = self.head
        players = []
        while current:
            player = {
                "Player ID": current.player_id,
                "Name": current.player_name,
                "Country": current.player_country,
                "Role": current.player_role,
                "Team": current.player_team
            }
            players.append(player)
            current = current.next
        return players

    # Edit a player
    def edit_player(self, player_id, new_name, new_country, new_role, new_team):
        current = self.head
        while current:
            if current.player_id == player_id:
                current.player_name = new_name
                current.player_country = new_country
                current.player_role = new_role
                current.player_team = new_team
                print(f"Player {player_id} updated.")
                return
            current = current.next
        print(f"Player ID {player_id} not found.")

    # Delete a player
    def delete_player(self, player_id):
        current = self.head
        prev = None
        while current:
            if current.player_id == player_id:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                print(f"Player {player_id} deleted.")
                return current
            prev = current
            current = current.next
        print(f"Player ID {player_id} not found.")
        return None

# Stack for Undo Feature
class UndoStack:
    def __init__(self):
        self.stack = []

    def push(self, action):
        self.stack.append(action)

    def pop(self):
        if not self.stack:
            print("No actions to undo.")
            return None
        return self.stack.pop()

# Hash Table for Search (using a dictionary)
class PlayerHashTable:
    def __init__(self):
        self.table = {}

    def add_player(self, player_id, player_name):
        self.table[player_id] = player_name

    def search_player(self, keyword):
        results = {player_id: name for player_id, name in self.table.items() if keyword.lower() in name.lower()}
        if results:
            for player_id, name in results.items():
                print(f"Player ID: {player_id}, Name: {name}")
        else:
            print(f"No players found with keyword '{keyword}'")

# Main Application for managing cricket players
class CricketApp:
    def __init__(self):
        self.player_list = PlayerLinkedList()
        self.undo_stack = UndoStack()
        self.player_table = PlayerHashTable()
        self.player_counter = 1
        self.load_from_file()

    # Load players from JSON file into the linked list
    def load_from_file(self):
        players_data = read_json_file()
        for player in players_data:
            self.player_list.add_player(
                player['Player ID'], player['Name'], player['Country'], player['Role'], player['Team'])
            self.player_table.add_player(player['Player ID'], player['Name'])
        self.player_counter = len(players_data) + 1

    # Save the linked list data into the JSON file
    def save_to_file(self):
        players_data = self.player_list.get_players()
        write_json_file(players_data)

    # Add a player
    def add_player(self, player_name, player_country, player_role, player_team):
        player_id = self.player_counter
        self.player_list.add_player(player_id, player_name, player_country, player_role, player_team)
        self.player_table.add_player(player_id, player_name)
        self.undo_stack.push(('add', player_id))
        self.player_counter += 1
        self.save_to_file()

    # Edit a player
    def edit_player(self, player_id, new_name, new_country, new_role, new_team):
        old_player = self.player_table.table.get(player_id)
        if old_player:
            self.player_list.edit_player(player_id, new_name, new_country, new_role, new_team)
            self.player_table.add_player(player_id, new_name)
            self.undo_stack.push(('edit', player_id, old_player))
            self.save_to_file()

    # Delete a player
    def delete_player(self, player_id):
        deleted_player = self.player_list.delete_player(player_id)
        if deleted_player:
            self.player_table.table.pop(player_id, None)
            self.undo_stack.push(('delete', player_id, deleted_player.player_name))
            self.save_to_file()

    # Undo last action
    def undo(self):
        last_action = self.undo_stack.pop()
        if last_action:
            action_type, player_id, *player_name = last_action
            if action_type == 'add':
                self.player_list.delete_player(player_id)
                self.player_table.table.pop(player_id, None)
            elif action_type == 'edit':
                self.player_list.edit_player(player_id, player_name[0], '', '', '')
                self.player_table.add_player(player_id, player_name[0])
            elif action_type == 'delete':
                self.player_list.add_player(player_id, player_name[0], '', '', '')
                self.player_table.add_player(player_id, player_name[0])
            self.save_to_file()

    # Search for players by keyword
    def search_players(self, keyword):
        self.player_table.search_player(keyword)

# Sample usage
if __name__ == "__main__":
    app = CricketApp()

    while True:
        print("\n1. Add Player")
        print("2. Display Players")
        print("3. Edit Player")
        print("4. Delete Player")
        print("5. Undo Last Action")
        print("6. Search Player")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter player name: ")
            country = input("Enter player country: ")
            role = input("Enter player role: ")
            team = input("Enter player team: ")
            app.add_player(name, country, role, team)

        elif choice == '2':
            print(json.dumps(read_json_file(), indent=4))

        elif choice == '3':
            player_id = int(input("Enter player ID to edit: "))
            new_name = input("Enter new player name: ")
            new_country = input("Enter new country: ")
            new_role = input("Enter new role: ")
            new_team = input("Enter new team: ")
            app.edit_player(player_id, new_name, new_country, new_role, new_team)

        elif choice == '4':
            player_id = int(input("Enter player ID to delete: "))
            app.delete_player(player_id)

        elif choice == '5':
            app.undo()

        elif choice == '6':
            keyword = input("Enter search keyword: ")
            app.search_players(keyword)

        elif choice == '7':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
