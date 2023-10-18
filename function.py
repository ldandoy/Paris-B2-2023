def valid_login(username, password):
    # bcrypt.check_password_hash(pw_hash, 'hunter2')
    if username == "admin" and password == "admin":
        return True
    else:
        return False
