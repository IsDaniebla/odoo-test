# Nombre del contenedor Docker
CONTAINER_NAME=odoo-17-docker-web-1

# Ruta del directorio donde están los módulos personalizados
ADDONS_PATH=addons

# Base de datos de Odoo
DB_NAME=test3

MODULE=mi_producto

# Tarea para actualizar los módulos
update-modules:
	docker exec -u odoo $(CONTAINER_NAME) odoo -d $(DB_NAME) -u all --stop-after-init

# Tarea para reiniciar el contenedor
restart-web:
	docker restart $(CONTAINER_NAME)

# Tarea completa: actualiza módulos y reinicia contenedor
reload:
	make update-module
	make restart-web
	@powershell.exe -Command "Import-Module BurntToast; New-BurntToastNotification -Text 'Odoo', 'Módulos actualizados exitosamente'" || echo '🔔 Notificación no enviada'
	@echo -e "\a"
	@echo "✅ Módulos actualizados"



# Tarea para actualizar un módulo específico
update-module:
	docker exec -u odoo $(CONTAINER_NAME) odoo -d $(DB_NAME) -u $(MODULE) --stop-after-init



.PHONY: update-modules restart-web reload update-module logs stop start rebuild 