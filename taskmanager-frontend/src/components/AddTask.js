// src/components/AddTask.js
import React, { useState } from 'react';
import axios from 'axios';

const AddTask = ({ onTaskAdded }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [dueDate, setDueDate] = useState('');
    const [status, setStatus] = useState('TO DO');

    const handleSubmit = (e) => {
        e.preventDefault();
        const task = { title, description, due_date: dueDate, status };
        
        axios.post('http://127.0.0.1:5000/tasks/add', task)
            .then(response => {
                console.log(response.data);
                onTaskAdded();
            })
            .catch(error => { 
                console.error ('There was an error!', error);
                alert('There was an error adding the task! Please check your input and try again.');
            });
        
        // Reset form fields
        setTitle('');
        setDescription('');
        setDueDate('');
        setStatus('TO DO');
    };

    return (
        <form onSubmit={handleSubmit}>
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
                required
            />
            <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                required
            />
            <select value={status} onChange={(e) => setStatus(e.target.value)} required>
                <option value="TO DO">TO DO</option>
                <option value="In Progress">In Progress</option>
                <option value="Completed">Completed</option>
            </select>
            <button type="submit">Add Task</button>
        </form>
    );
};

export default AddTask;
