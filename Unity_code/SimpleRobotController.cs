using UnityEngine;
namespace Unity.Robotics.UrdfImporter.Control //Stepper movement
{
    public class SimpleRobotController : MonoBehaviour
    {
        private readonly string[] jointNames = {
            "shoulder_link", "arm_link", "elbow_link",
            "forearm_link", "wrist_link", "hand_link"
        };

        private ArticulationBody[] jointArticulationBodies;

        // Control parameters (customize these as needed)
        public float stiffness = 10000f;
        public float damping = 100f;
        public float forceLimit = 1000f;

        void Start()
        {
            jointArticulationBodies = new ArticulationBody[jointNames.Length];

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
        }

        public void MoveRobot(float[] targetPositions)
        {
            if (targetPositions.Length != jointArticulationBodies.Length)
            {
                Debug.LogError("SimpleRobotController: The targetPositions array length does not match the number of robot joints.");
                return;
            }

            for (int i = 0; i < jointArticulationBodies.Length; i++)
            {
                var jointDrive = jointArticulationBodies[i].xDrive;
                jointDrive.target = targetPositions[i];
                jointArticulationBodies[i].xDrive = jointDrive;
            }
        }

        void Update()
        {
            if (Input.GetKeyDown(KeyCode.M))
            {
                float[] targetJointPositions = { 90f, 0f, 0f, 0f, 0f, 0f };
                MoveRobot(targetJointPositions);
            }
        }
    }
}