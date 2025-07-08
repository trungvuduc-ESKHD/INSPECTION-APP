
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_supabase_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase: Client = init_supabase_connection()

def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data
def save_users(users):
    for user in users:
        supabase.table("users").insert(user).execute()
