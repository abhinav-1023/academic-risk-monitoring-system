from utils.database import supabase

# -----------------------------------
# AUTHENTICATION FUNCTION
# -----------------------------------

def authenticate(

    username,

    password
):

    try:

        # -----------------------------------
        # FETCH USER
        # -----------------------------------

        response = supabase.table(
            "users"
        ).select("*").eq(
            "username",
            username
        ).eq(
            "password",
            password
        ).execute()

        users = response.data

        # -----------------------------------
        # CHECK USER
        # -----------------------------------

        if users:

            return users[0]["role"]

        else:

            return None

    except Exception as e:

        print("Authentication Error:", e)

        return None