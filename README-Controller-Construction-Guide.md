# NYSG Controller Construction Guide

## Summary
This guide is meant as a way for you to build your own controller. Follow the instructions carefully and use the Jupyter Notebooks for reference when you build the software controller. You can still use the system without the controller you build. Our controller also works as well, which you can use to compare functionality with.

## Materials
You only need one file: <br>
__student_controller_main.py__

__*DO NOT MAKE EDITS IN ANY OTHER FILES.*__<br>

**For Reference** 
Please reference controller_main.py if you ever get stuck. Also reference the 
jupyter notebook in the folder named Jupyter Notebook.

__*AGAIN, DO NOT MAKE EDITS IN ANY OTHER FILES.*__<br>

## The Code You Will Write.
All the code you will write are located in the sections marked at the beginning
with <br>
 ----------------------- EDIT BELOW HERE -----------------------<br>

and ending with <br>
 ----------------------- EDIT ABOVE HERE -----------------------<br>

__*DO NOT MAKE EDITS IN ANY OTHER AREAS OF THIS FILE.*__<br>
__*DO NOT MAKE EDITS IN ANY ABOVE OR BELOW THESE DEMARCATED SECTIONS OF CODE.*__<br>


 There will also be TODO flags inside the code portions where you are to fill in the code and instructions explaning what you need to do.

## Prequisites and Skills Required
1. Review and Work through Jupyter Notebooks
   1. Learn Assignment and variables
   2. Learn about different data types
      1. strings
      2. lists
      3. ints
      4. floats
      5. booleans
   3. Learn about control flow
      1. if statements
      2. for loops
      3. while loops
   4. Learn Function Calls
   5. Learn how to use external packages and libraries / modules
   6. Learn about classes
   7. Learn how to debug
2. Patience to figure out a solution
3. Ability to reason with code

If you are familiar with programming and with Python, you can consider the prerequiste part 1 to be satisfied.

## Solutions
Solutions are there if you get stuck in README-Controller-Main-Solutions.md

## Agenda 
There are 8 code chunks you need to fill in for the student_controller_main.py file.
You can find these by using CONTROL-F or ctrl-F or command-F to search for TODO's, which mark the sections that you are to do complete and fill in.

Here are the descriptions of the tasks.
1. Finish function main() by filling in one line of code. You need to initialize all the sensors and peripherals, which requires calling function init(). Set the result of init to a variable named init_dict, which is a dictionary holding all the sensor and peripherals.
2. 	Let us create the sensors that we need for this project.

    We need a light sensor, temperature-humidity sensor and moisture sensor.
    You can create these objects with the constructors: LightSensor, TempHumiditySensor, MoistureSensor,
    To get more information for each constructior, read the module code in
    folder Controller and looking in file sensor_class.py

    For the light sensor, use the i2c_channel that was created before this section
    of code. Similarly, use the i2c_channel for the TempHumidity Sensor.
    The Moisture Sensor needs to arguments to be called.
    Save the sensors to variables named light_sensor, temp_humid_sensor and moisture_sensor
    respectively.
3. 
	Let us create the peripherals for this project.

	We need a Solenoid Valve, Heat Pad, Fan and Plant Light. These are given by 
	the constructors SolenoidValve, HeatPad, Fan, and PlantLight. Each of these takes
	in a pin number. The pins are:
	Solenoid Valve: pin_constants.VALVE
	Heat Pad: pin_constants.HEAT,
	Fan: pin_constants.VENT,
	PlantLight: pin_constants.LED

	Further, each of the constructors takes in a burst time. Give them all 20 
	second burst times. The burst time is an integer. 

	The first argument to each constructor is the pin number, while the second is
	the burst time. There are no other arguments. 

	Finally, save eacj peripheral to its own variable. The cariables should be 
	named, respectively, valve, heat, fan and light. 
4. We need to be able to read data from the Interface files. We need to reading 
	in 5 items: the manual control status, the manual actions, the email settings
	the pwm settings and the frequency settings.

	TO read in data, call the function load_data. Because load_data is in module 
	pin_constants, you will have to us the module with a dot notation:
	pin_constants.load_data. 

	Load_data takes in one argument, the path of the interface file you want to read. 
	When you can in load_data, load_data returns to you the read in data. 

	First, read in manual_control_path and save the results of the function to a 
	variable named manual_control. 

	Second, read in manual_actions_path and save the results of the function to a 
	variable named manual_results. 

	Next, read in email_settings_path and save the results of the function to a 
	variable named email_settings. 

	Then, read in pwm_settings_path and save the results of the function to a 
	variable named pwm_settings. 

	Finally, read in freq_settings_path and save the results of the function to a 
	variable named freq_settings. 

    Remember, there are five variables you need to create via 5 function calls.
5.     We need to convert the healthy light integer into a string. We do it by       comparing the value of healthy light. 
    
    If healthy light is greater than or equal to 4, return the string "Full Sun"

    If healthy light is greater or equal to 3 and less than 4, return "Part Sun"

    If healthy light is greater or equal to 2 and less than 3, return "Part Sun"

    If healthy light is greater or equal to 1 and less than 2, return "Part Shade"

    If healthy light is greater or equal to 0 and less than 1, return "Full Sun"

    Remember how to use if statements, elif statements and booleans.

    Do not add in an else clause.

6.         We need to convert action to a string. Action can be an integer between 0 and 4 inclusive, or the string "low" or "high".capitalize

        If action is 0 or it is the string "off", return the string "off".

        If action is 1 return the string "big_decrease".

        If action is 2 or it is the string "low", return the string "low".

        If action is 3 return the string "small_increase".

        If action is 4 or it is the string "high", return the string "high".

        Use your boolean comparison equality operation, == , the double equals,
        as well as if-elif statements. Also return strings inside the if statements.


7. We want you to complete the headers of the while loop. 
        In this branch of the if statement, we want the code to runforever. We
        can use a while loop with true as the guard. Write in the guard. Then
        paste in the given code below to call the function to run inside the while loop.
        You do not need to know what await does. Just paste the code indented
		inside the while loop body.

        Given code:
        await one_cycle(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log,
                        alert_log, max_log_size, interval)
8.         In this branch of the if statement, we want the code to for a
        certain number of iterations, max_iter, specifically. max_iter is an integer
        representing how many iterations to run. We can use a for loop.
         We want you to fill in the for loop guard. Create an iteration variable.
        Use range to make sure you iterate for max_iter iterations.
        Paste in the given code below to call the function to run inside the for loop.
        You do not need to know what await does. Just paste the code indented
        inside the for loop body.

        Given code:
        await one_cycle(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log,
                          alert_log, max_log_size, interval)



## Testing
To test, run 
./start-system.sh

The controller and UI should start. Follow instructions to open the UI and see the results. 