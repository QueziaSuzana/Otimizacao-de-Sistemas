# Production Optimization with Resource Allocation 🏭📊

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![PuLP](https://img.shields.io/badge/PuLP-%2300599C?logo=pulp&logoColor=white)

An industrial optimization system that uses **Linear Programming** to maximize factory profits by determining the optimal production quantities while respecting resource constraints.

## Key Features

- 🎯 **Profit Maximization**: Calculates optimal product mix to maximize revenue
- ⚖️ **Resource Allocation**: Efficiently distributes raw materials and machine hours
- 📈 **Interactive Dashboard**: User-friendly interface with real-time optimization
- 📊 **Visual Analytics**: Production graphs and resource utilization charts

## Mathematical Approach

Uses **Integer Linear Programming (ILP)** to solve:
Maximize: Z = p₁x₁ + p₂x₂
Subject to:
a₁x₁ + a₂x₂ ≤ Raw Materials
b₁x₁ + b₂x₂ ≤ Machine Hours
x₁, x₂ ≥ 0 and integer
