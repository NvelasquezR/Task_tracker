#!/usr/bin/env python3
import json
import argparse
import os
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Carga las tareas desde el archivo JSON"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_tasks(self):
        """Guarda las tareas en el archivo JSON"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)
    
    def add_task(self, description):
        """Agrega una nueva tarea"""
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "status": "pendiente",  # pendiente, en_progreso, terminada
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✅ Tarea agregada (ID: {task['id']})")
    
    def update_task(self, task_id, description):
        """Actualiza la descripción de una tarea"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["description"] = description
                task["updated_at"] = datetime.now().isoformat()
                self.save_tasks()
                print(f"✅ Tarea {task_id} actualizada")
                return
        print(f"❌ Tarea con ID {task_id} no encontrada")
    
    def delete_task(self, task_id):
        """Elimina una tarea"""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                del self.tasks[i]
                self.save_tasks()
                print(f"✅ Tarea {task_id} eliminada")
                return
        print(f"❌ Tarea con ID {task_id} no encontrada")
    
    def update_status(self, task_id, status):
        """Actualiza el estado de una tarea"""
        valid_statuses = ["pendiente", "en_progreso", "terminada"]
        if status not in valid_statuses:
            print(f"❌ Estado inválido. Usa: {', '.join(valid_statuses)}")
            return
        
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = datetime.now().isoformat()
                self.save_tasks()
                print(f"✅ Tarea {task_id} marcada como '{status}'")
                return
        print(f"❌ Tarea con ID {task_id} no encontrada")
    
    def list_all_tasks(self):
        """Lista todas las tareas"""
        if not self.tasks:
            print("📝 No hay tareas registradas")
            return
        
        print("\n" + "="*50)
        print("📋 TODAS LAS TAREAS")
        print("="*50)
        for task in self.tasks:
            status_icon = self._get_status_icon(task["status"])
            print(f"{status_icon} ID: {task['id']} | {task['description']} | Estado: {task['status']}")
        print()
    
    def list_in_progress_tasks(self):
        """Lista las tareas en progreso"""
        in_progress = [task for task in self.tasks if task["status"] == "en_progreso"]
        
        if not in_progress:
            print("🔄 No hay tareas en progreso")
            return
        
        print("\n" + "="*50)
        print("🔄 TAREAS EN PROGRESO")
        print("="*50)
        for task in in_progress:
            print(f"🔄 ID: {task['id']} | {task['description']}")
        print()
    
    def list_pending_tasks(self):
        """Lista las tareas pendientes"""
        pending = [task for task in self.tasks if task["status"] == "pendiente"]
        
        if not pending:
            print("⏳ No hay tareas pendientes")
            return
        
        print("\n" + "="*50)
        print("⏳ TAREAS PENDIENTES")
        print("="*50)
        for task in pending:
            print(f"⏳ ID: {task['id']} | {task['description']}")
        print()
    
    def list_completed_tasks(self):
        """Lista las tareas terminadas"""
        completed = [task for task in self.tasks if task["status"] == "terminada"]
        
        if not completed:
            print("✅ No hay tareas terminadas")
            return
        
        print("\n" + "="*50)
        print("✅ TAREAS TERMINADAS")
        print("="*50)
        for task in completed:
            print(f"✅ ID: {task['id']} | {task['description']}")
        print()
    
    def _get_status_icon(self, status):
        """Devuelve un icono según el estado de la tarea"""
        icons = {
            "pendiente": "⏳",
            "en_progreso": "🔄",
            "terminada": "✅"
        }
        return icons.get(status, "📝")

def main():
    parser = argparse.ArgumentParser(description="Rastreador de Tareas")
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Agregar tarea
    parser_add = subparsers.add_parser('agregar', help='Agregar una nueva tarea')
    parser_add.add_argument('descripcion', help='Descripción de la tarea')
    
    # Actualizar tarea
    parser_update = subparsers.add_parser('actualizar', help='Actualizar una tarea existente')
    parser_update.add_argument('id', type=int, help='ID de la tarea')
    parser_update.add_argument('descripcion', help='Nueva descripción de la tarea')
    
    # Eliminar tarea
    parser_delete = subparsers.add_parser('eliminar', help='Eliminar una tarea')
    parser_delete.add_argument('id', type=int, help='ID de la tarea')
    
    # Cambiar estado
    parser_status = subparsers.add_parser('estado', help='Cambiar el estado de una tarea')
    parser_status.add_argument('id', type=int, help='ID de la tarea')
    parser_status.add_argument('estado', choices=['pendiente', 'en_progreso', 'terminada'], 
                              help='Nuevo estado de la tarea')
    
    # Listar tareas
    subparsers.add_parser('listar', help='Listar todas las tareas')
    subparsers.add_parser('pendientes', help='Listar tareas pendientes')
    subparsers.add_parser('en-progreso', help='Listar tareas en progreso')
    subparsers.add_parser('terminadas', help='Listar tareas terminadas')
    
    args = parser.parse_args()
    task_manager = TaskManager()
    
    if args.command == 'agregar':
        task_manager.add_task(args.descripcion)
    
    elif args.command == 'actualizar':
        task_manager.update_task(args.id, args.descripcion)
    
    elif args.command == 'eliminar':
        task_manager.delete_task(args.id)
    
    elif args.command == 'estado':
        task_manager.update_status(args.id, args.estado)
    
    elif args.command == 'listar':
        task_manager.list_all_tasks()
    
    elif args.command == 'pendientes':
        task_manager.list_pending_tasks()
    
    elif args.command == 'en-progreso':
        task_manager.list_in_progress_tasks()
    
    elif args.command == 'terminadas':
        task_manager.list_completed_tasks()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()