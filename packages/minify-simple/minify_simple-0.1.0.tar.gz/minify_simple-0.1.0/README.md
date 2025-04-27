# minify_simple
Minificar archivos web: js, css, html

# Descripción
Inspirado en crear un script para formatear archivos web en IDEs
como Zed, que permiten una alta configuración, pero dejan los detalles
a los programas externos.

En ese sentido se crea este proyecto, que consta de un script CLI para tal fin.
Combinado con [watchdog](https://pypi.org/project/watchdog/) y las [tareas](https://zed.dev/docs/tasks) de Zed, se obtiene un complemento para el minificado automático.

Se detalla, mas abajo, la configuración completa para un entorno linux.
Análogamente es aplicable a cualquier sistema donde se ejecute python.

# Instalar
```
pip install minify-simple
```

# Usar
## Python
```
from minify_simple.minify import Language, minify

# In
code = """
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
"""

minified = minify(code, Language.HTML)

# Out
<ul><li>Item 1</li><li>Item 2</li></ul>
```

## CLI
Minificar el mismo archivo:
```
minify-cli file.js
```
Minificar con sufijo .min:
```
# In
minify-cli -s .min file.js

# Out
file.min.js
```
Minificar indicando lenguaje (por defecto no se proporciona,
se toma de la extension del archivo):
```
minify-cli -l js file.js
```

### Ayuda
Para ver todos los parámetros del script CLI:
```
minify-cli --help
```

## Zed y watchdog
### Monitor de sistema
watchmedo es la herramienta que permite monitorear las carpetas del sistema:
```
watchmedo shell-command \
  -R \
  -p '*.js;*.css' \
  --ignore-patterns '*.min.js;*.min.css' \
  -c 'echo "${watch_src_path}" && minify-cli -s .min "${watch_src_path}"' \
  [/path/folder]
```

### Tarea Zed
Para evitar problemas con las tareas de Zed es recomendable crear
un **script** [.sh | .bat | ...] para ejecutar los comandos:
```
#!/bin/sh
echo $1
minify-cli -s .min $1
```

Salida de ejemplo del script:
```
...
./path/file.js
./path/file.min.js
./path/file.css
./path/file.min.css
...
```

Recomendable asignar permiso de ejecución:
```
chmod +x /path/to/script.sh
```

Luego la tarea Zed quedaría así:
```
{
  "label": "Run Watchdog Statics",
  "command": "watchmedo",
  "args": [
    "shell-command",
    "-R",
    "-p",
    "'*.js;*.css'",
    "--ignore-patterns",
    "'*.min.js;*.min.css'",
    "-c",
    "sh /path/script.sh",
    "${watch_src_path}",
    "/path/folder"
  ],
  "use_new_terminal": false,
  "shell": "system"
}
```

Con permiso de ejecución el script se puede invocar directamente:
```
  ...
  "-c",
  "./path/script.sh"
  ...
```

### Rendimiento
La tarea consume un promedio de 9.0 MB de memoria y muy poco uso del CPU
