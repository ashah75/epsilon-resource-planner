import { useEffect, useRef, useState } from 'react';

export default function Header({ openModal, onExport, onToggleReports, showReports }) {
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setShowMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleAddAction = (modal) => {
    openModal(modal);
    setShowMenu(false);
  };

  return (
    <header className="app-header">
      <div className="header-left">
        <div className="brand-mark">
          <img
            src="/epsilon-logo.svg"
            alt="Epsilon PS"
          />
        </div>
        <div className="brand-copy">
          <h1>Resource Planner</h1>
          <p>Professional Services Team Management</p>
        </div>
      </div>

      <div className="header-actions" ref={menuRef}>
        <div className="add-menu">
          <button
            className={`btn add-toggle ${showMenu ? 'open' : ''}`}
            onClick={() => setShowMenu(!showMenu)}
          >
            <span className="add-symbol">＋</span>
            Add
            <span className="chevron">▾</span>
          </button>

          {showMenu && (
            <div className="menu-dropdown">
              <button onClick={() => handleAddAction('person')}>
                <span>👤</span> Add Team Member
              </button>
              <button onClick={() => handleAddAction('client')}>
                <span>🏢</span> Add Client
              </button>
              <button onClick={() => handleAddAction('project')}>
                <span>📊</span> Add Project
              </button>
              <button onClick={() => handleAddAction('assignment')}>
                <span>📅</span> New Assignment
              </button>
              <button onClick={() => handleAddAction('upload')}>
                <span>📤</span> Bulk Upload
              </button>
            </div>
          )}
        </div>

        <button className="btn ghost" onClick={onExport}>
          📥 Export
        </button>

        <button
          className={`btn ghost ${showReports ? 'active' : ''}`}
          onClick={onToggleReports}
        >
          {showReports ? '⬅️ Back to Timeline' : '📈 View Reports'}
        </button>
      </div>
    </header>
  );
}
