import { useState } from 'react'

function Auth({ onAuthenticate }) {
  const [password, setPassword] = useState('')
  const [error, setError] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    
    // Password for Prof. Shen (you can change this)
    if (password === 'submarine2026') {
      sessionStorage.setItem('authenticated', 'true')
      onAuthenticate()
    } else {
      setError(true)
      setPassword('')
    }
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      backgroundColor: '#f5f5f5'
    }}>
      <div style={{ 
        backgroundColor: 'white', 
        padding: '3rem 2.5rem', 
        borderRadius: '12px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
        maxWidth: '420px',
        width: '100%'
      }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🔒</div>
          <h2 style={{ 
            margin: '0 0 0.5rem 0', 
            fontSize: '1.75rem',
            fontWeight: 700,
            color: '#1a1a1a'
          }}>
            Research Dashboard
          </h2>
          <p style={{ color: '#666', fontSize: '0.95rem', margin: 0 }}>
            Global Digital Infrastructure Political Economy Observatory
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ 
              display: 'block', 
              fontSize: '0.875rem', 
              fontWeight: 600,
              color: '#333',
              marginBottom: '0.5rem'
            }}>
              Access Password
            </label>
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value)
                setError(false)
              }}
              autoFocus
              style={{
                width: '100%',
                padding: '0.875rem 1rem',
                border: error ? '2px solid #e74c3c' : '2px solid #e0e0e0',
                borderRadius: '6px',
                fontSize: '1rem',
                outline: 'none',
                transition: 'border-color 0.2s',
                boxSizing: 'border-box'
              }}
              onFocus={(e) => e.target.style.borderColor = '#2196f3'}
              onBlur={(e) => e.target.style.borderColor = error ? '#e74c3c' : '#e0e0e0'}
            />
          </div>

          {error && (
            <div style={{ 
              padding: '0.75rem 1rem',
              backgroundColor: '#ffebee',
              border: '1px solid #ef5350',
              borderRadius: '6px',
              marginBottom: '1.5rem'
            }}>
              <p style={{ 
                color: '#c62828', 
                fontSize: '0.875rem', 
                margin: 0,
                fontWeight: 500
              }}>
                ⚠️ Incorrect password. Please try again.
              </p>
            </div>
          )}

          <button
            type="submit"
            style={{
              width: '100%',
              padding: '0.875rem',
              backgroundColor: '#2196f3',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              fontSize: '1rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.target.style.backgroundColor = '#1976d2'}
            onMouseOut={(e) => e.target.style.backgroundColor = '#2196f3'}
          >
            Access Dashboard
          </button>
        </form>

        <div style={{ 
          marginTop: '2rem', 
          paddingTop: '1.5rem',
          borderTop: '1px solid #e0e0e0',
          textAlign: 'center'
        }}>
          <p style={{ fontSize: '0.8rem', color: '#999', margin: 0 }}>
            This dashboard contains research data for authorized users only.
          </p>
          <p style={{ fontSize: '0.75rem', color: '#bbb', marginTop: '0.5rem' }}>
            For access credentials, contact the research team.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Auth