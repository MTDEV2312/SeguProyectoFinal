# 🎯 Portal Corporativo Simulado - Demo Educativo de Phishing

> **⚠️ IMPORTANTE: Esta aplicación es únicamente para propósitos educativos en ciberseguridad. NO debe ser utilizada para actividades maliciosas.**

## 📋 Descripción

Esta es una aplicación web simulada que replica un portal corporativo típico, diseñada específicamente para:
- Educación en ciberseguridad
- Demostraciones de phishing en entornos controlados
- Entrenamiento de concientización sobre seguridad
- Investigación académica en seguridad informática

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5 + Bootstrap 5 + Jinja2 Templates
- **Autenticación**: Supabase Auth
- **Base de Datos**: PostgreSQL (Supabase)
- **Contenedores**: Docker + Docker Compose
- **Estilos**: Bootstrap 5 + CSS personalizado

## 🏗️ Estructura del Proyecto

```
phishing-portal/
├── app/
│   ├── main.py              # Aplicación principal FastAPI
│   ├── auth.py              # Manejo de autenticación
│   ├── admin.py             # Funciones administrativas
│   ├── templates/           # Plantillas HTML
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── admin.html
│   │   └── forgot_password.html
│   └── static/
│       └── style.css        # Estilos personalizados
├── requirements.txt         # Dependencias Python
├── Dockerfile              # Configuración Docker
├── docker-compose.yml      # Orquestación de contenedores
├── .env                    # Variables de entorno
└── README.md              # Este archivo
```

## 🗄️ Configuración de Base de Datos (Supabase)

### Crear las siguientes tablas en Supabase:

#### 1. Tabla `profiles` (Perfiles de usuario)
```sql
CREATE TABLE profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    department TEXT DEFAULT 'General',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (id)
);

-- Habilitar RLS (Row Level Security)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Política para que los usuarios puedan ver y editar su propio perfil
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Política para que los admins puedan ver todos los perfiles
CREATE POLICY "Admins can view all profiles" ON profiles
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() AND role = 'admin'
        )
    );
```

#### 2. Tabla `activity_logs` (Logs de actividad)
```sql
CREATE TABLE activity_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    user_email TEXT NOT NULL,
    action TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Habilitar RLS
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;

-- Política para que solo los admins puedan ver los logs
CREATE POLICY "Admins can view activity logs" ON activity_logs
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles 
            WHERE id = auth.uid() AND role = 'admin'
        )
    );
```

#### 3. Función para actualizar updated_at automáticamente
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_profiles_updated_at 
    BEFORE UPDATE ON profiles 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Docker y Docker Compose instalados
- Cuenta en Supabase (gratis)
- Git (para clonar el repositorio)

### Pasos de Instalación

#### 1. Configurar Supabase
```bash
# 1. Crear proyecto en https://supabase.com
# 2. Obtener URL y API Key del proyecto
# 3. Ejecutar los scripts SQL mostrados arriba en el SQL Editor de Supabase
```

#### 2. Configurar Variables de Entorno
```bash
# El archivo .env ya está incluido con las credenciales
# Asegúrate de que contiene:
PUBLIC_SUPABASE_URL=https://vgnlkwhnkkcvdpbosucs.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 3. Ejecutar con Docker
```bash
# Construir y ejecutar
docker-compose up --build

# Para ejecutar en segundo plano
docker-compose up -d --build
```

#### 4. Acceder a la Aplicación
- Abrir navegador en: `http://localhost`
- Crear una cuenta nueva o usar credenciales existentes

## 👥 Funcionalidades

### 🔐 Autenticación
- **Registro de usuarios** con email y contraseña
- **Login seguro** mediante Supabase Auth
- **Recuperación de contraseña** (simulada)
- **Dos roles**: `user` y `admin`

### 👤 Dashboard de Usuario
- **Perfil personal** con información simulada
- **Noticias corporativas** (contenido de prueba)
- **Documentos internos** (enlaces simulados)
- **Accesos rápidos** a funciones corporativas

### 🛡️ Panel de Administración
- **Gestión de usuarios** (visualización únicamente)
- **Estadísticas del sistema**
- **Logs de actividad** (datos simulados)
- **Controles administrativos** (solo interfaz)

## 🎯 Propósito Educativo

### Casos de Uso Legítimos:
- **Entrenamientos de seguridad** en empresas
- **Cursos universitarios** de ciberseguridad
- **Simulacros de phishing** controlados
- **Investigación académica** en seguridad

### Características de Seguridad:
- **Banner de advertencia** visible
- **Datos simulados** únicamente
- **Sin recolección** de información real
- **Ambiente controlado** para aprendizaje

## 🔧 Desarrollo

### Ejecutar en Modo Desarrollo
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Agregar Usuario Administrador
```sql
-- En Supabase SQL Editor, después de registrar un usuario:
UPDATE profiles 
SET role = 'admin' 
WHERE email = 'tu-email@ejemplo.com';
```

## 📊 Métricas y Logs

La aplicación registra (de forma simulada):
- Intentos de login
- Accesos a documentos
- Acciones administrativas
- Actividad general del usuario

**Importante**: Todos los logs son simulados y no se almacenan datos reales.

## ⚠️ Disclaimers Legales

### ❌ Prohibido:
- Usar para phishing real
- Desplegar públicamente sin supervisión
- Recopilar datos personales reales
- Actividades maliciosas de cualquier tipo

### ✅ Permitido:
- Educación en ciberseguridad
- Entrenamientos corporativos autorizados
- Investigación académica supervisada
- Demostraciones en entornos controlados

## 🤝 Contribuciones

Las contribuciones son bienvenidas, especialmente para:
- Mejorar el realismo de la interfaz
- Agregar más funciones educativas
- Mejorar la documentación
- Corregir bugs de seguridad

## 📝 Licencia

Este proyecto está bajo licencia MIT para propósitos educativos únicamente.

## 📞 Soporte

Para preguntas educativas o problemas técnicos:
- Crear un issue en el repositorio
- Contactar al mantenedor del proyecto

---

**🎓 Recuerda: El conocimiento en ciberseguridad debe usarse para proteger, no para atacar.**
# SeguProyectoFinal
