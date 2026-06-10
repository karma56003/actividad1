# SISTEMA DE INVENTARIO v1.0 — Tienda El Progreso

### Desarrollado: Departamento de Informática | Python/Flask | SQLite

---

## ¿QUÉ HACE ESTE SISTEMA?

Gestión básica de inventario para tienda de abarrotes/abastos.
Permite registrar, editar y eliminar **Productos** y **Ventas**.

**LO QUE NO HACE (por diseño):**

- No hay reportes, no hay gráficas, no hay KPIs.
- No hay paginación: todos los registros se muestran en una sola tabla.
- El stock **no se descuenta automáticamente** al registrar una venta.
  Deberá actualizarlo usted mismo en la tabla de Productos.
- No hay relación formal (FK) entre Ventas y Productos.
- No hay filtros ni búsqueda avanzada.
- Si necesita saber cuánto vendió por categoría, use una calculadora.

---

## REQUISITOS

- Python 3.8 o superior
- pip

---

## INSTALACIÓN Y EJECUCIÓN

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Poblar la base de datos (50 registros de ejemplo)

```bash
python - <<'EOF'
import sqlite3
conn = sqlite3.connect("inventario.db")
with open("poblar_bd.sql", "r", encoding="utf-8") as f:
    conn.executescript(f.read())
conn.close()
print("Base de datos poblada correctamente.")
EOF
```

> **Alternativa:** si tiene `sqlite3` instalado en su sistema:
>
> ```bash
> sqlite3 inventario.db < poblar_bd.sql
> ```

### 3. Ejecutar la aplicación

```bash
python app.py
```

### 4. Abrir en el navegador

```
http://127.0.0.1:5000
```

---

## ESTRUCTURA DE ARCHIVOS

```
tienda_legacy/
├── app.py              ← Aplicación principal Flask
├── requirements.txt    ← Dependencias Python
├── poblar_bd.sql       ← Script SQL con 50 registros de ejemplo
├── inventario.db       ← Se crea automáticamente al ejecutar
├── README.md           ← Este archivo
└── templates/
    ├── base.html           ← Plantilla base (navbar, header, footer)
    ├── productos.html      ← Listado de productos
    ├── producto_form.html  ← Formulario crear/editar producto
    ├── ventas.html         ← Listado de ventas
    └── venta_form.html     ← Formulario registrar/editar venta
```

---

## BASE DE DATOS

Dos tablas planas, sin relaciones formales:

**Productos** `(id, nombre, categoria, precio, stock, proveedor, codigo, descripcion, fecha_ingreso)`

**Ventas** `(id, producto_id, cantidad, precio_venta, fecha, vendedor, cliente, notas)`

> `producto_id` en Ventas es solo un número. No hay CASCADE, no hay JOIN automático.
> Si borra un producto, sus ventas quedan huérfanas (con un ID que ya no existe).

---

## CREDENCIALES

No hay sistema de login.
Cualquiera que abra el navegador puede hacer todo.
Si necesita seguridad, ponga la computadora bajo llave.

---

## PROBLEMAS CONOCIDOS

| Problema                       | Solución                                 |
| ------------------------------ | ---------------------------------------- |
| La tabla no cabe en pantalla   | Use Ctrl+- para alejar el zoom           |
| Borré algo que no debía        | Restaure desde su respaldo (¿tiene uno?) |
| El stock no se actualiza solo  | Actualícelo manualmente                  |
| Necesito un reporte mensual    | Imprima la pantalla con Ctrl+P           |
| La base de datos está corrupta | Borre `inventario.db` y repita el paso 2 |

---

## SOPORTE

Contactar al Jefe de Sistemas en extensión 104.
Horario de atención: lunes a viernes 9:00–13:00.
_No llamar los viernes por la tarde._

##OBSERVACIONES
La base de datos actual tiene una estructura muy simple:

PRODUCTOS

- id PK
- nombre
- categoria
- precio
- stock
- proveedor
- codigo
- descripcion
- fecha_ingreso

VENTAS

- id PK
- producto_id Sin clave foránea formal
- cantidad
- precio_venta
- fecha
- vendedor
- cliente
- notas

Relación esperada:

Productos 1 -------- N Ventas

Pero esta relación no está protegida por la base de datos, porque producto_id en la tabla Ventas solo guarda un número. No existe una clave foránea que garantice que la venta pertenezca a un producto real.
##PROBLEMAS RELACIONADOS AL CODIGO
Primero, el sistema no tiene una base de datos relacional completa. Aunque existe el campo producto_id en ventas, no se declara como clave foránea. Esto puede provocar ventas huérfanas si se elimina un producto.

Segundo, el stock no se actualiza automáticamente cuando se registra una venta. Esto genera información desactualizada, porque el inventario puede mostrar cantidades que ya no existen físicamente.

Tercero, la pantalla de ventas tiene una falla de plantilla. La plantilla ventas.html usa un bloque llamado content, pero la plantilla base usa el bloque body. Por eso la ruta /ventas carga la estructura general, pero no muestra correctamente la tabla de ventas.

Cuarto, existe una incoherencia en la ruta del botón de registrar venta. En la plantilla se usa /venta/nueva, pero en el código la ruta correcta es /ventas/nueva. Esto produce error 404 al hacer clic desde esa pantalla.

Quinto, el sistema no tiene autenticación ni control de usuarios. Cualquier persona que acceda al navegador puede crear, editar o eliminar productos y ventas.

Sexto, el sistema usa una clave secreta escrita directamente en el código y ejecuta la aplicación con debug=True, lo cual no es recomendable para un entorno real.

Séptimo, las eliminaciones se hacen mediante enlaces GET, por ejemplo /productos/eliminar/<id> y /ventas/eliminar/<id>. Esto es riesgoso porque una eliminación debería hacerse mediante un método POST o DELETE para evitar borrados accidentales.

##PRINCIPIOS TGS AFECTADOS
a) Entropía

La entropía se observa cuando el sistema pierde orden, control y utilidad en la información. En este caso, la información pierde valor porque el stock no se descuenta automáticamente al registrar ventas. Esto provoca que el inventario se vuelva obsoleto.

También existe entropía porque las ventas pueden quedar huérfanas si se elimina un producto. Al no existir una clave foránea, el sistema no protege la integridad de los datos.

Otro punto de entropía es que las notas y clientes se registran como texto libre. Esto dificulta clasificar, analizar y convertir esos datos en información útil para la toma de decisiones.

Finalmente, la falla de la pantalla de ventas aumenta la entropía, porque los datos existen en la base de datos, pero no se visualizan correctamente para el usuario.

b) Falta de sinergia

La falta de sinergia ocurre porque las partes del sistema no trabajan juntas para producir información estratégica. La tabla de productos y la tabla de ventas existen, pero no se integran correctamente.

El sistema debería convertir los datos en información útil, por ejemplo: ventas por categoría, productos más vendidos, vendedores con mejor rendimiento, productos con bajo stock, ingresos por fecha o rentabilidad por proveedor. Sin embargo, actualmente solo permite registrar y listar datos.

Por eso, la suma de las partes no genera un valor superior. Productos y ventas funcionan como registros separados, no como una fuente de inteligencia para el negocio.

##PUNTOS A MEJORAR

Módulo de reportes de ventas.
Módulo de control automático de stock.
Módulo de alertas de stock mínimo.
Módulo de análisis por categoría, producto, vendedor y cliente.
Módulo de usuarios, roles y permisos.
Módulo de proveedores y compras.
Módulo de indicadores KPI.
Módulo de exportación a Excel o PDF.

## Conclusión ética y conexión con el ODS 8

La ineficiencia de este sistema afecta directamente al trabajador porque lo obliga a realizar tareas manuales, repetitivas y propensas a errores. Al no descontarse el stock automáticamente, el trabajador debe corregir datos a mano. Al no existir reportes, debe calcular ventas, productos críticos o resultados comerciales fuera del sistema.

Esto genera pérdida de tiempo, estrés laboral, errores administrativos y menor productividad. Desde una perspectiva ética, un sistema mal diseñado traslada la carga del error tecnológico al trabajador.

La conexión con el ODS 8, Trabajo Decente y Crecimiento Económico, es clara: un sistema eficiente debe mejorar las condiciones laborales, reducir tareas innecesarias y permitir que el trabajador se enfoque en actividades de mayor valor. Para cumplir este objetivo, el sistema debe evolucionar de un CRUD básico a un DSS capaz de apoyar decisiones, proteger datos y mejorar la productividad de la tienda.

## Conclusión general

El sistema actual cumple una función mínima de registro, pero no cumple con las necesidades de un negocio que requiere información estratégica. La falta de relaciones formales, reportes, actualización automática de stock, seguridad y análisis convierte al sistema en una herramienta limitada.
