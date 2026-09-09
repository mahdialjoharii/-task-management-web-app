import "./App.css"

function App() {
  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Task Management</h1>
        <p className="subtitle">Sign in to manage your tasks</p>

        <form>
          <label>Username</label>
          <input
            type="text"
            placeholder="Enter your username"
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
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