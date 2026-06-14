import time

class ProductionSystem:
    """Represents a simulated production system with a performance metric and status."""
    def __init__(self, name="CoreService"):
        self.name = name
        self.performance_metric = 0.95 # e.g., 95% uptime or efficiency
        self.status = "stable"
        print(f"[{self.name}] System initialized. Performance: {self.performance_metric*100:.0f}%")

    def degrade_performance(self, amount=0.1):
        self.performance_metric -= amount
        if self.performance_metric < 0.5:
            self.status = "critical"
        elif self.performance_metric < 0.8:
            self.status = "degraded"
        print(f"[{self.name}] Performance degraded to {self.performance_metric*100:.0f}%. Status: {self.status}")

class Developer:
    """Represents a developer who gives feedback on the production system."""
    def __init__(self, name="Alice"):
        self.name = name

    def give_feedback(self, system: ProductionSystem, feedback_type: str, details: str):
        print(f"\n[{self.name} giving feedback on {system.name}]")
        if feedback_type == "blaming":
            # This illustrates the 'risky' or 'bad' feedback mentioned in the article.
            # It's direct, lacks context, and can be perceived as confrontational.
            print(f"  Feedback (Blaming): '{details}'")
            return "blaming", details
        elif feedback_type == "urgent_unvetted":
            # This illustrates feedback with good intentions but potentially poor timing or lack of full impact assessment.
            # It might disrupt ongoing work or cause unnecessary alarm if not truly critical.
            print(f"  Feedback (Urgent/Unvetted): '{details}'")
            return "urgent_unvetted", details
        elif feedback_type == "constructive":
            # This illustrates the 'professional approach' and 'constructive feedback' emphasized in the article.
            # It's data-driven, solution-oriented, and considers the process.
            print(f"  Feedback (Constructive): '{details}'")
            return "constructive", details
        else:
            print(f"  Unknown feedback type: '{feedback_type}'")
            return "unknown", details

class FeedbackProcessor:
    """Simulates a manager or system evaluating feedback, leading to different outcomes."""
    def __init__(self, manager_name="Bob"):
        self.manager_name = manager_name
        print(f"\n[{self.manager_name} - Feedback Processor ready]")

    def process_feedback(self, dev_name: str, system: ProductionSystem, feedback_data: tuple):
        feedback_type, details = feedback_data
        print(f"\n[{self.manager_name} processing feedback from {dev_name} on {system.name}]")

        if feedback_type == "blaming":
            # This outcome reflects the article's warning about negative consequences for poorly delivered feedback.
            # The article states: "Unutmayın, önemli olan ne söylediğiniz kadar, bunu nasıl ve ne zaman söylediğinizdir."
            # (Remember, what you say is as important as how and when you say it.)
            print(f"  Received blaming feedback: '{details}'")
            print(f"  Outcome: Manager feels attacked, becomes defensive. Feedback is likely dismissed or causes friction.")
            print(f"  Consequence for {dev_name}: Perceived as unprofessional, potentially damages reputation.")
            return "negative_reputation"
        elif feedback_type == "urgent_unvetted":
            # This outcome reflects the risk of good intentions leading to disruptive results if timing or context is off.
            # The article mentions: "iyi niyetli girişimler, bazen beklenmedik ve olumsuz sonuçlarla karşılaşabilir."
            # (well-intentioned initiatives can sometimes encounter unexpected and negative consequences.)
            print(f"  Received urgent, unvetted feedback: '{details}'")
            if system.status == "critical":
                print(f"  Outcome: System is critical, urgent action is needed. Feedback is acted upon, and {dev_name} is seen as proactive.")
                print(f"  Consequence for {dev_name}: Could be seen as proactive in a crisis, but still risky if not a true emergency.")
                return "mixed_urgent_action"
            else:
                print(f"  Outcome: System is {system.status}. Urgent request without full context causes disruption to planned work.")
                print(f"  Consequence for {dev_name}: Seen as not understanding priorities, potentially causing rework or distraction.")
                return "disruptive_distraction"
        elif feedback_type == "constructive":
            # This outcome reflects the "solutions" part of the article and the benefits of professional feedback.
            # The article suggests: "kariyerinizi riske atmadan nasıl profesyonel bir yaklaşım sergileyebileceğinizi adım adım keşfedeceğiz."
            # (we will discover step by step how you can exhibit a professional approach without risking your career.)
            print(f"  Received constructive feedback: '{details}'")
            print(f"  Outcome: Manager appreciates the data-driven approach and proposed solutions. Feedback is prioritized for investigation.")
            print(f"  Consequence for {dev_name}: Seen as a valuable, proactive, and professional team member. Builds trust.")
            return "positive_recognition"
        else:
            print(f"  Outcome: Unknown feedback type. No action taken.")
            return "no_action"

# --- Simulation --- 
if __name__ == "__main__":
    prod_system = ProductionSystem()
    alice = Developer("Alice")
    bob = FeedbackProcessor("Bob (Manager)")

    print("\n--- Scenario 1: Blaming Feedback ---")
    feedback_1 = alice.give_feedback(prod_system, "blaming", "This system is terribly slow! It's broken, fix it now!")
    bob.process_feedback(alice.name, prod_system, feedback_1)

    print("\n--- Scenario 2: Urgent, Unvetted Feedback (System Stable) ---")
    feedback_2 = alice.give_feedback(prod_system, "urgent_unvetted", "I found a potential bug in the caching layer. We need to deploy a hotfix immediately!")
    bob.process_feedback(alice.name, prod_system, feedback_2)

    print("\n--- Scenario 3: Constructive Feedback (System Stable) ---")
    feedback_3 = alice.give_feedback(prod_system, "constructive",
                                     "I've observed a slight performance dip during peak hours (data attached). "
                                     "My preliminary analysis suggests a potential optimization in the database query for report X. "
                                     "I'd like to propose a small investigation during our next planning cycle.")
    bob.process_feedback(alice.name, prod_system, feedback_3)

    print("\n--- Scenario 4: Urgent, Unvetted Feedback (System Critical) ---")
    # Re-evaluating urgent feedback when the system is actually critical. Context matters.
    prod_system.degrade_performance(0.2) # System becomes degraded
    prod_system.degrade_performance(0.15) # System becomes critical
    feedback_4 = alice.give_feedback(prod_system, "urgent_unvetted", "The system is showing critical performance degradation! My previous finding about the caching layer might be related. We need to investigate immediately!")
    bob.process_feedback(alice.name, prod_system, feedback_4)
