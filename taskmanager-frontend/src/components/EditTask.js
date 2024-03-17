// src/components/EditTask.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EditTask = ({ task, setEditingTask, onTaskUpdated }) => {
    const [title, setTitle] = useState(task.title);
    const [description, setDescription] = useState(task.description);
    const [dueDate, setDueDate] = useState(task.due_date);
    const [status, setStatus] = useState(task.status);

    useEffect(() => {
        // Initialize the form with the current task details
        setTitle(task.title);
        setDescription(task.description);
        setDueDate(task.due_date);
        setStatus(task.status);
    }, [task]);

    const handleUpdateTask = (e) => {
        e.preventDefault();
        axios.put(`http://127.0.0.1:5000/tasks/update/${task.id}`, {
            title,
            description,
            due_date: dueDate,
            status,
        })
        .then(() => {
            setEditingTask(null); // Reset the editing task to hide the form
            onTaskUpdated(); // Notify the parent component to refresh the task list

        })
        .catch(error => {
            console.error('There was an error updating the task!', error);
            alert('There was an error updating the task! Please check your input and try again.');
        });
    };

    return (
        <form onSubmit={handleUpdateTask}>
            <h2>Edit Task</h2>
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Title"
                required
            />
            <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Description"
            />
            <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                required
            />
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
                <option value="TO DO">TO DO</option>
                <option value="In Progress">In Progress</option>
                <option value="Completed">Completed</option>
            </select>
            <button type="submit">Update Task</button>
            <button type="button" onClick={() => setEditingTask(null)}>Cancel</button>
        </form>
    );
};

export default EditTask;
