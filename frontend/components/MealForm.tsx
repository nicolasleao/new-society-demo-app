'use client';

import { useState } from 'react';
import { mealApi } from '@/lib/api';

interface MealFormProps {
  username: string;
  onMealAdded: () => void;
}

export default function MealForm({ username, onMealAdded }: MealFormProps) {
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim()) return;

    try {
      setLoading(true);
      setError(null);

      // Step 1: Infer macros from AI
      const inferredMeal = await mealApi.inferMealFromDescription({
        description: description.trim(),
        username,
      });

      // Step 2: Create the meal with inferred data
      await mealApi.createMeal({
        username,
        title: inferredMeal.title,
        carbs: inferredMeal.carbs,
        proteins: inferredMeal.proteins,
        fats: inferredMeal.fats,
        total_calories: inferredMeal.total_calories,
      });

      setDescription('');
      onMealAdded();
    } catch (error: any) {
      console.error('Error processing meal:', error);
      setError(error.response?.data?.detail || 'Failed to process meal. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-2">Add New Meal</h2>
      <p className="text-sm text-gray-500 mb-4">
        Describe your meal and AI will calculate the macros for you
      </p>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
            What did you eat?
          </label>
          <textarea
            id="description"
            required
            rows={4}
            disabled={loading}
            className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border placeholder-gray-500 text-gray-900 disabled:bg-gray-50 disabled:text-gray-500"
            placeholder="e.g., Two scrambled eggs with whole wheat toast and a glass of orange juice"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        {loading && (
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-md">
            <div className="flex items-center space-x-3">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
              <div className="flex-1">
                <p className="text-sm font-medium text-blue-900">Calculating macros...</p>
                <p className="text-xs text-blue-600 mt-0.5">Our AI is analyzing your meal</p>
              </div>
            </div>
            <div className="mt-3 space-y-2">
              <div className="flex space-x-2">
                <div className="h-2 bg-blue-200 rounded-full animate-pulse w-1/4"></div>
                <div className="h-2 bg-blue-200 rounded-full animate-pulse w-1/3" style={{ animationDelay: '0.1s' }}></div>
                <div className="h-2 bg-blue-200 rounded-full animate-pulse w-1/4" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}

        <div>
          <button
            type="submit"
            disabled={loading || !description.trim()}
            className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Processing...' : 'Add Meal with AI'}
          </button>
        </div>
      </form>
    </div>
  );
}