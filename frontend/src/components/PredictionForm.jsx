import React, { useState } from 'react';
import { predictionService } from '../services/api';
import ResultCard from './ResultCard';

function PredictionForm() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [formData, setFormData] = useState({
    gender: 'Male',
    senior_citizen: 0,
    partner: 'Yes',
    dependents: 'No',
    tenure: 12,
    phone_service: 'Yes',
    internet_service: 'DSL',
    online_security: 'No',
    online_backup: 'No',
    device_protection: 'No',
    tech_support: 'No',
    streaming_tv: 'No',
    streaming_movies: 'No',
    contract: 'Month-to-month',
    paperless_billing: 'Yes',
    payment_method: 'Electronic check',
    monthly_charges: 65.0,
    total_charges: 780.0,
  });

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'number' ? parseFloat(value) : (name === 'senior_citizen' ? parseInt(value) : value),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await predictionService.predict(formData);
      if (response.success) {
        setResult(response);
      } else {
        setError(response.error || 'Prediction failed');
      }
    } catch (err) {
      setError(err.error || 'Failed to make prediction. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h2 className="card-title" style={{ marginBottom: '30px' }}>Customer Information</h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
          {/* Gender */}
          <div className="form-group">
            <label className="form-label">Gender</label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>

          {/* Senior Citizen */}
          <div className="form-group">
            <label className="form-label">Senior Citizen</label>
            <select
              name="senior_citizen"
              value={formData.senior_citizen}
              onChange={handleChange}
              className="form-select"
            >
              <option value="0">No</option>
              <option value="1">Yes</option>
            </select>
          </div>

          {/* Partner */}
          <div className="form-group">
            <label className="form-label">Partner</label>
            <select
              name="partner"
              value={formData.partner}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>

          {/* Dependents */}
          <div className="form-group">
            <label className="form-label">Dependents</label>
            <select
              name="dependents"
              value={formData.dependents}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>

          {/* Tenure */}
          <div className="form-group">
            <label className="form-label">Tenure (months)</label>
            <input
              type="number"
              name="tenure"
              value={formData.tenure}
              onChange={handleChange}
              min="0"
              max="72"
              className="form-input"
            />
          </div>

          {/* Phone Service */}
          <div className="form-group">
            <label className="form-label">Phone Service</label>
            <select
              name="phone_service"
              value={formData.phone_service}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>

          {/* Internet Service */}
          <div className="form-group">
            <label className="form-label">Internet Service</label>
            <select
              name="internet_service"
              value={formData.internet_service}
              onChange={handleChange}
              className="form-select"
            >
              <option value="DSL">DSL</option>
              <option value="Fiber optic">Fiber optic</option>
              <option value="No">No internet service</option>
            </select>
          </div>

          {/* Online Security */}
          <div className="form-group">
            <label className="form-label">Online Security</label>
            <select
              name="online_security"
              value={formData.online_security}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          {/* Online Backup */}
          <div className="form-group">
            <label className="form-label">Online Backup</label>
            <select
              name="online_backup"
              value={formData.online_backup}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          {/* Device Protection */}
          <div className="form-group">
            <label className="form-label">Device Protection</label>
            <select
              name="device_protection"
              value={formData.device_protection}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          {/* Tech Support */}
          <div className="form-group">
            <label className="form-label">Tech Support</label>
            <select
              name="tech_support"
              value={formData.tech_support}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          {/* Streaming TV */}
          <div className="form-group">
            <label className="form-label">Streaming TV</label>
            <select
              name="streaming_tv"
              value={formData.streaming_tv}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          {/* Streaming Movies */}
          <div className="form-group">
            <label className="form-label">Streaming Movies</label>
            <select
              name="streaming_movies"
              value={formData.streaming_movies}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
              <option value="No internet service">No internet service</option>
            </select>
          </div>

          {/* Contract */}
          <div className="form-group">
            <label className="form-label">Contract Type</label>
            <select
              name="contract"
              value={formData.contract}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Month-to-month">Month-to-month</option>
              <option value="One year">One year</option>
              <option value="Two year">Two year</option>
            </select>
          </div>

          {/* Paperless Billing */}
          <div className="form-group">
            <label className="form-label">Paperless Billing</label>
            <select
              name="paperless_billing"
              value={formData.paperless_billing}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>

          {/* Payment Method */}
          <div className="form-group">
            <label className="form-label">Payment Method</label>
            <select
              name="payment_method"
              value={formData.payment_method}
              onChange={handleChange}
              className="form-select"
            >
              <option value="Electronic check">Electronic check</option>
              <option value="Mailed check">Mailed check</option>
              <option value="Bank transfer (automatic)">Bank transfer (automatic)</option>
              <option value="Credit card (automatic)">Credit card (automatic)</option>
            </select>
          </div>

          {/* Monthly Charges */}
          <div className="form-group">
            <label className="form-label">Monthly Charges ($)</label>
            <input
              type="number"
              name="monthly_charges"
              value={formData.monthly_charges}
              onChange={handleChange}
              min="0"
              step="0.01"
              className="form-input"
            />
          </div>

          {/* Total Charges */}
          <div className="form-group">
            <label className="form-label">Total Charges ($)</label>
            <input
              type="number"
              name="total_charges"
              value={formData.total_charges}
              onChange={handleChange}
              min="0"
              step="0.01"
              className="form-input"
            />
          </div>
        </div>

        {error && <div className="form-error" style={{ marginTop: '20px' }}>{error}</div>}

        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary btn-large"
          style={{
            width: '100%',
            marginTop: '30px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '10px',
          }}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Analyzing Customer...
            </>
          ) : (
            '🔮 Predict Churn'
          )}
        </button>
      </form>

      <ResultCard result={result} />
    </div>
  );
}

export default PredictionForm;
