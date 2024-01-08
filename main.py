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
        await ctx.send(f"Historique des commandes :\n{historiq}")
    else:
        await ctx.send("L'historique est vide.")
    enregistrer_commande(ctx)
@client.command(name="next")
async def next_command(ctx):
     user_id = str(ctx.author.id)
     next_command=command_history.next_command(user_id)
     enregistrer_commande(ctx)
     if next_command:
         await ctx.send(f"Commande suivante : {next_command}")
     else:
         await ctx.send("Vous êtes à la fin de l'historique.")

@client.command(name="prev")
async def prev_command(ctx):
    user_id = str(ctx.author.id)
    prev_command=command_history.prev_command(user_id)
    enregistrer_commande(ctx)
    if prev_command:
        await ctx.send(f"Commande précédente : {prev_command}")
    else:
        await ctx.send("Vous êtes au début de l'historique.")
 #vider l'historique
@client.command(name="vider_historique")
async def vider_historique(ctx):
    command_history.clear_history()
    enregistrer_commande(ctx)
    await ctx.send("L'historique a été vidé.")
@client.command(name="derniere_commande")
async def derniere_commande(ctx):
    # execution de la commande
    last_command = command_history.get_last()
    enregistrer_commande(ctx)
    # reponse
    if last_command is not None:
        await ctx.send(f"La dernière commande était : {last_command}")
    else:
        await ctx.send("Aucune commande enregistrée.")
@client.command(name="commandes")
async def commandes_utilisateur(ctx, member: discord.Member):
    username = member.name
    commands = command_history.get_commands_by_user(username)
    enregistrer_commande(ctx)
    if commands:
        response = "\n".join(commands)
        await ctx.send(f"Commandes de {member.mention}:\n{response}")
    else:
        await ctx.send(f"Aucune commande trouvée pour {member.mention}.")
    enregistrer_commande(ctx)

#tâche 2

@client.command(name="acceder_historique")
async def request_history_access(ctx):
    user_id = ctx.author.id
    enregistrer_commande(ctx)
    if user_id != tache2.queue:
        tache2.queue.append(user_id)
        await ctx.send("Vous avez été ajouté à la file d'attente pour accéder à l'historique.")
    else:
        await ctx.send("Vous êtes déjà dans la file d'attente.")

@client.command(name="")
async def request_access_discord(ctx):
    user_id = ctx.author.id
    position = tache2.request_access(user_id)
    enregistrer_commande(ctx)
    if position != -1:
        await ctx.send(f"Votre position dans la file d'attente est {position}.")
    else:
        await ctx.send("Vous êtes déjà dans la file d'attente.")

@client.command(name="liberer_historique")
async def release_access_discord(ctx):
    user_id = ctx.author.id
    enregistrer_commande(ctx)
    if tache2.release_access(user_id):
        await ctx.send("Vous avez libéré l'accès à l'historique.")
        next_user_id = tache2.get_next_user()
        if next_user_id:
            await ctx.send(f"<@{next_user_id}> peut maintenant accéder à l'historique.")
    else:
        await ctx.send("Vous ne pouvez pas libérer l'accès en ce moment.")

#tache 3

@client.command(name="start_discussion")
async def start_discussion(ctx):
    user_id = ctx.author.id
    enregistrer_commande(ctx)
    discussion_node[user_id] = tache3.root
    await ctx.send(discussion_node[user_id].question)

@client.command(name="answer")
async def answer(ctx, *, reponse):
    user_id = ctx.author.id
    enregistrer_commande(ctx)
    if user_id in discussion_node:
        node_actuel = discussion_node[user_id]
        reponse = reponse.lower()  # Convertir la réponse en minuscules

        # Recherche de la réponse correspondante (également en minuscules)
        reponse_trouvee = next((r for r in node_actuel.reponse if r.lower() == reponse), None)

        if reponse_trouvee:
            discussion_node[user_id] = node_actuel.reponse[reponse_trouvee]
            await ctx.send(discussion_node[user_id].question)
        else:
            await ctx.send("Je ne comprends pas cette réponse. Veuillez choisir une option valide.")
    else:
        await ctx.send("Veuillez d'abord démarrer la discussion avec !start_discussion.")

@client.command(name="reset")
async def reset(ctx):
    user_id = ctx.author.id
    enregistrer_commande(ctx)
    discussion_node[user_id] = tache3.root  # Réinitialiser le nœud de discussion à la racine
    await ctx.send("La discussion a été réinitialisée. " + tache3.root.question)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Je ne connais pas cette commande. Veuillez rentrer une autre.")
        enregistrer_commande(ctx)

@client.command(name="speak_about")
async def speak_about(ctx, *, sujet):
    enregistrer_commande(ctx)
    if tache3.search(tache3.root, sujet):
        await ctx.send(f"Oui, je peux parler de {sujet}.")
    else:
        await ctx.send(f"Non, je ne traite pas le sujet de {sujet}.")


client.run(config.Token)
