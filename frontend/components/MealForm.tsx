'use client';

import { useState } from 'react';
import { mealApi } from '@/lib/api';

interface MealFormProps {
  username: string;
  onMealAdded: () => void;
}

export default function MealForm({ username, onMealAdded }: MealFormProps) {
  const [title, setTitle] = useState('');
  const [carbs, setCarbs] = useState('');
  const [proteins, setProteins] = useState('');
  const [fats, setFats] = useState('');
  const [calories, setCalories] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    try {
      setLoading(true);
      await mealApi.createMeal({
        username,
        title: title.trim(),
        carbs: parseFloat(carbs) || 0,
        proteins: parseFloat(proteins) || 0,
        fats: parseFloat(fats) || 0,
        total_calories: parseFloat(calories) || 0,
      });

      setTitle('');
      setCarbs('');
      setProteins('');
      setFats('');
      setCalories('');
      onMealAdded();
    } catch (error) {
      console.error('Error creating meal:', error);
      alert('Error creating meal. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Add New Meal</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700">
            Meal Title
          </label>
          <input
            type="text"
            id="title"
            required
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
            placeholder="e.g., Breakfast, Chicken Salad"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <label htmlFor="carbs" className="block text-sm font-medium text-gray-700">
              Carbs (g)
            </label>
            <input
              type="number"
              id="carbs"
              min="0"
              step="0.1"
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
              placeholder="0"
              value={carbs}
              onChange={(e) => setCarbs(e.target.value)}
            />
          </div>

          <div>
            <label htmlFor="proteins" className="block text-sm font-medium text-gray-700">
              Proteins (g)
            </label>
            <input
              type="number"
              id="proteins"
              min="0"
              step="0.1"
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
              placeholder="0"
              value={proteins}
              onChange={(e) => setProteins(e.target.value)}
            />
          </div>

          <div>
            <label htmlFor="fats" className="block text-sm font-medium text-gray-700">
              Fats (g)
            </label>
            <input
              type="number"
              id="fats"
              min="0"
              step="0.1"
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
              placeholder="0"
              value={fats}
              onChange={(e) => setFats(e.target.value)}
            />
          </div>

          <div>
            <label htmlFor="calories" className="block text-sm font-medium text-gray-700">
              Calories
            </label>
            <input
              type="number"
              id="calories"
              min="0"
              step="1"
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
              placeholder="0"
              value={calories}
              onChange={(e) => setCalories(e.target.value)}
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Adding...' : 'Add Meal'}
          </button>
        </div>
      </form>
    </div>
  );
}