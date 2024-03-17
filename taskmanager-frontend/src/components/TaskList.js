// Update your TaskList.js to include Task component usage
import Task from './Task';

const TaskList = ({ tasks ,onEdit, onDelete }) => {

    return (
        <div>
            <h2>Tasks</h2>
            {tasks.map(task => (
                <Task key={task.id} task={task} onDelete={onDelete} onEdit={onEdit} />
            ))}
        </div>
    );
};

export default TaskList;
