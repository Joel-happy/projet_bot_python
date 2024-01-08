queue = []

def request_access(user_id):
    if user_id not in queue:
        queue.append(user_id)
        return len(queue)  # Retourner la position dans la file
    return -1  # Indiquer que l'utilisateur est déjà dans la file

def release_access(user_id):
    if queue and queue[0] == user_id:
        queue.pop(0)
        return True
    return False

def is_user_in_queue_front(user_id):
    return queue and queue[0] == user_id
def get_next_user():
    return queue[0] if queue else None
