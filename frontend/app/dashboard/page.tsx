'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { mealApi, Meal, TodayStats } from '@/lib/api';
import StatsDisplay from '@/components/StatsDisplay';
import MealForm from '@/components/MealForm';
import MealTable from '@/components/MealTable';

export default function Dashboard() {
  const [username, setUsername] = useState<string>('');
  const [meals, setMeals] = useState<Meal[]>([]);
  const [todayStats, setTodayStats] = useState<TodayStats | null>(null);
  const [dateFilter, setDateFilter] = useState<string>('today');
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const savedUsername = localStorage.getItem('username');
    if (!savedUsername) {
      router.push('/');
      return;
    }
    setUsername(savedUsername);
    loadData(savedUsername);
  }, [router]);

  const loadData = async (user: string) => {
    try {
      setLoading(true);
      const [mealsData, statsData] = await Promise.all([
        mealApi.getMeals(user, dateFilter),
        mealApi.getTodayStats(user)
      ]);
      setMeals(mealsData);
      setTodayStats(statsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMealAdded = () => {
    loadData(username);
  };

  const handleMealDeleted = () => {
    loadData(username);
  };

  const handleDateFilterChange = (newFilter: string) => {
    setDateFilter(newFilter);
    mealApi.getMeals(username, newFilter).then(setMeals);
  };

  const handleLogout = () => {
    localStorage.removeItem('username');
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Calory Tracker</h1>
            <p className="text-gray-600">Welcome, {username}</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Logout
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <MealForm username={username} onMealAdded={handleMealAdded} />
            <div className="mt-8">
              <MealTable
                meals={meals}
                dateFilter={dateFilter}
                onDateFilterChange={handleDateFilterChange}
                onMealDeleted={handleMealDeleted}
              />
            </div>
          </div>
          <div>
            <StatsDisplay stats={todayStats} />
          </div>
        </div>
      </div>
    </div>
  );
}