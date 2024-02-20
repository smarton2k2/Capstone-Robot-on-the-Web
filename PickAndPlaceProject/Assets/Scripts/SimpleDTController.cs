using System;
using RosMessageTypes.Geometry;
using RosMessageTypes.NiryoMoveit;
using Unity.Robotics.ROSTCPConnector;
using UnityEngine.Networking;
using Unity.Robotics.UrdfImporter;
using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class SimpleDTController : MonoBehaviour
{
    const int k_NumRobotJoints = 6;

    public static readonly string[] LinkNames =
        { "world/base_link/shoulder_link", "/arm_link", "/elbow_link", "/forearm_link", "/wrist_link", "/hand_link" };

    // Variables required for ROS communication
    [SerializeField]
    GameObject m_NiryoOne;
    readonly Quaternion m_PickOrientation = Quaternion.Euler(90, 90, 0);

    public Button sendbutton;

    // Robot Joints
        UrdfJointRevolute[] m_JointArticulationBodies;

    // ROS Connector
    ROSConnection m_Ros;

    void Start()
    {

        m_JointArticulationBodies = new UrdfJointRevolute[k_NumRobotJoints];

        var linkName = string.Empty;
        for (var i = 0; i < k_NumRobotJoints; i++)
        {
            linkName += LinkNames[i];
            m_JointArticulationBodies[i] = m_NiryoOne.transform.Find(linkName).GetComponent<UrdfJointRevolute>();
        }
        
        if (sendbutton != null)
        {
            sendbutton.onClick.AddListener(Publish);
        }
    }

    public void Publish()
    {
        var sourceDestinationMessage = new NiryoMoveitJointsMsg();

        for (var i = 0; i < k_NumRobotJoints; i++)
        {
            sourceDestinationMessage.joints[i] = m_JointArticulationBodies[i].GetPosition();
        }
        StartCoroutine(PostJointData("http://localhost:5000/recieve_data", sourceDestinationMessage.joints ));
    }

    IEnumerator PostJointData(string url, double[] jointPositionsData)
    {
        string jsonData = "{\"positions\":[" + jointPositionsData[0] + "," + jointPositionsData[1] + "," + jointPositionsData[2] + "," + jointPositionsData[3] + "," + jointPositionsData[4] + "," + jointPositionsData[5] + "]}";
        Debug.Log(jsonData);
        using(UnityWebRequest request = UnityWebRequest.Post(url, jsonData))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);
            request.uploadHandler = (UploadHandler) new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = (DownloadHandler) new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            yield return request.SendWebRequest();
            Debug.Log("Status Code: " + request.responseCode);
        }
    }

}
