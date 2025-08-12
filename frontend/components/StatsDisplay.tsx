'use client';

import { TodayStats } from '@/lib/api';
import MacroPieChart from './MacroPieChart';

interface StatsDisplayProps {
  stats: TodayStats | null;
}

export default function StatsDisplay({ stats }: StatsDisplayProps) {
  if (!stats) {
    return (
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Today&apos;s Summary</h2>
        <div className="text-center text-gray-500">Loading...</div>
      </div>
    );
  }

  const hasData = stats.total_calories > 0 || stats.meal_count > 0;

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Today&apos;s Summary</h2>
      
      {!hasData ? (
        <div className="text-center text-gray-500 py-8">
          <p>No meals logged today.</p>
          <p className="text-sm mt-1">Add your first meal to see your stats!</p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Macro Stats */}
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {stats.total_carbs.toFixed(1)}
              </div>
              <div className="text-sm text-gray-600">Carbs (g)</div>
            </div>
            
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {stats.total_proteins.toFixed(1)}
              </div>
              <div className="text-sm text-gray-600">Proteins (g)</div>
            </div>
            
            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <div className="text-2xl font-bold text-yellow-600">
                {stats.total_fats.toFixed(1)}
              </div>
              <div className="text-sm text-gray-600">Fats (g)</div>
            </div>
            
            <div className="text-center p-4 bg-red-50 rounded-lg">
              <div className="text-2xl font-bold text-red-600">
                {stats.total_calories.toFixed(0)}
              </div>
              <div className="text-sm text-gray-600">Calories</div>
            </div>
          </div>

          {/* Meal Count */}
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-xl font-semibold text-gray-700">
              {stats.meal_count} {stats.meal_count === 1 ? 'meal' : 'meals'} logged
            </div>
            <div className="text-sm text-gray-500 mt-1">
              {new Date(stats.date).toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </div>
          </div>

          {/* Pie Chart */}
          <div className="mt-6 pb-4">
            <h3 className="text-md font-medium text-gray-900 mb-3 text-center">
              Macro Distribution
            </h3>
            <div className="h-80">
              <MacroPieChart
                carbs={stats.total_carbs}
                proteins={stats.total_proteins}
                fats={stats.total_fats}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}