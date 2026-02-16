from enum import IntEnum # here we are using IntEnum to define a new type of enum that is an integer
from typing import List, Optional #
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

api=FastAPI()

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    todo_name: str = Field(...,min_length=3,max_length=512,description="Name of the todo")
    todo_desc: str= Field(..., description='Description of the todo')
    priority: Priority= Field(default=Priority.LOW,description='Priority of the todo')

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int =Field(..., description='Unique identifier of the todo')

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None,min_length=3,max_length=512,description="Name of the todo")
    todo_desc: Optional[str]= Field(None, description='Description of the todo')
    priority: Optional[Priority]= Field(None,description='Priority of the todo')

all_todos=[
   Todo(todo_id=1, todo_name='Sports', todo_desc='Go to the gym', priority=Priority.HIGH),      
   Todo(todo_id=2, todo_name='Study', todo_desc='Study for the exam', priority=Priority.MEDIUM),
   Todo(todo_id=3, todo_name='Read', todo_desc='Read the book', priority=Priority.LOW),
   Todo(todo_id=4, todo_name='Write', todo_desc='Write the essay', priority=Priority.MEDIUM),
   Todo(todo_id=5, todo_name='Exercise', todo_desc='Exercise for the body', priority=Priority.HIGH),
   Todo(todo_id=6, todo_name='Sleep', todo_desc='Sleep for the mind', priority=Priority.LOW),
   Todo(todo_id=7, todo_name='Eat', todo_desc='Eat for the body', priority=Priority.MEDIUM),
   Todo(todo_id=8, todo_name='Drink', todo_desc='Drink for the mind', priority=Priority.HIGH),
   Todo(todo_id=9, todo_name='Think', todo_desc='Think for the soul', priority=Priority.LOW),
   Todo(todo_id=10, todo_name='Dream', todo_desc='Dream for the future', priority=Priority.MEDIUM),
]

@api.get('/todos/{todo_id}',response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id== todo_id:
                return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@api.get('/todos',response_model=List[Todo])
def get_todos(first_n: int= None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
    

@api.post('/todos',response_model=Todo)
def create_todo(todo: TodoCreate):

    new_todo_id=max(todo.todo_id for todo in all_todos)+1

    new_todo=Todo(todo_id=new_todo_id,
                  todo_name=todo.todo_name,
                  todo_desc=todo.todo_desc,
                  priority=todo.priority)

    all_todos.append(new_todo)

    return new_todo

@api.put('/todos/{todo_id}',response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id== todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name= updated_todo.todo_name
            if updated_todo.todo_desc is not None:
                todo.todo_desc= updated_todo.todo_desc
            if updated_todo.priority is not None:
                todo.priority= updated_todo.priority
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@api.delete('/todos/{todo_id}',response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id== todo_id:
            deleted_todo=all_todos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail="Todo not found")