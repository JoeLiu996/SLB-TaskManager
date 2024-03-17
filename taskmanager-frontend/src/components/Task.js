// src/components/Task.js
import React from 'react';
import axios from 'axios';

const Task = ({ task, onDelete, onEdit }) => {
    const handleDelete = () => {
        axios.delete(`http://127.0.0.1:5000/tasks/delete/${task.id}`)
            .then(() => {
                onDelete(); // Notify parent component to refresh the list
            })
            .catch(error => console.error('There was an error!', error));
    };

    return (
        <div>
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <p>Due: {task.due_date}</p>
            <p>Status: {task.status}</p>
            <button onClick={() => onEdit(task)}>Edit</button>
            <button onClick={handleDelete}>Delete</button>
        </div>
    );
};

export default Task;
