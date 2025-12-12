export default function Header({ openModal, onExport, onToggleReports, showReports }) {
  
  return (
    <header style={{ marginBottom: '0.75rem', animation: 'fadeInDown 0.6s ease-out' }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
        marginBottom: 0
      }}>
        <div style={{ flexShrink: 0 }}>
          <img 
            src="/epsilon-logo.svg" 
            alt="Epsilon PS" 
            style={{
              height: '48px',
              width: 'auto',
              maxWidth: '200px',
              objectFit: 'contain'
            }}
          />
        </div>
        
        <div style={{ flex: 1 }}>
          <h1 style={{
            fontFamily: "'Crimson Pro', serif",
            fontSize: '2.5rem',
            fontWeight: 600,
            letterSpacing: '-0.02em',
            marginBottom: '0.5rem',
            background: 'linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            Resource Planner
          </h1>
          <p style={{
            color: 'var(--text-secondary)',
            fontSize: '1.1rem',
            letterSpacing: '0.02em',
            margin: 0
          }}>
            Professional Services Team Management
          </p>
        </div>
        
        <div style={{
          display: 'flex',
          gap: '0.75rem',
          flexShrink: 0,
          animation: 'fadeIn 0.8s ease-out 0.2s both'
        }}>
          <button 
            className="btn-icon" 
            onClick={() => openModal('person')}
            title="Add Team Member"
          >
            <span>👤</span>
            <div className="tooltip">Add Team Member</div>
          </button>
          
          <button 
            className="btn-icon" 
            onClick={() => openModal('client')}
            title="Add Client"
          >
            <span>🏢</span>
            <div className="tooltip">Add Client</div>
          </button>
          
          <button 
            className="btn-icon" 
            onClick={() => openModal('project')}
            title="Add Project"
          >
            <span>📊</span>
            <div className="tooltip">Add Project</div>
          </button>
          
          <button 
            className="btn-icon" 
            onClick={() => openModal('assignment')}
            title="Assign to Project"
          >
            <span>📅</span>
            <div className="tooltip">Assign to Project</div>
          </button>
          
          <button 
            className="btn-icon" 
            onClick={() => openModal('upload')}
            title="Upload Data"
          >
            <span>📤</span>
            <div className="tooltip">Upload Data</div>
          </button>
          
          <button 
            className="btn-icon" 
            onClick={onExport}
            title="Export Data"
          >
            <span>📥</span>
            <div className="tooltip">Export Data</div>
          </button>
          
          <button 
            className={`btn-icon ${showReports ? 'active' : ''}`}
            onClick={onToggleReports}
            title={showReports ? "Back to Timeline" : "View Reports"}
          >
            <span>{showReports ? '📊' : '📈'}</span>
            <div className="tooltip">{showReports ? "Back to Timeline" : "View Reports"}</div>
          </button>
        </div>
      </div>
    </header>
  );
}
