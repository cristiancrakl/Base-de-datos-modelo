SELECT a.descripcion, a.valor, p.nombre AS nombre_proveedor
FROM proveedor p, articulo a
WHERE p.nit = a.nit 
  AND p.celular LIKE '%7%';


SELECT concat(c.nombre1, ' ', c.apellido1) AS nombre_cliente, b.nombre AS nombre_barrio
FROM barrio b, cliente c, factura f
WHERE (b.comuna = c.comuna AND b.cod_barrio = c.cod_barrio)
  AND c.documento = f.documento
  AND f.fecha BETWEEN '2020-01-01' AND '2020-12-31';


SELECT concat(c.nombre1, ' ', c.apellido1) AS nombre_cliente, b.nombre AS nombre_barrio
FROM barrio b
INNER JOIN cliente c 
	ON (b.comuna = c.comuna AND b.cod_barrio = c.cod_barrio)
INNER JOIN factura f 
	ON c.documento = f.documento
WHERE f.fecha BETWEEN '2020-01-01' AND '2020-12-31';


