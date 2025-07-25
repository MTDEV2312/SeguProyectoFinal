from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

security = HTTPBearer(auto_error=False)

def create_supabase_client() -> Client:
    """Crear cliente de Supabase"""
    url = os.getenv("PUBLIC_SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        raise ValueError("Las variables de entorno de Supabase no están configuradas")
    
    return create_client(url, key)

def get_current_user(request: Request):
    """Obtener usuario actual desde la cookie/token"""
    supabase = create_supabase_client()
    
    # Intentar obtener token de la cookie
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        return None
    
    try:
        # Verificar token con Supabase
        response = supabase.auth.get_user(access_token)
        return response.user if response.user else None
    except Exception as e:
        print(f"Error verificando token: {e}")
        return None

def auth_required(request: Request):
    """Dependency para rutas que requieren autenticación"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")
    return user

def admin_required(request: Request):
    """Dependency para rutas que requieren permisos de admin"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    # Verificar si el usuario es admin
    supabase = create_supabase_client()
    try:
        profile_response = supabase.table("profiles").select("role").eq("id", user.id).execute()
        if profile_response.data and profile_response.data[0].get("role") == "admin":
            return user
        else:
            raise HTTPException(status_code=403, detail="Permisos de administrador requeridos")
    except Exception as e:
        print(f"Error verificando permisos de admin: {e}")
        raise HTTPException(status_code=403, detail="Error verificando permisos")
