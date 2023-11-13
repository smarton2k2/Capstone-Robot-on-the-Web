using UnityEngine;
namespace Unity.Robotics.UrdfImporter.Control //Smoother movement
{
    public class SimpleRobotController : MonoBehaviour
    {
        private readonly string[] jointNames = {
            "shoulder_link", "arm_link", "elbow_link",
            "forearm_link", "wrist_link", "hand_link"
        };

        private ArticulationBody[] jointArticulationBodies;

        public float stiffness = 10000f;
        public float damping = 100f;
        public float forceLimit = 1000f;
        private float[] startPositions;
        private float[] targetPositions;
        private float moveStartTime;
        public float movementDuration = 2.0f;

        void Start()
        {
            jointArticulationBodies = new ArticulationBody[jointNames.Length];

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
                float fraction = (Time.time - moveStartTime) / movementDuration;

                if (fraction >= 1)
                {
                    fraction = 1;
                    targetPositions = null;
                }

                for (int i = 0; i < jointArticulationBodies.Length; i++)
                {
                    float interpolatedPosition = Mathf.Lerp(startPositions[i], targetPositions[i], fraction);
                    var jointDrive = jointArticulationBodies[i].xDrive;
                    jointDrive.target = interpolatedPosition;
                    jointArticulationBodies[i].xDrive = jointDrive;
                }
            }

            if (Input.GetKeyDown(KeyCode.M))
            {
                float[] newTargetPositions = { 90f, 0f, 0f, 0f, 0f, 0f };
                SetTargetPositions(newTargetPositions);
            }
        }
    }
}