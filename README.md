# Lab 1: Hello, ESP32!
## William Lynch A14588777 

---

### Overview

This labs main focus was getting familiar with the ESP32 board and the arduino IDE.  We got the board set up and our arduino IDE configured for the board and created a few programs.

---

### Tutorials

The first tutorial went through setting up the arduino.  We installed the arduino IDE, configured it for our specific ESP32 board and tested uploading a sketch. The second tutorial went into the basics of writing code for the ardunio.  We looked at digital write and the basics of syntax in embedded C. WE learned about what the setup and loop phases our.  There was some basic information about LEDs and their implementation and some information about nonblock timing.  The third tutorial was about using the serial monitor in conjunction with using serial write in the code.  It told us it is important to add Serial.begin in the start of our if we want to use the monitor.

---

### Challenge 1

Challenge 1 got us setting up a basic LED blink circuit.  I used block timing as it did not specify that we could not. It was also not clear what the requirements for Hz meant and it was not answered by the TA's in slack, so I assumed that 10 Hz meant it just had to blink 10 times in a second.  I implemented that strategy for those first 3.  We just set the voltage to high on the LED's pin when we want it on, set a delay for how long we want it on, and then set the voltage to low when we want it off and another delay before it is on again.

| ![Gif of Condition](images/c1_part1_a.gif) | ![Gif of Condition](images/c1_part1_b.gif) | ![Gif of Condition](images/c1_part1_c.gif) |
|----|----|----|
| ![Gif of Condition](images/c1_part2_a.gif) | ![Gif of Condition](images/c1_part2_b.gif) | ![Gif of Condition](images/c1_part2_c.gif) |

---

### Challenge 2

Challenge two was slightly more complex.  The main idea with this challenge was using nonblock timing and using logic to turn the button into a push button.  The idea behind the push button logic was that we were saving the previous state of the button and comparing it to the current so we can see when there has been a change in state.  We only want to do counter when there has been a change in state.  We output the value of the counter to the monitor every second. We time this every second by using non block timing.  The non block timing allows us to also be running the whole loop waiting to see if the button is pressed. 

| ![Gif of Condition](images/c2.gif) |

---

### Challenge 3

Challenge 3 took challenge 2 a step further. We wanted to implement a timer that counted how many times the button had been pressed, but to also decrease if the button had not been pressed for 3 seconds.  My implementation reused a lot of logic from my previous challenge, but every time the state changed we would add to the timer, which meant that the button had been pressed, and we would also start the countdown to 3 seconds within this logic.  If the time elapsed 3 seconds then we would start decreasing the time 1 second at a time which will stop this loop as soon as the button is pressed again.  Meanwhile we have another set of nonblock timing running printing to the monitor the timer value.

| ![Gif of Condition](images/c3.gif) |