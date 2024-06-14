import numpy as np
import matplotlib.pyplot as plt

# Decorator for a single step
def step(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Hybrid Equations (Continuous and Discrete Dynamics)
class HybridEquation:
    def __init__(self, f_continuous, g_stochastic, jump_condition, jump_map, y0, t0, t1, dt, noise_intensity):
        self.f_continuous = f_continuous  # Continuous part
        self.g_stochastic = g_stochastic  # Stochastic part
        self.jump_condition = jump_condition  # Condition for jumps
        self.jump_map = jump_map  # Mapping for jumps
        self.y = y0
        self.t = t0
        self.t1 = t1
        self.dt = dt
        self.noise_intensity = noise_intensity
        self.steps = int((t1 - t0) / dt)
        self.trajectory = [y0]
        self.time = [t0]
    
    @step
    def euler_maruyama_step(self, y, dt):
        noise = self.noise_intensity * np.sqrt(dt) * np.random.normal(size=y.shape)
        return y + self.f_continuous(y) * dt + self.g_stochastic(y) * noise
    
    def solve(self):
        for _ in range(self.steps):
            if self.jump_condition(self.y, self.t):
                self.y = self.jump_map(self.y, self.t)
            else:
                self.y = self.euler_maruyama_step(self.y, self.dt)
            self.t += self.dt
            self.trajectory.append(self.y)
            self.time.append(self.t)
        return np.array(self.time), np.array(self.trajectory)

# Example usage within a library
def example_usage():
    # Define continuous, stochastic parts and jump conditions/maps
    def f_continuous(y):
        return np.array([y[1], -y[0]])
    
    def g_stochastic(y):
        return np.array([0.0, 0.1])
    
    def jump_condition(y, t):
        return t % 1.0 < 1e-2  # Jump every 1 time unit
    
    def jump_map(y, t):
        return np.array([y[0], -y[1]])  # Simple jump: invert velocity
    
    # Initial conditions
    y0 = np.array([1.0, 0.0])
    t0 = 0.0
    t1 = 10.0
    dt = 0.01
    noise_intensity = 0.1
    
    # Create Hybrid Equation solver
    hybrid_solver = HybridEquation(f_continuous, g_stochastic, jump_condition, jump_map, y0, t0, t1, dt, noise_intensity)
    
    # Solve Hybrid Equation
    time, trajectory = hybrid_solver.solve()
    
    return time, trajectory

# Functions to process and visualize the results
def process_hybrid_solution(time, trajectory):
    # Basic statistics or analysis can be added here
    return time, trajectory

def plot_hybrid_solution(time, trajectory):
    plt.figure()
    plt.plot(time, trajectory[:, 0], label='Position')
    plt.plot(time, trajectory[:, 1], label='Velocity')
    plt.title('Hybrid Equation Solution')
    plt.xlabel('Time')
    plt.ylabel('State')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    time, trajectory = example_usage()
    
    # Process results
    processed_time, processed_trajectory = process_hybrid_solution(time, trajectory)
    
    # Plot results
    plot_hybrid_solution(processed_time, processed_trajectory)


import numpy as np
import matplotlib.pyplot as plt

# Decorator for a single step
def step(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Jump Diffusion Solver
class JumpDiffusion:
    def __init__(self, f, g, jump_intensity, jump_size, y0, t0, t1, dt, noise_intensity):
        self.f = f  # Continuous part
        self.g = g  # Stochastic part
        self.jump_intensity = jump_intensity  # Intensity (rate) of the jump process (lambda)
        self.jump_size = jump_size  # Function to determine the size of jumps
        self.y = y0
        self.t = t0
        self.t1 = t1
        self.dt = dt
        self.noise_intensity = noise_intensity
        self.steps = int((t1 - t0) / dt)
        self.trajectory = [y0]
        self.time = [t0]
    
    @step
    def euler_maruyama_step(self, y, dt):
        noise = self.noise_intensity * np.sqrt(dt) * np.random.normal(size=y.shape)
        return y + self.f(y) * dt + self.g(y) * noise
    
    @step
    def apply_jump(self, y):
        if np.random.uniform() < self.jump_intensity * self.dt:
            return y + self.jump_size(y)
        return y
    
    def solve(self):
        for _ in range(self.steps):
            self.y = self.euler_maruyama_step(self.y, self.dt)
            self.y = self.apply_jump(self.y)
            self.t += self.dt
            self.trajectory.append(self.y)
            self.time.append(self.t)
        return np.array(self.time), np.array(self.trajectory)

# Example usage within a library
def example_usage():
    # Define continuous, stochastic parts, and jump size function
    def f(y):
        return np.array([0.05 * y[0]])
    
    def g(y):
        return np.array([0.1 * y[0]])
    
    def jump_size(y):
        return np.array([0.5 * y[0]])
    
    # Initial conditions
    y0 = np.array([1.0])
    t0 = 0.0
    t1 = 10.0
    dt = 0.01
    noise_intensity = 0.1
    jump_intensity = 0.1  # Lambda (rate of jumps)
    
    # Create Jump Diffusion solver
    jump_diffusion_solver = JumpDiffusion(f, g, jump_intensity, jump_size, y0, t0, t1, dt, noise_intensity)
    
    # Solve Jump Diffusion
    time, trajectory = jump_diffusion_solver.solve()
    
    return time, trajectory

# Functions to process and visualize the results
def process_jump_diffusion_solution(time, trajectory):
    # Basic statistics or analysis can be added here
    return time, trajectory

def plot_jump_diffusion_solution(time, trajectory):
    plt.figure()
    plt.plot(time, trajectory)
    plt.title('Jump Diffusion Solution')
    plt.xlabel('Time')
    plt.ylabel('State')
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    time, trajectory = example_usage()
    
    # Process results
    processed_time, processed_trajectory = process_jump_diffusion_solution(time, trajectory)
    
    # Plot results
    plot_jump_diffusion_solution(processed_time, processed_trajectory)

