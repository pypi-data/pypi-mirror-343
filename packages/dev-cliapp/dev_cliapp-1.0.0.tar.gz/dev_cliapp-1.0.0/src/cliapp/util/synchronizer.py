import asyncio
from typing import Coroutine, List, Callable, Any


def run(method: Coroutine, *args: Any, **kwargs: Any) -> None:
    """
    Runs an async coroutine until completion in a new event loop.
    This is typically used for running the top-level async function
    in a script.

    Args:
        method: The async coroutine function to run.
        *args: Positional arguments to pass to the coroutine.
        **kwargs: Keyword arguments to pass to the coroutine.
    """
    # Run the coroutine until it completes
    asyncio.run(method(*args, **kwargs))


async def resolve(futures: List[asyncio.Future]) -> List[Any]:
    """
    Awaits a list of futures concurrently and returns their results.
    This is a wrapper around asyncio.gather.

    Args:
        futures: A list of asyncio Future objects.

    Returns:
        A list of results corresponding to the completed futures.
    """
    # Gather results from multiple futures concurrently
    return await asyncio.gather(*futures)


async def execute(function: Callable, *args: Any, **kwargs: Any) -> Any:
    """
    Runs a synchronous (blocking) function in a separate thread
    using the event loop's executor to avoid blocking the loop.

    Args:
        function: The synchronous function to run.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        The result of the synchronous function.
    """
    # Define a helper function to wrap the blocking call
    def blockingFn():
        return function(*args, **kwargs)

    # Get the current event loop
    loop = asyncio.get_event_loop()
    
    # Run the blocking function in the default thread pool executor
    return await loop.run_in_executor(None, blockingFn)