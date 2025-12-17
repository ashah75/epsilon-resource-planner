import { useEffect, useRef, useState } from 'react';

const icons = {
  person: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="8" r="4" />
      <path d="M5 20c0-3.31 3.13-6 7-6s7 2.69 7 6" />
    </svg>
  ),
  client: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M4 7h16v12H4z" />
      <path d="M8 7V5h8v2" />
      <path d="M9 11h6M9 15h4" />
    </svg>
  ),
  project: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5 17l4-4 3 3 5-6" />
      <circle cx="6" cy="6" r="2" />
      <circle cx="12" cy="10" r="2" />
      <circle cx="18" cy="7" r="2" />
    </svg>
  ),
  assignment: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <rect x="4" y="5" width="16" height="14" rx="2" />
      <path d="M8 3v4M16 3v4M8 11h8M8 15h6" />
    </svg>
  ),
  upload: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 16V4" />
      <path d="M8 8l4-4 4 4" />
      <path d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2" />
    </svg>
  ),
  export: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v9" />
      <path d="M8 9l4-4 4 4" />
      <path d="M4 15v2a2 2 0 002 2h12a2 2 0 002-2v-2" />
    </svg>
  ),
  reports: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M4 20h16" />
      <path d="M7 20V10" />
      <path d="M12 20V4" />
      <path d="M17 20v-6" />
    </svg>
  ),
  back: (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M15 18l-6-6 6-6" />
    </svg>
  )
};

function IconBadge({ type }) {
  return <span className="icon-badge">{icons[type]}</span>;
}

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
          <img src="/epsilon-logo.svg" alt="Epsilon PS" />
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
                <IconBadge type="person" /> Add Team Member
              </button>
              <button onClick={() => handleAddAction('client')}>
                <IconBadge type="client" /> Add Client
              </button>
              <button onClick={() => handleAddAction('project')}>
                <IconBadge type="project" /> Add Project
              </button>
              <button onClick={() => handleAddAction('assignment')}>
                <IconBadge type="assignment" /> New Assignment
              </button>
              <button onClick={() => handleAddAction('upload')}>
                <IconBadge type="upload" /> Bulk Upload
              </button>
            </div>
          )}
        </div>

        <button className="btn ghost" onClick={onExport}>
          <IconBadge type="export" /> Export
        </button>

        <button
          className={`btn ghost ${showReports ? 'active' : ''}`}
          onClick={onToggleReports}
        >
          <IconBadge type={showReports ? 'back' : 'reports'} />
          {showReports ? 'Back to Timeline' : 'View Reports'}
        </button>
      </div>
    </header>
  );
}
