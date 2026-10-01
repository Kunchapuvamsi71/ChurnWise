import React from 'react';

function ResultCard({ result }) {
  if (!result) return null;

  const getRiskColor = () => {
    if (result.risk_level === 'HIGH') return '#ef4444';
    if (result.risk_level === 'MEDIUM') return '#f59e0b';
    return '#10b981';
  };

  const getRiskBgColor = () => {
    if (result.risk_level === 'HIGH') return 'rgba(239, 68, 68, 0.1)';
    if (result.risk_level === 'MEDIUM') return 'rgba(245, 158, 11, 0.1)';
    return 'rgba(16, 185, 129, 0.1)';
  };

  const probability = Math.round(result.probability * 100);

  return (
    <div className="card" style={{ marginTop: '30px' }}>
      <h2 className="card-title" style={{ marginBottom: '30px' }}>Prediction Result</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '30px', marginBottom: '30px' }}>
        {/* Churn Probability */}
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '150px',
            height: '150px',
            margin: '0 auto',
            borderRadius: '50%',
            background: `conic-gradient(${getRiskColor()} 0deg ${probability * 3.6}deg, rgba(148, 163, 184, 0.2) ${probability * 3.6}deg 360deg)`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: `0 0 20px ${getRiskColor()}40`,
          }}>
            <div style={{
              width: '140px',
              height: '140px',
              borderRadius: '50%',
              background: 'rgba(15, 23, 42, 0.95)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <div style={{ fontSize: '2.5rem', fontWeight: '700', color: getRiskColor() }}>
                {probability}%
              </div>
              <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Churn Probability</div>
            </div>
          </div>
        </div>

        {/* Risk Level */}
        <div style={{
          background: getRiskBgColor(),
          border: `2px solid ${getRiskColor()}`,
          borderRadius: '12px',
          padding: '30px',
          textAlign: 'center',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}>
          <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '10px' }}>Risk Level</div>
          <div style={{
            fontSize: '2rem',
            fontWeight: '700',
            color: getRiskColor(),
            marginBottom: '10px',
          }}>
            {result.risk_level}
          </div>
          <div style={{ fontSize: '0.875rem', color: '#cbd5e1' }}>
            {result.risk_level === 'HIGH' && 'Immediate retention action recommended'}
            {result.risk_level === 'MEDIUM' && 'Monitor and engage customer'}
            {result.risk_level === 'LOW' && 'Customer stable, maintain engagement'}
          </div>
        </div>

        {/* Prediction */}
        <div style={{
          background: result.prediction === 'CHURN' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)',
          border: `2px solid ${result.prediction === 'CHURN' ? '#ef4444' : '#10b981'}`,
          borderRadius: '12px',
          padding: '30px',
          textAlign: 'center',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}>
          <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginBottom: '10px' }}>Prediction</div>
          <div style={{
            fontSize: '1.5rem',
            fontWeight: '700',
            color: result.prediction === 'CHURN' ? '#ef4444' : '#10b981',
            marginBottom: '10px',
          }}>
            {result.prediction === 'CHURN' ? '⚠️ LIKELY TO CHURN' : '✓ NOT LIKELY TO CHURN'}
          </div>
          <div style={{ fontSize: '0.875rem', color: '#cbd5e1' }}>
            {result.prediction === 'CHURN' ? 'High risk of customer departure' : 'Customer retention stable'}
          </div>
        </div>
      </div>

      {/* Important Factors */}
      <div style={{ marginBottom: '30px' }}>
        <h3 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#f1f5f9', marginBottom: '15px' }}>📊 Important Factors</h3>
        <div style={{ display: 'grid', gap: '10px' }}>
          {result.factors && result.factors.length > 0 ? (
            result.factors.map((factor, index) => (
              <div
                key={index}
                style={{
                  background: 'rgba(59, 130, 246, 0.1)',
                  border: '1px solid rgba(59, 130, 246, 0.3)',
                  borderRadius: '8px',
                  padding: '12px 16px',
                  color: '#cbd5e1',
                  fontSize: '0.95rem',
                }}
              >
                • {factor}
              </div>
            ))
          ) : (
            <div style={{ color: '#94a3b8' }}>No significant risk factors identified</div>
          )}
        </div>
      </div>

      {/* Recommendations */}
      <div>
        <h3 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#f1f5f9', marginBottom: '15px' }}>💡 Recommended Retention Actions</h3>
        <div style={{ display: 'grid', gap: '10px' }}>
          {result.recommendations && result.recommendations.length > 0 ? (
            result.recommendations.map((recommendation, index) => (
              <div
                key={index}
                style={{
                  background: 'rgba(139, 92, 246, 0.1)',
                  border: '1px solid rgba(139, 92, 246, 0.3)',
                  borderRadius: '8px',
                  padding: '12px 16px',
                  color: '#cbd5e1',
                  fontSize: '0.95rem',
                }}
              >
                ✓ {recommendation}
              </div>
            ))
          ) : (
            <div style={{ color: '#94a3b8' }}>No specific recommendations at this time</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ResultCard;
