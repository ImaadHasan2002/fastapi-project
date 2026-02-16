from fastapi import FastAPI
from fastapi.routing import request_response # here we are 

api=FastAPI()

all_todos=[
    {'todo_id':1 , 'todo_name': 'Sports', 'todo_desc':'Go to the gym'},
    {'todo_id':2 , 'todo_name': 'Study', 'todo_desc':'Study for the exam'},
    {'todo_id':3 , 'todo_name': 'Read', 'todo_desc':'Read the book'},
    {'todo_id':4 , 'todo_name': 'Write', 'todo_desc':'Write the essay'},
    {'todo_id':5 , 'todo_name': 'Exercise', 'todo_desc':'Exercise for the body'},
    {'todo_id':6 , 'todo_name': 'Sleep', 'todo_desc':'Sleep for the mind'},
    {'todo_id':7 , 'todo_name': 'Eat', 'todo_desc':'Eat for the body'},
    {'todo_id':8 , 'todo_name': 'Drink', 'todo_desc':'Drink for the mind'},
    {'todo_id':9 , 'todo_name': 'Think', 'todo_desc':'Think for the soul'},
    {'todo_id':10 , 'todo_name': 'Dream', 'todo_desc':'Dream for the future'},
]

@api.get('/')
def index():
    return {"message": "hello world"}

@api.get('/todos/{todo_id}')
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id']== todo_id:
            return {'result': todo}

@api.get('/todos')
def get_todos(first_n: int= None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos

@api.post('/todos')
def create_todo(todo: dict):
    new_todo_id=max(todo['todo_id'] for todo in all_todos)+1

    new_todo= {
        'todo_id': new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_desc': todo['todo_desc'],
    }

    all_todos.append(new_todo)
    return {'result': new_todo}

@api.put('/todos/{todo_id}')
def update_todo(todo_id: int, updated_todo: dict):
    for todo in all_todos:
        if todo['todo_id']== todo_id:
            todo['todo_name']= updated_todo['todo_name']
            todo['todo_desc']= updated_todo['todo_desc']
            return {'result': todo}
    return "Error: Todo not found"

@api.delete('/todos/{todo_id}')
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo['todo_id']== todo_id:
            deleted_todo=all_todos.pop(index)
            return {'result': deleted_todo}
    return "Error: Todo not found"