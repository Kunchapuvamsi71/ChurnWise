import React from 'react';

function StatCard({ title, value, subtitle, icon, color = 'blue' }) {
  const colorStyles = {
    blue: { background: 'rgba(59, 130, 246, 0.1)', border: 'rgba(59, 130, 246, 0.5)' },
    purple: { background: 'rgba(139, 92, 246, 0.1)', border: 'rgba(139, 92, 246, 0.5)' },
    green: { background: 'rgba(16, 185, 129, 0.1)', border: 'rgba(16, 185, 129, 0.5)' },
    red: { background: 'rgba(239, 68, 68, 0.1)', border: 'rgba(239, 68, 68, 0.5)' },
  };

  return (
    <div
      className="card"
      style={{
        background: colorStyles[color].background,
        border: `2px solid ${colorStyles[color].border}`,
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
        <div>
          <div className="card-subtitle">{title}</div>
          <div style={{ fontSize: '2rem', fontWeight: '700', color: '#f1f5f9', marginBottom: '8px' }}>
            {value}
          </div>
          {subtitle && <div style={{ fontSize: '0.875rem', color: '#94a3b8' }}>{subtitle}</div>}
        </div>
        {icon && <div style={{ fontSize: '2rem' }}>{icon}</div>}
      </div>
    </div>
  );
}

export default StatCard;
