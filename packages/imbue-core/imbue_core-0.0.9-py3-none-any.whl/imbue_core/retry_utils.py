from loguru import logger
from tenacity import RetryCallState


def log_before_sleep(retry_state: RetryCallState) -> None:
    fn_name = retry_state.fn.__name__ if retry_state.fn is not None else "unknown"
    sleep_time = retry_state.next_action.sleep if retry_state.next_action is not None else 0
    outcome = retry_state.outcome
    if outcome is not None:
        exception = outcome.exception()
        error_message = type(exception).__name__ + ": " + str(exception)
    else:
        error_message = "unknown"
    logger.debug(
        f"Retrying {fn_name} in {sleep_time:.2f} seconds, attempt {retry_state.attempt_number} after error: {error_message}"
    )
