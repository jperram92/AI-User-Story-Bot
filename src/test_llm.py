import asyncio
import logging
from services.llm_service import LLMService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_llm():
    # Create test data
    test_context = {
        "role": "customer service representative",
        "goal": "view customer history",
        "benefit": "provide better support",
        "acceptance_criteria": [
            "Can view past purchases",
            "Can see support ticket history"
        ]
    }

    # Initialize the service
    llm_service = LLMService()

    # Process the test data
    logger.info("Starting LLM test...")
    logger.info(f"Original context: {test_context}")
    
    result = await llm_service.process(test_context)
    
    logger.info(f"Enhanced result: {result}")
    
    # Print results in a readable format
    print("\nResults Summary:")
    print("-" * 50)
    print("Original:")
    print(f"Goal: {test_context['goal']}")
    print(f"Benefit: {test_context['benefit']}")
    print("\nEnhanced:")
    print(f"Goal: {result['goal']}")
    print(f"Benefit: {result['benefit']}")

if __name__ == "__main__":
    asyncio.run(test_llm())
