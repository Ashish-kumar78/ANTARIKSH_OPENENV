---
title: Antariksh
emoji: 🛰️
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
tags:
  - openenv
---

# Antariksh Satellite Dashboard

This space hosts the Antariksh Satellite Scheduling Dashboard. It uses a multi-stage Docker build to serve a React frontend on a FastAPI backend.

## Environment Overview and Motivation

Antariksh is a reinforcement learning environment where agents manage satellite fleets under real-world constraints: disasters, resource depletion, weather events, and role-based scheduling. It simulates real-world satellite operations used by space agencies for disaster response and Earth observation, providing a complex scheduling challenge for AI agents.

## Action and Observation Spaces

### Observation Space
The state of the environment provides:
- **Satellites**: Array of satellite data, each including `id`, `battery` (0-100), `position` [lon, lat], `role` (planner/executor), `active` status, `tasks_completed`, and `storage_used`.
- **Tasks**: Array of pending/tracked tasks, including `id`, `location` [lon, lat], `priority` (low/medium/high/critical), exact cost requirements (`battery_cost`, `storage_cost`), `assigned_to`, and `disaster_related` flags.
- **Environment Context**: Current `weather` (clear/storm/solar_flare/overload), `disaster_active` (boolean), `disaster_sector`, `step` count, and total `score`.

### Action Space
At each step, the agent can issue one of the following commands:
- `assign_task`: Assigns a specific task to a specific satellite.
- `change_role`: Changes the operational role of a satellite (e.g., from executor to planner).
- `skip`: Take no action and advance to the next timestep.

## Task Descriptions and Difficulty Levels

- **Easy - Basic Task Completion**: 
  The agent manages 5 satellites and 10 tasks. There are no disasters or chaos events. The main goal is to complete as many tasks as possible within 30 steps. 
- **Medium - Resource-Aware Scheduling**: 
  The agent manages 7 satellites and 20 tasks with occasional weather events. Must balance task completion, battery efficiency, and storage management over 50 steps.
- **Hard - Disaster Response Coordination**: 
  The agent manages 10 satellites and 35 tasks under active disaster conditions. Must prioritize disaster-related tasks while maintaining resource efficiency and chaos resilience (e.g., solar flares, comms overload) over 80 steps.

## Setup and Usage Instructions

The environment is fully containerized and intended to run out-of-the-box using Docker. 

To build the image and start the application:
```bash
# 1. Build the Docker container
docker build -t antariksh-space .

# 2. Run the environment
docker run -p 7860:7860 antariksh-space
```

Once running, navigate to `http://localhost:7860` in your browser to access the RL dashboard and evaluate agents or interact manually. API requests can also be made against port `7860`.

## Baseline Performance Scores

A standard greedy baseline agent achieves the following completion scores on the environment:
- **Easy**: 1.0 (100% completion)
- **Medium**: ~0.87 (87% efficiency)
- **Hard**: ~0.66 (66% efficiency)
