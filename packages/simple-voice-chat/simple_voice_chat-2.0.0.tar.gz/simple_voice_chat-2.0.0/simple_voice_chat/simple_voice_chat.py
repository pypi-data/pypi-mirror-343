import argparse
import json

# import logging # Removed standard logging
import random  # Added for random port selection
import sys  # Added for exiting on error

import threading  # Added for running server in background
import time
import datetime  # Added for heartbeat timestamping
import uvicorn  # Added for server control
import webbrowser  # Added for browser launch option
from pathlib import Path
from typing import List, Dict, Any, AsyncGenerator, Optional

from loguru import logger  # Added loguru
import litellm
import numpy as np
import webview  # Added for pywebview

from fastapi import FastAPI, Request
from fastapi.responses import (
    HTMLResponse,
    StreamingResponse,
    JSONResponse,
)
from fastrtc import (
    AdditionalOutputs,
    ReplyOnPause,
    Stream,
    get_twilio_turn_credentials,
    AlgoOptions,
    SileroVadOptions,
)
from gradio.utils import get_space  # Keep for get_twilio_turn_credentials check
from openai import OpenAI, AuthenticationError  # Added AuthenticationError
from pydantic import BaseModel

# Import raw environment variable accessors
# These will be used as defaults for argparse arguments
from .utils.env import (  # Use relative import for package structure
    LLM_HOST_ENV,  # Renamed
    LLM_PORT_ENV,  # Renamed
    DEFAULT_LLM_MODEL_ENV,  # Renamed
    LLM_API_KEY_ENV,  # Renamed
    STT_HOST_ENV,
    STT_PORT_ENV,
    STT_MODEL_ENV,
    STT_LANGUAGE_ENV,
    STT_API_KEY_ENV,
    STT_NO_SPEECH_PROB_THRESHOLD_ENV,
    STT_AVG_LOGPROB_THRESHOLD_ENV,
    STT_MIN_WORDS_THRESHOLD_ENV,
    TTS_HOST_ENV,
    TTS_PORT_ENV,
    TTS_MODEL_ENV,
    DEFAULT_VOICE_TTS_ENV,
    TTS_API_KEY_ENV,
    DEFAULT_TTS_SPEED_ENV,
    TTS_ACRONYM_PRESERVE_LIST_ENV,
    APP_PORT_ENV,
    SYSTEM_MESSAGE_ENV,  # Now Optional[str]
)

# Import other utils functions
from .utils.tts import (  # Use relative import for package structure
    get_voices,
    generate_tts_for_sentence,
    prepare_available_voices_data,  # Import new helper
)
from .utils.llms import (  # Use relative import for package structure
    get_models_and_costs_from_proxy,
    get_models_and_costs_from_litellm,
    calculate_llm_cost,  # Import the renamed function
)
from .utils.misc import is_port_in_use  # Use relative import for package structure
from .utils.stt import (
    transcribe_audio,
    check_stt_confidence,
)  # Use relative import for package structure

# load_dotenv() # Moved to utils.env

# --- Application Version ---
APP_VERSION = "2.0.0"
# --- End Application Version ---

# Environment variable loading and defaults are now handled in utils.env
# Logging related to env vars is also moved there.

# --- Global Configuration Variables (Set after parsing args) ---
# These will hold the final configuration values used by the application
llm_api_base: Optional[str] = None
stt_api_base: Optional[str] = None
tts_base_url: Optional[str] = None
use_llm_proxy: bool = False  # Renamed from use_litellm_proxy
TTS_ACRONYM_PRESERVE_SET: set[str] = set()
SYSTEM_MESSAGE: str = (
    ""  # Will hold the final system message string (empty if unspecified)
)
APP_PORT: int = 7860  # Default, will be updated by args
IS_OPENAI_TTS: bool = False  # Flag to indicate if using OpenAI TTS
IS_OPENAI_STT: bool = False  # Flag to indicate if using OpenAI STT

# --- State Variables (Managed during runtime) ---
AVAILABLE_MODELS: List[str] = []
MODEL_COST_DATA: Dict[str, Dict[str, float]] = {}
current_llm_model: Optional[str] = (
    None  # Set after parsing args and checking availability
)
AVAILABLE_VOICES_TTS: List[str] = []
# Known voices for OpenAI TTS API
OPENAI_TTS_VOICES = [
    "alloy",
    "echo",
    "fable",
    "onyx",
    "nova",
    "shimmer",
    "ash",
]  # Added ash
selected_voice: Optional[str] = None  # Set after parsing args and checking availability

# --- Clients (Initialized after parsing args) ---
tts_client: Optional[OpenAI] = None
stt_client: Optional[OpenAI] = None
# --- End Global Configuration & State ---

# --- Pricing Constants ---
# OpenAI TTS Pricing (USD per 1,000,000 characters) - As of Dec 2024
OPENAI_TTS_PRICING = {
    "tts-1": 15.00,
    "tts-1-hd": 30.00,
}
# --- End Pricing Constants ---


# --- Argument Parsing ---
# Moved parser creation inside main() to avoid global side effects if imported
# parser = argparse.ArgumentParser(...) # Moved

# --- Apply Argument Values to Global Configuration ---
# Moved configuration logic inside main()

# --- Logging Configuration (Loguru) ---
# Moved logger setup inside main()

# --- Log Final Configuration ---
# Moved logging inside main()

# --- Populate Models and Costs ---
# Moved population logic inside main()

# --- Client Initialization ---
# Moved client initialization inside main()

# --- Populate Available Voices (Revised Logic) ---
# Moved voice population logic inside main()

# --- Current Directory ---
# Moved inside main() where needed, or use relative paths


# --- Core Response Logic (Async Streaming with Background TTS) ---
async def response(
    audio: tuple[int, np.ndarray],
    chatbot: list[dict] | None = None,
) -> AsyncGenerator[Any, None]:
    """
    Handles audio input, performs STT, streams LLM response text chunks to UI,
    generates TTS concurrently, and yields final audio and updates.
    """
    # Access module-level variables set after arg parsing in main()
    # No need for 'global' for reading module-level variables like current_llm_model, selected_voice, etc.
    # Clients (tts_client, stt_client) are also accessed directly.
    # Args object holds command-line/env config (passed to main or accessed globally if needed)

    # Ensure clients are initialized (should be, but good practice)
    if not stt_client or not tts_client:
        logger.error("STT or TTS client not initialized. Cannot process request.")
        # Yield error state?
        return

    # Work with a copy to avoid modifying the input list directly and ensure clean state per call
    current_chatbot = (chatbot or []).copy()
    logger.info(
        f"--- Entering response function with history length: {len(current_chatbot)} ---"
    )
    # Use the copy for generating messages for the LLM
    messages = [{"role": d["role"], "content": d["content"]} for d in current_chatbot]

    # Add system message if defined
    if SYSTEM_MESSAGE:
        # Prepend system message if not already present (e.g., first turn)
        if not messages or messages[0].get("role") != "system":
            messages.insert(0, {"role": "system", "content": SYSTEM_MESSAGE})
            logger.debug("Prepended system message to LLM input.")
        elif (
            messages[0].get("role") == "system"
            and messages[0].get("content") != SYSTEM_MESSAGE
        ):
            # Update system message if it changed (though this shouldn't happen with current setup)
            messages[0]["content"] = SYSTEM_MESSAGE
            logger.debug("Updated existing system message in LLM input.")

    # Signal STT processing start
    yield AdditionalOutputs(
        {
            "type": "status_update",
            "status": "stt_processing",
            "message": "Transcribing...",
        }
    )

    # --- Speech-to-Text using imported function ---
    # Pass config values from args object (accessed via main's scope or global) and initialized client/base_url
    # Need access to args parsed in main()
    stt_success, prompt, stt_response_obj, stt_error = await transcribe_audio(
        audio,
        stt_client,  # Initialized client
        args.stt_model,  # From args (needs access)
        args.stt_language,  # From args (needs access)
        stt_api_base,  # Derived from args
    )

    if not stt_success:
        logger.error(f"STT failed: {stt_error}")
        stt_error_msg = {
            "role": "assistant",
            "content": f"[STT Error: {stt_error or 'Unknown STT failure'}]",
        }
        yield AdditionalOutputs({"type": "chatbot_update", "message": stt_error_msg})
        # Yield final state and status even on STT error to reset frontend
        logger.warning("Yielding final state after STT error...")
        yield AdditionalOutputs(
            {
                "type": "final_chatbot_state",
                "history": current_chatbot,
            }  # Yield original state
        )
        yield AdditionalOutputs(
            {
                "type": "status_update",
                "status": "idle",
                "message": "Ready (after STT error)",
            }
        )
        logger.info("--- Exiting response function after STT error ---")
        return

    # --- STT Confidence Check using imported function ---
    # Pass threshold values from args object (needs access)
    reject_transcription, rejection_reason = check_stt_confidence(
        stt_response_obj,
        prompt,
        args.stt_no_speech_prob_threshold,  # From args (needs access)
        args.stt_avg_logprob_threshold,  # From args (needs access)
        args.stt_min_words_threshold,  # From args (needs access)
    )

    if reject_transcription:
        logger.warning(f"STT confidence check failed: {rejection_reason}")
        # Yield status updates to go back to idle without processing this prompt
        yield AdditionalOutputs(
            {
                "type": "status_update",
                "status": "idle",
                "message": f"Listening (low confidence: {rejection_reason})",
            }
        )
        # Yield final state (unchanged history)
        yield AdditionalOutputs(
            {
                "type": "final_chatbot_state",
                "history": current_chatbot,  # Send back original history
            }
        )
        logger.info(
            "--- Exiting response function due to low STT confidence/word count ---"
        )
        return

    # --- Proceed if STT successful and confidence check passed ---
    # Yield user message update and add to the *copy*
    user_message = {"role": "user", "content": prompt}
    current_chatbot.append(user_message)
    yield AdditionalOutputs({"type": "chatbot_update", "message": user_message})
    # Update messages list based on the modified copy
    messages.append(user_message)

    # --- Streaming Chat Completion & Concurrent TTS ---
    llm_response_stream = None
    full_response_text = ""
    sentence_buffer = ""
    # tts_tasks = [] # Removed: We will yield audio immediately
    final_usage_info = None
    llm_error_occurred = False
    first_chunk_yielded = False  # Track if we yielded the first chunk for UI
    response_completed_normally = False  # Track normal completion
    total_tts_chars = 0  # Initialize TTS character counter

    try:
        # Signal waiting for LLM
        yield AdditionalOutputs(
            {
                "type": "status_update",
                "status": "llm_waiting",
                "message": "Waiting for AI...",
            }
        )
        llm_start_time = time.time()
        logger.info(
            f"Sending prompt to LLM ({current_llm_model}) for streaming..."
        )  # Changed to info
        llm_args_dict = {  # Renamed to avoid conflict with global 'args'
            "model": current_llm_model,
            "messages": messages,  # Use the history including the user prompt
            "stream": True,
            "stream_options": {
                "include_usage": True
            },  # Request usage data in the stream
            # Use module-level llm_api_base and use_llm_proxy derived from args
            **({"api_base": llm_api_base} if use_llm_proxy else {}),  # Use renamed flag
        }
        # Use API key from args (Renamed) (needs access)
        if args.llm_api_key:  # Renamed arg
            llm_args_dict["api_key"] = args.llm_api_key  # Renamed arg

        llm_response_stream = await litellm.acompletion(**llm_args_dict)

        async for chunk in llm_response_stream:
            logger.debug(f"CHUNK: {chunk}")
            # print(f"CHUNK: {chunk}") # Optional: uncomment for verbose chunk logging
            # Check for content delta first
            delta_content = None
            if chunk.choices and chunk.choices[0].delta:
                delta_content = chunk.choices[0].delta.content

            if delta_content:
                # Yield text chunk immediately for UI update
                yield AdditionalOutputs(
                    {"type": "text_chunk_update", "content": delta_content}
                )
                first_chunk_yielded = True

                sentence_buffer += delta_content
                full_response_text += delta_content

            # Check for usage information in the chunk (often in the *last* chunk)
            # LiteLLM might attach it differently depending on the provider.
            # Let's check more robustly.
            chunk_usage = getattr(chunk, "usage", None) or getattr(
                chunk, "_usage", None
            )  # Check common attributes
            if chunk_usage:
                # If usage is already a dict, use it, otherwise try .dict()
                if isinstance(chunk_usage, dict):
                    final_usage_info = chunk_usage
                elif hasattr(chunk_usage, "dict"):
                    final_usage_info = chunk_usage.dict()
                else:
                    final_usage_info = vars(chunk_usage)  # Fallback to vars()

                logger.info(
                    f"Captured usage info from LLM chunk: {final_usage_info}"
                )  # Changed to info

            # Process buffer when a newline is found (simple sentence splitting)
            # Check delta_content again to avoid processing non-content chunks
            if delta_content:
                while "\n" in sentence_buffer:
                    sentence, rest = sentence_buffer.split("\n", 1)
                    sentence = sentence.strip()  # Clean sentence
                    sentence_buffer = rest  # Keep the remainder

                    if sentence:
                        # Count characters for TTS cost calculation
                        total_tts_chars += len(sentence)
                        logger.debug(
                            f"Generating TTS for sentence: '{sentence[:50]}...' ({len(sentence)} chars)"
                        )
                        # Pass TTS config values from args (needs access) and module-level state/clients
                        audio_result = await generate_tts_for_sentence(
                            sentence,
                            tts_client,  # Initialized client
                            args.tts_model,  # From args (needs access)
                            selected_voice,  # Current selected voice (module-level)
                            args.tts_speed,  # From args (needs access)
                            TTS_ACRONYM_PRESERVE_SET,  # Derived from args (module-level)
                        )
                        if audio_result:
                            logger.debug(
                                f"Yielding audio chunk for sentence: '{sentence[:50]}...'"
                            )
                            yield audio_result
                        else:
                            logger.warning(
                                f"TTS failed for sentence, skipping audio yield: '{sentence[:50]}...'"
                            )
                    else:
                        logger.debug("Skipping empty line for TTS task.")

        # After the loop, process any remaining text in the buffer
        remaining_sentence = sentence_buffer.strip()
        if remaining_sentence:
            # Count characters for TTS cost calculation
            total_tts_chars += len(remaining_sentence)
            # Yield audio for the remaining buffer immediately
            logger.debug(
                f"Generating TTS for remaining buffer: '{remaining_sentence[:50]}...' ({len(remaining_sentence)} chars)"
            )
            # Pass TTS config values from args (needs access) and module-level state/clients
            audio_result = await generate_tts_for_sentence(
                remaining_sentence,
                tts_client,  # Initialized client
                args.tts_model,  # From args (needs access)
                selected_voice,  # Current selected voice (module-level)
                args.tts_speed,  # From args (needs access)
                TTS_ACRONYM_PRESERVE_SET,  # Derived from args (module-level)
            )
            if audio_result:
                logger.debug(
                    f"Yielding audio chunk for remaining buffer: '{remaining_sentence[:50]}...'"
                )
                yield audio_result
            else:
                logger.warning(
                    f"TTS failed for remaining buffer, skipping audio yield: '{remaining_sentence[:50]}...'"
                )

        llm_end_time = time.time()
        logger.info(
            f"LLM streaming finished ({llm_end_time - llm_start_time:.2f}s). Full response length: {len(full_response_text)}"
        )
        logger.info(
            f"Total characters sent to TTS: {total_tts_chars}"
        )  # Log total TTS chars

        # --- Final Updates (After LLM stream and TTS generation/yielding) ---
        response_completed_normally = (
            not llm_error_occurred
        )  # Mark normal completion if no LLM error occurred

        # 1. Cost Calculation (LLM and TTS)
        cost_result = {}  # Initialize cost result dict
        tts_cost = 0.0  # Initialize TTS cost

        # Calculate TTS cost if applicable
        if IS_OPENAI_TTS and total_tts_chars > 0:
            tts_model_used = args.tts_model  # Needs access to args
            if tts_model_used in OPENAI_TTS_PRICING:
                price_per_million_chars = OPENAI_TTS_PRICING[tts_model_used]
                tts_cost = (total_tts_chars / 1_000_000) * price_per_million_chars
                logger.info(
                    f"Calculated OpenAI TTS cost for {total_tts_chars} chars ({tts_model_used}): ${tts_cost:.6f}"
                )
            else:
                logger.warning(
                    f"Cannot calculate TTS cost: Pricing unknown for model '{tts_model_used}'."
                )
        elif total_tts_chars > 0:
            logger.info(
                f"TTS cost calculation skipped (not using OpenAI TTS or 0 chars). Total chars: {total_tts_chars}"
            )

        cost_result["tts_cost"] = tts_cost  # Add TTS cost (even if 0) to the result

        # Calculate LLM cost (if usage info available)
        if final_usage_info:
            # Pass the global MODEL_COST_DATA to the imported function (Renamed)
            llm_cost_result = calculate_llm_cost(  # Renamed function call
                current_llm_model, final_usage_info, MODEL_COST_DATA
            )
            # Merge LLM cost results into the main cost_result dict
            cost_result.update(llm_cost_result)
            logger.info("LLM cost calculation successful.")
        elif not llm_error_occurred:
            logger.warning(
                "No final usage information received from LLM stream, cannot calculate LLM cost accurately."
            )
            cost_result["error"] = "LLM usage info missing"
            cost_result["model"] = current_llm_model
            # Ensure LLM cost fields are present but potentially zero or marked
            cost_result.setdefault("input_cost", 0.0)
            cost_result.setdefault("output_cost", 0.0)
            cost_result.setdefault(
                "total_cost", 0.0
            )  # This might be misleading, maybe remove? Let's keep it for structure.

        # Yield combined cost update
        logger.info(f"Yielding combined cost update: {cost_result}")
        yield AdditionalOutputs({"type": "cost_update", "data": cost_result})
        logger.info("Cost update yielded.")

        # 2. Add Full Assistant Text Response to History (to the copy)
        assistant_message = None  # Define outside the 'if'
        if not llm_error_occurred and full_response_text:
            assistant_message = {"role": "assistant", "content": full_response_text}
            # Check against the copy and append to the copy
            if not current_chatbot or current_chatbot[-1] != assistant_message:
                current_chatbot.append(assistant_message)
                logger.info(
                    "Full assistant response added to chatbot history copy for next turn."
                )
            else:
                logger.info(
                    "Full assistant response already present in history, skipping append."
                )
        elif not llm_error_occurred:
            logger.warning(
                "LLM stream completed but produced no text content. History not updated."
            )

        # 3. Yield Final Chatbot State Update (if response completed normally)
        # This signals the end of the bot's turn and provides the final history.
        if response_completed_normally:
            logger.info("Yielding final chatbot state update...")
            # Send the modified copy of the history.
            yield AdditionalOutputs(
                {
                    "type": "final_chatbot_state",
                    "history": current_chatbot,
                }  # Yield the copy
            )
            logger.info("Final chatbot state update yielded.")

        # 4. Yield Final Status Update (always, should be the last yield in the success path)
        final_status_message = (
            "Ready" if response_completed_normally else "Ready (after error)"
        )
        logger.info(f"Yielding final status update ({final_status_message})...")
        yield AdditionalOutputs(
            {
                "type": "status_update",
                "status": "idle",
                "message": final_status_message,
            }
        )
        logger.info("Final status update yielded.")

    except AuthenticationError as e:  # Catch OpenAI specific auth errors
        logger.error(f"OpenAI Authentication Error during processing: {e}")
        response_completed_normally = False
        llm_error_occurred = True  # Treat as LLM/TTS error

        error_content = f"\n[Authentication Error: Check your API key ({e})]"
        if not first_chunk_yielded:
            llm_error_msg = {"role": "assistant", "content": error_content.strip()}
            yield AdditionalOutputs(
                {"type": "chatbot_update", "message": llm_error_msg}
            )
        else:
            yield AdditionalOutputs(
                {"type": "text_chunk_update", "content": error_content}
            )

        logger.warning("Yielding final chatbot state (after auth exception)...")
        yield AdditionalOutputs(
            {"type": "final_chatbot_state", "history": current_chatbot}
        )
        logger.warning("Final chatbot state (after auth exception) yielded.")

        logger.warning("Yielding final status update (idle, after auth exception)...")
        yield AdditionalOutputs(
            {"type": "status_update", "status": "idle", "message": "Ready (Auth Error)"}
        )
        logger.warning("Final status update (idle, after auth exception) yielded.")

    except Exception as e:
        # --- Error Handling Path ---
        logger.error(
            f"Error during LLM streaming or TTS processing: {e}", exc_info=True
        )  # Add traceback
        response_completed_normally = False  # Ensure this is false on exception
        llm_error_occurred = True  # Ensure error is flagged

        # Yield an error message to the UI
        error_content = f"\n[LLM/TTS Error: {type(e).__name__}]"  # Show error type
        if not first_chunk_yielded:
            # If no text yielded, send as a full message
            llm_error_msg = {"role": "assistant", "content": error_content.strip()}
            yield AdditionalOutputs(
                {"type": "chatbot_update", "message": llm_error_msg}
            )
            # Note: We don't add this error message to current_chatbot to keep history clean
        else:
            # If text chunks were already sent, append error info via chunk update
            yield AdditionalOutputs(
                {"type": "text_chunk_update", "content": error_content}
            )

        # Yield the final chatbot state (as it was when the error occurred)
        # This includes the user message but not the failed assistant response.
        logger.warning("Yielding final chatbot state (after exception)...")
        yield AdditionalOutputs(
            {
                "type": "final_chatbot_state",
                "history": current_chatbot,
            }  # Yield state at time of error
        )
        logger.warning("Final chatbot state (after exception) yielded.")

        # Ensure final status update is yielded last in the error path too
        logger.warning("Yielding final status update (idle, after exception)...")
        yield AdditionalOutputs(
            {
                "type": "status_update",
                "status": "idle",
                "message": "Ready (after error)",
            }
        )
        logger.warning("Final status update (idle, after exception) yielded.")

    # This log executes *after* the try/except/finally block completes and generator exits
    logger.info(
        f"--- Response function generator finished (Completed normally: {response_completed_normally}) ---"
    )


# --- FastAPI Setup ---
# Moved stream creation inside main() to access args for VAD tuning if needed
# stream = Stream(...) # Moved


class Message(BaseModel):
    role: str
    content: str


class InputData(BaseModel):
    webrtc_id: str
    chatbot: list[Message]


# Moved app creation inside main()
# app = FastAPI()
# stream.mount(app) # Moved

# --- Endpoint Definitions ---
# These need access to the 'app' and 'stream' objects created in main()
# We can define them here but register them with the app inside main()


def register_endpoints(app: FastAPI, stream: Stream):
    """Registers FastAPI endpoints."""
    # Get current directory relative to this file
    curr_dir = Path(__file__).parent

    @app.get("/")
    async def _():
        rtc_config = get_twilio_turn_credentials() if get_space() else None
        index_path = curr_dir / "index.html"
        if not index_path.exists():
            logger.error("index.html not found in the current directory!")
            return HTMLResponse(
                content="<html><body><h1>Error: index.html not found</h1></body></html>",
                status_code=500,
            )

        html_content = index_path.read_text()
        # Inject RTC config
        if rtc_config:
            html_content = html_content.replace(
                "__RTC_CONFIGURATION__", json.dumps(rtc_config)
            )
        else:
            html_content = html_content.replace("__RTC_CONFIGURATION__", "null")

        # Inject the system message (using the final SYSTEM_MESSAGE string)
        html_content = html_content.replace(
            "__SYSTEM_MESSAGE_JSON__", json.dumps(SYSTEM_MESSAGE)
        )
        # Inject the auto-start flag (from args) (needs access)
        html_content = html_content.replace(
            "__AUTO_START_FLAG__", json.dumps(args.auto_start)  # Use args directly
        )
        # Inject the application version
        html_content = html_content.replace("__APP_VERSION__", APP_VERSION)

        return HTMLResponse(content=html_content, status_code=200)

    @app.post("/input_hook")
    async def _(body: InputData):
        chatbot_history = [msg.model_dump() for msg in body.chatbot]
        # Since the handler is now async, setting input might need adjustment
        # if fastrtc doesn't handle async handler state passing automatically.
        # Assuming fastrtc handles passing the `chatbot` argument to the async handler correctly.
        # If issues arise, we might need to store/retrieve state differently.
        stream.set_input(body.webrtc_id, chatbot_history)  # Keep as is for now
        return {"status": "ok"}

    @app.get("/outputs")
    def _(webrtc_id: str):
        async def output_stream():
            try:
                async for output in stream.output_stream(webrtc_id):
                    # The async handler `response` now yields audio tuples directly
                    # and AdditionalOutputs for SSE events.
                    if isinstance(output, AdditionalOutputs):
                        data_payload = output.args[0]
                        if isinstance(data_payload, dict) and "type" in data_payload:
                            event_type = data_payload["type"]
                            try:
                                event_data_json = json.dumps(data_payload)
                                logger.debug(
                                    f"Sending SSE event: type={event_type}, data={event_data_json[:100]}..."
                                )
                                yield f"event: {event_type}\ndata: {event_data_json}\n\n"
                            except TypeError as e:
                                logger.error(
                                    f"Failed to serialize AdditionalOutputs payload to JSON: {e}. Payload: {data_payload}"
                                )
                        else:
                            logger.warning(
                                f"Received AdditionalOutputs with unexpected payload structure: {data_payload}"
                            )
                    # Audio chunks are handled by WebRTC track, not sent via SSE.
                    # The handler yields them, fastrtc puts them on the track.
                    elif (
                        isinstance(output, tuple)
                        and len(output) == 2
                        and isinstance(output[1], np.ndarray)
                    ):
                        # This case should be handled by fastrtc internally for the audio track.
                        # We don't need to send it via SSE. Log if it appears here unexpectedly.
                        logger.debug(
                            f"Output stream received audio tuple for webrtc_id {webrtc_id}, should be handled by track."
                        )
                        pass  # Audio is sent via WebRTC track
                    elif isinstance(output, bytes):
                        logger.warning(
                            "Received raw bytes directly in output stream, expected AdditionalOutputs or audio tuple via handler."
                        )
                    else:
                        logger.warning(
                            f"Received unexpected output type in stream: {type(output)}"
                        )
            except Exception as e:
                logger.error(f"Error in output stream for webrtc_id {webrtc_id}: {e}")
                # Optionally send an error event to the client via SSE if possible
                try:
                    error_payload = {
                        "type": "error_event",
                        "message": f"Server stream error: {e}",
                    }
                    yield f"event: error_event\ndata: {json.dumps(error_payload)}\n\n"
                except Exception as send_err:
                    logger.error(
                        f"Failed to send error event to client {webrtc_id}: {send_err}"
                    )

        return StreamingResponse(output_stream(), media_type="text/event-stream")

    # --- Endpoint to Get Available Models ---
    @app.get("/available_models")
    async def get_available_models():
        global current_llm_model, AVAILABLE_MODELS
        # AVAILABLE_MODELS is now populated at startup based on proxy or litellm.model_cost
        # It will contain prefixed names if using proxy
        return JSONResponse(
            {"available": AVAILABLE_MODELS, "current": current_llm_model}
        )

    # --- Endpoint to Get Available Voices ---
    @app.get("/available_voices_tts")
    async def get_available_voices():
        # Access module-level state variables
        # No 'global' needed for reading
        # AVAILABLE_VOICES_TTS is populated correctly at startup based on IS_OPENAI_TTS flag
        response_data = prepare_available_voices_data(
            selected_voice, AVAILABLE_VOICES_TTS
        )
        return JSONResponse(response_data)

    # --- End Voice Endpoint ---

    # --- Endpoint to Switch Voice ---
    @app.post("/switch_voice")
    async def switch_voice(request: Request):
        global selected_voice  # Need global to modify module-level state
        try:
            data = await request.json()
            new_voice_name = data.get("voice_name")

            if new_voice_name:
                if new_voice_name != selected_voice:
                    # Check if the new voice exists in our dynamically loaded/predefined list
                    if new_voice_name in AVAILABLE_VOICES_TTS:
                        selected_voice = new_voice_name
                        logger.info(f"Switched active TTS voice to: {selected_voice}")
                        return JSONResponse(
                            {"status": "success", "voice": selected_voice}
                        )
                    else:
                        # Voice not found in the available list
                        logger.warning(
                            f"Attempted to switch to voice '{new_voice_name}' which is not in the available list: {AVAILABLE_VOICES_TTS}"
                        )
                        return JSONResponse(
                            {
                                "status": "error",
                                "message": f"Voice '{new_voice_name}' is not available.",
                            },
                            status_code=400,
                        )
                else:
                    logger.info(f"Voice already set to: {new_voice_name}")
                    return JSONResponse(
                        {"status": "success", "voice": selected_voice}
                    )  # Still success
            else:
                logger.warning(f"Missing voice_name in switch request.")
                return JSONResponse(
                    {
                        "status": "error",
                        "message": f"Missing 'voice_name' in request body.",
                    },
                    status_code=400,
                )
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON body in /switch_voice")
            return JSONResponse(
                {"status": "error", "message": "Invalid JSON format in request body"},
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Error processing /switch_voice request: {e}")
            return JSONResponse(
                {"status": "error", "message": f"Internal server error: {e}"},
                status_code=500,
            )

    # --- End Switch Voice Endpoint ---

    # --- Endpoint to Switch Model ---
    @app.post("/switch_model")
    async def switch_model(request: Request):
        global current_llm_model  # Need global to modify module-level state
        # AVAILABLE_MODELS and MODEL_COST_DATA are read-only here
        try:
            data = await request.json()
            new_model_name = data.get(
                "model_name"
            )  # This name comes from the frontend dropdown (already prefixed if from proxy)

            if new_model_name:
                if new_model_name != current_llm_model:
                    # Check if the new model exists in our loaded list (which contains prefixed names if applicable)
                    if new_model_name in AVAILABLE_MODELS:
                        current_llm_model = new_model_name
                        logger.info(
                            f"Switched active LLM model to: {current_llm_model}"
                        )
                        # Check if cost data is available for the switched model (using the potentially prefixed name)
                        if (
                            new_model_name not in MODEL_COST_DATA
                            or MODEL_COST_DATA[new_model_name].get(
                                "input_cost_per_token"
                            )
                            is None
                        ):
                            logger.warning(
                                f"Cost data might be missing or incomplete for the newly selected model '{current_llm_model}'."
                            )
                        return JSONResponse(
                            {"status": "success", "model": current_llm_model}
                        )
                    else:
                        # Model not found in the available list
                        logger.warning(
                            f"Attempted to switch to model '{new_model_name}' which is not in the available list: {AVAILABLE_MODELS}"
                        )
                        return JSONResponse(
                            {
                                "status": "error",
                                "message": f"Model '{new_model_name}' is not available.",
                            },
                            status_code=400,
                        )
                else:
                    logger.info(f"Model already set to: {new_model_name}")
                    return JSONResponse(
                        {"status": "success", "model": current_llm_model}
                    )  # Still success
            else:
                logger.warning(f"Missing model_name in switch request.")
                return JSONResponse(
                    {
                        "status": "error",
                        "message": f"Missing 'model_name' in request body.",
                    },
                    status_code=400,
                )
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON body in /switch_model")
            return JSONResponse(
                {"status": "error", "message": "Invalid JSON format in request body"},
                status_code=400,
            )
        except Exception as e:
            logger.error(f"Error processing /switch_model request: {e}")
            return JSONResponse(
                {"status": "error", "message": f"Internal server error: {e}"},
                status_code=500,
            )

    # --- Heartbeat Endpoint ---
    @app.post("/heartbeat")
    async def heartbeat(request: Request):
        """Receives heartbeat pings from the frontend."""
        global last_heartbeat_time
        try:
            # Update the last heartbeat time using timezone-aware datetime
            last_heartbeat_time = datetime.datetime.now(datetime.timezone.utc)
            # Log received heartbeat and payload for debugging
            payload = await request.json()
            logger.debug(
                f"Heartbeat received at {last_heartbeat_time}. Payload: {payload}"
            )
            return {"status": "ok"}
        except json.JSONDecodeError:
            # Handle cases where the body might not be valid JSON (e.g., empty from sendBeacon)
            last_heartbeat_time = datetime.datetime.now(datetime.timezone.utc)
            logger.debug(
                f"Heartbeat received at {last_heartbeat_time} (no valid JSON payload)."
            )
            return {"status": "ok"}
        except Exception as e:
            logger.error(f"Error processing heartbeat: {e}")
            return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


# --- Pywebview API Class ---
class Api:
    def __init__(self, window):
        self._window = window

    def close(self):
        """Close the pywebview window."""
        logger.info("API close method called.")
        if self._window:
            self._window.destroy()
        # No os._exit needed, window closure triggers shutdown in main thread


# --- Heartbeat Globals ---
last_heartbeat_time: datetime.datetime | None = None
heartbeat_timeout: int = 15  # Seconds before assuming client disconnected
shutdown_event = threading.Event()  # Used to signal monitor thread to stop
pywebview_window = None  # To hold the pywebview window object if created
# --- End Heartbeat Globals ---

# Global variable to hold the Uvicorn server instance
uvicorn_server = None

# Global variable to hold parsed args (needed by response and endpoints)
args: Optional[argparse.Namespace] = None


# --- Heartbeat Monitoring Thread ---
def monitor_heartbeat_thread():
    """Monitors the time since the last heartbeat and triggers shutdown if timeout occurs."""
    global last_heartbeat_time, uvicorn_server, pywebview_window, shutdown_event
    logger.info("Heartbeat monitor thread started.")
    initial_wait_done = False

    while not shutdown_event.is_set():
        if last_heartbeat_time is None:
            if not initial_wait_done:
                logger.info(
                    f"Waiting for the first heartbeat (timeout check in {heartbeat_timeout * 2}s)..."
                )
                # Wait longer initially before the first check
                shutdown_event.wait(heartbeat_timeout * 2)
                initial_wait_done = True
                if shutdown_event.is_set():
                    break  # Exit if shutdown requested during initial wait
                continue  # Re-check condition after initial wait
            else:
                # If still None after initial wait, maybe log periodically?
                logger.debug("Still waiting for first heartbeat...")
                shutdown_event.wait(5)  # Check every 5 seconds after initial wait
                if shutdown_event.is_set():
                    break
                continue

        # Calculate time since last heartbeat
        time_since_last = (
            datetime.datetime.now(datetime.timezone.utc) - last_heartbeat_time
        )
        logger.debug(
            f"Time since last heartbeat: {time_since_last.total_seconds():.1f}s"
        )

        if time_since_last.total_seconds() > heartbeat_timeout:
            logger.warning(
                f"Heartbeat timeout ({heartbeat_timeout}s exceeded). Initiating shutdown."
            )
            # 1. Signal Uvicorn server to shut down
            if uvicorn_server:
                logger.info("Signaling Uvicorn server to stop...")
                uvicorn_server.should_exit = True
            else:
                logger.warning(
                    "Uvicorn server instance not found, cannot signal shutdown."
                )

            # 2. If in pywebview mode, destroy the window to unblock the main thread
            if pywebview_window:
                logger.info("Destroying pywebview window...")
                try:
                    # Schedule the destroy call on the main GUI thread if necessary
                    # For simplicity, try direct call first, might work depending on pywebview version/OS
                    pywebview_window.destroy()
                except Exception as e:
                    logger.error(
                        f"Error destroying pywebview window from monitor thread: {e}"
                    )
                    # Fallback: Try to signal main thread differently if needed, or rely on Uvicorn shutdown

            # 3. Exit the monitor thread
            break

        # Wait for a short interval before checking again
        shutdown_event.wait(5)  # Check every 5 seconds

    logger.info("Heartbeat monitor thread finished.")


def main() -> int:
    """Main function to parse arguments, set up, and run the application."""
    # Make globals modifiable within this function
    global args, llm_api_base, stt_api_base, tts_base_url, use_llm_proxy
    global TTS_ACRONYM_PRESERVE_SET, SYSTEM_MESSAGE, APP_PORT, IS_OPENAI_TTS, IS_OPENAI_STT
    global AVAILABLE_MODELS, MODEL_COST_DATA, current_llm_model, AVAILABLE_VOICES_TTS
    global selected_voice, tts_client, stt_client
    global uvicorn_server, pywebview_window  # For server/window management

    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(
        description="Run a simple voice chat interface using a configurable LLM provider, STT server, and TTS."
    )

    # --- General Arguments ---
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address to bind the FastAPI server to. Default: 127.0.0.1",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(APP_PORT_ENV),  # Default from env
        help=f"Preferred port to run the FastAPI server on. Default: {APP_PORT_ENV}. (Env: APP_PORT)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG level)",
    )
    parser.add_argument(
        "--auto-start",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Automatically start the connection when the application loads. Default: True",
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        default=False,
        help="Launch the application in the default web browser instead of a dedicated GUI window. Default: False",
    )
    parser.add_argument(
        "--system-message",
        type=str,
        default=SYSTEM_MESSAGE_ENV,  # Default from env (can be None)
        help=f"System message to prepend to the chat history. Default: (from SYSTEM_MESSAGE env var, empty if unset).",
    )

    # --- LLM Arguments (Renamed) ---
    parser.add_argument(
        "--llm-host",  # Renamed
        type=str,
        default=LLM_HOST_ENV,  # Default from env (Renamed)
        help="Host address of the LLM proxy server (optional). Default: None. (Env: LLM_HOST)",  # Renamed env var
    )
    parser.add_argument(
        "--llm-port",  # Renamed
        type=str,  # Read as string, convert later if needed
        default=LLM_PORT_ENV,  # Default from env (Renamed)
        help="Port of the LLM proxy server (optional). Default: None. (Env: LLM_PORT)",  # Renamed env var
    )
    parser.add_argument(
        "--llm-model",  # Renamed
        type=str,
        default=DEFAULT_LLM_MODEL_ENV,  # Default from env (Renamed)
        help=f"Default LLM model to use (e.g., 'gpt-4o', 'litellm_proxy/claude-3-opus'). Default: '{DEFAULT_LLM_MODEL_ENV}'. (Env: LLM_MODEL)",  # Renamed env var, updated example prefix
    )
    parser.add_argument(
        "--llm-api-key",  # Renamed
        type=str,
        default=LLM_API_KEY_ENV,  # Default from env (Renamed)
        help="API key for the LLM provider/proxy (optional, depends on setup). Default: None. (Env: LLM_API_KEY)",  # Renamed env var
    )

    # --- STT Arguments ---
    parser.add_argument(
        "--stt-host",
        type=str,
        default=STT_HOST_ENV,  # Default from env (now api.openai.com)
        help=f"Host address of the STT server (e.g., 'api.openai.com' or 'localhost'). Default: '{STT_HOST_ENV}'. (Env: STT_HOST)",
    )
    parser.add_argument(
        "--stt-port",
        type=str,  # Read as string, convert later
        default=STT_PORT_ENV,  # Default from env (now 443)
        help=f"Port of the STT server (e.g., 443 for OpenAI, 8002 for local). Default: '{STT_PORT_ENV}'. (Env: STT_PORT)",
    )
    parser.add_argument(
        "--stt-model",
        type=str,
        default=STT_MODEL_ENV,  # Default from env (now whisper-1)
        help=f"STT model to use (e.g., 'whisper-1' for OpenAI, 'deepdml/faster-whisper-large-v3-turbo-ct2' for local). Default: '{STT_MODEL_ENV}'. (Env: STT_MODEL)",
    )
    parser.add_argument(
        "--stt-language",
        type=str,
        default=STT_LANGUAGE_ENV,  # Default from env
        help="Language code for STT (e.g., 'en', 'fr'). If unset, Whisper usually auto-detects. Default: None. (Env: STT_LANGUAGE)",
    )
    parser.add_argument(
        "--stt-api-key",
        type=str,
        default=STT_API_KEY_ENV,  # Default from env
        help="API key for the STT server (REQUIRED for OpenAI STT). Default: None. (Env: STT_API_KEY)",
    )
    parser.add_argument(
        "--stt-no-speech-prob-threshold",
        type=float,
        default=float(STT_NO_SPEECH_PROB_THRESHOLD_ENV),  # Default from env
        help=f"STT confidence threshold: Reject if no_speech_prob is higher than this. Default: {STT_NO_SPEECH_PROB_THRESHOLD_ENV}. (Env: STT_NO_SPEECH_PROB_THRESHOLD)",
    )
    parser.add_argument(
        "--stt-avg-logprob-threshold",
        type=float,
        default=float(STT_AVG_LOGPROB_THRESHOLD_ENV),  # Default from env
        help=f"STT confidence threshold: Reject if avg_logprob is lower than this. Default: {STT_AVG_LOGPROB_THRESHOLD_ENV}. (Env: STT_AVG_LOGPROB_THRESHOLD)",
    )
    parser.add_argument(
        "--stt-min-words-threshold",
        type=int,
        default=int(STT_MIN_WORDS_THRESHOLD_ENV),  # Default from env
        help=f"STT confidence threshold: Reject if the number of words is less than this. Default: {STT_MIN_WORDS_THRESHOLD_ENV}. (Env: STT_MIN_WORDS_THRESHOLD)",
    )

    # --- TTS Arguments ---
    parser.add_argument(
        "--tts-host",
        type=str,
        default=TTS_HOST_ENV,  # Default from env (now api.openai.com)
        help=f"Host address of the TTS server (e.g., 'api.openai.com' or 'localhost'). Default: '{TTS_HOST_ENV}'. (Env: TTS_HOST)",
    )
    parser.add_argument(
        "--tts-port",
        type=str,  # Read as string, convert later
        default=TTS_PORT_ENV,  # Default from env (now 443)
        help=f"Port of the TTS server (e.g., 443 for OpenAI, 8880 for local). Default: '{TTS_PORT_ENV}'. (Env: TTS_PORT)",
    )
    parser.add_argument(
        "--tts-model",
        type=str,
        default=TTS_MODEL_ENV,  # Default from env (now tts-1)
        help=f"TTS model to use (e.g., 'tts-1', 'tts-1-hd' for OpenAI, 'kokoro' for local). Default: '{TTS_MODEL_ENV}'. (Env: TTS_MODEL)",
    )
    parser.add_argument(
        "--tts-voice",
        type=str,
        default=DEFAULT_VOICE_TTS_ENV,  # Default from env (now ash)
        help=f"Default TTS voice to use (e.g., 'alloy', 'ash', 'echo' for OpenAI, 'ff_siwis' for local). Default: '{DEFAULT_VOICE_TTS_ENV}'. (Env: TTS_VOICE)",
    )
    parser.add_argument(
        "--tts-api-key",
        type=str,
        default=TTS_API_KEY_ENV,  # Default from env
        help="API key for the TTS server (REQUIRED for OpenAI TTS). Default: None. (Env: TTS_API_KEY)",
    )
    parser.add_argument(
        "--tts-speed",
        type=float,
        default=float(DEFAULT_TTS_SPEED_ENV),  # Default from env
        help=f"Default TTS speed multiplier. Default: {DEFAULT_TTS_SPEED_ENV}. (Env: TTS_SPEED)",
    )
    parser.add_argument(
        "--tts-acronym-preserve-list",
        type=str,
        default=TTS_ACRONYM_PRESERVE_LIST_ENV,  # Default from env
        help=f"Comma-separated list of acronyms to preserve during TTS (currently only used for Kokoro TTS). Default: '{TTS_ACRONYM_PRESERVE_LIST_ENV}'. (Env: TTS_ACRONYM_PRESERVE_LIST)",
    )

    args = parser.parse_args()  # Assign to global 'args'

    # --- Apply Argument Values to Global Configuration ---

    # General
    APP_PORT = args.port
    # Handle potential None for system_message argument
    system_message_arg = args.system_message
    SYSTEM_MESSAGE = (
        system_message_arg.strip() if system_message_arg is not None else ""
    )

    # LLM Configuration (Using Renamed Args)
    use_llm_proxy = bool(args.llm_host and args.llm_port)  # Renamed arg
    if use_llm_proxy:
        try:
            llm_port_int = int(args.llm_port)  # Renamed arg
            llm_api_base = f"http://{args.llm_host}:{llm_port_int}/v1"  # Renamed arg
        except (ValueError, TypeError):
            logger.error(
                f"Invalid LLM port specified: '{args.llm_port}'. Disabling proxy."  # Renamed arg
            )
            use_llm_proxy = False
            llm_api_base = None  # Ensure it's None if proxy disabled due to bad port
    else:
        llm_api_base = None  # Explicitly None if not using proxy

    # STT Configuration (Revised Logic)
    stt_host = args.stt_host
    stt_port_str = args.stt_port  # Keep as string for comparison
    stt_api_key = args.stt_api_key  # Keep API key separate

    # Determine if using OpenAI STT based on host
    IS_OPENAI_STT = stt_host == "api.openai.com"

    if IS_OPENAI_STT:
        # Special case for OpenAI API
        stt_api_base = "https://api.openai.com/v1"
        logger.info(f"Configuring STT for OpenAI API at {stt_api_base}")
        if not stt_api_key:
            logger.critical(
                "STT_API_KEY is required when using OpenAI STT (stt-host=api.openai.com). "
                "Set the STT_API_KEY environment variable or provide --stt-api-key argument. Exiting."
            )
            return 1  # Return error code
    else:
        # Assume local or other custom server
        try:
            stt_port_int = int(stt_port_str)
            # Assume http for non-OpenAI servers
            scheme = "http"
            stt_api_base = f"{scheme}://{stt_host}:{stt_port_int}/v1"
            logger.info(f"Configuring STT for custom server at {stt_api_base}")
            # API key might be optional for custom servers
            if not stt_api_key:
                logger.warning(
                    f"No STT API key provided for custom server at {stt_api_base}. Assuming it's not needed."
                )

        except (ValueError, TypeError):
            logger.critical(
                f"Invalid STT port specified for custom server: '{stt_port_str}'. Cannot connect. Exiting."
            )
            return 1  # Return error code

    # TTS Configuration (Revised Logic)
    tts_host = args.tts_host
    tts_port_str = args.tts_port  # Keep as string for comparison
    tts_api_key = args.tts_api_key  # Keep API key separate

    # Determine if using OpenAI TTS based on host
    IS_OPENAI_TTS = tts_host == "api.openai.com"

    if IS_OPENAI_TTS:
        # Special case for OpenAI API
        tts_base_url = "https://api.openai.com/v1"
        logger.info(f"Configuring TTS for OpenAI API at {tts_base_url}")
        if not tts_api_key:
            logger.critical(
                "TTS_API_KEY is required when using OpenAI TTS (tts-host=api.openai.com). "
                "Set the TTS_API_KEY environment variable or provide --tts-api-key argument. Exiting."
            )
            return 1  # Return error code
    else:
        # Assume local or other custom server
        try:
            tts_port_int = int(tts_port_str)
            # Assume http for non-OpenAI servers unless port is 443? Let's default to http.
            scheme = "http"
            # Allow overriding scheme via host? No, keep it simple for now.
            tts_base_url = f"{scheme}://{tts_host}:{tts_port_int}/v1"
            logger.info(f"Configuring TTS for custom server at {tts_base_url}")
            # API key might be optional for custom servers
            if not tts_api_key:
                logger.warning(
                    f"No TTS API key provided for custom server at {tts_base_url}. Assuming it's not needed."
                )

        except (ValueError, TypeError):
            logger.critical(
                f"Invalid TTS port specified for custom server: '{tts_port_str}'. Cannot connect. Exiting."
            )
            return 1  # Return error code

    # TTS Acronyms
    TTS_ACRONYM_PRESERVE_SET = {
        word.strip().upper()
        for word in args.tts_acronym_preserve_list.split(",")
        if word.strip()
    }

    # --- Logging Configuration (Loguru) ---
    # Setup logger *after* parsing verbose flag
    logger.remove()  # Remove default handler

    log_level = "DEBUG" if args.verbose else "INFO"
    # Define format based on level
    log_format_debug = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    log_format_info = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    log_format = log_format_debug if log_level == "DEBUG" else log_format_info

    logger.add(
        sys.stderr,
        level=log_level,
        format=log_format,
        colorize=True,
        enqueue=True,
        backtrace=args.verbose,  # Enable backtrace only in verbose mode
        diagnose=args.verbose,  # Enable diagnose only in verbose mode
    )

    # Intercept standard logging messages
    # Set levels for libraries more finely if needed after interception
    logger.debug(
        f"Loaded TTS_ACRONYM_PRESERVE_SET: {TTS_ACRONYM_PRESERVE_SET}"
    )  # Log the loaded set
    # logger.level("websockets", level="INFO") # Example if needed
    # logger.level("fastrtc", level="INFO")
    # logger.level("uvicorn", level="WARNING") # Uvicorn logs might need specific handling
    # logger.level("litellm", level="INFO") # Keep litellm logs if desired
    # logger.level("requests", level="WARNING") # Example

    # --- Log Final Configuration ---
    logger.info(f"Logging level set to: {log_level}")
    logger.info(f"Application Version: {APP_VERSION}")  # Log the version
    logger.info(f"Application server host: {args.host}")
    logger.info(
        f"Application server preferred port: {args.port}"
    )  # Log preferred, actual might change
    if use_llm_proxy:
        logger.info(f"Using LLM proxy at: {llm_api_base}")  # Updated log message
        if args.llm_api_key:  # Renamed arg
            logger.info("Using LLM API key provided.")  # Updated log message
        else:
            logger.info("No LLM API key provided.")  # Updated log message
    else:
        logger.info(
            "Not using LLM proxy (using default LLM routing)."
        )  # Updated log message
        if args.llm_api_key:  # Renamed arg
            logger.info(
                "Using LLM API key provided (for direct routing)."
            )  # Updated log message

    # Log STT config based on type
    if IS_OPENAI_STT:
        logger.info(f"Using OpenAI STT at: {stt_api_base}")
        logger.info(f"Using STT model: {args.stt_model}")
        logger.info("Using STT API key provided (Required for OpenAI).")
    else:
        logger.info(f"Using Custom STT server at: {stt_api_base}")
        logger.info(f"Using STT model: {args.stt_model}")
        if args.stt_api_key:
            logger.info("Using STT API key provided.")
        else:
            logger.info("No STT API key provided (assumed optional for custom server).")

    if args.stt_language:
        logger.info(f"Using STT language: {args.stt_language}")
    else:
        logger.info("No STT language specified, Whisper will auto-detect.")
    logger.info(
        f"STT Confidence Thresholds: no_speech_prob > {args.stt_no_speech_prob_threshold}, avg_logprob < {args.stt_avg_logprob_threshold}, min_words < {args.stt_min_words_threshold}"
    )

    # Log TTS config based on type
    if IS_OPENAI_TTS:
        logger.info(f"Using OpenAI TTS at: {tts_base_url}")
        logger.info(f"Using TTS model: {args.tts_model}")
        logger.info(f"Default TTS voice: {args.tts_voice}")
        logger.info(f"Default TTS speed: {args.tts_speed}")
        logger.info("Using TTS API key provided (Required for OpenAI).")
        # Log OpenAI TTS pricing being used
        if args.tts_model in OPENAI_TTS_PRICING:
            logger.info(
                f"OpenAI TTS pricing for '{args.tts_model}': ${OPENAI_TTS_PRICING[args.tts_model]:.2f} / 1M chars"
            )
        else:
            logger.warning(
                f"OpenAI TTS pricing not defined for model '{args.tts_model}'. Cost calculation will be $0."
            )
    else:
        logger.info(f"Using Custom TTS server at: {tts_base_url}")
        logger.info(f"Using TTS model: {args.tts_model}")
        logger.info(f"Default TTS voice: {args.tts_voice}")
        logger.info(f"Default TTS speed: {args.tts_speed}")
        if args.tts_api_key:
            logger.info("Using TTS API key provided.")
        else:
            logger.info("No TTS API key provided (assumed optional for custom server).")
    logger.debug(f"Loaded TTS_ACRONYM_PRESERVE_SET: {TTS_ACRONYM_PRESERVE_SET}")

    if SYSTEM_MESSAGE:  # Check the final SYSTEM_MESSAGE string
        logger.info(f"Loaded SYSTEM_MESSAGE: '{SYSTEM_MESSAGE[:50]}...'")
    else:
        logger.info("No SYSTEM_MESSAGE defined.")

    # --- Populate Models and Costs ---
    # Uses global llm_api_base and args.llm_api_key which are set above
    if use_llm_proxy:
        AVAILABLE_MODELS, MODEL_COST_DATA = get_models_and_costs_from_proxy(
            llm_api_base, args.llm_api_key  # Use renamed args for API key
        )
    else:
        AVAILABLE_MODELS, MODEL_COST_DATA = get_models_and_costs_from_litellm()

    # Fallback if no models were found
    if not AVAILABLE_MODELS:
        logger.warning(
            "No models found from proxy or litellm.model_cost. Using fallback."
        )
        AVAILABLE_MODELS = ["fallback/unknown-model"]

    # Determine the initial model using args.llm_model as the preference (Renamed arg)
    initial_model_preference = args.llm_model  # Renamed arg
    if initial_model_preference and initial_model_preference in AVAILABLE_MODELS:
        current_llm_model = initial_model_preference
        logger.info(
            f"Using LLM model from --llm-model argument (or env default): {current_llm_model}"  # Renamed arg
        )
    elif AVAILABLE_MODELS and AVAILABLE_MODELS[0] != "fallback/unknown-model":
        if initial_model_preference:  # Log if the preferred wasn't found
            logger.warning(
                f"LLM model '{initial_model_preference}' from --llm-model (or env default) not found in available list {AVAILABLE_MODELS}. Trying first available model."  # Renamed arg
            )
        current_llm_model = AVAILABLE_MODELS[0]
        logger.info(f"Using first available model: {current_llm_model}")
    elif initial_model_preference:  # Use preferred even if not in list, but warn
        current_llm_model = initial_model_preference
        logger.warning(
            f"Model '{current_llm_model}' from --llm-model (or env default) not found in available list, but using it as requested. Cost calculation might fail."  # Renamed arg
        )
    else:  # No preference and no available models
        current_llm_model = "fallback/unknown-model"
        logger.error(
            "No valid LLM models available or specified. Functionality may be impaired."
        )
        # Consider exiting: return 1

    logger.info(f"Initial LLM model set to: {current_llm_model}")

    # --- Client Initialization ---
    # Uses global tts_base_url, stt_api_base and args.*_api_key set above
    try:
        tts_client = OpenAI(
            base_url=tts_base_url,
            api_key=args.tts_api_key,  # Use args (required for OpenAI)
        )
        # Perform a simple check if using OpenAI to validate the API key early
        if IS_OPENAI_TTS:
            try:
                # Try listing models as a simple auth check (adjust if needed)
                # Note: OpenAI Python v1+ doesn't have a simple 'list voices' or similar lightweight check easily available
                # We might rely on the first TTS call to fail if the key is bad.
                # Or, attempt a low-cost operation if available. For now, we'll let the first TTS call handle auth errors.
                logger.info(
                    "OpenAI TTS client initialized. API key will be validated on first use."
                )
                pass
            except AuthenticationError as e:
                logger.critical(
                    f"OpenAI API key is invalid: {e}. Please check TTS_API_KEY. Exiting."
                )
                return 1  # Return error code
            except Exception as e:
                logger.warning(
                    f"Could not perform initial validation of OpenAI API key: {e}"
                )

    except Exception as e:
        logger.critical(f"Failed to initialize TTS client: {e}. Exiting.")
        return 1  # Return error code

    try:
        stt_client = OpenAI(
            base_url=stt_api_base,
            api_key=args.stt_api_key,  # Use args (required for OpenAI)
        )
        # Perform a simple check if using OpenAI to validate the API key early
        if IS_OPENAI_STT:
            try:
                # Try listing models as a simple auth check (adjust if needed)
                # Note: OpenAI Python v1+ doesn't have a simple 'list voices' or similar lightweight check easily available
                # We might rely on the first STT call to fail if the key is bad.
                # Or, attempt a low-cost operation if available. For now, we'll let the first STT call handle auth errors.
                logger.info(
                    "OpenAI STT client initialized. API key will be validated on first use."
                )
                pass
            except AuthenticationError as e:
                logger.critical(
                    f"OpenAI API key is invalid: {e}. Please check STT_API_KEY. Exiting."
                )
                return 1  # Return error code
            except Exception as e:
                logger.warning(
                    f"Could not perform initial validation of OpenAI API key: {e}"
                )

    except Exception as e:
        logger.critical(f"Failed to initialize STT client: {e}. Exiting.")
        return 1  # Return error code

    # --- Populate Available Voices (Revised Logic) ---
    if IS_OPENAI_TTS:
        # Use the predefined list for OpenAI
        AVAILABLE_VOICES_TTS = OPENAI_TTS_VOICES
        logger.info(f"Using predefined OpenAI TTS voices: {AVAILABLE_VOICES_TTS}")
    else:
        # Use the get_voices function for custom servers
        logger.info(
            f"Querying custom TTS server ({tts_base_url}) for available voices..."
        )
        AVAILABLE_VOICES_TTS = get_voices(tts_base_url, args.tts_api_key)  # Use args
        if not AVAILABLE_VOICES_TTS:
            logger.warning(
                f"Could not retrieve voices from custom TTS server at {tts_base_url}. TTS might fail."
            )
        else:
            logger.info(
                f"Available voices from custom TTS server: {AVAILABLE_VOICES_TTS}"
            )

    # Validate the initial selected_voice using args.tts_voice as the preference
    initial_voice_preference = args.tts_voice
    if initial_voice_preference and initial_voice_preference in AVAILABLE_VOICES_TTS:
        selected_voice = initial_voice_preference
        logger.info(
            f"Using TTS voice from --tts-voice argument (or env default): {selected_voice}"
        )
    elif AVAILABLE_VOICES_TTS:
        if initial_voice_preference:  # Log if preferred wasn't found
            logger.warning(
                f"TTS voice '{initial_voice_preference}' from --tts-voice (or env default) not found in available voices: {AVAILABLE_VOICES_TTS}. Trying first available voice."
            )
        selected_voice = AVAILABLE_VOICES_TTS[0]
        logger.info(f"Using first available voice instead: {selected_voice}")
    else:
        # No voices available OR preferred voice invalid and no others available
        selected_voice = initial_voice_preference  # Keep the potentially invalid one
        logger.error(
            f"No voices available from TTS engine, or specified voice '{selected_voice}' is invalid. TTS will likely fail."
        )
        # If using OpenAI and the default 'ash' wasn't found (which shouldn't happen unless OPENAI_TTS_VOICES is wrong)
        if IS_OPENAI_TTS and selected_voice not in OPENAI_TTS_VOICES:
            logger.critical(
                f"Specified OpenAI voice '{selected_voice}' is not valid. Valid options: {OPENAI_TTS_VOICES}. Exiting."
            )
            return 1  # Return error code

    logger.info(f"Initial TTS voice set to: {selected_voice}")

    # --- FastAPI Setup ---
    stream = Stream(
        modality="audio",
        mode="send-receive",
        handler=ReplyOnPause(
            response,
            # --- VAD Tuning Parameters (Adjusted for LESS sensitivity in noisy environments) ---
            algo_options=AlgoOptions(
                # Duration of audio chunks processed by VAD (seconds). Default: 0.6
                audio_chunk_duration=3.0,
                # Probability threshold to consider speech *started*. Default: 0.2
                started_talking_threshold=0.2,
                # Probability threshold to consider a chunk *as speech*. Lower values bridge pauses better. Default: 0.1
                speech_threshold=0.2,  # Decreased further from 0.1 to bridge pauses even more effectively
            ),
            model_options=SileroVadOptions(
                # VAD model's internal speech probability threshold. Lower values make it less sensitive to silence (more likely to detect speech). Default: 0.5
                threshold=0.5,
                # Minimum duration of speech to be considered valid (milliseconds). Higher values ignore short sounds like coughs. Default: 250
                min_speech_duration_ms=400,  # Kept at 400
                # Minimum duration of silence after speech to trigger pause (milliseconds). Higher values allow longer pauses. Default: 100
                min_silence_duration_ms=3500,  # Increased from 2500 to allow longer pauses
            ),
            can_interrupt=True,  # Default: Allow interrupting the bot's response
            # startup_fn=None,    # Default: No function called on connection start
        ),
        rtc_configuration=get_twilio_turn_credentials() if get_space() else None,
        concurrency_limit=5 if get_space() else None,
        time_limit=90 if get_space() else None,
    )

    app = FastAPI()
    stream.mount(app)
    register_endpoints(app, stream)  # Register the endpoints defined above

    # --- Server and UI Launch ---
    # Use host and port from parsed args
    host = args.host
    preferred_port = args.port  # Already an int from argparse
    port = preferred_port
    max_retries = 10

    # Check if the *preferred* port is available
    if is_port_in_use(port, host):
        logger.warning(
            f"Preferred port {port} on host {host} is in use. Searching for an available port..."
        )
        found_port = False
        for attempt in range(max_retries):
            # Only search on the specified host
            new_port = random.randint(1024, 65535)
            logger.debug(f"Attempt {attempt+1}: Checking port {new_port} on {host}...")
            if not is_port_in_use(new_port, host):
                port = new_port
                found_port = True
                logger.info(f"Found available port: {port} on host {host}")
                break
        if not found_port:
            logger.error(
                f"Could not find an available port on host {host} after {max_retries} attempts. Exiting."
            )
            return 1  # Return error code
    else:
        logger.info(f"Using preferred port {port} on host {host}")

    # Update APP_PORT global in case a random port was chosen,
    # although it's not strictly necessary as `port` is used below.
    APP_PORT = port
    url = f"http://{host}:{port}"

    def run_server():
        global uvicorn_server
        try:
            # Use host and port variables determined above
            config = uvicorn.Config(
                app,
                host=host,
                port=port,
                log_config=None,  # Use determined host and port
            )
            uvicorn_server = uvicorn.Server(config)
            logger.info(f"Starting Uvicorn server on {host}:{port}...")
            uvicorn_server.run()  # This blocks until shutdown is triggered
            logger.info("Uvicorn server has stopped.")
        except Exception as e:
            logger.critical(f"Uvicorn server encountered an error: {e}")
        finally:
            uvicorn_server = None  # Clear the global reference

    # Start the heartbeat monitor thread
    monitor_thread = threading.Thread(target=monitor_heartbeat_thread, daemon=True)
    monitor_thread.start()

    # Start the Uvicorn server thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    logger.debug("Waiting for Uvicorn server to initialize...")
    # Wait a bit longer to ensure the server object is likely created
    time.sleep(3.0)

    if not server_thread.is_alive() or uvicorn_server is None:
        logger.critical(
            "Uvicorn server thread failed to start or initialize correctly. Exiting."
        )
        return 1  # Return error code
    else:
        logger.debug("Server thread appears to be running.")

    exit_code = 0  # Default exit code
    try:
        if args.browser:
            logger.info(f"Opening application in default web browser at: {url}")
            webbrowser.open(url, new=1)  # Open in a new window
            logger.info(
                "Application opened in browser. Server is running in the background."
            )
            logger.info("Press Ctrl+C to stop the server.")
            # Keep the main thread alive to allow the daemon server thread to run
            try:
                # Wait indefinitely for the server thread to finish (it won't unless interrupted)
                server_thread.join()
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt received, shutting down.")
            finally:
                # Signal the heartbeat monitor thread to stop
                logger.info("Signaling heartbeat monitor thread to stop...")
                shutdown_event.set()

                # Signal the Uvicorn server to shut down if it's still running (might be redundant)
                if (
                    uvicorn_server
                    and server_thread.is_alive()
                    and not uvicorn_server.should_exit
                ):
                    logger.info("Signaling Uvicorn server to shut down...")
                    uvicorn_server.should_exit = True
                elif uvicorn_server and uvicorn_server.should_exit:
                    logger.info("Uvicorn server already signaled to shut down.")
                elif not server_thread.is_alive():
                    logger.info("Server thread already stopped.")
                else:
                    logger.warning(
                        "Uvicorn server instance not found, cannot signal shutdown."
                    )

                # Wait for the server thread to finish after signaling (if it was running)
                if server_thread.is_alive():
                    logger.info("Waiting for Uvicorn server thread to join...")
                    server_thread.join(timeout=5.0)
                    if server_thread.is_alive():
                        logger.warning(
                            "Uvicorn server thread did not exit gracefully after 5 seconds."
                        )
                    else:
                        logger.info("Uvicorn server thread joined successfully.")

                # Wait for the monitor thread to finish
                logger.info("Waiting for heartbeat monitor thread to join...")
                monitor_thread.join(timeout=2.0)
                if monitor_thread.is_alive():
                    logger.warning(
                        "Heartbeat monitor thread did not exit gracefully after 2 seconds."
                    )
                else:
                    logger.info("Heartbeat monitor thread joined successfully.")
        else:  # This else belongs to the if args.browser block
            logger.info(f"Creating pywebview window for URL: {url}")
            api = Api(None)  # pywebview API instance
            # Store window object globally for monitor thread access
            pywebview_window = webview.create_window(
                f"Simple Voice Chat v{APP_VERSION}",
                url,
                width=800,
                height=800,
                js_api=api,  # Updated height from 700 to 800, Added version to title
            )
            api._window = pywebview_window  # Pass window object to API class instance

            logger.info("Starting pywebview...")
            try:
                # This blocks until the window is closed
                webview.start(debug=args.verbose)
            except Exception as e:
                logger.critical(f"Pywebview encountered an error: {e}")
                exit_code = 1  # Set error code
            finally:
                logger.info("Pywebview window closed or heartbeat timed out.")
                # Signal the heartbeat monitor thread to stop
                logger.info("Signaling heartbeat monitor thread to stop...")
                shutdown_event.set()

                # Signal the Uvicorn server to shut down (might be redundant if heartbeat timed out)
                if uvicorn_server and not uvicorn_server.should_exit:
                    logger.info("Signaling Uvicorn server to shut down...")
                    uvicorn_server.should_exit = True
                elif uvicorn_server and uvicorn_server.should_exit:
                    logger.info("Uvicorn server already signaled to shut down.")
                else:
                    logger.warning(
                        "Uvicorn server instance not found, cannot signal shutdown."
                    )

                # Wait for the server thread to finish
                logger.info("Waiting for Uvicorn server thread to join...")
                server_thread.join(timeout=5.0)
                if server_thread.is_alive():
                    logger.warning(
                        "Uvicorn server thread did not exit gracefully after 5 seconds."
                    )
                else:
                    logger.info("Uvicorn server thread joined successfully.")

                # Wait for the monitor thread to finish
                logger.info("Waiting for heartbeat monitor thread to join...")
                monitor_thread.join(timeout=2.0)
                if monitor_thread.is_alive():
                    logger.warning(
                        "Heartbeat monitor thread did not exit gracefully after 2 seconds."
                    )
                else:
                    logger.info("Heartbeat monitor thread joined successfully.")
    except Exception as e:
        logger.critical(
            f"An unexpected error occurred in the main execution block: {e}",
            exc_info=True,
        )
        exit_code = 1  # Set error code
        # Ensure shutdown signals are sent even on unexpected main errors
        shutdown_event.set()
        if uvicorn_server and not uvicorn_server.should_exit:
            uvicorn_server.should_exit = True
        # Wait for threads? Maybe not necessary if exiting immediately.

    logger.info(f"Main function returning exit code: {exit_code}")
    return exit_code


if __name__ == "__main__":
    # This block is now only executed when running the script directly (python simple_voice_chat.py)
    # It calls the main() function which contains all the setup and execution logic.
    sys.exit(main())
