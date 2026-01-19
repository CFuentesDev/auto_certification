# Auto Verificación y Certificación

**Nombre Técnico**: `auto_certification`  
**Versión**: 0.1  
**Autor**: Carlos Fuentes (CFuentes.Dev)  
**Licencia**: LGPL-3

## Resumen

El módulo `auto_certification` mejora los módulos de eLearning y Encuestas de Odoo introduciendo un flujo de **Certificación Automática**. Permite a los participantes de un curso recibir una certificación automáticamente al completar todas las diapositivas requeridas, sin necesidad de aprobar una encuesta tipo examen tradicional.

Esto es ideal para cursos de tipo "Lectura y Confirmación" donde el requisito es simplemente consumir todo el contenido.

## Características Principales

1.  **Mecanismo de Evaluación Auto-Aprobada**: Introduce un nuevo tipo de puntuación "Aprobación Automática" en las Encuestas.
2.  **Generación Automática de Token y Completado**: Cuando un usuario termina la última diapositiva requerida, el sistema automáticamente:
    - Crea un registro exitoso en `survey.user_input` con un token de acceso válido.
    - Marca la diapositiva de certificación como "Completada".
    - Otorga la certificación al contacto (partner).
3.  **Validación Inteligente**:
    - **Al Cargar la Página**: Verifica el estado de completado cuando el usuario visita la página del curso.
    - **Al Completar Diapositiva**: Dispara verificaciones cada vez que una diapositiva se marca como completada.
4.  **Integración Backend y Frontend**: Compatible con las vistas estándar de eLearning de Odoo.

## Configuración y Uso

### 1. Crear la Certificación (Encuesta)
1.  Vaya a **Encuestas**.
2.  Cree una nueva Encuesta.
3.  En la pestaña **Opciones**, bajo **Puntuación**, seleccione **Aprobación Automática**.
    *   *Nota: Las opciones estándar incluyen 'Puntuación con respuestas', 'Puntuación sin respuestas', etc. Este módulo agrega 'Aprobación Automática'.*

### 2. Vincular a un Curso de eLearning
1.  Vaya a **eLearning** y seleccione o cree un Curso.
2.  Añada un nuevo Contenido.
3.  Establezca el **Tipo** como **Certificación**.
4.  Seleccione la **Certificación** (Encuesta) que creó en el paso 1.

### 3. Experiencia del Usuario
- El usuario navega a través de las diapositivas del curso.
- A medida que completa las diapositivas, el sistema rastrea el progreso.
- Al finalizar el último contenido requerido (aparte de la certificación misma), la diapositiva de Certificación permanece pendiente.
- El usuario puede simplemente visitar la página principal del curso o la diapositiva de certificación, y el sistema detectará automáticamente que se cumplieron los requisitos.
- La Certificación se marca como **Hecho**, y el usuario puede descargar su certificado inmediatamente.

## Detalles Técnicos

### Dependencias
- `survey`
- `website_slides`
- `website_slides_survey`

### Modelos Extendidos

#### `slide.channel`
- **Método `_check_and_generate_auto_certification(slide, partner)`**:
    - Lógica central del módulo.
    - Verifica si todas las *otras* diapositivas publicadas en el canal están completas.
    - Si es así, crea automáticamente un `survey.user_input` con `scoring_success=True` y actualiza `slide.slide.partner`.

#### `survey.survey`
- Añade la opción `auto_pass` al campo de selección `scoring_type`.

#### `slide.slide`
- **Campo `is_auto_pass_certification`**: Campo computado booleano que devuelve `True` si la encuesta vinculada tiene `scoring_type='auto_pass'`. Se usa para identificar rápidamente diapositivas de auto-certificación en búsquedas filtradas.

#### `slide.slide.partner`
- Extiende los métodos `write` y `create` para disparar `_check_and_generate_auto_certification` en el canal padre cada vez que cualquier diapositiva se marca como completada.

### Controladores
- **`WebsiteSlidesCustom`**:
    - Sobreescribe la ruta `/slides/<channel>`.
    - Realiza una verificación automática cuando el usuario visita la página de inicio del curso para asegurar que si terminaron la última diapositiva pero no refrescaron, aún obtengan el certificado.

---
*Generado por Antigravity Assistant*