using System;
using System.Collections;
using System.Security.Permissions;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using Unity.Robotics.UrdfImporter;
using System.IO;

namespace Unity.Robotics.UrdfImporter
{
    public class SimpleRobotController : MonoBehaviour
    {
        // The names of the joints in the order that they appear in the robot
        private readonly string[] jointNames = {
            "shoulder_link", "arm_link", "elbow_link",
            "forearm_link", "wrist_link", "hand_link"
        };

        // The array to hold the ArticulationBody components for each joint
        private ArticulationBody[] jointArticulationBodies;
        public float stiffness;
        public float damping;
        public float forceLimit;
        private float[] targetPositions;
        private float[] startPositions;
        private float moveStartTime;
        public float movementDuration;
        public Text TemperatureText;
        public Text VoltageText;
        public Text EffortText;
        public float fraction;

        public int selectedIndex = 0;
        public float jointControlSpeed = 5f;
        private bool manualControlEnabled = false;
        private float[] currentTargetPositions = { 0f, 0f, 0f, 0f, 0f, 0f };
        private string csvFilePath = "D:/My Documents/Unity Files/Unity-Robotics-Hub/tutorials/pick_and_place/PickAndPlaceProject/Data/Data.csv";


         public class Data
        {
            public float[] effort;
            public float[] position;
            public float[] temperatures;
            public float[] voltages;
        }

        void Start()
        {
            jointArticulationBodies = new ArticulationBody[jointNames.Length];
            StartCoroutine(GetDataFromAzure());

            for (int i = 0; i < jointNames.Length; i++)
            {
                ArticulationBody joint = GameObject.Find(jointNames[i]).GetComponent<ArticulationBody>();
                if (joint == null)
                {
                    Debug.LogError($"SimpleRobotController: Could not find joint: {jointNames[i]}");
                    continue;
                }
                jointArticulationBodies[i] = joint;

                var jointDrive = joint.xDrive;
                jointDrive.stiffness = stiffness;
                jointDrive.damping = damping;
                jointDrive.forceLimit = forceLimit;
                joint.xDrive = jointDrive;
            }

            startPositions = new float[jointNames.Length];

        }


        IEnumerator GetDataFromAzure()
        {
            while(true)
            {
                // Debug.Log(manualControlEnabled);
                if (manualControlEnabled)
                {
                    Debug.Log("Manual control enabled");
                    yield return null;
                }
                else{
                    Debug.Log("Manual control disabled");
                    using(UnityWebRequest request =  UnityWebRequest.Get("http://localhost:5000/get_data"))
                    {
                        yield return request.SendWebRequest();
                        if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
                        {
                            Debug.LogError(request.error);
                        }
                        else
                        {
                            string responseText = request.downloadHandler.text;
                            Data jsondata = JsonUtility.FromJson<Data>(responseText);
                            AppendDataToCSV(jsondata);

                            if (jsondata.position.Length == jointNames.Length)
                            {
                                float[] newTargetPositions = new float[jointNames.Length];
                                for (int i = 0; i < jointNames.Length; i++)
                                {
                                    // Convert each position from radians to degrees
                                    newTargetPositions[i] = jsondata.position[i] * Mathf.Rad2Deg;
                                }
                                SetTargetPositions(newTargetPositions);
                                TemperatureText.text = "Temperature: " + jsondata.temperatures[1].ToString() + "°C "+ jsondata.temperatures[2].ToString() + "°C "+ jsondata.temperatures[3].ToString() + "°C "+ jsondata.temperatures[4].ToString() + "°C "+ jsondata.temperatures[5].ToString() + "°C "+ jsondata.temperatures[6].ToString() + "°C "+ jsondata.temperatures[0].ToString() + "°C";
                                EffortText.text = "Effort: " + jsondata.effort[0].ToString() + "Nm "+ jsondata.effort[1].ToString() + "Nm "+ jsondata.effort[2].ToString() + "Nm "+ jsondata.effort[3].ToString() + "Nm "+ jsondata.effort[4].ToString() + "Nm "+ jsondata.effort[5].ToString() + "Nm ";
                                VoltageText.text = "Voltage: " + jsondata.voltages[0].ToString() + "V "+ jsondata.voltages[1].ToString() + "V "+ jsondata.voltages[2].ToString() + "V "+ jsondata.voltages[3].ToString() + "V "+ jsondata.voltages[4].ToString() + "V "+ jsondata.voltages[5].ToString() + "V";
                                
                            }
                            else
                            {
                                Debug.LogError("SimpleRobotController: The targetPositions array length does not match the number of robot joints.");
                                yield break;
                            }
                        }
                    }
                }
                
                yield return new WaitForSeconds(0.5f);
            }
        }
        void AppendDataToCSV(Data data)
        {
            string filePath = csvFilePath;

            // Convert arrays to semicolon-separated strings
            string effortString = string.Join(";", data.effort);
            string positionString = string.Join(";", data.position);
            string temperatureString = string.Join(";", data.temperatures);
            string voltageString = string.Join(";", data.voltages);

            // Combine the data with the timestamp
            string timestamp = DateTime.Now.ToString("yyyyMMddHHmmss");
            string line = $"{timestamp},{effortString},{positionString},{temperatureString},{voltageString}\n";

            // Append the line to the CSV file
            File.AppendAllText(filePath, line);
        }
        public void SetTargetPositions(float[] targets)
        {
            if (targets.Length != jointArticulationBodies.Length)
            {
                Debug.LogError("SimpleRobotController: The targetPositions array length does not match the number of robot joints.");
                return;
            }

            moveStartTime = Time.time;
            for (int i = 0; i < jointArticulationBodies.Length; i++)
            {
                startPositions[i] = jointArticulationBodies[i].xDrive.target;
            }

            targetPositions = targets;
        }

        void Update()
        {
            if (Input.GetKeyDown(KeyCode.T)) // Toggle control mode with 'T'
            {
                manualControlEnabled = !manualControlEnabled;
            }

            if (manualControlEnabled)
            {
                HandleJointSelection();
                HandleJointMovement();
            }

            if (targetPositions != null)
            {
                for (int i = 0; i < jointArticulationBodies.Length; i++)
                {
                    float interpolatedPosition = Mathf.Lerp(startPositions[i], targetPositions[i], fraction);
                    var jointDrive = jointArticulationBodies[i].xDrive;
                    // jointDrive.target =targetPositions[i];
                    jointDrive.target =interpolatedPosition;
                    jointArticulationBodies[i].xDrive = jointDrive;
                }
            }

            if (Input.GetKeyDown(KeyCode.R))
            {
                float[] newTargetPositions = { 0f, 0f, 0f, 0f, 0f, 0f };
                SetTargetPositions(newTargetPositions);
            }
        }

        void HandleJointSelection()
        {
            if (Input.GetKeyDown(KeyCode.RightArrow))
            {
                selectedIndex = (selectedIndex + 1) % jointNames.Length;
            }
            else if (Input.GetKeyDown(KeyCode.LeftArrow))
            {
                selectedIndex = (selectedIndex - 1 + jointNames.Length) % jointNames.Length;
            }
        }

        void HandleJointMovement()
        {
            float moveInput = Input.GetAxis("Vertical");
            if (moveInput != 0)
            {
                float moveDirection = Mathf.Sign(moveInput);
                float moveAmount = moveDirection * jointControlSpeed * Time.deltaTime;
                float newTargetPosition = jointArticulationBodies[selectedIndex].xDrive.target + moveAmount;
                currentTargetPositions[selectedIndex] = newTargetPosition;
                SetTargetPositions(currentTargetPositions);


            }
        }
    }
}