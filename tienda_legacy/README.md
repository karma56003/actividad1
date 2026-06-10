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
