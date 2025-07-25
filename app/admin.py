from fastapi import Depends, HTTPException
from .auth import admin_required, create_supabase_client

def get_all_users():
    """Obtener todos los usuarios (solo para admins)"""
    supabase = create_supabase_client()
    try:
        response = supabase.table("profiles").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error obteniendo usuarios: {e}")
        return []

def simulate_user_action(action: str, user_email: str):
    """Simular acciones de administración (solo frontend, no efectos reales)"""
    # En una aplicación real de phishing, aquí registrarías las acciones
    # Para propósitos educativos, solo simulamos
    print(f"SIMULACIÓN - Acción: {action} para usuario: {user_email}")
    return {"status": "success", "message": f"Acción '{action}' simulada para {user_email}"}

def get_activity_logs():
    """Obtener logs de actividad simulados"""
    # En una aplicación real, estos vendrían de la base de datos
    return [
        {"timestamp": "2025-01-20 15:45:12", "user": "admin@company.com", "action": "Acceso al panel de administración"},
        {"timestamp": "2025-01-20 15:30:22", "user": "juan.perez@company.com", "action": "Inicio de sesión exitoso"},
        {"timestamp": "2025-01-20 15:25:15", "user": "maria.garcia@company.com", "action": "Descarga de documento: Políticas de IT"},
        {"timestamp": "2025-01-20 15:20:08", "user": "carlos.rodriguez@company.com", "action": "Cambio de contraseña"},
        {"timestamp": "2025-01-20 15:15:33", "user": "ana.martinez@company.com", "action": "Inicio de sesión exitoso"},
        {"timestamp": "2025-01-20 15:10:44", "user": "luis.torres@company.com", "action": "Intento de acceso fallido - credenciales incorrectas"},
        {"timestamp": "2025-01-20 15:05:17", "user": "pedro.sanchez@company.com", "action": "Solicitud de recuperación de contraseña"},
        {"timestamp": "2025-01-20 15:00:33", "user": "sofia.lopez@company.com", "action": "Descarga de documento: Manual del Empleado"}
    ]
