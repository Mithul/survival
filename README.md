# Survival
Simulate the learning to survive of basic organisms

## Dependencies
### Python Dependencies

* tensorflow
* numpy
* pygame
* termcolor

### System Dependencies

* Currently requires a NVIDIA GPU for tensorflow with CuDA and CuDNN installed and tensorflow GPU version installed
* Require a resolution of 1280x720 pixels since it is hardcoded as the resolution for PyGame screen. 

## Running the code

```bash
python main.py
```

In case of lag or stuttering, reduce the frame rate in of the following line:
```python
	#main.py
	while 1:
		...
		clock.tick(<frame_rate>)
```

or increase the probability of a random sample in the following line
```python
	def animator(bots):
		...
		if random.random() > <probability_of_random_sample>:
```

## TODO
* Collectables that increase health
* Way to distinguish sprites
* Save frames as images/video
* Predators that will go after bots
* Avoid predators