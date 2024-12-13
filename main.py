from field import Field
from resource_orchestrator import ResourceOrchestrator

def main():
    # Initialize a 1-acre field (208x208 grid)
    field = Field()

    # Define the resource type: ("flower", value_collected=1, number_of_collections=10)
    flower_type = ("flower", 1, 10)

    # Create a Resource Orchestrator to manage 50 flowers
    resource_orchestrator = ResourceOrchestrator(field, flower_type, count=50)

    # Spread the flowers across the field
    resource_orchestrator.spread_resources()

    # Display the field and resources
    print("Field with Resources:")
    field.display()
    print("\nResources:")
    resource_orchestrator.display_resources()

if __name__ == "__main__":
    main()
