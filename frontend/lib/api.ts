import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Meal {
  id: number;
  username: string;
  title: string;
  carbs: number;
  proteins: number;
  fats: number;
  total_calories: number;
  created_at: string;
  deleted_at: string | null;
}

export interface MealCreate {
  username: string;
  title: string;
  carbs: number;
  proteins: number;
  fats: number;
  total_calories: number;
}

export interface Stats {
  total_carbs: number;
  total_proteins: number;
  total_fats: number;
  total_calories: number;
  meal_count: number;
}

export interface TodayStats extends Stats {
  date: string;
}

export const mealApi = {
  createMeal: async (meal: MealCreate): Promise<Meal> => {
    const response = await api.post('/meals', meal);
    return response.data;
  },

  getMeals: async (username: string, dateFilter?: string): Promise<Meal[]> => {
    const params = dateFilter ? { date_filter: dateFilter } : {};
    const response = await api.get(`/meals/${username}`, { params });
    return response.data;
  },

  deleteMeal: async (mealId: number): Promise<void> => {
    await api.delete(`/meals/${mealId}`);
  },

  getStats: async (username: string): Promise<Stats> => {
    const response = await api.get(`/stats/${username}`);
    return response.data;
  },

  getTodayStats: async (username: string): Promise<TodayStats> => {
    const response = await api.get(`/stats/${username}/today`);
    return response.data;
  },
};

export default api;