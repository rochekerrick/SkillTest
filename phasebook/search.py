from flask import Blueprint, request, jsonify

from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return jsonify(search_users(request.args)), 200

def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters, sorted by priority
    """
    if not args:
        return USERS

    # Calculate priority score for each user based on how they were matched
    matched_users_with_priority = []

    # Sorting procedure (1:id, 2:name, 3:age, 4:occupation)
    for user in USERS:
        priority_score = 0

        if 'id' in args and user.get('id') == args['id']:
            priority_score += 4
        if 'name' in args and args['name'].lower() in user.get('name', '').lower():
            priority_score += 3
        if 'age' in args and abs(int(args['age']) - user.get('age', 0)) <= 1:
            priority_score += 2
        if 'occupation' in args and args['occupation'].lower() in user.get('occupation', '').lower():
            priority_score += 1

        matched_users_with_priority.append((user, priority_score))

    # Sort matched users based on priority score
    sorted_users = sorted(matched_users_with_priority, key=lambda x: x[1], reverse=True)

    # Convert sorted users back to a list of dictionaries
    return [dict(user[0]) for user in sorted_users]
