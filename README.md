# Verificentro 🚗💨
## 📌 Reglas del Proyecto
Este proyecto es colaborativo y sigue ciertas reglas para mantener un código limpio, organizado y funcional para todos los desarrolladores.

---

## 🔄 Flujo de Trabajo con Git
- 1️⃣ Clonar el repositorio
    - Si aún no tienes el repositorio en tu máquina, clónalo con:
    ```sh
    git clone <URL_DEL_REPO>
    cd Verificentro
    ```
- 2️⃣ Crear una nueva rama
    - Siempre trabaja en una rama nueva basada en main o develop:

    ```sh
    git checkout develop  # Asegurar estar en la rama base
    git pull origin develop  # Asegurar estar actualizado
    git checkout -b feature/nombre-de-la-feature  # Crear nueva rama
    ```
- 3️⃣ Hacer commits
  - Haz commits pequeños y significativos siguiendo esta estructura:

    ### 📌 Estructura del mensaje del commit:

    ```xml
    <Tipo>: <Breve descripción>

    <Explicación opcional del cambio si es necesario>
    ```
    ### 📌 Tipos de commit recomendados:

    - feat: Nueva funcionalidad

    - fix: Corrección de errores

    - refactor: Reestructuración de código sin cambios en funcionalidad

    - docs: Cambios en documentación

    - style: Cambios de formato (espaciado, comas, etc.)

    - test: Agregar o modificar pruebas

    - chore: Mantenimiento o configuraciones

    ### Ejemplo de commit válido:

    ```sh
    git commit -m "feat: agregar validaciones en el módulo de citas"
    ```
- 4️⃣ Subir los cambios
  - Antes de hacer push, asegúrate de actualizar tu rama:

    ```sh
    git pull origin develop --rebase  # Traer cambios de develop y evitar conflictos
    git push origin "feature/nombre-de-la-feature" o "develop" o "nombre de la rama en la que estes trabajando"
    ```
    Cuando el código esté listo, crea un Pull Request (PR) en GitHub y espera la revisión de al menos un compañero antes de hacer merge.

## 📊 Reglas para la Base de Datos (PostgreSQL)
- 1️⃣ Nunca subas archivos de migración innecesarios

  - Si hiciste cambios en los modelos, ejecuta:

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

- 2️⃣ Si modificas la estructura de la BD:
  - Avisa en el grupo del equipo

  - Documenta los cambios en el archivo estructura_proyecto.txt

- 3️⃣ Si agregaste datos de prueba, usa fixtures:
  - Para exportar datos de prueba:

    ```sh
    python manage.py dumpdata app.modelo --indent 4 > fixtures/nombre.json
    ```
  - Para importar datos de prueba:

    ```sh
    python manage.py loaddata fixtures/nombre.json
    ```

## 🔍 Buenas Prácticas
- ✅ Mantén el código limpio y ordenado
- ✅ Usa nombres de variables y funciones descriptivos
- ✅ Documenta los cambios importantes
- ✅ Prueba tu código antes de subirlo

### 📌 Reglas de Formato:

- Usa 4 espacios para la indentación

- No dejes print() o código comentado sin razón

- Usa .gitignore para evitar subir archivos innecesarios

### 🛠️ Configuración del Entorno
- 1️⃣ Crea un entorno virtual y activa:

    ```sh
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate  # Windows
    ```
- 2️⃣ Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```
    Si agregaste dependencias escribelas en `requirements.txt`.
    
- 3️⃣ Configura la base de datos en settings.py:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'verificentro_db',
            'USER': 'usuario',
            'PASSWORD': 'contraseña',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
- 4️⃣ Ejecuta el servidor:
    ```sh
    python manage.py runserver
    ```

### 📢 Comunicación
    Usa GitHub Issues para reportar errores o solicitar nuevas funcionalidades

    Para dudas, utiliza el grupo de comunicación del equipo

## 🚀 ¡Feliz coding! 😃
