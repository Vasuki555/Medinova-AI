/**
 * SVG Line Chart Component
 * Premium, interactive line chart rendered via native SVGs with gradients.
 */

import { useState } from 'react';

const SVGLineChart = ({ data = [], title = 'Vitals Trend', color = '#2E90FA', height: chartH = 150 }) => {
  const [hoveredPoint, setHoveredPoint] = useState(null);

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-32 text-neutral-400 text-sm">
        No tracking history found
      </div>
    );
  }

  const width = 500;
  const height = 200;
  const paddingLeft = 40;
  const paddingRight = 20;
  const paddingTop = 20;
  const paddingBottom = 30;

  const chartWidth = width - paddingLeft - paddingRight;
  const chartHeight = height - paddingTop - paddingBottom;

  // Support both {y, label} and {value, label} formats
  const yValues = data.map(d => d.y ?? d.value ?? 0);
  const maxVal = Math.max(...yValues, 1);
  const minVal = Math.min(...yValues, 0);
  const range = maxVal - minVal || 1;

  const points = data.map((d, index) => {
    const val = d.y ?? d.value ?? 0;
    const x = paddingLeft + (index / (data.length - 1 || 1)) * chartWidth;
    const y = paddingTop + chartHeight - ((val - minVal) / range) * chartHeight;
    return { x, y, label: d.label, value: val };
  });

  let pathD = '';
  if (points.length > 0) {
    pathD = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
      pathD += ` L ${points[i].x} ${points[i].y}`;
    }
  }

  let areaD = '';
  if (points.length > 0) {
    areaD = `${pathD} L ${points[points.length - 1].x} ${paddingTop + chartHeight} L ${points[0].x} ${paddingTop + chartHeight} Z`;
  }

  const gradId = `chart-grad-${Math.random().toString(36).slice(2, 7)}`;

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        {title && <h4 className="text-sm font-semibold text-neutral-700 dark:text-neutral-200">{title}</h4>}
        {hoveredPoint && (
          <span className="text-xs px-2 py-0.5 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-lg font-bold">
            {hoveredPoint.label}: {hoveredPoint.value}
          </span>
        )}
      </div>

      <svg viewBox={`0 0 ${width} ${height}`} className="w-full overflow-visible" style={{ height: chartH }}>
        <defs>
          <linearGradient id={gradId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity="0.3" />
            <stop offset="100%" stopColor={color} stopOpacity="0.0" />
          </linearGradient>
        </defs>

        {[0, 0.25, 0.5, 0.75, 1].map((ratio, index) => {
          const y = paddingTop + ratio * chartHeight;
          const labelVal = Math.round(maxVal - ratio * range);
          return (
            <g key={index}>
              <line x1={paddingLeft} y1={y} x2={width - paddingRight} y2={y}
                stroke="#e5e7eb" strokeWidth="1" strokeDasharray="4 4" />
              <text x={paddingLeft - 8} y={y + 4} textAnchor="end"
                fontSize="9" fill="#9ca3af">{labelVal}</text>
            </g>
          );
        })}

        {areaD && <path d={areaD} fill={`url(#${gradId})`} />}
        {pathD && (
          <path d={pathD} fill="none" stroke={color} strokeWidth="2.5"
            strokeLinecap="round" strokeLinejoin="round" />
        )}

        {points.map((pt, index) => {
          if (data.length > 8 && index % 2 !== 0) return null;
          return (
            <text key={index} x={pt.x} y={height - 8} textAnchor="middle" fontSize="9" fill="#6b7280">
              {pt.label}
            </text>
          );
        })}

        {points.map((pt, index) => (
          <circle
            key={index}
            cx={pt.x}
            cy={pt.y}
            r="4.5"
            fill="white"
            stroke={color}
            strokeWidth="2.5"
            className="cursor-pointer"
            onMouseEnter={() => setHoveredPoint(pt)}
            onMouseLeave={() => setHoveredPoint(null)}
          />
        ))}
      </svg>
    </div>
  );
};

export { SVGLineChart };
export default SVGLineChart;
