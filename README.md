# Robot Grid Simulator

A Python-based game simulator where you control a robot navigating obstacle-filled grids of increasing difficulty. Built with `tkinter`, this project offers a graphical and interactive way to simulate robot commands and basic path navigation.

## Features

- Grid-based robot movement (Easy, Medium, Hard levels)
- Game-style UI with dark mode
- Visual and sound warnings for blocked paths
- Battery system with recharge option
- Goal detection to complete the mission
- Animated movements and obstacle logic
- Expandable levels and scalable grid
- ROS2 integration roadmap

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Talatoto/robot-grid-simulator.git
   cd robot-grid-simulator
   ```

2. Run the simulator:
   ```bash
   python3 robotSimulator.py
   ```

Note: Requires Python 3.9+ and uses `tkinter` (included with standard Python installation).

## File Structure

```
robot-grid-simulator/
│
├── robotSimulator.py    # Main GUI simulator
└── README.md             # This file
```

## Feature Descriptions

- Level Selector: Choose from Easy, Medium, or Hard, each with different grid size and obstacles.
- Robot Commands:
  - Forward, Turn Left/Right, Report, Recharge
  - Directional buttons and keyboard bindings
- Status Feedback:
  - Position, Direction, Battery in real-time
- Win Condition: Reaching the green tile ends the game with a victory prompt.

## ROS2 Integration Roadmap

Planned future enhancements:
- ROS2 message-passing for command inputs
- RViz visualization of the robot grid
- Remote control over ROS2 topics/actions
- Real-time path planning with nav stack

## Authors

- Tala Raed

## License

Free to use, fork, and extend.

