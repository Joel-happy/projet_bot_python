from datetime import datetime
class Command:#commandes
    def __init__(self, user, command, timestamp):
        self.user = user
        self.command = command
        self.formatted_timestamp = self.format_date(timestamp)
        self.next_node = None
        self.previous_node = None

    def format_date(self,timestamp):
        return timestamp.strftime("%d/%m/%Y %H:%M:%S")
class History:#historique
    def __init__(self):
        self.first_node = None
        self.current_node = None
        self.size = 0
    def append(self, user,command,formatted_timestamp):
        new_command=Command(user,command,formatted_timestamp)
        #Implémentation de l'ajout d'un élément
        if self.first_node == None:
            self.first_node = new_command
            return
        self.size += 1
        current_node = self.first_node
        while current_node.next_node != None:
            current_node = current_node.next_node
        current_node.next_node = new_command
        new_command.previous_node=current_node
        self.current_node=new_command


    def next_command(self):
        if self.current_node and self.current_node.next_node:
            self.current_node = self.current_node.next_node
            return self.current_node.command
        return None

    def prev_command(self):
        if self.current_node and self.current_node.previous_node:
            self.current_node = self.current_node.previous_node
            return self.current_node.command
        return None
    def show_history(self):
        if self.current_node == None:
            return "Aucune commande enregistrée."
        return f"Commande actuelle : {self.current_node.command}"

    # pour effacer l'historique
    def clear_history(self):
        self.first_node = None

    def get_last(self):
        if self.first_node  == None:
            return None  # Retourne None si la liste est vide

        current_node = self.first_node
        while current_node.next_node  != None:
            current_node = current_node.next_node
        last_command_info = f"{current_node.command}  rentrée par: @{current_node.user}  "
        return last_command_info

    def get_commands_by_user(self, username):
        print(f"Recherche des commandes pour : {username}")
        current_node = self.first_node
        user_commands = []
        while current_node != None:
            if current_node.user == username:
                # Vous pouvez formater la sortie comme vous le souhaitez ici
                command_info = f"{current_node.formatted_timestamp} - {current_node.command}"
                user_commands.append(command_info)
            current_node = current_node.next_node
        return user_commands

# La ligne `self.size += 1` n'est pas nécessaire si vous n'avez pas de variable `size`
            # Si vous souhaitez garder une trace de la taille, assurez-vous d'ajouter une variable `size` dans __init__ et décommentez cette ligne.
            # self.size += 1