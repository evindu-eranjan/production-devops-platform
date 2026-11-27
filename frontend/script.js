
const API_URL = "http://56.10.172.216:8000";

// Load all tasks from backend
async function loadTasks() {
    const taskList = document.getElementById("task-list");

    try {
        const response = await fetch(`${API_URL}/tasks`);

        if (!response.ok) {
            throw new Error("Failed to load tasks");
        }

        const tasks = await response.json();

        taskList.innerHTML = "";

        if (tasks.length === 0) {
            taskList.innerHTML = "<p>No tasks found.</p>";
            return;
        }

        tasks.forEach(task => {
            const taskItem = document.createElement("div");
            taskItem.className = "task-item";

            const taskInfo = document.createElement("div");

            const title = document.createElement("h3");
            title.textContent = task.title;

            const description = document.createElement("p");
            description.textContent = task.description;

            const status = document.createElement("p");
            status.textContent = task.completed
                ? "Completed"
                : "Pending";

            taskInfo.append(title, description, status);

            const actions = document.createElement("div");

            if (!task.completed) {
                const completeButton = document.createElement("button");
                completeButton.textContent = "Complete";
                completeButton.onclick = () => completeTask(task.id);
                actions.appendChild(completeButton);
            }

            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";
            deleteButton.style.marginLeft = "8px";
            deleteButton.style.background = "#dc2626";
            deleteButton.onclick = () => deleteTask(task.id);

            actions.appendChild(deleteButton);

            taskItem.append(taskInfo, actions);
            taskList.appendChild(taskItem);
        });

    } catch (error) {
        taskList.textContent =
            "Unable to load tasks. Please check the API connection.";
        console.error(error);
    }
}

// Create a new task
document.getElementById("task-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                description: description,
                completed: false
            })
        });

        if (!response.ok) {
            throw new Error("Failed to create task");
        }

        this.reset();
        await loadTasks();

    } catch (error) {
        alert("Unable to create task.");
        console.error(error);
    }
});

// Mark task as completed
async function completeTask(taskId) {
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                completed: true
            })
        });

        if (!response.ok) {
            throw new Error("Failed to complete task");
        }

        await loadTasks();

    } catch (error) {
        alert("Unable to complete task.");
        console.error(error);
    }
}

// Delete a task
async function deleteTask(taskId) {
    if (!confirm("Are you sure you want to delete this task?")) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Failed to delete task");
        }

        await loadTasks();

    } catch (error) {
        alert("Unable to delete task.");
        console.error(error);
    }
}

// Load tasks when page opens
loadTasks();
