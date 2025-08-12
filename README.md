# MINIMAL calory tracker app

This is a barebones macronutrient and calory tracker app for demo purposes
We don't need user authentication, let's greatly simplify it by just having a username

We'll have a postgresql db with a single table:
meals

the meals table will have a username column to identify what user we're talking about
a title, created_at, deleted_at, carbs, proteins, fats, and total_calories columns

THe UI should be extremely simple, the first screen the user just types their username and this gives access to their data, then the second screen should have a total counter of each macro and total calories, a pie chart of macros
a form to input new meal, and a table below of previous meals with a filter option that defaults to just today.

the meals table should have a delete button with a confirmation modal so the users can delete their meals.

## stack
frontend:
nextjs

backend:
fastapi
postgresql
sqlalchemy
