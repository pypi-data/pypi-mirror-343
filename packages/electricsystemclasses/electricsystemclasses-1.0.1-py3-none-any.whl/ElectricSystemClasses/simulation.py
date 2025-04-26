# Copyright 2025 ropimen
#
# This file is licensed under the Server Side Public License (SSPL), Version 1.0.
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# https://www.mongodb.com/legal/licensing/server-side-public-license
#
# This file is part of ElectricSystemClasses.
#
# ElectricSystemClasses is a Python package providing a collection of classes for simulating electric systems.

#step in seconds
#period in hours

def simulate(step_size, period, user_timeframe):
    if period*3600/step_size != int(period*3600/step_size):
        raise ValueError("Simulation period must be divisible by step size.")
    
    simulation_steps = int(period * 3600 / step_size)
    print("Starting Simulation")
    for i in range(simulation_steps):

        # step --> i
        # current step in hours --> h
        # step in hours --> t 

        #print(f"Simulation step {i+1}/{simulation_steps}")

        step_in_hours = step_size / 3600
        current_step_in_hours = i * step_size / 3600

        user_timeframe(i, current_step_in_hours, step_in_hours)