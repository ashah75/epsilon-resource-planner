import { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { parseCSV } from '../../utils/export';

/**
 * UploadModal - Modal for bulk uploading data via CSV
 * Props:
 *   isOpen: boolean - whether modal is visible
 *   onClose: function - callback to close modal
 */
export default function UploadModal({ isOpen, onClose }) {
  const { 
    bulkUploadPeople, 
    bulkUploadClients, 
    bulkUploadProjects, 
    bulkUploadAssignments 
  } = useApp();
  
  const [uploadType, setUploadType] = useState('people');
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState([]);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);

  // Reset form when modal opens/closes
  useEffect(() => {
    if (isOpen) {
      setUploadType('people');
      setFile(null);
      setPreview([]);
      setErrors({});
      setUploadResult(null);
    }
  }, [isOpen]);

  const handleTypeChange = (e) => {
    setUploadType(e.target.value);
    setFile(null);
    setPreview([]);
    setErrors({});
    setUploadResult(null);
  };

  const handleFileChange = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    // Validate file type
    if (!selectedFile.name.endsWith('.csv')) {
      setErrors({ file: 'Please select a CSV file' });
      return;
    }

    setFile(selectedFile);
    setErrors({});
    setUploadResult(null);

    // Parse and preview the file
    try {
      const text = await selectedFile.text();
      const parsed = parseCSV(text);
      
      if (parsed.length === 0) {
        setErrors({ file: 'CSV file is empty' });
        setPreview([]);
        return;
      }

      // Validate columns based on type
      const requiredColumns = getRequiredColumns(uploadType);
      const headers = Object.keys(parsed[0]);
      const missingColumns = requiredColumns.filter(col => !headers.includes(col));
      
      if (missingColumns.length > 0) {
        setErrors({ 
          file: `Missing required columns: ${missingColumns.join(', ')}`
        });
        setPreview([]);
        return;
      }

      // Show preview (first 5 rows)
      setPreview(parsed.slice(0, 5));
    } catch (error) {
      setErrors({ file: 'Failed to parse CSV file' });
      setPreview([]);
    }
  };

  const getRequiredColumns = (type) => {
    switch (type) {
      case 'people':
        return ['name', 'role'];
      case 'clients':
        return ['name'];
      case 'projects':
        return ['name', 'client_id'];
      case 'assignments':
        return ['person_id', 'project_id', 'start_date', 'end_date', 'percentage'];
      default:
        return [];
    }
  };

  const getCSVTemplate = (type) => {
    switch (type) {
      case 'people':
        return 'name,role\nJohn Doe,Developer\nJane Smith,Designer';
      case 'clients':
        return 'name\nAcme Corp\nTech Inc';
      case 'projects':
        return 'name,client_id\nWebsite Redesign,1\nMobile App,2';
      case 'assignments':
        return 'person_id,project_id,start_date,end_date,percentage\n1,1,2024-01-01,2024-03-31,50\n2,2,2024-02-01,2024-04-30,75';
      default:
        return '';
    }
  };

  const downloadTemplate = () => {
    const template = getCSVTemplate(uploadType);
    const blob = new Blob([template], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${uploadType}_template.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setErrors({ file: 'Please select a file' });
      return;
    }

    if (preview.length === 0) {
      setErrors({ file: 'No valid data to upload' });
      return;
    }

    setIsSubmitting(true);
    setErrors({});

    try {
      const text = await file.text();
      const data = parseCSV(text);
      
      let result;
      switch (uploadType) {
        case 'people':
          result = await bulkUploadPeople(data);
          break;
        case 'clients':
          result = await bulkUploadClients(data);
          break;
        case 'projects':
          result = await bulkUploadProjects(data);
          break;
        case 'assignments':
          result = await bulkUploadAssignments(data);
          break;
        default:
          throw new Error('Invalid upload type');
      }

      setUploadResult({
        success: true,
        message: `Successfully uploaded ${data.length} ${uploadType}`
      });

      // Close modal after 2 seconds
      setTimeout(() => {
        onClose();
      }, 2000);
    } catch (error) {
      setErrors({ 
        submit: error.message || 'Failed to upload data' 
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal modal-large">
        <div className="modal-header">
          <h2>Bulk Upload CSV</h2>
          <button className="close-button" onClick={onClose} aria-label="Close">
            ×
          </button>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {errors.submit && (
              <div className="error-message">{errors.submit}</div>
            )}
            
            {uploadResult && uploadResult.success && (
              <div className="success-message">
                ✓ {uploadResult.message}
              </div>
            )}
            
            <div className="form-group">
              <label htmlFor="uploadType">
                Upload Type <span className="required">*</span>
              </label>
              <select
                id="uploadType"
                value={uploadType}
                onChange={handleTypeChange}
                disabled={isSubmitting}
              >
                <option value="people">Team Members</option>
                <option value="clients">Clients</option>
                <option value="projects">Projects</option>
                <option value="assignments">Assignments</option>
              </select>
            </div>

            <div className="upload-instructions">
              <h3>CSV Format Instructions</h3>
              <p>
                Your CSV file must include the following columns:
              </p>
              <ul>
                {getRequiredColumns(uploadType).map(col => (
                  <li key={col}><code>{col}</code></li>
                ))}
              </ul>
              <button 
                type="button" 
                className="button button-secondary button-small"
                onClick={downloadTemplate}
              >
                📥 Download Template
              </button>
            </div>
            
            <div className="form-group">
              <label htmlFor="csvFile">
                Select CSV File <span className="required">*</span>
              </label>
              <input
                type="file"
                id="csvFile"
                accept=".csv"
                onChange={handleFileChange}
                className={errors.file ? 'error' : ''}
                disabled={isSubmitting}
              />
              {errors.file && (
                <span className="field-error">{errors.file}</span>
              )}
            </div>

            {preview.length > 0 && (
              <div className="preview-section">
                <h3>Preview (first 5 rows)</h3>
                <div className="table-container">
                  <table className="preview-table">
                    <thead>
                      <tr>
                        {Object.keys(preview[0]).map(header => (
                          <th key={header}>{header}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {preview.map((row, idx) => (
                        <tr key={idx}>
                          {Object.values(row).map((cell, cellIdx) => (
                            <td key={cellIdx}>{cell}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <p className="preview-note">
                  Total rows to upload: <strong>{preview.length}</strong>
                  {preview.length === 5 && ' (showing first 5)'}
                </p>
              </div>
            )}
          </div>
          
          <div className="modal-footer">
            <button 
              type="button" 
              className="button button-secondary" 
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="button button-primary"
              disabled={isSubmitting || !file || preview.length === 0}
            >
              {isSubmitting ? 'Uploading...' : `Upload ${uploadType}`}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
