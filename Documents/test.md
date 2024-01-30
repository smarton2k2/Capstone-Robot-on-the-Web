# Paper
## Abstract
## Keywords
Digital Twin, Robotics, Cloud Computing, Real-Time Data Synchronization, Remote Monitoring, Remote Control, Virtual Environment, Data Security, Interactive Technologies, Machine Learning, Human-Robot collaborations, Industrial Engineering.
## Introduction
A digital twin is a digital representation of an object or process in context of its environment. Prior methodologies used DTDL(Digital Twin Definition Language) to map digital twin with data from the physical environment. 

Figure --azure dtdl-- shows an example of a digital twin made with Azure DTDL.

These methods made the digital systems slow, non-interactive and vulnerable. It was also not possible to map movements and other forces of the physical object to the digital twin.

--picture of azure dtdl--

Digital twin is the forefront of Industry 4.0 technology, and digitizing industrial automated robots is very important. The approach proposed is a method to create digital twins of industiral robots and makes sure 
its real-time, secure and interactible.
This method does not use DTDL. Instead the system uses ROS(Robotics Operating System) and URDF(Universal Robotics Descripton Format) along with cloud based services like - IoT(Internet of Things) and ML(Machine Learning)
services. ROS is an open source set of software libraries that helps build robot applications and URDF is an XML(Extensible Markup Language) that is used to describe a robot to a ROS based system. 

The also approach uses cloud based services to enhance human robot collaboration. An IoT server is created on the cloud to transfer telemetry data to and from the robot and also to make the system accessible. The IoT server
is also used to save and transfer data to the Machine Learning service.
 
## Structure Design
Figure --HLD-- shows the general structure of the system.

This approach integrate four systems together, they are:-

- Data Acqusition System
    - Collects, packages and encrypts telemetry-data(e.g. temperature, voltage) from the physical robot.
- Remote Control System
    - Collects anecrypts instruction-data from digital twin.
- Cloud System
    - Transfers data between physical robot and digital twin and hosts the AI model that performs the predictive maintenance.
- Digital Client System
    - Used to show telemtery data from robot and for human interactions.

-- picture of HLD --


## Implementation
In this section, the implementation of the method will explained in detail.
- Data Acquisiton System:
    - This system comprises of two key components: the physical robot and a support device. The physical robot is a Niryo Ned2 from Niryo -a 6-axis robot that runs on a ROS based system and the support device is a Raspberry Pi 3b+ board. Figure --niryo-- shows a picture of the Niryo robot. The Raspberry Pi functions as a ROS client (subscriber to ROS nodes on the robot) that continuously collect telemtry data from the robot(e.g. temperature, voltage, position and load). The ROS nodes operate on a Publisher-Subscriber mode of operation, wherein the robot is the publisher and the support device is the subscriber. This makes the system asynchronous and makes sure there are no promises that need to fulfilled (promises are fullfillments that stop other services and processes to ensure completion of synchronous task).
    - Upon receiving data from the robot's nodes, the support device encrypts the data and sends it to the designated IoT Server. To strengthen the systems' security, several measures are in place. Firstly, the robot is configured to be a standalone unit,i.e., isolated from direct internet access to prevent network based vulnerabilities. Furthermore, there is a reverse proxy is implemented on the support device, that helps defend against DDOS(Distributed Denial Of Service). Finally, all data transmitted will be encrypted and serialized to prevent MITM(Man In The Middle) attacks.

    --picture of niryo--

---
---

- Remote Control System:
    - A system that allows the use to 
- Cloud System:
	- Though an MQTT connection is ideal for transferring telemetry data over the internet (because of its speed), an HTTPS connection is used 	for the various security options available. The data is transferred to 	an IoT server (since telemetry data collection and processing is fast). We used two Azure IoT servers - one for data from robot and one for data from digital twin (this can be done with one server as well); We are also using Azure's Machine Learning services to train and deploy our predictive model (predictive maintenance model).

	- The IoT service and Machine Learning Service run in parallel to make sure there is no promise or delay. The IoT service is only responsible for channeling data from the robot to digital twin and vice versa.
	
    - The Machine Learning Service continuosly collects data from the IoT channel (via a storage object) and performs predictive analysis on the data. The data is also stored to re-train the model later on.

- Digital Client System:
	- On the client side, a Python applications interface with the Azure IoT service as a subscriber to one server and publisher to another. The subscriber part receives data from the IoT Server 1 as it is being published( published by robot). Then it is de-serialized and sent to our digital twin to be viewed by the user. The publisher part receives data from the digital twin (robot control instructions from user). Then the data is serialized and published to the other IoT server 2. The digital twin itself is made using Unity3D - a real time 3D development platform. The model of the robot was made using the URDF of the robot. The Unity applications transfers data to and from the Python application. We used Python as it quicker in handling large amounts of data, this allows us send data to the digital twin at a controlled rate.

	- -Picture of Digital twin-

	<!-- The digital twin also allows the user to directly give movement commands to the robot. -->

## References
- https://learn.microsoft.com/en-us/azure/digital-twins/concepts-models
- https://www.ros.org
- A. Fuller, Z. Fan, C. Day and C. Barlow, "Digital Twin: Enabling Technologies, Challenges and Open Research," in IEEE Access, vol. 8, pp. 108952-108971, 2020, doi: 10.1109/ACCESS.2020.2998358.
