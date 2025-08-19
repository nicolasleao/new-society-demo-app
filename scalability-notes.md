# Codebase Maintainability / Scalability

# 1. What Is Scalability
Scalability is a system or business’s ability to grow—handle more users or data—without performance drops or proportionally higher costs

## Why it matters?
Scaling poorly puts you at risk: sudden user spikes (a marketing hit, seasonal demand) can break your system right when you’re gaining traction

## The dillema
There's a trade-off between speed of development and scalability.
Building something that scales well is hard and developers have the tendency to overengineer,
while entrepreneurs have the tendency to build something that doesn't scale well to get it on the market ASAP.

- A balance between these two is needed, but it can be achieved by some simple principles and rules that we'll cover during this talk;

# 2. Types of Scalability: Vertical vs. Horizontal

- Vertical Scaling (Scale‑Up): Boost capacity of a single server by adding CPU, RAM, or storage 

- Horizontal Scaling (Scale‑Out): Add more servers or instances to share load; often more resilient and cost-effective at scale

----

# 3. System Architecture

## 3.1. Monolithic vs. Microservices
- Monolithic apps are simple to start, but scale poorly under unpredictable loads

- Microservices break functionality into independent services, improving modularity and allowing parts of the system to scale independently

## 3.2. HTTP service communication vs. Event-Driven

### **HTTP (Request–Response Model)**

Your services communicate with each other via HTTP requests, like your frontend and backend.

* **Strengths**:

  * Simple and intuitive.
  * Easy to debug and prototype.
  * Works well when interactions are short and predictable.
* **Limitations**:

  * Tight coupling: the different services must both be available at the same time.
  * Can become a bottleneck under heavy loads, since every interaction is synchronous.

Example in a calory tracker app:
User submits meals throughout the day, the backend makes requests to the `meals` microservice to log them. On every new meal added, the `meals` service makes a request to the `statistics` microservice to update the total calories.

At the end of the day, the user looks at their statistics, the backend makes requests to the `statistics` microservice to get them.

### **Event-Driven Architecture (EDA)**

* **How it works**: Systems communicate by emitting *events* (messages) that other services can react to asynchronously.
* **Analogy**: Like posting in a group chat — you send a message, anyone subscribed can react when they see it, at their own pace.

* **Strengths**:
  * Decoupled: services don’t need to know about each other directly.
  * Scales better under bursts of activity (events can be queued).
  * Enables real-time and reactive features.
* **Limitations**:

  * More complex to design and debug.
  * Harder to guarantee order or consistency of events without extra tooling.

Example in a calory tracker app:
User submits meals throughout the day, the backend emits an event `meal_logged`.
The `statistics` service listens for these events and updates totals in the background.

This way, logging meals stays fast even if processing nutrition totals is heavy.

----

# 4. Scalability Patterns
## 4.1 separation of concerns / decoupling
- Each file in the codebase should handle a single concern without hardcoded dependencies on other files in the code.

## 4.2
- Your code should be modular, plan for microservices even if your app is still a monolith