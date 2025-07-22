from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models import Task
from app.schemas import TaskCreate, TaskRead
from app.auth import get_session, get_current_user
from app.models import User

router = APIRouter(prefix="/tasks", tags=["Tarefas"])

@router.get("/", response_model=list[TaskRead])
def get_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()
    return tasks

@router.post("/", response_model=TaskRead)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = Task(**task_data.dict(), user_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    
    task.title = task_data.title
    task.description = task_data.description
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    
    session.delete(task)
    session.commit()
    return {"detail": "Tarefa deletada com sucesso."}
