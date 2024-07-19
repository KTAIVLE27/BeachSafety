def mask_user_data(user):
    user_name = user.user_name
    if len(user_name) > 2:
        user_name = user_name[0] + '*' * (len(user_name) - 2) + user_name[-1]

    user_phone = user.user_phone
    # Assuming phone number format is 010-1234-5678
    if len(user_phone) == 11:  # e.g., 01012345678
        user_phone = user_phone[:3] + '****' + user_phone[7:]
    elif len(user_phone) == 13 and '-' in user_phone:  # e.g., 010-1234-5678
        parts = user_phone.split('-')
        if len(parts) == 3:
            user_phone = parts[0] + '-' + '****' + '-' + parts[2]

    user_email = user.user_email
    email_parts = user_email.split('@')
    email_local = email_parts[0]
    if len(email_local) > 3:
        email_local = email_local[:3] + '*' * (len(email_local) - 3)
    user_email = email_local + '@' + email_parts[1]

    return {
        'user_no': user.user_no,
        'user_name': user_name,
        'user_role': user.user_role,
        'user_phone': user_phone,
        'user_email': user_email,
        'user_joinday': user.user_joinday,
        'last_login': user.last_login,
    }
