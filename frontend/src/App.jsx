import { useState } from "react"
import "./App.css"

function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [loggedIn, setLoggedIn] = useState(false)
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

  console.log("Current user:", meData)
}
  } catch (error) {
    console.error("Login error:", error)
  }
}

  if (loggedIn) {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome to Task Management!</p>
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