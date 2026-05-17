from utils.database import supabase


def authenticate(username, password):

    response = supabase.table("users").select("*").eq(
        "username",
        username
    ).eq(
        "password",
        password
    ).execute()

    data = response.data

    if len(data) > 0:

        return data[0]["role"]

    return None