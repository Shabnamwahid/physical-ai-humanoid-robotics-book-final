//** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  textbookSidebar: [
    {
      type: 'category',
      label: 'Introduction to Physical AI',
      link: {
        type: 'doc',
        id: 'chapter-1-introduction-to-physical-ai/chapter-1-introduction-to-physical-ai',
      },
      items: [
        'chapter-1-introduction-to-physical-ai/1.1-defining-physical-ai',
        'chapter-1-introduction-to-physical-ai/1.2-historical-context',
        'chapter-1-introduction-to-physical-ai/1.3-key-components',
        'chapter-1-introduction-to-physical-ai/1.4-applications',
        'chapter-1-introduction-to-physical-ai/1.5-challenges-opportunities',
        'chapter-1-introduction-to-physical-ai/1.6-future-directions',
      ],
    },
    {
      type: 'category',
      label: 'Humanoid Robotics Basics',
      link: {
        type: 'doc',
        id: 'chapter-2-basics-of-humanoid-robotics/chapter-2-basics-of-humanoid-robotics',
      },
      collapsed: true, 
      items: [
        'chapter-2-basics-of-humanoid-robotics/2.1-anatomy',
        'chapter-2-basics-of-humanoid-robotics/2.2-biomechanics',
        'chapter-2-basics-of-humanoid-robotics/2.3-balance-locomotion',
        'chapter-2-basics-of-humanoid-robotics/2.4-actuator-technologies',
        'chapter-2-basics-of-humanoid-robotics/2.5-safety-considerations',
        'chapter-2-basics-of-humanoid-robotics/2.6-platforms-overview',
      ],
    },
    {
      type: 'category',
      label: 'ROS 2 Fundamentals',
      link: {
        type: 'doc',
        id: 'chapter-3-ros-2-fundamentals/chapter-3-ros-2-fundamentals',
      },
      collapsed: true, 
      items: [
        'chapter-3-ros-2-fundamentals/3.1-architecture',
        'chapter-3-ros-2-fundamentals/3.2-installation-setup',
        'chapter-3-ros-2-fundamentals/3.3-message-passing',
        'chapter-3-ros-2-fundamentals/3.4-parameter-management',
        'chapter-3-ros-2-fundamentals/3.5-lifecycle-management',
        'chapter-3-ros-2-fundamentals/3.6-testing-debugging',
      ],
    },
    {
      type: 'category',
      label: 'Digital Twin Simulation',
      link: {
        type: 'doc',
        id: 'chapter-4-digital-twin-simulation/chapter-4-digital-twin-simulation',
      },
      collapsed: true, 
      items: [
        'chapter-4-digital-twin-simulation/4.1-digital-twin-concepts',
        'chapter-4-digital-twin-simulation/4.2-gazebo-environment',
        'chapter-4-digital-twin-simulation/4.3-unity-integration',
        'chapter-4-digital-twin-simulation/4.4-sensor-modeling',
        'chapter-4-digital-twin-simulation/4.5-physics-accuracy',
        'chapter-4-digital-twin-simulation/4.6-sim-to-real-transfer',
      ],
    },
    {
      type: 'category',
      label: 'NVIDIA Isaac Sim',
      link: {
        type: 'doc',
        id: 'chapter-5-nvidia-isaac-sim/chapter-5-nvidia-isaac-sim',
      },
      collapsed: true, 
      items: [
        'chapter-5-nvidia-isaac-sim/5.1-isaac-sim-overview',
        'chapter-5-nvidia-isaac-sim/5.2-perception-pipeline',
        'chapter-5-nvidia-isaac-sim/5.3-slam-algorithms',
        'chapter-5-nvidia-isaac-sim/5.4-path-planning',
        'chapter-5-nvidia-isaac-sim/5.5-gpu-acceleration',
        'chapter-5-nvidia-isaac-sim/5.6-deep-learning-integration',
      ],
    },
    {
      type: 'category',
      label: 'Vision-Language-Action',
      link: {
        type: 'doc',
        id: 'chapter-6-vision-language-action/chapter-6-vision-language-action',
      },
      collapsed: true, 
      items: [
        'chapter-6-vision-language-action/6.1-multimodal-ai',
        'chapter-6-vision-language-action/6.2-visual-perception',
        'chapter-6-vision-language-action/6.3-natural-language-processing',
        'chapter-6-vision-language-action/6.4-action-planning',
        'chapter-6-vision-language-action/6.5-decision-making',
        'chapter-6-vision-language-action/6.6-human-robot-interaction',
      ],
    },
    {
      type: 'category',
      label: 'Conversational Robotics',
      link: {
        type: 'doc',
        id: 'chapter-7-conversational-robotics/chapter-7-conversational-robotics',
      },
      collapsed: true, 
      items: [
        'chapter-7-conversational-robotics/7.1-dialogue-systems',
        'chapter-7-conversational-robotics/7.2-llm-integration',
        'chapter-7-conversational-robotics/7.3-context-awareness',
        'chapter-7-conversational-robotics/7.4-voice-interfaces',
        'chapter-7-conversational-robotics/7.5-emotional-intelligence',
        'chapter-7-conversational-robotics/7.6-privacy-security',
      ],
    },
    {
      type: 'category',
      label: 'Capstone Project',
      link: {
        type: 'doc',
        id: 'chapter-8-capstone-project/chapter-8-capstone-project',
      },
      collapsed: true, 
      items: [
        'chapter-8-capstone-project/8.1-project-planning',
        'chapter-8-capstone-project/8.2-system-integration',
        'chapter-8-capstone-project/8.3-testing-validation',
        'chapter-8-capstone-project/8.4-performance-optimization',
        'chapter-8-capstone-project/8.5-documentation-deployment',
        'chapter-8-capstone-project/8.6-future-enhancements',
      ],
    },
    {
      type: 'category',
      label: 'Appendices',
      collapsed: true,
      items: [
        'appendices/index',
        'appendices/installation-guides',
        'appendices/troubleshooting',
        'appendices/code-examples',
        'appendices/further-reading',
      ],
    },
  ],
};

module.exports = sidebars;