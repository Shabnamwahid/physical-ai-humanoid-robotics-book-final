---
title: Code Examples Repository
sidebar_position: 3
description: Complete code listings referenced in the textbook
---

# Appendix B: Code Examples Repository

This appendix contains complete code examples referenced throughout the textbook, organized by chapter and topic.

## Table of Contents
1. [Chapter 3: ROS 2 Examples](#chapter-3-ros-2-examples)
2. [Chapter 4: Simulation Examples](#chapter-4-simulation-examples)
3. [Chapter 5: Isaac Examples](#chapter-5-isaac-examples)
4. [Chapter 6: VLA Examples](#chapter-6-vla-examples)
5. [Chapter 7: Conversational AI Examples](#chapter-7-conversational-ai-examples)
6. [Utility Functions](#utility-functions)

## Chapter 3: ROS 2 Examples

### Simple Publisher Node
```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Simple Subscriber Node
```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Service Server Example
```python
#!/usr/bin/env python3

from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        return response


def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Chapter 4: Simulation Examples

### Gazebo Model Spawn Script
```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity
import sys
import os


class SpawnNode(Node):

    def __init__(self):
        super().__init__('spawn_node')
        self.cli = self.create_client(SpawnEntity, '/spawn_entity')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

    def send_request(self):
        # Load the URDF file
        urdf_path = sys.argv[1] if len(sys.argv) > 1 else 'path/to/robot.urdf'

        with open(urdf_path, 'r') as urdf_file:
            urdf = urdf_file.read()

        request = SpawnEntity.Request()
        request.name = "my_robot"
        request.xml = urdf
        request.initial_pose.position.x = 0.0
        request.initial_pose.position.y = 0.0
        request.initial_pose.position.z = 1.0
        self.future = self.cli.call_async(request)


def main(args=None):
    rclpy.init(args=args)

    spawn_node = SpawnNode()
    spawn_node.send_request()

    while rclpy.ok():
        rclpy.spin_once(spawn_node)
        if spawn_node.future.done():
            try:
                response = spawn_node.future.result()
            except Exception as e:
                spawn_node.get_logger().info('Service call failed %r' % (e,))
            else:
                spawn_node.get_logger().info('Result %r' % (response.success,))
            break

    spawn_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Unity Simulation Integration (C# Example)
```csharp
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json;

public class RobotController : MonoBehaviour
{
    public float moveSpeed = 5.0f;
    public float rotationSpeed = 100.0f;

    private Dictionary<string, System.Action> commandMap;

    void Start()
    {
        commandMap = new Dictionary<string, System.Action>
        {
            {"move_forward", MoveForward},
            {"turn_left", TurnLeft},
            {"turn_right", TurnRight},
            {"stop", Stop}
        };
    }

    void Update()
    {
        // Process commands from external source
        ProcessCommands();
    }

    public void ProcessCommands()
    {
        // In a real implementation, this would receive commands from ROS or another system
        // For example, through TCP/IP, WebSocket, or shared memory
    }

    public void ExecuteCommand(string command)
    {
        if (commandMap.ContainsKey(command))
        {
            commandMap[command]();
        }
    }

    void MoveForward()
    {
        transform.Translate(Vector3.forward * moveSpeed * Time.deltaTime);
    }

    void TurnLeft()
    {
        transform.Rotate(Vector3.up, -rotationSpeed * Time.deltaTime);
    }

    void TurnRight()
    {
        transform.Rotate(Vector3.up, rotationSpeed * Time.deltaTime);
    }

    void Stop()
    {
        // Stop any movement
    }
}
```

## Chapter 5: Isaac Examples

### Isaac ROS Perception Pipeline
```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class IsaacPerceptionNode(Node):

    def __init__(self):
        super().__init__('isaac_perception_node')
        self.subscription = self.create_subscription(
            Image,
            'camera/image_raw',
            self.image_callback,
            10)
        self.publisher = self.create_publisher(Image, 'camera/image_processed', 10)
        self.bridge = CvBridge()

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Perform computer vision processing
        processed_image = self.process_image(cv_image)

        # Convert back to ROS Image message
        processed_msg = self.bridge.cv2_to_imgmsg(processed_image, encoding='bgr8')
        processed_msg.header = msg.header

        # Publish processed image
        self.publisher.publish(processed_msg)

    def process_image(self, image):
        # Example: Simple edge detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        # Convert back to 3-channel for visualization
        edge_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return edge_image


def main(args=None):
    rclpy.init(args=args)
    node = IsaacPerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Chapter 6: VLA Examples

### Vision-Language-Action Integration
```python
import torch
import clip
from PIL import Image
import numpy as np
import openai
from transformers import BlipProcessor, BlipForConditionalGeneration


class VisionLanguageActionSystem:
    def __init__(self):
        # Load pre-trained models
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.clip_model, self.clip_preprocess = clip.load("ViT-B/32", device=self.device)

        # BLIP for image captioning
        self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(self.device)

        # Initialize action planning system
        self.action_space = {
            'move_forward': lambda: print("Moving forward"),
            'turn_left': lambda: print("Turning left"),
            'turn_right': lambda: print("Turning right"),
            'pick_up': lambda: print("Picking up object"),
            'place_down': lambda: print("Placing down object")
        }

    def perceive_scene(self, image_path):
        """Generate scene description from image"""
        raw_image = Image.open(image_path).convert('RGB')

        # Generate caption
        inputs = self.blip_processor(raw_image, return_tensors="pt").to(self.device)
        out = self.blip_model.generate(**inputs)
        caption = self.blip_processor.decode(out[0], skip_special_tokens=True)

        return caption

    def understand_command(self, command, scene_description):
        """Process natural language command in context of scene"""
        prompt = f"Given the scene: '{scene_description}', interpret the command: '{command}'. What should be done?"

        # In a real implementation, this would use a more sophisticated model
        # For now, we'll use a simple keyword-based approach
        if 'move' in command.lower() and 'forward' in command.lower():
            return 'move_forward'
        elif 'turn' in command.lower() and 'left' in command.lower():
            return 'turn_left'
        elif 'turn' in command.lower() and 'right' in command.lower():
            return 'turn_right'
        elif 'pick' in command.lower() or 'grasp' in command.lower():
            return 'pick_up'
        elif 'place' in command.lower() or 'put' in command.lower():
            return 'place_down'
        else:
            return None

    def plan_action(self, command, scene_description):
        """Plan action based on command and scene"""
        action = self.understand_command(command, scene_description)
        return action

    def execute_action(self, action):
        """Execute planned action"""
        if action in self.action_space:
            self.action_space[action]()
            return True
        else:
            print(f"Action '{action}' not recognized")
            return False

    def process_interaction(self, image_path, command):
        """Complete VLA pipeline: Vision -> Language -> Action"""
        # 1. Perceive scene
        scene_description = self.perceive_scene(image_path)
        print(f"Scene: {scene_description}")

        # 2. Understand command in context
        action = self.plan_action(command, scene_description)

        # 3. Execute action
        if action:
            print(f"Executing action: {action}")
            self.execute_action(action)
        else:
            print("Could not determine appropriate action")


# Example usage
if __name__ == "__main__":
    vla_system = VisionLanguageActionSystem()

    # Example: Process an image with a command
    # vla_system.process_interaction("path/to/image.jpg", "Move the red block to the left")
```

## Chapter 7: Conversational AI Examples

### Simple Chat Interface with Context
```python
import openai
import json
from datetime import datetime


class ConversationalRobot:
    def __init__(self, api_key=None):
        if api_key:
            openai.api_key = api_key

        # Conversation history
        self.conversation_history = []

        # System context
        self.system_context = {
            "role": "system",
            "content": "You are a helpful robotic assistant. You can answer questions about robotics, AI, and provide assistance with technical problems. Keep responses concise but informative."
        }

    def add_to_history(self, role, content):
        """Add message to conversation history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(message)

    def get_response(self, user_input):
        """Get response from AI model"""
        # Add user message to history
        self.add_to_history("user", user_input)

        # Prepare messages for API call
        messages = [self.system_context] + [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.conversation_history[-10:]  # Use last 10 messages
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=200,
                temperature=0.7
            )

            ai_response = response.choices[0].message['content'].strip()

            # Add AI response to history
            self.add_to_history("assistant", ai_response)

            return ai_response

        except Exception as e:
            error_msg = f"Error getting response: {str(e)}"
            self.add_to_history("assistant", error_msg)
            return error_msg

    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []

    def get_conversation_context(self):
        """Get current conversation context"""
        return self.conversation_history


# Example usage
if __name__ == "__main__":
    # Initialize the conversational robot
    robot = ConversationalRobot(api_key="your-api-key-here")

    # Example conversation
    response = robot.get_response("Hello, can you help me with ROS 2?")
    print(f"Robot: {response}")

    response = robot.get_response("How do I create a publisher node?")
    print(f"Robot: {response}")
```

## Utility Functions

### Vector Database Integration
```python
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import numpy as np


class VectorDB:
    def __init__(self, host="localhost", port=6333):
        self.client = QdrantClient(host=host, port=port)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Create collection if it doesn't exist
        try:
            self.client.get_collection("textbook_content")
        except:
            self.client.create_collection(
                collection_name="textbook_content",
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )

    def add_document(self, text, metadata=None):
        """Add a document to the vector database"""
        embedding = self.model.encode([text])[0].tolist()

        self.client.upsert(
            collection_name="textbook_content",
            points=[
                models.PointStruct(
                    id=len(self.client.scroll(collection_name="textbook_content")[0]),
                    vector=embedding,
                    payload={"text": text, **(metadata or {})}
                )
            ]
        )

    def search(self, query, limit=5):
        """Search for similar documents"""
        query_embedding = self.model.encode([query])[0].tolist()

        results = self.client.search(
            collection_name="textbook_content",
            query_vector=query_embedding,
            limit=limit
        )

        return [(hit.payload["text"], hit.score) for hit in results]
```

### Configuration Management
```python
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    # Database settings
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "")

    # AI settings
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # Server settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # Security
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Rate limiting
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1000"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))


# Usage
config = Config()
```

## Running the Examples

To run these examples:

1. Ensure you have the required dependencies installed:
```bash
pip install rclpy  # For ROS 2 examples
pip install opencv-python  # For computer vision
pip install torch torchvision torchaudio  # For deep learning
pip install openai  # For API access
pip install transformers  # For NLP
pip install qdrant-client  # For vector database
pip install sentence-transformers  # For embeddings
```

2. For ROS 2 examples, make sure to source your ROS 2 environment:
```bash
source /opt/ros/humble/setup.bash
```

3. Run Python examples directly:
```bash
python3 example_file.py
```

These examples provide a foundation for the concepts discussed in the textbook. You can extend them based on your specific requirements and use cases.