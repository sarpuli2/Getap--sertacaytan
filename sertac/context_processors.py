# sertac/context_processors.py

def user_info(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    user_surname = request.session.get('user_surname')
    
    return {
        'user_id': user_id,
        'user_name': user_name,
        'user_surname': user_surname,
    }
