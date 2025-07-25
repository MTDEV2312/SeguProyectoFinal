from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from .auth import auth_required, get_current_user, create_supabase_client
from .admin import admin_required
import json

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Corporate Portal - Educational Phishing Demo")

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Crear cliente de Supabase
supabase: Client = create_supabase_client()

# Datos simulados
FAKE_COMPANY_NEWS = [
    {
        "title": "Nueva Política de Seguridad Implementada",
        "date": "2025-01-15",
        "content": "Se ha implementado una nueva política de seguridad que requiere cambio de contraseñas cada 90 días."
    },
    {
        "title": "Actualización del Sistema HR",
        "date": "2025-01-10",
        "content": "El sistema de recursos humanos estará en mantenimiento el próximo fin de semana."
    },
    {
        "title": "Bonificaciones Anuales Disponibles",
        "date": "2025-01-05",
        "content": "Las bonificaciones del año fiscal 2024 ya están disponibles para consulta en el portal."
    }
]

FAKE_DOCUMENTS = [
    {"name": "Manual del Empleado 2025", "type": "PDF", "size": "2.3 MB"},
    {"name": "Políticas de IT", "type": "DOC", "size": "1.8 MB"},
    {"name": "Procedimientos de Emergencia", "type": "PDF", "size": "956 KB"},
    {"name": "Código de Conducta", "type": "PDF", "size": "1.2 MB"},
    {"name": "Formularios de Vacaciones", "type": "XLS", "size": "234 KB"}
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página de inicio - redirige al login si no está autenticado"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de login"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    """Procesar login con Supabase Auth"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            # Crear respuesta de redirección
            redirect_response = RedirectResponse(url="/dashboard", status_code=302)
            # En una aplicación real, establecerías cookies seguras aquí
            redirect_response.set_cookie(key="access_token", value=response.session.access_token, httponly=True)
            return redirect_response
        else:
            return templates.TemplateResponse("login.html", {
                "request": request, 
                "error": "Credenciales inválidas"
            })
    except Exception as e:
        print(f"Error de login: {e}")
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Error al iniciar sesión. Verifique sus credenciales."
        })

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Página de registro"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, email: str = Form(...), password: str = Form(...), full_name: str = Form(...)):
    """Procesar registro con Supabase Auth"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name,
                    "role": "user",  # Rol por defecto
                    "department": "General"
                }
            }
        })
        
        if response.user:
            # Insertar datos adicionales del perfil en la tabla profiles
            profile_data = {
                "id": response.user.id,
                "email": email,
                "full_name": full_name,
                "role": "user",
                "department": "General",
                "created_at": "now()"
            }
            
            supabase.table("profiles").insert(profile_data).execute()
            
            return templates.TemplateResponse("login.html", {
                "request": request, 
                "success": "Cuenta creada exitosamente. Por favor, inicie sesión."
            })
        else:
            return templates.TemplateResponse("register.html", {
                "request": request, 
                "error": "Error al crear la cuenta"
            })
    except Exception as e:
        print(f"Error de registro: {e}")
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "error": "Error al crear la cuenta. El email podría ya estar en uso."
        })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user=Depends(auth_required)):
    """Dashboard principal del usuario"""
    # Obtener datos del perfil del usuario
    try:
        profile_response = supabase.table("profiles").select("*").eq("id", current_user.id).execute()
        profile = profile_response.data[0] if profile_response.data else None
        
        if not profile:
            # Crear perfil si no existe
            profile = {
                "id": current_user.id,
                "email": current_user.email,
                "full_name": current_user.user_metadata.get("full_name", "Usuario"),
                "role": "user",
                "department": "General"
            }
            supabase.table("profiles").insert(profile).execute()
    except Exception as e:
        print(f"Error obteniendo perfil: {e}")
        profile = {
            "email": current_user.email,
            "full_name": current_user.user_metadata.get("full_name", "Usuario"),
            "role": "user",
            "department": "General"
        }
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": profile,
        "news": FAKE_COMPANY_NEWS,
        "documents": FAKE_DOCUMENTS
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, current_user=Depends(admin_required)):
    """Panel de administración - solo para admins"""
    try:
        # Obtener lista de usuarios
        users_response = supabase.table("profiles").select("*").execute()
        users = users_response.data if users_response.data else []
        
        # Logs de actividad simulados
        activity_logs = [
            {"timestamp": "2025-01-20 14:30:22", "user": "juan.perez@company.com", "action": "Inicio de sesión exitoso"},
            {"timestamp": "2025-01-20 14:25:15", "user": "maria.garcia@company.com", "action": "Descarga de documento: Manual del Empleado"},
            {"timestamp": "2025-01-20 14:20:08", "user": "carlos.rodriguez@company.com", "action": "Cambio de contraseña"},
            {"timestamp": "2025-01-20 14:15:33", "user": "ana.martinez@company.com", "action": "Inicio de sesión exitoso"},
            {"timestamp": "2025-01-20 14:10:44", "user": "luis.torres@company.com", "action": "Intento de acceso denegado"}
        ]
        
        return templates.TemplateResponse("admin.html", {
            "request": request,
            "users": users,
            "activity_logs": activity_logs,
            "admin_user": current_user
        })
    except Exception as e:
        print(f"Error en panel admin: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/logout")
async def logout():
    """Cerrar sesión"""
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response

@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Página de recuperación de contraseña (simulada)"""
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@app.post("/forgot-password")
async def forgot_password(request: Request, email: str = Form(...)):
    """Procesar recuperación de contraseña (simulada)"""
    # En una demo real, no enviarías emails reales
    return templates.TemplateResponse("forgot_password.html", {
        "request": request,
        "success": "Si el email existe en nuestro sistema, recibirá instrucciones de recuperación. (SIMULADO - No se envía email real)"
    })

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 80))
    uvicorn.run(app, host="0.0.0.0", port=port)
