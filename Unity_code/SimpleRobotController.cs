using System;
using System.Collections;
using System.Security.Permissions;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using Unity.Robotics.UrdfImporter;

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
        private UrdfJointRevolute[] m_JointArticulationBodies;
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
        public Button sendButton;

         public class Data
        {
            public float[] effort;
            public float[] position;
            public float[] temperatures;
            public float[] voltages;
        }

        public class JointsendData
        {
            public float[] positions;
        }


        void Start()
        {
            jointArticulationBodies = new ArticulationBody[jointNames.Length];
            StartCoroutine(GetDataFromAzure());

            // Find and store a reference to each joint's ArticulationBody
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

            // if (sendButton != null)
            // {
            //     sendButton.onClick.AddListener(SendDataToServer);
            // }

        }

        IEnumerator PostJointData(string url, JointsendData jointPositionsData)
        {
            string jsonData = JsonUtility.ToJson(jointPositionsData);
            using (UnityWebRequest request = UnityWebRequest.Post(url, jsonData))
            {
                byte[] bodyRaw = new System.Text.UTF8Encoding().GetBytes(jsonData);
                request.uploadHandler =  new UploadHandlerRaw(bodyRaw);
                request.downloadHandler = new DownloadHandlerBuffer();
                request.SetRequestHeader("Content-Type", "application/json");

                yield return request.SendWebRequest();

                if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
                {
                    Debug.LogError("Error sending joint positions: " + request.error);
                }
                else
                {
                    Debug.Log("Joint positions sent successfully");
                }
            }
        }


        void SendDataToServer()
        {
            JointsendData jointPositionsData = new JointsendData
            {
                positions = new float[jointArticulationBodies.Length],
            };

            for (int i = 0; i < jointArticulationBodies.Length; i++)
            {
                jointPositionsData.positions[i] = jointArticulationBodies[i].jointPosition[0] * Mathf.Deg2Rad;
            }

            // StartCoroutine(PostJointData("http://localhost:5000/recieve_data", jointPositionsData));
            Debug.Log(jointPositionsData.positions[0]+", "+jointPositionsData.positions[1]+", "+jointPositionsData.positions[2]+", "+jointPositionsData.positions[3]+", "+jointPositionsData.positions[4]+", "+jointPositionsData.positions[5]);
        }


        IEnumerator GetDataFromAzure()
        {
            while(true)
            {
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
                        // Debug.Log("Position 0 " + jsondata.position[0] +" Position 1 " + jsondata.position[1] +" Position 2 " + jsondata.position[2] +" Position 3 " + jsondata.position[3] +" Position 4 " + jsondata.position[4]+" Position 5 " + jsondata.position[5]);

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
                yield return new WaitForSeconds(0.5f);
            }
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

            if (Input.GetKeyDown(KeyCode.M))
            {
                float[] newTargetPositions = { 0f, 0f, 0f, 0f, 0f, 0f };
                SetTargetPositions(newTargetPositions);
            }
        }
    }
}