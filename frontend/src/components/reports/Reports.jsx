import { useState, useMemo } from 'react';
import { parseDateString, getPeriodDates } from '../../utils/dates';
import { getClientColor } from '../../utils/colors';
import * as XLSX from 'xlsx';

/**
 * Reports Component - Comprehensive reporting view
 * Props:
 *   people: array - all team members
 *   clients: array - all clients
 *   projects: array - all projects
 *   assignments: array - all assignments
 *   onBack: function - callback to return to timeline
 */
export default function Reports({ people, clients, projects, assignments, onBack }) {
  const [currentPeriodOffset, setCurrentPeriodOffset] = useState(0);
  const [viewType, setViewType] = useState('team'); // 'team', 'project', 'client'

  // Generate 6 months for report
  const months = useMemo(() => {
    const result = [];
    for (let i = 0; i < 6; i++) {
      const period = getPeriodDates(currentPeriodOffset + i);
      result.push(period);
    }
    return result;
  }, [currentPeriodOffset]);

  // Calculate team allocation by month
  const teamAllocation = useMemo(() => {
    return people.map(person => {
      const personData = { person };
      months.forEach((month, idx) => {
        const monthAssignments = assignments.filter(a => {
          if (a.person_id !== person.id) return false;
          const assignStart = parseDateString(a.start_date);
          const assignEnd = parseDateString(a.end_date);
          return assignStart <= month.endDate && assignEnd >= month.startDate;
        });
        const total = monthAssignments.reduce((sum, a) => sum + a.percentage, 0);
        personData[`month${idx}`] = total;
      });
      return personData;
    });
  }, [people, months, assignments]);

  // Calculate project distribution
  const projectDistribution = useMemo(() => {
    return projects.map(project => {
      const projectAssignments = assignments.filter(a => a.project_id === project.id);
      const uniquePeople = [...new Set(projectAssignments.map(a => a.person_id))];
      const totalAllocation = projectAssignments.reduce((sum, a) => sum + a.percentage, 0);
      const client = clients.find(c => c.id === project.client_id);
      
      return {
        project,
        client,
        peopleCount: uniquePeople.length,
        totalAllocation,
        avgAllocation: uniquePeople.length > 0 ? totalAllocation / uniquePeople.length : 0
      };
    }).sort((a, b) => b.totalAllocation - a.totalAllocation);
  }, [projects, assignments, clients]);

  // Calculate client engagement
  const clientEngagement = useMemo(() => {
    return clients.map(client => {
      const clientProjects = projects.filter(p => p.client_id === client.id);
      const clientAssignments = assignments.filter(a => {
        const project = projects.find(p => p.id === a.project_id);
        return project && project.client_id === client.id;
      });
      const uniquePeople = [...new Set(clientAssignments.map(a => a.person_id))];
      const totalAllocation = clientAssignments.reduce((sum, a) => sum + a.percentage, 0);
      
      return {
        client,
        projectCount: clientProjects.length,
        peopleCount: uniquePeople.length,
        totalAllocation,
        color: getClientColor(client.id)
      };
    }).sort((a, b) => b.totalAllocation - a.totalAllocation);
  }, [clients, projects, assignments]);

  // Export to XLSX
  const handleExport = () => {
    const wb = XLSX.utils.book_new();

    // Team Allocation Sheet
    const teamData = [
      ['Person', 'Role', ...months.map(m => m.label)],
      ...teamAllocation.map(row => [
        row.person.name,
        row.person.role,
        ...months.map((_, idx) => `${row[`month${idx}`]}%`)
      ])
    ];
    const teamSheet = XLSX.utils.aoa_to_sheet(teamData);
    XLSX.utils.book_append_sheet(wb, teamSheet, 'Team Allocation');

    // Project Distribution Sheet
    const projectData = [
      ['Project', 'Client', 'People', 'Total Allocation', 'Avg Allocation'],
      ...projectDistribution.map(row => [
        row.project.name,
        row.client?.name || 'Unknown',
        row.peopleCount,
        `${row.totalAllocation}%`,
        `${Math.round(row.avgAllocation)}%`
      ])
    ];
    const projectSheet = XLSX.utils.aoa_to_sheet(projectData);
    XLSX.utils.book_append_sheet(wb, projectSheet, 'Project Distribution');

    // Client Engagement Sheet
    const clientData = [
      ['Client', 'Projects', 'People', 'Total Allocation'],
      ...clientEngagement.map(row => [
        row.client.name,
        row.projectCount,
        row.peopleCount,
        `${row.totalAllocation}%`
      ])
    ];
    const clientSheet = XLSX.utils.aoa_to_sheet(clientData);
    XLSX.utils.book_append_sheet(wb, clientSheet, 'Client Engagement');

    // Write file
    XLSX.writeFile(wb, 'resource-allocation-report.xlsx');
  };

  const getAllocationColor = (percentage) => {
    if (percentage > 100) return '#ef4444'; // Red - over-allocated
    if (percentage > 70) return '#f59e0b'; // Orange - high
    if (percentage > 30) return '#3b82f6'; // Blue - medium
    return '#10b981'; // Green - low
  };

  return (
    <div style={{
      background: 'var(--bg-secondary)',
      borderRadius: '12px',
      padding: '1.5rem',
      border: '1px solid var(--border)'
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1.5rem',
        paddingBottom: '1rem',
        borderBottom: '2px solid var(--border)'
      }}>
        <div>
          <h2 style={{
            fontFamily: "'Crimson Pro', serif",
            fontSize: '1.75rem',
            fontWeight: 600,
            marginBottom: '0.5rem'
          }}>
            Reports & Analytics
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', margin: 0 }}>
            {months[0].label} - {months[5].label}
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          {/* Period Navigation */}
          <button 
            className="btn-icon" 
            onClick={() => setCurrentPeriodOffset(currentPeriodOffset - 6)}
            title="Previous 6 Months"
          >
            <span>←</span>
          </button>
          <button 
            className="btn-icon" 
            onClick={() => setCurrentPeriodOffset(0)}
            title="Current Period"
          >
            <span>📅</span>
          </button>
          <button 
            className="btn-icon" 
            onClick={() => setCurrentPeriodOffset(currentPeriodOffset + 6)}
            title="Next 6 Months"
          >
            <span>→</span>
          </button>
          
          <div style={{ width: '1px', height: '32px', background: 'var(--border)', margin: '0 0.5rem' }} />
          
          {/* Export */}
          <button className="btn" onClick={handleExport}>
            📥 Export XLSX
          </button>
          
          {/* Back */}
          <button className="btn" onClick={onBack}>
            ← Back to Timeline
          </button>
        </div>
      </div>

      {/* View Tabs */}
      <div style={{
        display: 'flex',
        gap: '0.5rem',
        marginBottom: '1.5rem',
        borderBottom: '1px solid var(--border)',
        paddingBottom: '0.5rem'
      }}>
        <button
          className={`btn ${viewType === 'team' ? 'btn-active' : ''}`}
          onClick={() => setViewType('team')}
          style={{ padding: '0.5rem 1rem' }}
        >
          👥 Team Allocation
        </button>
        <button
          className={`btn ${viewType === 'project' ? 'btn-active' : ''}`}
          onClick={() => setViewType('project')}
          style={{ padding: '0.5rem 1rem' }}
        >
          📊 Project Distribution
        </button>
        <button
          className={`btn ${viewType === 'client' ? 'btn-active' : ''}`}
          onClick={() => setViewType('client')}
          style={{ padding: '0.5rem 1rem' }}
        >
          🏢 Client Engagement
        </button>
      </div>

      {/* Team Allocation View */}
      {viewType === 'team' && (
        <div style={{ overflowX: 'auto' }}>
          <table className="report-table">
            <thead>
              <tr>
                <th>Person</th>
                <th>Role</th>
                {months.map(month => (
                  <th key={month.label}>{month.label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {teamAllocation.map((row, idx) => (
                <tr key={idx}>
                  <td style={{ fontWeight: 600 }}>{row.person.name}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>{row.person.role}</td>
                  {months.map((_, mIdx) => {
                    const allocation = row[`month${mIdx}`];
                    return (
                      <td
                        key={mIdx}
                        style={{
                          color: getAllocationColor(allocation),
                          fontWeight: allocation > 100 ? 700 : 600,
                          textAlign: 'center'
                        }}
                      >
                        {allocation}%
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Project Distribution View */}
      {viewType === 'project' && (
        <div style={{ overflowX: 'auto' }}>
          <table className="report-table">
            <thead>
              <tr>
                <th>Project</th>
                <th>Client</th>
                <th>People</th>
                <th>Total Allocation</th>
                <th>Avg per Person</th>
              </tr>
            </thead>
            <tbody>
              {projectDistribution.map((row, idx) => (
                <tr key={idx}>
                  <td style={{ fontWeight: 600 }}>{row.project.name}</td>
                  <td>
                    <span
                      style={{
                        display: 'inline-block',
                        width: '12px',
                        height: '12px',
                        borderRadius: '50%',
                        background: getClientColor(row.client?.id),
                        marginRight: '0.5rem'
                      }}
                    />
                    {row.client?.name || 'Unknown'}
                  </td>
                  <td style={{ textAlign: 'center' }}>{row.peopleCount}</td>
                  <td style={{ textAlign: 'center', fontWeight: 600 }}>
                    {row.totalAllocation}%
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    {Math.round(row.avgAllocation)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Client Engagement View */}
      {viewType === 'client' && (
        <div style={{ overflowX: 'auto' }}>
          <table className="report-table">
            <thead>
              <tr>
                <th>Client</th>
                <th>Projects</th>
                <th>People</th>
                <th>Total Allocation</th>
              </tr>
            </thead>
            <tbody>
              {clientEngagement.map((row, idx) => (
                <tr key={idx}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span
                        style={{
                          display: 'inline-block',
                          width: '16px',
                          height: '16px',
                          borderRadius: '50%',
                          background: row.color
                        }}
                      />
                      <span style={{ fontWeight: 600 }}>{row.client.name}</span>
                    </div>
                  </td>
                  <td style={{ textAlign: 'center' }}>{row.projectCount}</td>
                  <td style={{ textAlign: 'center' }}>{row.peopleCount}</td>
                  <td style={{ textAlign: 'center', fontWeight: 600 }}>
                    {row.totalAllocation}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
