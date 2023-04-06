# NeuralDrive

This project is focused on creating a self-driving car using the PiCar platform applying a machine-learning neural network model to sustain autonomous driving capabilities on a mapped track.

## Demo Below
[![Everything Is AWESOME](https://i.imgur.com/ih3pjVu.png)](https://youtu.be/0TQXyrXcrts "Neural Drive Demo")

## Features

- Autonomous driving: The car is capable of following a track autonomously using a trained neural network model.
- Real-time image processing: The car processes images from its camera in real-time to make decisions about steering and speed.
- Customizable: The project can be customized to use different machine learning frameworks and models, and can be adapted to work with other robotic platforms.

## Getting Started

### Prerequisites

- Raspberry Pi and PiCar
- Python 3.x
- TensorFlow or PyTorch
- OpenCV

### Installation
git clone `https://github.com/kputhanangadi/autopilot-project.git`
1. Clone the repository
2. Install the necessary dependencies
You can install all the dependencies for this class by typing `pip install -r requirements.txt`
3. Train the neural network model using your own data
`python train_model.py --data_path /path/to/training/data`
4. Integrate the model with the PiCar's software

## Usage

1. Run the program on the PiCar
2. Place the car on a track and watch it drive autonomously
3. Adjust the model's parameters as needed to improve performance

## Contributing

If you'd like to contribute to the development of this application, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them
4. Push your changes to your fork
5. Create a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

