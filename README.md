# survival
Simulate the learning to survive of basic organisms

## Running the code

```bash
python main.py
```

In case of lag or stuttering, reduce the frame rate in of the following line:
```python
	def animator(bots):
		...
		canvas.after(<time_to_wait>, animator,bots)
```

or increase the probability of a random sample in the following line
```python
	def animator(bots):
		...
		if random.random() > <probability_of_random_sample>:
```