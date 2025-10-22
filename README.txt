COMANDOS EJECUTABLES
# Agregar tarea
python task_manager.py agregar "Estudiar Python"

# Actualizar tarea
python task_manager.py actualizar 1 "Estudiar Python y Django"

# Eliminar tarea
python task_manager.py eliminar 1

# Cambiar estado
python task_manager.py estado 1 en_progreso
python task_manager.py estado 1 terminada
python task_manager.py estado 1 pendiente

# Listar tareas
python task_manager.py listar
python task_manager.py pendientes
python task_manager.py en-progreso
python task_manager.py terminadas