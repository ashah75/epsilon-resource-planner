import { useState, useEffect } from 'react';
import { AppProvider, useApp } from './context/AppContext';
import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';
import Timeline from './components/timeline/Timeline';
import Reports from './components/reports/Reports';
import PersonModal from './components/modals/PersonModal';
import ClientModal from './components/modals/ClientModal';
import ProjectModal from './components/modals/ProjectModal';
import AssignmentModal from './components/modals/AssignmentModal';
import UploadModal from './components/modals/UploadModal';
import { exportToExcel } from './utils/export';
import './styles/globals.css';

function AppContent() {
  const { loading, error, loadAllData, people, clients, projects, assignments } = useApp();
  
  // Modal state
  const [activeModal, setActiveModal] = useState(null);
  const [editingItem, setEditingItem] = useState(null);
  const [preselectedPersonId, setPreselectedPersonId] = useState(null);
  const [preselectedProjectId, setPreselectedProjectId] = useState(null);
  const [prefilledDates, setPrefilledDates] = useState(null);
  
  // View state
  const [showReports, setShowReports] = useState(false);
  
  // Load all data on mount
  useEffect(() => {
    loadAllData();
  }, []);
  
  const openModal = (modalName, item = null) => {
    console.log('🔓 openModal called with:', modalName, item ? 'WITH ITEM' : 'NO ITEM');
    if (item) {
      console.log('🔓 Item data:', item);
    }
    setActiveModal(modalName);
    setEditingItem(item);
  };
  
  const closeModal = () => {
    setActiveModal(null);
    setEditingItem(null);
    setPreselectedPersonId(null);
    setPreselectedProjectId(null);
    setPrefilledDates(null);
  };
  
  const handleExport = () => {
    try {
      exportToExcel(people, clients, projects, assignments);
    } catch (error) {
      alert('Failed to export: ' + error.message);
    }
  };
  
  const handleAddAssignment = (personId = null, startDate = null, endDate = null, projectId = null) => {
    setPreselectedPersonId(personId);
    setPreselectedProjectId(projectId);
    setPrefilledDates(startDate && endDate ? { start_date: startDate, end_date: endDate } : null);
    setEditingItem(null);
    openModal('assignment');
  };
  
  const handleEditAssignment = (assignment) => {
    console.log('🎯 ==================== APP: handleEditAssignment CALLED ====================');
    console.log('🎯 Received assignment:', assignment);
    console.log('🎯 Assignment ID:', assignment?.id);
    console.log('🎯 Assignment dates:', assignment?.startDate, '→', assignment?.endDate);
    console.log('🎯 Assignment percentage:', assignment?.percentage);
    
    console.log('🎯 Clearing preselected values');
    setPreselectedPersonId(null);
    setPreselectedProjectId(null);
    setPrefilledDates(null);
    
    console.log('🎯 Opening modal with assignment directly');
    // Pass assignment directly to openModal to avoid async state issues
    openModal('assignment', assignment);
    
    console.log('🎯 ==================== END handleEditAssignment ====================');
  };
  
  const toggleReports = () => {
    setShowReports(!showReports);
  };
  
  if (loading) {
    return <div className="loading">Loading...</div>;
  }
  
  if (error) {
    return (
      <div className="error">
        <h2>Error Loading Data</h2>
        <p>{error}</p>
        <button className="button button-primary" onClick={loadAllData}>
          Retry
        </button>
      </div>
    );
  }
  
  return (
    <div className="app-container" style={{ 
      maxWidth: '1800px', 
      margin: '0 auto', 
      padding: '1rem' 
    }}>
      <Header 
        openModal={openModal}
        onExport={handleExport}
        onToggleReports={toggleReports}
        showReports={showReports}
      />
      
      {showReports ? (
        <Reports 
          people={people}
          clients={clients}
          projects={projects}
          assignments={assignments}
          onBack={toggleReports}
        />
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: '280px 1fr',
          gap: '0.75rem',
          animation: 'fadeIn 1s ease-out 0.4s both'
        }}>
          <Sidebar 
            openModal={openModal}
            onAddAssignment={handleAddAssignment}
          />
          <Timeline 
            onAddAssignment={handleAddAssignment}
            onEditAssignment={handleEditAssignment}
          />
        </div>
      )}
      
      {/* Modals */}
      {activeModal === 'person' && (
        <PersonModal 
          isOpen={true} 
          onClose={closeModal} 
          person={editingItem}
        />
      )}
      
      {activeModal === 'client' && (
        <ClientModal 
          isOpen={true} 
          onClose={closeModal} 
          client={editingItem}
        />
      )}
      
      {activeModal === 'project' && (
        <ProjectModal 
          isOpen={true} 
          onClose={closeModal} 
          project={editingItem}
        />
      )}
      
      {activeModal === 'assignment' && (() => {
        console.log('🎨 ==================== RENDERING AssignmentModal ====================');
        console.log('🎨 editingItem:', editingItem);
        console.log('🎨 preselectedPersonId:', preselectedPersonId);
        console.log('🎨 preselectedProjectId:', preselectedProjectId);
        console.log('🎨 prefilledDates:', prefilledDates);
        console.log('🎨 ==================== END RENDERING ====================');
        
        return (
          <AssignmentModal 
            isOpen={true} 
            onClose={closeModal}
            assignment={editingItem}
            preselectedPersonId={preselectedPersonId}
            preselectedProjectId={preselectedProjectId}
            prefilledDates={prefilledDates}
          />
        );
      })()}
      
      {activeModal === 'upload' && (
        <UploadModal 
          isOpen={true} 
          onClose={closeModal} 
        />
      )}
    </div>
  );
}

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;
