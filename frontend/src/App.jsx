import { useState, useEffect, useRef } from "react"
import "./App.css"

function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [email, setEmail] = useState("")
  const [registerMode, setRegisterMode] = useState(false)
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
  const [assignedUserId, setAssignedUserId] = useState("")
  const [currentUserId, setCurrentUserId] = useState(null)
  const [editingTask, setEditingTask] = useState(null)
  const [editingProject, setEditingProject] = useState(null)
  const [draggedTask, setDraggedTask] = useState(null)
  const [profileOpen, setProfileOpen] = useState(false)
  const [accountOpen, setAccountOpen] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [comments, setComments] = useState([]);
  const commentsRef = useRef(null)
  const [commentText, setCommentText] = useState("");
  const [commentsLoading, setCommentsLoading] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);

  useEffect(() => {
  const handleClickOutside = () => {
    if (editingProject) {
      setEditingProject(null)
    }
  }

  document.addEventListener("click", handleClickOutside)

  return () => {
    document.removeEventListener("click", handleClickOutside)
  }
}, [editingProject])

  useEffect(() => {
   const token = localStorage.getItem("token")

   if (!token) return

   const restoreSession = async () => {
     try {
       const response = await fetch("http://127.0.0.1:8000/users/me", {
         headers: {
           Authorization: `Bearer ${token}`,
         },
        })

        if (!response.ok) {
         localStorage.removeItem("token")
         return
        }

        const data = await response.json()

        setCurrentUserId(data.user_id)
        setLoggedIn(true)

        console.log("Session restored:", data)
      } catch (error) {
        console.error("Restore session error:", error)
      }
    }

    restoreSession()
  }, [])

  useEffect(() => {
   const handleClickOutside = (event) => {
     if (
       profileOpen &&
       !event.target.closest(".profile-section")
      ) {
       setProfileOpen(false)
        }
    }

   document.addEventListener("click", handleClickOutside)

   return () => {
     document.removeEventListener("click", handleClickOutside)
    }
  }, [profileOpen])

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
  setAssignedUserId(meData.user_id)

  console.log("Current user:", meData)
}
 else {
  alert(data.detail || "Invalid username or password")
 }
  } catch (error) {
    console.error("Login error:", error)
  }
}

const handleRegister = async (event) => {
  event.preventDefault()

  if (!username.trim() || !email.trim() || !password.trim()) {
    alert("Please fill in all fields")
    return
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/users/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    })

    const data = await response.json()

    console.log("Register status:", response.status)
    console.log("Register response:", data)

    if (response.ok) {
      alert("Account created successfully!")

      setUsername("")
      setEmail("")
      setPassword("")
      setRegisterMode(false)
    } else {
      alert(data.detail || "Registration failed")
    }
  } catch (error) {
    console.error("Register error:", error)
    alert("Something went wrong. Please try again.")
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
    if (!response.ok) {
     alert(data.detail || "Failed to create project")
     return
    }

    setProjects((currentProjects) => [...currentProjects, data])
    setProjectName("")
  } catch (error) {
    console.error("Create project error:", error)
  }
}

const handleEditProject = (project) => {
  setEditingProject({
    id: project.id,
    project_name: project.project_name,
  })
}

const handleUpdateProject = async () => {
  if (!editingProject.project_name.trim()) {
    alert("Please enter a project name")
    return
  }

  const token = localStorage.getItem("token")

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/projects/${editingProject.id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          project_name: editingProject.project_name,
        }),
      }
    )

    const data = await response.json()

    console.log("Update project status:", response.status)
    console.log("Updated project:", data)

    if (!response.ok) {
      const errorMessage = Array.isArray(data.detail)
        ? data.detail.map((error) => error.msg).join(", ")
        : data.detail || "Failed to update project"

      alert(errorMessage)
      return
    }

    setProjects((currentProjects) =>
      currentProjects.map((project) =>
        project.id === data.id ? data : project
      )
    )

    if (selectedProject?.id === data.id) {
      setSelectedProject(data)
    }

    setEditingProject(null)
  } catch (error) {
    console.error("Update project error:", error)
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

    if (!response.ok) {
     alert(data.detail || "Failed to delete project")
     return
    }

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

  if (!assignedUserId) {
   alert("Please select an assigned user")
   return
  }

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
        assigned_user_id: Number(assignedUserId),
        status: taskStatus,
        due_date: taskDueDate,
      }),
    })

    const data = await response.json()

    console.log("Create task status:", response.status)
    console.log("Created task:", data)
    console.log(
     "Create task error details:",
     JSON.stringify(data.detail, null, 2)
    )
   if (!response.ok) {
    const errorMessage = Array.isArray(data.detail)
     ? data.detail
        .map((error) => error.msg)
        .join(", ")
     : data.detail || "Failed to create task"

    alert(errorMessage)
    return
   }

    setTasks((currentTasks) => [...currentTasks, data])
    setTaskName("")
    setTaskDueDate("")
    setTaskStatus("TODO")
    setAssignedUserId(currentUserId)
  } catch (error) {
    console.error("Create task error:", error)
  }
}

const handleDragStart = (task) => {
  setDraggedTask(task)
}

const handleDragOver = (event) => {
  event.preventDefault()
}

const handleDrop = async (newStatus) => {
  if (!draggedTask) return

  if (draggedTask.status === newStatus) {
    setDraggedTask(null)
    return
  }

  const token = localStorage.getItem("token")

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/tasks/${draggedTask.id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          status: newStatus,
        }),
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.detail || "Failed to update task status")
      return
    }

    setTasks((currentTasks) =>
      currentTasks.map((task) =>
        task.id === data.id ? data : task
      )
    )

  } catch (error) {
    console.error("Drag and drop error:", error)
  }

  setDraggedTask(null)
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

    if (!response.ok) {
     alert(data.detail || "Failed to delete task")
     return
    }

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

  if (!editingTask.name.trim()) {
   alert("Please enter a task name")
   return
  }

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

    if (!response.ok) {
     alert(data.detail || "Failed to update task")
     return
    }

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

const fetchComments = async (taskId) => {
  setCommentsLoading(true);

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/comments/?task_id=${taskId}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error("Failed to fetch comments");
    }

    const data = await response.json();
    setComments(data);
  } catch (error) {
    console.error("Error fetching comments:", error);
    setComments([]);
  } finally {
    setCommentsLoading(false);
  }
};

const handleSelectTask = (task) => {
  setSelectedTask(task)
  setCommentText("")
  fetchComments(task.id)
}

const handleCreateComment = async () => {
  if (!selectedTask || !commentText.trim()) {
    return
  }

  const token = localStorage.getItem("token")

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/comments/?task_id=${selectedTask.id}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          content: commentText,
        }),
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.detail || "Failed to create comment")
      return
    }

    setComments((currentComments) => [...currentComments, data])
    setCommentText("")
  } catch (error) {
    console.error("Create comment error:", error)
  }
}

const handleDeleteComment = async (commentId) => {
  const confirmDelete = window.confirm(
    "Are you sure you want to delete this comment?"
  )

  if (!confirmDelete) {
    return
  }

  const token = localStorage.getItem("token")

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/comments/${commentId}`,
      {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.detail || "Failed to delete comment")
      return
    }

    setComments((currentComments) =>
      currentComments.filter((comment) => comment.id !== commentId)
    )
  } catch (error) {
    console.error("Delete comment error:", error)
  }
}

useEffect(() => {
  const handleClickOutside = (event) => {
    if (
      commentsRef.current &&
      !commentsRef.current.contains(event.target)
    ) {
      setSelectedTask(null)
      setComments([])
      setCommentText("")
    }
  }

  document.addEventListener("mousedown", handleClickOutside)

  return () => {
    document.removeEventListener("mousedown", handleClickOutside)
  }
}, [])

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
      if (!Array.isArray(data)) {
        console.error("Failed to fetch projects:", data)
        return
      }

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
      if (!Array.isArray(data)) {
        console.error("Failed to fetch users:", data)
        return
      }

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
      if (!Array.isArray(data)) {
        console.error("Failed to fetch tasks:", data)
        return
      }

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
    <>
   {accountOpen && (
    <div className="account-overlay">
     <div className="account-card">

       <button
         className="account-close"
         onClick={() => setAccountOpen(false)}
       >
         ×
       </button>

       <div className="account-avatar">
         {currentUsername.charAt(0).toUpperCase()}
       </div>

       <h2>{currentUsername}</h2>

       <p>Account ID: {currentUserId}</p>

       <button
         className="account-logout"
         onClick={handleLogout}
       >
         🚪 Logout
       </button>

      </div>
    </div>
    
 )}

  
    < div className={`dashboard ${sidebarOpen ? "sidebar-open" : "sidebar-closed"}`}>

      <aside className={`sidebar ${sidebarOpen ? "open" : "closed"}`}>
       <div className="sidebar-logo">
        <h2>Task Manager</h2>
       </div>

       <nav className="sidebar-nav">
        <button className="active">🏠 Dashboard</button>

        <button
         onClick={() => {
          document
          .querySelector(".projects-section")
          ?.scrollIntoView({ behavior: "smooth" })
         }}
       >
         📁 Projects
        </button>
       </nav>

       <div className="sidebar-bottom">
        <button className="sidebar-logout" onClick={handleLogout}>
         🚪 Logout
        </button>
       </div>
      </aside>

  <header className="dashboard-header">
    <button
     className="sidebar-toggle"
     onClick={() => setSidebarOpen(!sidebarOpen)} 
    >
     ☰
    </button>

   <div>
     <h1>Dashboard</h1>
     <p>Welcome back, {currentUsername} !</p>
   </div>

   <div className="profile-section">

     <div
      className="profile-info"
      onClick={() => setProfileOpen(!profileOpen)}
     >
      <div className="profile-avatar">
       {currentUsername.charAt(0).toUpperCase()}
      </div>

      <div>
       <strong>{currentUsername} </strong>
       <span>Account</span>
      </div>

      <span className="profile-arrow">
       {profileOpen ? "▲" : "▼"}
      </span>
     </div>

      {profileOpen && (
       <div className="profile-dropdown">
        <button
         onClick={() => {
         setAccountOpen(true)
         setProfileOpen(false)
         }}
        >
         👤 My Account
        </button>

        <button onClick={handleLogout}>
         🚪 Logout
        </button>
       </div>
       
      )}

    </div>
  </header>

  <main className="dashboard-content">

    <div className="stats-grid">
     <div className="stat-card">
      <div className="stat-card-top">
       <span>Total Tasks</span>
       <span className="stat-icon">📋</span>
      </div>
      <strong>{totalTasks}</strong>
     </div>

     <div className="stat-card">
      <div className="stat-card-top">
       <span>To Do</span>
       <span className="stat-icon">📝</span>
      </div>
      <strong>{todoTasks}</strong>
     </div>

     <div className="stat-card">
      <div className="stat-card-top">
       <span>In Progress</span>
       <span className="stat-icon">🔄</span>
      </div>
      <strong>{inProgressTasks}</strong>
     </div>

     <div className="stat-card">
      <div className="stat-card-top">
       <span>Completed</span>
       <span className="stat-icon">✅</span>
      </div>
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
        
        {selectedProject?.user_id === currentUserId && (
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
           onChange={(e) => setAssignedUserId(Number(e.target.value))}
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
        </div>)}

        <div className="tasks-section">
          
          <div className="kanban-board">
            <div
             className="kanban-column"
             onDragOver={handleDragOver}
             onDrop={() => handleDrop("TODO")}
            >
             <h3>To Do</h3>

             {tasks
                .filter((task) => task.status === "TODO")
                .map((task) => (
                  <div
                   className="kanban-task"
                   key={task.id}
                   draggable={true}
                   onDragStart={() => handleDragStart(task)}
                   onClick={() => handleSelectTask(task)}
                  >
                   <div className="kanban-task-name">
                   {task.name}
                   </div>

                   <span className={`status-badge ${task.status.toLowerCase()}`}>
                   {task.status === "TODO"
                    ? "To Do"
                    : task.status === "IN_PROGRESS"
                    ? "In Progress"
                    : "Done"}
                   </span>

                    {task.due_date && (
                      <div className={`kanban-task-date ${getDueDateStatus(task.due_date)}`}>
                       Due: {task.due_date}

                       {getDueDateStatus(task.due_date) === "overdue" && (
                        <span> 🔴 Overdue</span>
                       )}

                       {getDueDateStatus(task.due_date) === "soon" && (
                        <span> 🟠 Soon</span>
                       )}
                      </div>
                    )}

                    {task.user_id === currentUserId ? (
                     <span className="assigned-to-you">
                      ⭐ Assigned to you
                     </span>
                    ) : (
                     <span className="assigned-to">
                       👤 Assigned to:{" "}
                       {users.find((user) => user.id === task.user_id)?.username || "Unknown user"}
                     </span>
                    )}

                    <div className="kanban-task-actions">
                      <button
                         className="edit-task-button"
                         onClick={(event) => {
                          event.stopPropagation()
                          handleEditTask(task)
                         }}
                      >
                         Edit
                      </button>

                      {selectedProject?.user_id === currentUserId && (
                        <button
                         className="delete-task-button"
                         onClick={(event) => {
                           event.stopPropagation()
                           handleDeleteTask(task.id)
                         }}
                        >
                         Delete
                        </button>
                     )}
                   </div>

                  </div>
               ))}
            </div>

            <div
             className="kanban-column"
             onDragOver={handleDragOver}
             onDrop={() => handleDrop("IN_PROGRESS")}
            >
             <h3>In Progress</h3>

             {tasks
              .filter((task) => task.status === "IN_PROGRESS")
              .map((task) => (
               <div
                   className="kanban-task"
                   key={task.id}
                   draggable={true}
                   onDragStart={() => handleDragStart(task)}
                   onClick={() => handleSelectTask(task)}
                  >
                   <div className="kanban-task-name">
                   {task.name}
                   </div>

                   <span className={`status-badge ${task.status.toLowerCase()}`}>
                   {task.status === "TODO"
                    ? "To Do"
                    : task.status === "IN_PROGRESS"
                    ? "In Progress"
                    : "Done"}
                   </span>

                    {task.due_date && (
                      <div className={`kanban-task-date ${getDueDateStatus(task.due_date)}`}>
                       Due: {task.due_date}

                       {getDueDateStatus(task.due_date) === "overdue" && (
                        <span> 🔴 Overdue</span>
                       )}

                       {getDueDateStatus(task.due_date) === "soon" && (
                        <span> 🟠 Soon</span>
                       )}
                      </div>
                    )}

                    {task.user_id === currentUserId ? (
                     <span className="assigned-to-you">
                      ⭐ Assigned to you
                     </span>
                    ) : (
                     <span className="assigned-to">
                       👤 Assigned to:{" "}
                       {users.find((user) => user.id === task.user_id)?.username || "Unknown user"}
                     </span>
                    )}

                    <div className="kanban-task-actions">
                      <button
                         className="edit-task-button"
                         onClick={(event) => {
                          event.stopPropagation()
                          handleEditTask(task)
                         }}
                      >
                         Edit
                      </button>

                      {selectedProject?.user_id === currentUserId && (
                        <button
                         className="delete-task-button"
                         onClick={(event) => {
                           event.stopPropagation()
                           handleDeleteTask(task.id)
                         }}
                        >
                         Delete
                        </button>
                     )}
                   </div>

                  </div>
              ))}
            </div>

            <div
             className="kanban-column"
             onDragOver={handleDragOver}
             onDrop={() => handleDrop("DONE")}
            >
             <h3>Done</h3>

            {tasks
             .filter((task) => task.status === "DONE")
             .map((task) => (
              <div
                   className="kanban-task"
                   key={task.id}
                   draggable={true}
                   onDragStart={() => handleDragStart(task)}
                   onClick={() => handleSelectTask(task)}
                  >
                   <div className="kanban-task-name">
                   {task.name}
                   </div>

                   <span className={`status-badge ${task.status.toLowerCase()}`}>
                   {task.status === "TODO"
                    ? "To Do"
                    : task.status === "IN_PROGRESS"
                    ? "In Progress"
                    : "Done"}
                   </span>

                    {task.due_date && (
                      <div className={`kanban-task-date ${getDueDateStatus(task.due_date)}`}>
                       Due: {task.due_date}

                       {getDueDateStatus(task.due_date) === "overdue" && (
                        <span> 🔴 Overdue</span>
                       )}

                       {getDueDateStatus(task.due_date) === "soon" && (
                        <span> 🟠 Soon</span>
                       )}
                      </div>
                    )}

                    {task.user_id === currentUserId ? (
                     <span className="assigned-to-you">
                      ⭐ Assigned to you
                     </span>
                    ) : (
                     <span className="assigned-to">
                       👤 Assigned to:{" "}
                       {users.find((user) => user.id === task.user_id)?.username || "Unknown user"}
                     </span>
                    )}

                    <div className="kanban-task-actions">
                      <button
                         className="edit-task-button"
                         onClick={(event) => {
                          event.stopPropagation()
                          handleEditTask(task)
                         }}
                      >
                         Edit
                      </button>

                      {selectedProject?.user_id === currentUserId && (
                        <button
                         className="delete-task-button"
                         onClick={(event) => {
                           event.stopPropagation()
                           handleDeleteTask(task.id)
                         }}
                        >
                         Delete
                        </button>
                     )}
                   </div>

                  </div>
             ))}
            </div>
          </div>

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

          {selectedTask && (
            <div
              className="comments-section"
              ref={commentsRef}
            >
              <h3>Comments</h3>

              {comments.length === 0 ? (
              <p>No comments yet.</p>
            ) : (
              <div className="comments-list">
               {comments.map((comment) => {
                 const commentUser = users.find(
                  (user) => user.id === comment.user_id
                 )

                 return (
                  <div className="comment" key={comment.id}>
                   <strong>
                    {commentUser ? commentUser.username : "Unknown User"}
                   </strong>

                   <p>{comment.content}</p>

                   {(() => {
                      const taskProject = projects.find(
                       (project) => project.id === selectedTask.project_id
                      )

                      const canDeleteComment =
                        comment.user_id === currentUserId ||
                        taskProject?.user_id === currentUserId

                      return canDeleteComment ? (
                        <button
                          className="delete-comment"
                          onClick={() => handleDeleteComment(comment.id)}
                        >
                         Delete
                        </button>
                      ) : null
                    })()}
                  </div>
                 )
                })}
              </div>
            )}

            <div className="comment-form">
             <input
              type="text"
              placeholder="Write a comment..."
              value={commentText}
              onChange={(event) => setCommentText(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                handleCreateComment()
                }
              }}
             />

             <button onClick={handleCreateComment}>
              Add Comment
             </button>
            </div>
          </div>
        )}

          
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
           <div
            className="project-card-content"
            key={project.id}
            onClick={(event) => {
              event.stopPropagation()

              if (editingProject?.id === project.id) {
               return
              }

              setSelectedProject(project)
              setEditingTask(null)
            }}
           >
            <div>
             {editingProject?.id === project.id ? (
              <input
               type="text"
               value={editingProject.project_name}
               onChange={(event) =>
                setEditingProject({
                  ...editingProject,
                 project_name: event.target.value,
                })
               }
               onClick={(event) => event.stopPropagation()}
              />
            ) : (
              <h3>{project.project_name}</h3>
            )}
             <br></br>
            </div>

            {project.user_id === currentUserId && (
             <>
               {editingProject?.id === project.id ? (
                <>
                  <button
                    className="save-project-button"
                    onClick={(event) => {
                      event.stopPropagation()
                      handleUpdateProject()
                    }}
                  >
                    Save Changes
                  </button>

                  <button
                   className="cancel-project-button"
                   onClick={(event) => {
                     event.stopPropagation()
                     setEditingProject(null)
                    }}
                  >
                    Cancel
                  </button>
                </>
              ) : (
                <button
                  className="edit-project-button"
                  onClick={(event) => {
                    event.stopPropagation()
                    handleEditProject(project)
                  }}
                >
                  Edit
                </button>
              )}
            </>
          )}

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
</>
  )
}

return (
  <div className="login-page">
      <div className="login-card">
        <h1>Task Management</h1>
        <p className="subtitle">Sign in to manage your tasks</p>

        <form onSubmit={registerMode ? handleRegister : handleLogin}>
          <label>Username</label>

            <input
             type="text"
             placeholder="Enter your username"
             value={username}
             onChange={(event) => setUsername(event.target.value)}
            />

           {registerMode && (
            <>
           <label>Email</label>

           <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
            </>
        )}

        <label>Password</label>

         <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
         />

         <button type="submit">
          {registerMode ? "Register" : "Login"}
         </button>
        </form>

        <p className="register-text">
         {registerMode
          ? "Already have an account?"
          : "Don't have an account?"}{" "}

          <span onClick={() => setRegisterMode(!registerMode)}>
          {registerMode ? "Login" : "Register"}
          </span>
        </p>
      </div>
    </div>
  )
}

export default App