import { useEffect, useState } from "react"
import "./App.css"

function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [currentUsername, setCurrentUsername] = useState("")
  const [loggedIn, setLoggedIn] = useState(false)
  const [projects, setProjects] = useState([])
  const [projectName, setProjectName] = useState("")
  const [selectedProject, setSelectedProject] = useState(null)
  const [tasks, setTasks] = useState([])
  const [taskName, setTaskName] = useState("")
  const [taskDueDate, setTaskDueDate] = useState("")
  const [taskStatus, setTaskStatus] = useState("TODO")
  const [users, setUsers] = useState([])
  const [assignedUserId, setAssignedUserId] = useState(1)
  const [currentUserId, setCurrentUserId] = useState(null)
  const [editingTask, setEditingTask] = useState(null)

  const handleLogout = () => {
  localStorage.removeItem("token")
  setLoggedIn(false)
  setCurrentUserId(null)
  setCurrentUsername("")
  setSelectedProject(null)
  setTasks([])
  }

  const handleLogin = async (event) => {
  
    event.preventDefault()

  const formData = new URLSearchParams()
  formData.append("username", username)
  formData.append("password", password)

  try {
    const response = await fetch("http://127.0.0.1:8000/users/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    })

    const data = await response.json()

    console.log("Status:", response.status)
    console.log("Response:", data)

    if (response.ok) {
  localStorage.setItem("token", data.access_token)
  setLoggedIn(true)
  const meResponse = await fetch("http://127.0.0.1:8000/users/me", {
    headers: {
      Authorization: `Bearer ${data.access_token}`,
    },
  })

  const meData = await meResponse.json()
  setCurrentUserId(meData.user_id)
  console.log("Current user:", meData)
}
  } catch (error) {
    console.error("Login error:", error)
  }
}

const handleCreateProject = async () => {
  if (!projectName.trim()) {
    alert("Please enter a project name")
    return
  }

  const token = localStorage.getItem("token")

  try {
    const response = await fetch("http://127.0.0.1:8000/projects/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ project_name: projectName }),
    })

    const data = await response.json()

    console.log("Create project status:", response.status)
    console.log("Created project:", data)

    setProjects((currentProjects) => [...currentProjects, data])
    setProjectName("")
  } catch (error) {
    console.error("Create project error:", error)
  }
}

const handleDeleteProject = async (projectId) => {
  const confirmed = window.confirm(
    "Are you sure you want to delete this project and all its tasks?"
  )

  if (!confirmed) return

  const token = localStorage.getItem("token")

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/projects/${projectId}`,
      {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    const data = await response.json()

    console.log("Delete project status:", response.status)
    console.log("Delete project response:", data)

    setProjects((currentProjects) =>
      currentProjects.filter((project) => project.id !== projectId)
    )

    if (selectedProject?.id === projectId) {
      setSelectedProject(null)
      setTasks([])
      setEditingTask(null)
    }
  } catch (error) {
    console.error("Delete project error:", error)
  }
}

const getDueDateStatus = (dueDate) => {
  if (!dueDate) return "none"

  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const due = new Date(dueDate)
  due.setHours(0, 0, 0, 0)

  const difference = due - today
  const days = difference / (1000 * 60 * 60 * 24)

  if (days < 0) return "overdue"
  if (days <= 2) return "soon"

  return "normal"
}

const handleCreateTask = async () => {
  if (!taskName.trim()) {
   alert("Please enter a task name")
   return
  }

  if (!selectedProject) {
    return
  }

  const token = localStorage.getItem("token")

  try {
    const response = await fetch("http://127.0.0.1:8000/tasks/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        name: taskName,
        project_id: selectedProject.id,
        assigned_user_id: assignedUserId,
        status: taskStatus,
        due_date: taskDueDate,
      }),
    })

    const data = await response.json()

    console.log("Create task status:", response.status)
    console.log("Created task:", data)

    setTasks((currentTasks) => [...currentTasks, data])
    setTaskName("")
    setTaskDueDate("")
    setTaskStatus("TODO")
    setAssignedUserId(currentUserId)
  } catch (error) {
    console.error("Create task error:", error)
  }
}

const handleEditTask = (task) => {
  setEditingTask(task)
  console.log("Editing task:", task)
}

const handleDeleteTask = async (taskId) => {
  const confirmed = window.confirm("Are you sure you want to delete this task?")

  if (!confirmed) {
    return
  }
  const token = localStorage.getItem("token")

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/tasks/${taskId}`,
      {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    const data = await response.json()

    console.log("Delete task status:", response.status)
    console.log("Delete task response:", data)

    setTasks((currentTasks) =>
  currentTasks.filter((task) => task.id !== taskId)
            )

  } catch (error) {
    console.error("Delete task error:", error)
  }
}

const handleUpdateTask = async () => {
  const token = localStorage.getItem("token")

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/tasks/${editingTask.id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: editingTask.name,
          status: editingTask.status,
          due_date: editingTask.due_date,
        }),
      }
    )

    const data = await response.json()

    console.log("Update task status:", response.status)
    console.log("Updated task:", data)

    setTasks((currentTasks) =>
     currentTasks.map((task) =>
      task.id === data.id ? data : task
  )
)

    setEditingTask(null)

  } catch (error) {
    console.error("Update task error:", error)
  }
}

useEffect(() => {
  if (!loggedIn) {
    return
  }

  const token = localStorage.getItem("token")

  fetch("http://127.0.0.1:8000/projects/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {
  console.log("Projects:", data)
  setProjects(data)
})
    .catch((error) => {
      console.error("Projects error:", error)
    })
}, [loggedIn])

useEffect(() => {
  if (!loggedIn) {
    return
  }

  const token = localStorage.getItem("token")

  fetch("http://127.0.0.1:8000/users/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Users:", data)
      setUsers(data)
    })
    .catch((error) => {
      console.error("Users error:", error)
    })
}, [loggedIn])

useEffect(() => {
  if (!currentUserId || users.length === 0) return

  const currentUser = users.find(
    (user) => user.id === currentUserId
  )

  if (currentUser) {
    setCurrentUsername(currentUser.username)
  }
}, [currentUserId, users])

useEffect(() => {
  if (!selectedProject) {
    return
  }

  const token = localStorage.getItem("token")

  fetch(
    `http://127.0.0.1:8000/tasks/?project_id=${selectedProject.id}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )
    .then((response) => response.json())
    .then((data) => {
      console.log("Tasks:", data)
      setTasks(data)
    })
    .catch((error) => {
      console.error("Tasks error:", error)
    })
}, [selectedProject])
  if (loggedIn) {

    const totalTasks = tasks.length

    const completedTasks = tasks.filter(
     (task) => task.status === "DONE"
    ).length

    const inProgressTasks = tasks.filter(
     (task) => task.status === "IN_PROGRESS"
    ).length

    const todoTasks = tasks.filter(
     (task) => task.status === "TODO"
    ).length

  return (
    <div className="dashboard">

  <header className="dashboard-header">
   <div>
     <h1>Dashboard</h1>
     <p>Welcome back, {currentUsername} !</p>
   </div>

   <div className="profile-section">
     <div className="profile-info">
       <div className="profile-avatar">
         {currentUsername.charAt(0).toUpperCase()}
       </div>

       <div>
         <strong>{currentUsername} </strong>
         <span>Account</span>
       </div>
     </div>

     <button className="logout-button" onClick={handleLogout}>
       Logout
     </button>
    </div>
  </header>

  <main className="dashboard-content">

    <div className="stats-grid">
     <div className="stat-card">
      <span>Total Tasks</span>
      <strong>{totalTasks}</strong>
     </div>

     <div className="stat-card">
      <span>To Do</span>
      <strong>{todoTasks}</strong>
     </div>

     <div className="stat-card">
      <span>In Progress</span>
      <strong>{inProgressTasks}</strong>
     </div>

     <div className="stat-card">
      <span>Completed</span>
      <strong>{completedTasks}</strong>
     </div>
    </div>

    {selectedProject && (
      <section className="selected-project-section">

        <div className="section-header">
          <div>
            <span className="section-label">CURRENT PROJECT</span>
            <h2>{selectedProject.project_name}</h2>
          </div>
        </div>

        <div className="create-task">
          <input
            type="text"
            placeholder="Enter task name"
            value={taskName}
            onChange={(event) => setTaskName(event.target.value)}
          />

          <input
            type="date"
            value={taskDueDate}
            onChange={(event) => setTaskDueDate(event.target.value)}
          />

          <select
            value={taskStatus}
            onChange={(event) => setTaskStatus(event.target.value)}
          >
            <option value="TODO">To Do</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="DONE">Done</option>
          </select>

          <select
            value={assignedUserId}
            onChange={(event) => setAssignedUserId(Number(event.target.value))}
          >
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.username}
              </option>
            ))}
          </select>

          <button onClick={handleCreateTask}>
            Create Task
          </button>
        </div>

        <div className="tasks-section">
          <h3>Tasks</h3>

          {editingTask && (
            <div className="edit-task">
              <h3>Edit Task</h3>

              <input
                type="text"
                value={editingTask.name}
                onChange={(event) =>
                  setEditingTask({
                    ...editingTask,
                    name: event.target.value,
                  })
                }
              />

              <select
                value={editingTask.status}
                onChange={(event) =>
                  setEditingTask({
                    ...editingTask,
                    status: event.target.value,
                  })
                }
              >
                <option value="TODO">To Do</option>
                <option value="IN_PROGRESS">In Progress</option>
                <option value="DONE">Done</option>
              </select>

              <input
                type="date"
                value={editingTask.due_date || ""}
                onChange={(event) =>
                  setEditingTask({
                    ...editingTask,
                    due_date: event.target.value,
                  })
                }
              />

              <button onClick={handleUpdateTask}>
                Save Changes
              </button>

              <button onClick={() => setEditingTask(null)}>
                Cancel
              </button>

            </div>
          )}

          {tasks.map((task) => (
            <div className="task-card" key={task.id}>
              <div className="task-card-header">
                <h4>{task.name}</h4>

                <span className={`status-badge ${task.status.toLowerCase()}`}>
                  {task.status === "TODO"
                     ? "To Do"
                     : task.status === "IN_PROGRESS"
                     ? "In Progress"
                     : "Done"}
                </span>
              </div>

              <div className="task-details">
               <p className={`task-due-date ${getDueDateStatus(task.due_date)}`}>
                <strong>Due Date:</strong>{" "}
                {task.due_date ? task.due_date : "No due date"}
               </p>

               <p>
                <strong>Assigned to:</strong>{" "}
                {users.find((user) => user.id === task.user_id)?.username ||"Unassigned"}
               </p>
              </div>

              <div className="task-actions">
               <button onClick={() => handleEditTask(task)}>
                Edit
               </button>

               <button onClick={() => handleDeleteTask(task.id)}>
                Delete
               </button>
              </div>
            </div>
          ))}
        </div>

      </section>
    )}

    <section className="projects-section">

      <div className="create-project">
        <input
          type="text"
          placeholder="Enter project name"
          value={projectName}
          onChange={(event) => setProjectName(event.target.value)}
        />

        <button onClick={handleCreateProject}>
          Create Project
        </button>
      </div>

      <h2>My Projects</h2>

      <div className="projects-grid">
        {projects.map((project) => (
          <div
            className="project-card"
            key={project.id}
            onClick={() => {
             setSelectedProject(project)
             setEditingTask(null)
            }}
          >
           <div className="project-card-content">
           <h3>{project.project_name}</h3>

           <button
            className="delete-project-button"
            onClick={(event) => {
             event.stopPropagation()
             handleDeleteProject(project.id)
           }}
          >
           Delete
          </button>
        </div>
      </div>
        ))}
      </div>

    </section>

  </main>
</div>
  )
}

return (
  <div className="login-page">
      <div className="login-card">
        <h1>Task Management</h1>
        <p className="subtitle">Sign in to manage your tasks</p>

        <form onSubmit={handleLogin}>
          <label>Username</label>
          <input
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />

          <button type="submit">Login</button>
        </form>

        <p className="register-text">
          Don't have an account? <span>Register</span>
        </p>
      </div>
    </div>
  )
}

export default App