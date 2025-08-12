'use client';

import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts';

interface MacroPieChartProps {
  carbs: number;
  proteins: number;
  fats: number;
}

const COLORS = {
  carbs: '#3B82F6',     // Blue
  proteins: '#10B981',  // Green  
  fats: '#F59E0B',      // Yellow
};

export default function MacroPieChart({ carbs, proteins, fats }: MacroPieChartProps) {
  const total = carbs + proteins + fats;
  
  if (total === 0) {
    return (
      <div className="h-48 flex items-center justify-center text-gray-500 text-sm">
        No macro data to display
      </div>
    );
  }

  const data = [
    {
      name: 'Carbs',
      value: carbs,
      percentage: ((carbs / total) * 100).toFixed(1),
    },
    {
      name: 'Proteins',
      value: proteins,
      percentage: ((proteins / total) * 100).toFixed(1),
    },
    {
      name: 'Fats',
      value: fats,
      percentage: ((fats / total) * 100).toFixed(1),
    },
  ].filter(item => item.value > 0);

  const CustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percentage }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    if (parseFloat(percentage) < 10) return null;

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        className="text-xs font-medium"
      >
        {`${percentage}%`}
      </text>
    );
  };

  return (
    <div className="h-48">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={CustomLabel}
            outerRadius={60}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={COLORS[entry.name.toLowerCase() as keyof typeof COLORS]} 
              />
            ))}
          </Pie>
          <Legend 
            verticalAlign="bottom" 
            height={36}
            formatter={(value, entry: any) => 
              `${value}: ${entry.payload.value}g (${entry.payload.percentage}%)`
            }
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}