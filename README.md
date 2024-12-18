
# **AI Interactive Learning Framework**

## **Overview**

This project implements an interactive AI-driven framework designed to assess and guide users in learning Artificial Intelligence (AI). It leverages multiple agents for specialized tasks, including evaluating responses, generating questions, adjusting tones based on emotional states, and orchestrating the overall process.

The system architecture uses Fetch.AI's `uAgents` framework to manage agent communication and integrates APIs such as **Claude**, **Gemini**, and **OpenAI** to deliver advanced AI functionalities. The agents collaborate to deliver a personalized and engaging learning experience.

---

## **Project Workflow**

The following diagram provides a visual representation of the system workflow:

![Workflow Diagram](Untitled%20diagram-2024-12-12-150916.png)

1. The **user** interacts with the chatbot, starting with an initial question.
2. The **Assessment Agent** evaluates the user's response and determines the skill level.
3. The **Question Generator** creates relevant follow-up questions using the **Claude API**, while analyzing emotional states.
4. The **Emotional Wrapper** adjusts the tone of the response using **OpenAI API** and recommends a learning path.
5. The **Orchestrator** ensures smooth coordination between all agents and sends the final output to the user.

---

## **Agents and Components**

### **1. Assessment Agent (`Assessing_agent.py`)**
- Evaluates user responses using the `Gemini-2.0-Flash-Exp` model.
- Generates confidence scores and determines the question level (beginner, intermediate, advanced).

### **2. ChatBot (`ChatBot.py`)**
- Manages user interactions and conversation history.
- Handles initial questions and communicates with other agents for follow-up tasks.

### **3. Question Generation Agent (`QuestionGenerator.py`)**
- Uses **Claude API** (`Claude-3-Haiku-20240307`) to generate contextually relevant questions based on user input.
- Analyzes the emotional state of the user and crafts questions accordingly.

### **4. Emotional Wrapper Agent (`emotional_wrapper.py`)**
- Adjusts the tone of questions based on the user's emotional state.
- Provides a personalized learning path tailored to the user's skill level.

### **5. Orchestrator (`orchestrator.py`)**
- Coordinates the flow of information between all agents.
- Manages message routing and ensures the smooth functioning of the system.

---

## **Features**

- **Adaptive Assessment:** Dynamically evaluates user responses and adapts the difficulty of questions.
- **Emotionally Intelligent Responses:** Adjusts tone and interaction style based on user emotions.
- **Personalized Learning Path:** Recommends a learning plan suited to the user's skill level.
- **Claude API Integration:** Generates advanced, contextually relevant, and emotionally intelligent follow-up questions.
- **Modular Agent Design:** Decentralized architecture using Fetch.AI’s `uAgents` framework for seamless interaction between agents.
- **Interactive Chatbot:** Provides a conversational interface for user engagement.

---

## **Requirements**

### **Install Dependencies**
Ensure you have Python 3.8+ installed. Install the required dependencies with the following command:

```bash
pip install -r requirements.txt
```

### **Environment Variables**
Create a `.env` file in the project root with the following keys:

```plaintext
GEMINI_API_KEY=your_gemini_api_key
Claude_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
```

---

## **How to Run the Project**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/amangupta05/AI-Summit-New-York.git
   cd AI-Summit-New-York
   ```

2. **Run the Agents**

   - **Assessment Agent:**
     ```bash
     python Assessing_agent.py
     ```
     This agent evaluates the user's responses and determines question levels.

   - **ChatBot:**
     ```bash
     python ChatBot.py
     ```
     The chatbot initiates the interaction and maintains conversation history.

   - **Question Generator:**
     ```bash
     python QuestionGenerator.py
     ```
     This agent uses the **Claude API** to generate follow-up questions and detect emotional states. Ensure you have a valid `Claude_API_KEY` set in the `.env` file.

   - **Emotional Wrapper:**
     ```bash
     python emotional_wrapper.py
     ```
     Adjusts the tone of questions and provides a tailored learning path.

   - **Orchestrator:**
     ```bash
     python orchestrator.py
     ```
     Coordinates the flow of communication between all agents.

3. **Workflow Diagram**
   - The workflow diagram is available above for a visual representation.

---

## **Claude API Integration**

The **Question Generation Agent** integrates with Anthropic's **Claude API** (`Claude-3-Haiku-20240307`) to generate advanced and context-aware questions. This agent:
- Analyzes user responses and conversation history.
- Crafts questions that are emotionally intelligent and relevant to the AI topic.
- Detects the user's emotional state (e.g., excited, anxious, neutral) to adjust the question tone accordingly.

---

## **Contributing**

Contributions are welcome! Feel free to open issues or submit pull requests for enhancements or bug fixes.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Contact**

For questions or feedback, please contact:

- **Email:** amangupta52001@gmail.com
- **GitHub:** [Aman Gupta](https://github.com/amangupta05)

---



