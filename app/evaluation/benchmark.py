"""
Evaluation Benchmark runner.
"""
import asyncio
from app.orchestrator.pipeline import AgentPipeline
from app.evaluation.sample_cases import EVALUATION_CASES
from app.evaluation.evaluator import PipelineEvaluator

async def run_benchmark():
    print("Starting ThinkFlow Evaluation Benchmark...")
    results = []
    
    for case in EVALUATION_CASES:
        print(f"\nRunning Case: {case['id']}")
        pipeline = AgentPipeline()
        
        context = await pipeline.run(case["prompt"])
        
        evaluation = PipelineEvaluator.evaluate(context)
        
        success_match = (context.status == "completed") == case["expected_success"]
        
        results.append({
            "case_id": case["id"],
            "expected_match": success_match,
            "evaluation": evaluation
        })
        print(f"Result: {context.status} | Score: {evaluation['execution_score']}/{evaluation['max_score']}")
        
    print("\nBenchmark Complete.")
    return results

if __name__ == "__main__":
    asyncio.run(run_benchmark())
