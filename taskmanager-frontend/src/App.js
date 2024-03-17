// src/App.js
import React, { useState } from 'react';
import TaskList from './components/TaskList';
import AddTask from './components/AddTask';
import EditTask from './components/EditTask';
import axios from 'axios';
import { useEffect } from 'react';
import './App.css';

function App() {
  const [editingTask, setEditingTask] = useState(null);
  const [tasks, setTasks] = useState([]);

  // Fetch tasks from the backend
  const fetchTasks = () => {
    axios.get('http://127.0.0.1:5000/tasks')
      .then(response => {
        setTasks(response.data);
      })
      .catch(error => console.log("Error fetching tasks:", error));
  };

  // Effect hook to fetch tasks on component mount
  useEffect(() => {
    fetchTasks();
  }, []);

  // Function to refresh the task list
  const handleAdded = () => {
    fetchTasks(); // Re-fetch tasks after a new one is added
  };

  // Function to handle the delete button click
  const onDelete = () => {
    // Refresh the list after deleting
      fetchTasks();
  };

  // Function to handle the edit button click
  const handleEdit = (task) => {
      setEditingTask(task);
  };

  const handleTaskUpdated = () => {
    fetchTasks();
};


  return (
    <div className="App">
      <h1>TaskManager-SLB</h1>
      {editingTask ? (
        <EditTask task={editingTask} setEditingTask={setEditingTask} onTaskUpdated={handleTaskUpdated} />
      ) : (
        <>
          <AddTask onTaskAdded={handleAdded} />
          <TaskList tasks={tasks} onEdit={handleEdit} onDelete={onDelete} />
        </>
      )}
    </div>
  );
}

export default App;
