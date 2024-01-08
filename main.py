import discord
import config
import tache1
import tache2
import tache3
from discord.ext import commands


intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    global command_history
    print("Le bot est prêt !")
    command_history = tache1.History.load_history('historique_commandes.json')
user_discussion_states = {}
# Création de l'instance de l'historique des commandes
discussion_node = {}

def enregistrer_commande(ctx):
    user = str(ctx.author)
    command_text = ctx.message.content
    timestamp = ctx.message.created_at
    command_history.append(user, command_text, timestamp)
    command_history.save_history('historique_commandes.json')
@client.command(name="Hello")
async def delete(ctx):
    messages = await ctx.channel.history(limit=150).flatten()
    await ctx.channel.delete_messages(messages)

# @client.event
# async def on_typing(channel, user, when):
#     await channel.send(user.name + " is typing")


@client.event
async def on_member_join(member):
    general_channel = client.get_channel()
    await general_channel.send("Bienvenue sur le serveur ! " + member.name)


@client.command(name="afficher_historique")
async def afficher_historique(ctx):
    user_id = ctx.author.id
    if tache2.is_user_in_queue_front(user_id):
        historiq = command_history.show_history()
        if historiq:
            await ctx.send(f"Historique des commandes :\n{historiq}")
        else:
            # Informez l'utilisateur que l'historique est vide
            await ctx.send("L'historique est actuellement vide.")
    else:
        await ctx.send("Vous n'êtes pas en tête de la liste d'attente pour accéder à l'historique.")
    enregistrer_commande(ctx)
@client.command(name="next")
async def next_command(ctx):
    user_id = str(ctx.author.id)
    if tache2.is_user_in_queue_front(user_id):
        next_command = command_history.next_command(user_id)
        if next_command:
            await ctx.send(f"Commande : {next_command}")
        else:
            await ctx.send("Vous êtes à la fin de l'historique.")
    else:
        await ctx.send("Vous devez être en tête de la file d'attente pour accéder à l'historique.")
    enregistrer_commande(ctx)


@client.command(name="prev")
async def prev_command(ctx):
    user_id = str(ctx.author.id)
    if tache2.is_user_in_queue_front(user_id):
        prev_command = command_history.prev_command(user_id)
        if prev_command:
            await ctx.send(f"Commande : {prev_command}")
        else:
            await ctx.send("Vous êtes au début de l'historique.")
    else:
        await ctx.send("Vous devez être en tête de la file d'attente pour accéder à l'historique.")
    enregistrer_commande(ctx)

 #vider l'historique
@client.command(name="vider_historique")
async def vider_historique(ctx):
    user_id = str(ctx.author.id)
    if tache2.is_user_in_queue_front(user_id):
        command_history.clear_history()
        await ctx.send("L'historique a été vidé.")
    else:
        await ctx.send("Vous devez être en tête de la file d'attente pour vider l'historique.")
    enregistrer_commande(ctx)

@client.command(name="derniere_commande")
async def derniere_commande(ctx):
    user_id = str(ctx.author.id)
    if tache2.is_user_in_queue_front(user_id):
        last_command = command_history.get_last()
        if last_command:
            await ctx.send(f"La dernière commande était : {last_command}")
        else:
            await ctx.send("Aucune commande enregistrée.")
    else:
        await ctx.send("Vous devez être en tête de la file d'attente pour voir la dernière commande.")
    enregistrer_commande(ctx)

@client.command(name="commandes")
async def commandes_utilisateur(ctx, member: discord.Member):
    user_id = str(ctx.author.id)
    if tache2.is_user_in_queue_front(user_id):
        username = member.name
        commands = command_history.get_commands_by_user(username)
        if commands:
            response = "\n".join(commands)
            await ctx.send(f"Commandes de {member.mention}:\n{response}")
        else:
            await ctx.send(f"Aucune commande trouvée pour {member.mention}.")
    else:
        await ctx.send("Vous devez être en tête de la file d'attente pour voir la dernière commande.")
    enregistrer_commande(ctx)


#tâche 2

@client.command(name="acceder_historique")
async def request_history_access(ctx):
    user_id = ctx.author.id
    if user_id != tache2.queue:
        tache2.queue.append(user_id)
        await ctx.send("Vous avez été ajouté à la file d'attente pour accéder à l'historique.")
    else:
        await ctx.send("Vous êtes déjà dans la file d'attente.")
    enregistrer_commande(ctx)
@client.command(name="position")
async def request_access_discord(ctx):
    user_id = ctx.author.id
    position = tache2.request_access(user_id)
    if position != -1:
        await ctx.send(f"Votre position dans la file d'attente est {position}.")
    else:
        await ctx.send("Vous êtes déjà dans la file d'attente.")
    enregistrer_commande(ctx)

@client.command(name="liberer_historique")
async def release_access_discord(ctx):
    user_id = ctx.author.id
    if tache2.release_access(user_id):
        await ctx.send("Vous avez libéré l'accès à l'historique.")
        next_user_id = tache2.get_next_user()
        if next_user_id:
            await ctx.send(f"<@{next_user_id}> peut maintenant accéder à l'historique.")
    else:
        await ctx.send("Vous ne pouvez pas libérer l'accès en ce moment.")
    enregistrer_commande(ctx)
#tache 3

@client.command(name="start_discussion")
async def start_discussion(ctx):
    user_id = ctx.author.id
    if user_id not in user_discussion_states:
        user_discussion_states[user_id] = UserDiscussionState()
    user_discussion_states[user_id].update_state(tache3.root)
    await ctx.send(tache3.root.question)
    enregistrer_commande(ctx)
@client.command(name="answer")
async def answer(ctx, *, reponse):
    user_id = ctx.author.id
    if user_id in user_discussion_states:
        current_state = user_discussion_states[user_id]
        node_actuel = current_state.current_node
        reponse_trouvee = node_actuel.reponse.get(reponse.lower(), None)
        if reponse_trouvee:
            user_discussion_states[user_id].update_state(reponse_trouvee)
            await ctx.send(reponse_trouvee.question)
        else:
            await ctx.send("Je ne comprends pas cette réponse. Veuillez choisir une option valide.")
    else:
        await ctx.send("Veuillez d'abord démarrer la discussion avec !start_discussion.")
    enregistrer_commande(ctx)

@client.command(name="reset")
async def reset(ctx):
    user_id = ctx.author.id
    if user_id in user_discussion_states:
        user_discussion_states[user_id].update_state(tache3.root)
    await ctx.send("La discussion a été réinitialisée. " + tache3.root.question)
    enregistrer_commande(ctx)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Je ne connais pas cette commande. Veuillez rentrer une autre.")
    enregistrer_commande(ctx)

@client.command(name="speak_about")
async def speak_about(ctx, *, sujet):
    if tache3.search(tache3.root, sujet):
        await ctx.send(f"Oui, je peux parler de {sujet}.")
    else:
        await ctx.send(f"Non, je ne traite pas le sujet de {sujet}.")
    enregistrer_commande(ctx)

#tâche 4
def update_discussion_state(user_id, new_node):
    if user_id not in user_discussion_states:
        user_discussion_states[user_id] = UserDiscussionState()
    user_discussion_states[user_id].update_state(new_node)

client.run(config.Token)
