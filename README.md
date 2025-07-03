# PCS Chrono - Cycling Time Trial Data Analysis

A Python project for scraping, analyzing, and visualizing cycling time trial data from ([ProCyclingStats (PCS)](https://www.procyclingstats.com)). This project collects comprehensive data on time trial races, results, and rider statistics to provide insights into professional cycling performance.

## 📊 Project Overview

This project analyzes time trial performance in professional cycling by collecting data on:
    - Time trial races and their characteristics (distance, elevation, weather)
    - Individual rider results and rankings
    - Rider profiles and specialization metrics
    - Performance correlations and trends

## 🗂️ Data Structure

The project maintains three main datasets:

### Races ([data/races.csv](data/races.csv))

    - **305 time trial races** from 2020-2025
    - Race metadata: distance, elevation, profile difficulty, weather conditions
    - Race classification and ranking information
    - Winner times and average speeds

### Results ([data/results.csv](data/results.csv))

    - Individual rider results across all races
    - Position, points, and time gaps
    - Links to race and rider profiles

### Riders ([data/riders.csv](data/riders.csv))

    - Rider profiles with physical characteristics (height, weight)
    - Specialization scores: TT, GC, Sprint, Climber, Hills
    - Nationality and career statistics
