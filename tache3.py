class DiscussionNode:
    def __init__(self, question, reponse=None):
        self.question = question
        self.reponse = reponse or {}  # Dictionnaire {réponse : DiscussionNode}

#arbre de questions
root = DiscussionNode(
    "Bonjour, je suis Pascally, votre assistant virtuel en informatique. Souhaitez-vous discuter d'informatique avec moi ?",
    {
        "oui": DiscussionNode(
            "Super ! Quel domaine de l'informatique vous intéresse particulièrement ?",
            {
                "Programmation": DiscussionNode(
                    "La programmation, c'est passionnant ! Êtes-vous intéressé par un langage spécifique ?",
                    {
                        "Python": DiscussionNode("Python est très populaire pour sa simplicité. Travaillez-vous sur des projets personnels ?"),
                        "JavaScript": DiscussionNode("JavaScript est incontournable pour le développement web. Développez-vous des applications web ?")
                    }
                ),
                "Data": DiscussionNode(
                    "Le domaine des données est en plein essor. Êtes-vous plus intéressé par la Data Science ou le Big Data ?"
                ),
                "Cybersécurité": DiscussionNode(
                    "La cybersécurité est essentielle. Êtes-vous intéressé par l'apprentissage des techniques de défense ou d'attaque ?"
                ),
                "Réseaux": DiscussionNode(
                    "Les réseaux sont la colonne vertébrale de l'internet. Cherchez-vous à comprendre le fonctionnement des réseaux ou à résoudre des problèmes spécifiques ?"
                ),
                "IA": DiscussionNode(
                    "L'intelligence artificielle transforme notre monde. Êtes-vous intéressé par l'apprentissage automatique ou par l'IA appliquée à des domaines spécifiques ?"
                )
            }
        ),
        "non": DiscussionNode(
            "Pas de problème. Avez-vous un autre sujet en tête sur lequel vous aimeriez discuter ?"
        )
    }
)

def search(node, sujet):
    if sujet.lower() in node.question.lower():
        return True
    for reponse, suivant in node.reponse.items():
        if search(suivant, sujet):
            return True
    return False

#tâche 4
class UserDiscussionState:
    def __init__(self):
        self.current_node = None  # L'état actuel de la discussion

    def update_state(self, new_node):
        self.current_node = new_node

