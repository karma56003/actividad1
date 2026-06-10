"""
Sistema de Inventario v1.0 - Tienda El Progreso
Desarrollado: 2009 | Última modificación: hace mucho
NO TOCAR SIN AUTORIZACIÓN DEL JEFE DE SISTEMAS
"""

import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.secret_key = "tienda123"  # TODO: cambiar esto "algún día"
DATABASE = "inventario.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS Productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                categoria TEXT,
                precio REAL,
                stock INTEGER,
                proveedor TEXT,
                codigo TEXT,
                descripcion TEXT,
                fecha_ingreso TEXT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS Ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER,
                cantidad INTEGER,
                precio_venta REAL,
                fecha TEXT,
                vendedor TEXT,
                cliente TEXT,
                notas TEXT
            )
        """)
        db.commit()


# ─────────────────────────────────────────────
#  PRODUCTOS
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return redirect(url_for("listar_productos"))


@app.route("/productos")
def listar_productos():
    db = get_db()
    # Sin paginación. Todo junto. Siempre.
    productos = db.execute("SELECT * FROM Productos ORDER BY id ASC").fetchall()
    return render_template("productos.html", productos=productos)


@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "INSERT INTO Productos (nombre, categoria, precio, stock, proveedor, codigo, descripcion, fecha_ingreso) VALUES (?,?,?,?,?,?,?,?)",
            (
                request.form["nombre"],
                request.form["categoria"],
                request.form["precio"],
                request.form["stock"],
                request.form["proveedor"],
                request.form["codigo"],
                request.form["descripcion"],
                request.form["fecha_ingreso"],
            ),
        )
        db.commit()
        flash("Producto guardado.")
        return redirect(url_for("listar_productos"))
    return render_template("producto_form.html", producto=None, accion="Crear")


@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    db = get_db()
    producto = db.execute("SELECT * FROM Productos WHERE id=?", (id,)).fetchone()
    if not producto:
        flash("Producto no encontrado.")
        return redirect(url_for("listar_productos"))
    if request.method == "POST":
        db.execute(
            "UPDATE Productos SET nombre=?, categoria=?, precio=?, stock=?, proveedor=?, codigo=?, descripcion=?, fecha_ingreso=? WHERE id=?",
            (
                request.form["nombre"],
                request.form["categoria"],
                request.form["precio"],
                request.form["stock"],
                request.form["proveedor"],
                request.form["codigo"],
                request.form["descripcion"],
                request.form["fecha_ingreso"],
                id,
            ),
        )
        db.commit()
        flash("Producto actualizado.")
        return redirect(url_for("listar_productos"))
    return render_template("producto_form.html", producto=producto, accion="Editar")


@app.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):
    db = get_db()
    db.execute("DELETE FROM Productos WHERE id=?", (id,))
    db.commit()
    flash("Producto eliminado.")
    return redirect(url_for("listar_productos"))


# ─────────────────────────────────────────────
#  VENTAS
# ─────────────────────────────────────────────

@app.route("/ventas")
def listar_ventas():
    db = get_db()
    # JOIN manual porque "las relaciones complican las cosas"
    ventas = db.execute("SELECT * FROM Ventas ORDER BY id ASC").fetchall()
    productos = db.execute("SELECT id, nombre FROM Productos").fetchall()
    prod_map = {p["id"]: p["nombre"] for p in productos}
    return render_template("ventas.html", ventas=ventas, prod_map=prod_map)


@app.route("/ventas/nueva", methods=["GET", "POST"])
def nueva_venta():
    db = get_db()
    productos = db.execute("SELECT * FROM Productos").fetchall()
    if request.method == "POST":
        db.execute(
            "INSERT INTO Ventas (producto_id, cantidad, precio_venta, fecha, vendedor, cliente, notas) VALUES (?,?,?,?,?,?,?)",
            (
                request.form["producto_id"],
                request.form["cantidad"],
                request.form["precio_venta"],
                request.form["fecha"],
                request.form["vendedor"],
                request.form["cliente"],
                request.form["notas"],
            ),
        )
        db.commit()
        flash("Venta registrada.")
        return redirect(url_for("listar_ventas"))
    return render_template("venta_form.html", venta=None, productos=productos, accion="Registrar")


@app.route("/ventas/editar/<int:id>", methods=["GET", "POST"])
def editar_venta(id):
    db = get_db()
    venta = db.execute("SELECT * FROM Ventas WHERE id=?", (id,)).fetchone()
    productos = db.execute("SELECT * FROM Productos").fetchall()
    if not venta:
        flash("Venta no encontrada.")
        return redirect(url_for("listar_ventas"))
    if request.method == "POST":
        db.execute(
            "UPDATE Ventas SET producto_id=?, cantidad=?, precio_venta=?, fecha=?, vendedor=?, cliente=?, notas=? WHERE id=?",
            (
                request.form["producto_id"],
                request.form["cantidad"],
                request.form["precio_venta"],
                request.form["fecha"],
                request.form["vendedor"],
                request.form["cliente"],
                request.form["notas"],
                id,
            ),
        )
        db.commit()
        flash("Venta actualizada.")
        return redirect(url_for("listar_ventas"))
    return render_template("venta_form.html", venta=venta, productos=productos, accion="Editar")


@app.route("/ventas/eliminar/<int:id>")
def eliminar_venta(id):
    db = get_db()
    db.execute("DELETE FROM Ventas WHERE id=?", (id,))
    db.commit()
    flash("Venta eliminada.")
    return redirect(url_for("listar_ventas"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)