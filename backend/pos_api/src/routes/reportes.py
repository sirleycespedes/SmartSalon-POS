from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models.database import db, Venta, VentaServicio, VentaProducto, Cliente, Empleado, Servicio, Producto, Cita
from datetime import datetime, timedelta
from sqlalchemy import func, extract

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    try:
        # Estadísticas del día actual
        hoy = datetime.now().date()
        inicio_dia = datetime.combine(hoy, datetime.min.time())
        fin_dia = datetime.combine(hoy, datetime.max.time())
        
        # Ventas del día
        ventas_hoy = Venta.query.filter(
            Venta.fecha_venta >= inicio_dia,
            Venta.fecha_venta <= fin_dia,
            Venta.estado == 'completada'
        ).all()
        
        ingresos_hoy = sum(float(venta.total) for venta in ventas_hoy)
        
        # Citas del día
        citas_hoy = Cita.query.filter(
            Cita.fecha_hora >= inicio_dia,
            Cita.fecha_hora <= fin_dia
        ).all()
        
        citas_por_estado = {}
        for cita in citas_hoy:
            estado = cita.estado
            citas_por_estado[estado] = citas_por_estado.get(estado, 0) + 1
        
        # Productos con bajo stock
        productos_bajo_stock = Producto.query.filter(
            Producto.stock_actual <= Producto.stock_minimo,
            Producto.activo == True
        ).count()
        
        # Clientes activos
        clientes_activos = Cliente.query.filter_by(activo=True).count()
        
        # Empleados activos
        empleados_activos = Empleado.query.filter_by(activo=True).count()
        
        # Servicios más populares (último mes)
        inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        servicios_populares = db.session.query(
            Servicio.nombre,
            func.count(VentaServicio.id).label('total_ventas'),
            func.sum(VentaServicio.subtotal).label('total_ingresos')
        ).join(
            VentaServicio, Servicio.id == VentaServicio.servicio_id
        ).join(
            Venta, VentaServicio.venta_id == Venta.id
        ).filter(
            Venta.fecha_venta >= inicio_mes,
            Venta.estado == 'completada'
        ).group_by(
            Servicio.id, Servicio.nombre
        ).order_by(
            func.count(VentaServicio.id).desc()
        ).limit(5).all()
        
        servicios_populares_data = [
            {
                'nombre': nombre,
                'total_ventas': total_ventas,
                'total_ingresos': float(total_ingresos) if total_ingresos else 0
            }
            for nombre, total_ventas, total_ingresos in servicios_populares
        ]
        
        # Ingresos por semana (últimas 4 semanas)
        ingresos_semanales = []
        for i in range(4):
            inicio_semana = datetime.now() - timedelta(weeks=i+1)
            inicio_semana = inicio_semana - timedelta(days=inicio_semana.weekday())
            fin_semana = inicio_semana + timedelta(days=6)
            
            ventas_semana = Venta.query.filter(
                Venta.fecha_venta >= inicio_semana,
                Venta.fecha_venta <= fin_semana,
                Venta.estado == 'completada'
            ).all()
            
            total_semana = sum(float(venta.total) for venta in ventas_semana)
            
            ingresos_semanales.append({
                'semana': f"Semana {inicio_semana.strftime('%d/%m')} - {fin_semana.strftime('%d/%m')}",
                'ingresos': total_semana
            })
        
        ingresos_semanales.reverse()  # Mostrar de más antigua a más reciente
        
        return jsonify({
            'resumen_dia': {
                'ventas': len(ventas_hoy),
                'ingresos': ingresos_hoy,
                'citas': len(citas_hoy),
                'citas_por_estado': citas_por_estado
            },
            'estadisticas_generales': {
                'productos_bajo_stock': productos_bajo_stock,
                'clientes_activos': clientes_activos,
                'empleados_activos': empleados_activos
            },
            'servicios_populares': servicios_populares_data,
            'ingresos_semanales': ingresos_semanales
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/ventas-periodo', methods=['GET'])
@jwt_required()
def get_reporte_ventas_periodo():
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        empleado_id = request.args.get('empleado_id', type=int)
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({'error': 'Fecha de inicio y fin son requeridas'}), 400
        
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)
        
        query = Venta.query.filter(
            Venta.fecha_venta >= fecha_inicio,
            Venta.fecha_venta < fecha_fin,
            Venta.estado == 'completada'
        )
        
        if empleado_id:
            query = query.filter(Venta.empleado_id == empleado_id)
        
        ventas = query.all()
        
        # Resumen general
        total_ventas = len(ventas)
        total_ingresos = sum(float(venta.total) for venta in ventas)
        promedio_venta = total_ingresos / total_ventas if total_ventas > 0 else 0
        
        # Ventas por empleado
        ventas_por_empleado = {}
        for venta in ventas:
            if venta.empleado:
                empleado_key = f"{venta.empleado.nombre} {venta.empleado.apellido}"
                if empleado_key not in ventas_por_empleado:
                    ventas_por_empleado[empleado_key] = {
                        'empleado': venta.empleado.to_dict(),
                        'cantidad_ventas': 0,
                        'total_ingresos': 0,
                        'comisiones': 0
                    }
                ventas_por_empleado[empleado_key]['cantidad_ventas'] += 1
                ventas_por_empleado[empleado_key]['total_ingresos'] += float(venta.total)
                comision = float(venta.total) * (float(venta.empleado.comision_porcentaje) / 100)
                ventas_por_empleado[empleado_key]['comisiones'] += comision
        
        # Servicios más vendidos
        servicios_vendidos = {}
        for venta in ventas:
            for venta_servicio in venta.servicios:
                servicio_id = venta_servicio.servicio_id
                if servicio_id not in servicios_vendidos:
                    servicios_vendidos[servicio_id] = {
                        'servicio': venta_servicio.servicio.to_dict(),
                        'cantidad': 0,
                        'total_ingresos': 0
                    }
                servicios_vendidos[servicio_id]['cantidad'] += venta_servicio.cantidad
                servicios_vendidos[servicio_id]['total_ingresos'] += float(venta_servicio.subtotal)
        
        # Productos más vendidos
        productos_vendidos = {}
        for venta in ventas:
            for venta_producto in venta.productos:
                producto_id = venta_producto.producto_id
                if producto_id not in productos_vendidos:
                    productos_vendidos[producto_id] = {
                        'producto': venta_producto.producto.to_dict(),
                        'cantidad': 0,
                        'total_ingresos': 0
                    }
                productos_vendidos[producto_id]['cantidad'] += venta_producto.cantidad
                productos_vendidos[producto_id]['total_ingresos'] += float(venta_producto.subtotal)
        
        # Ventas por método de pago
        ventas_por_metodo = {}
        for venta in ventas:
            metodo = venta.metodo_pago
            if metodo not in ventas_por_metodo:
                ventas_por_metodo[metodo] = {'cantidad': 0, 'total': 0}
            ventas_por_metodo[metodo]['cantidad'] += 1
            ventas_por_metodo[metodo]['total'] += float(venta.total)
        
        return jsonify({
            'periodo': {
                'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
                'fecha_fin': (fecha_fin - timedelta(days=1)).strftime('%Y-%m-%d')
            },
            'resumen': {
                'total_ventas': total_ventas,
                'total_ingresos': total_ingresos,
                'promedio_venta': promedio_venta
            },
            'ventas_por_empleado': list(ventas_por_empleado.values()),
            'servicios_vendidos': sorted(list(servicios_vendidos.values()), key=lambda x: x['cantidad'], reverse=True),
            'productos_vendidos': sorted(list(productos_vendidos.values()), key=lambda x: x['cantidad'], reverse=True),
            'ventas_por_metodo': ventas_por_metodo
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/inventario', methods=['GET'])
@jwt_required()
def get_reporte_inventario():
    try:
        bajo_stock = request.args.get('bajo_stock', 'false').lower() == 'true'
        
        query = Producto.query.filter_by(activo=True)
        
        if bajo_stock:
            query = query.filter(Producto.stock_actual <= Producto.stock_minimo)
        
        productos = query.all()
        
        # Calcular valor total del inventario
        valor_total_inventario = sum(float(producto.precio) * producto.stock_actual for producto in productos)
        
        # Productos con bajo stock
        productos_bajo_stock = [
            producto.to_dict() for producto in productos 
            if producto.stock_actual <= producto.stock_minimo
        ]
        
        # Productos sin stock
        productos_sin_stock = [
            producto.to_dict() for producto in productos 
            if producto.stock_actual == 0
        ]
        
        # Productos más vendidos (último mes)
        inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        productos_mas_vendidos = db.session.query(
            Producto.nombre,
            func.sum(VentaProducto.cantidad).label('total_vendido'),
            func.sum(VentaProducto.subtotal).label('total_ingresos')
        ).join(
            VentaProducto, Producto.id == VentaProducto.producto_id
        ).join(
            Venta, VentaProducto.venta_id == Venta.id
        ).filter(
            Venta.fecha_venta >= inicio_mes,
            Venta.estado == 'completada'
        ).group_by(
            Producto.id, Producto.nombre
        ).order_by(
            func.sum(VentaProducto.cantidad).desc()
        ).limit(10).all()
        
        productos_mas_vendidos_data = [
            {
                'nombre': nombre,
                'total_vendido': int(total_vendido) if total_vendido else 0,
                'total_ingresos': float(total_ingresos) if total_ingresos else 0
            }
            for nombre, total_vendido, total_ingresos in productos_mas_vendidos
        ]
        
        return jsonify({
            'resumen': {
                'total_productos': len(productos),
                'productos_bajo_stock': len(productos_bajo_stock),
                'productos_sin_stock': len(productos_sin_stock),
                'valor_total_inventario': valor_total_inventario
            },
            'productos': [producto.to_dict() for producto in productos],
            'productos_bajo_stock': productos_bajo_stock,
            'productos_sin_stock': productos_sin_stock,
            'productos_mas_vendidos': productos_mas_vendidos_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/clientes', methods=['GET'])
@jwt_required()
def get_reporte_clientes():
    try:
        # Clientes más frecuentes (por número de citas)
        clientes_frecuentes = db.session.query(
            Cliente,
            func.count(Cita.id).label('total_citas'),
            func.sum(Venta.total).label('total_gastado')
        ).outerjoin(
            Cita, Cliente.id == Cita.cliente_id
        ).outerjoin(
            Venta, Cliente.id == Venta.cliente_id
        ).filter(
            Cliente.activo == True
        ).group_by(
            Cliente.id
        ).order_by(
            func.count(Cita.id).desc()
        ).limit(20).all()
        
        clientes_frecuentes_data = []
        for cliente, total_citas, total_gastado in clientes_frecuentes:
            cliente_dict = cliente.to_dict()
            cliente_dict['total_citas'] = total_citas if total_citas else 0
            cliente_dict['total_gastado'] = float(total_gastado) if total_gastado else 0
            clientes_frecuentes_data.append(cliente_dict)
        
        # Nuevos clientes (último mes)
        inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        nuevos_clientes = Cliente.query.filter(
            Cliente.fecha_creacion >= inicio_mes,
            Cliente.activo == True
        ).count()
        
        # Total de clientes activos
        total_clientes = Cliente.query.filter_by(activo=True).count()
        
        # Clientes por mes (últimos 6 meses)
        clientes_por_mes = []
        for i in range(6):
            if i == 0:
                inicio_periodo = inicio_mes
                fin_periodo = datetime.now()
            else:
                inicio_periodo = (inicio_mes - timedelta(days=32*i)).replace(day=1)
                fin_periodo = inicio_periodo.replace(day=28) + timedelta(days=4)
                fin_periodo = fin_periodo - timedelta(days=fin_periodo.day)
            
            clientes_periodo = Cliente.query.filter(
                Cliente.fecha_creacion >= inicio_periodo,
                Cliente.fecha_creacion <= fin_periodo,
                Cliente.activo == True
            ).count()
            
            clientes_por_mes.append({
                'mes': inicio_periodo.strftime('%Y-%m'),
                'nuevos_clientes': clientes_periodo
            })
        
        clientes_por_mes.reverse()
        
        return jsonify({
            'resumen': {
                'total_clientes': total_clientes,
                'nuevos_clientes_mes': nuevos_clientes
            },
            'clientes_frecuentes': clientes_frecuentes_data,
            'clientes_por_mes': clientes_por_mes
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

