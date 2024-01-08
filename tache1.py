from datetime import datetime
import json
class Command:#commandes
    def __init__(self, user, command, timestamp):
        self.user = user
        self.command = command
        self.formatted_timestamp = timestamp if isinstance(timestamp, str) else self.format_date(timestamp)
        self.next_node = None
        self.previous_node = None
        self.histories = {}
    def format_date(self,timestamp):
        return timestamp.strftime("%d/%m/%Y %H:%M:%S")
class History:#historique
    def __init__(self):
        self.first_node = None
        self.current_node = None
        self.size = 0
        self.user_pointers = {}
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



    def next_command(self, user_id):
        # Assurez-vous que l'utilisateur est dans le dictionnaire
        if user_id not in self.user_pointers:
            self.user_pointers[user_id] = self.first_node

        # Obtenez le pointeur actuel pour cet utilisateur
        current_node = self.user_pointers[user_id]

        # Vérifiez s'il y a une commande suivante
        if current_node and current_node.next_node:
            self.user_pointers[user_id] = current_node.next_node
            return current_node.next_node.command
        return None

    def prev_command(self, user_id):
        # Vérifiez si l'utilisateur a déjà un pointeur, sinon initialisez-le
        if user_id not in self.user_pointers:
            self.user_pointers[user_id] = self.first_node

        current_node = self.user_pointers[user_id]

        # Vérifiez s'il y a une commande précédente
        if current_node and current_node.previous_node:
            self.user_pointers[user_id] = current_node.previous_node
            return current_node.previous_node.command
        return None
    def show_history(self):
        if self.current_node == None:
            return "Aucune commande enregistrée."
        return f"Commande actuelle : {self.current_node.command}"

    # pour effacer l'historique
    def clear_history(self):
        self.first_node = None

    # pour avoir la dernière commande
    def get_last(self):
        if self.first_node  == None:
            return None  # Retourne None si la liste est vide

        current_node = self.first_node
        while current_node.next_node  != None:
            current_node = current_node.next_node
        last_command_info = f"{current_node.command}  rentrée par: @{current_node.user}  "
        return last_command_info

    #avoir la dernière commande d'un utilisateur
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
    #Tâche 5
    #où se déroule la sauvegarde de l'historique
    def save_history(self, filepath):
        history_to_save = []
        current_node = self.first_node
        while current_node:
            history_to_save.append({
                'user': current_node.user,
                'command': current_node.command,
                'formatted_timestamp': current_node.formatted_timestamp
            })
            current_node = current_node.next_node

        with open(filepath, 'w') as file:
            json.dump(history_to_save, file)

    #le chargement de l'historique
    @staticmethod
    def load_history(filepath):
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                if not data:  # Si le fichier est vide ou le contenu n'est pas valide
                    return History()
                history_instance = History()
                for item in data:
                    timestamp = datetime.strptime(item['formatted_timestamp'],"%d/%m/%Y %H:%M:%S")
                    history_instance.append(item['user'], item['command'], timestamp)
                    history_instance.current_node = history_instance.first_node
                return history_instance
        except FileNotFoundError:
            return History()  # Retourne une instance vide si le fichier n'existe pas