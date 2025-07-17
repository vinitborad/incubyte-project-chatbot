# Simple Test Suite for Sweet Shop Chatbot

## Overview
This is a simplified test suite for the sweet shop chatbot project, focusing on core functionality testing as requested.

## Test Structure

### 1. Unit Tests (`tests/`)

#### `test_database.py`
- **test_get_all_sweets_success**: Tests successful retrieval of sweets from database
- **test_get_all_sweets_empty_database**: Tests handling of empty database

#### `test_tools.py` 
- **test_buy_sweet_success**: Tests successful sweet purchase
- **test_buy_sweet_not_found**: Tests handling when sweet is not found
- **test_get_available_sweets_success**: Tests successful sweets listing
- **test_get_available_sweets_empty_inventory**: Tests empty inventory handling

#### `test_chatbot.py`
- **test_graph_compiles_successfully**: Tests agent graph compilation
- **test_call_model_adds_system_prompt**: Tests system prompt addition
- **test_should_continue_with_tool_calls**: Tests tool call continuation logic
- **test_should_continue_without_tool_calls**: Tests response without tools
- **test_agent_with_history_basic_flow**: Tests basic agent conversation flow

#### `test_main.py` (API Controller Tests)
- **test_chat_endpoint_success**: Tests successful chat API endpoint
- **test_chat_endpoint_missing_session_id**: Tests missing session ID validation
- **test_chat_endpoint_missing_message**: Tests missing message validation
- **test_api_documentation_accessible**: Tests API docs accessibility

### 2. Integration Tests (`test_integration.py`)
- **test_get_sweets_flow**: Tests complete flow for getting available sweets
- **test_buy_sweet_flow**: Tests complete flow for buying sweets
- **test_agent_creation**: Tests agent creation and initialization

### 3. Performance Tests (`test_performance.py`)
- **test_get_sweets_response_time**: Tests response time for getting sweets
- **test_agent_creation_time**: Tests agent creation performance

## Running Tests

### Simple Test Run
```bash
python run_tests.py
```

### Manual pytest Run
```bash
pytest tests/ -v
```

## Test Dependencies
- pytest
- pytest-asyncio
- pytest-mock
- pytest-cov
- responses (for HTTP mocking)
- unittest.mock (built-in)

## Key Features Tested
1. **Agent Graph**: Core chatbot logic and conversation flow
2. **API Controller**: FastAPI endpoints and request handling
3. **Database Operations**: Sweet inventory management
4. **Tools Integration**: LangChain tools for buying and listing sweets
5. **Basic Performance**: Response times for critical operations

## Test Results
✅ 20 tests passing  
⚠️ 6 warnings (LangChain deprecation warnings - non-blocking)

All test cases are now working correctly. The test suite covers the essential functionality while keeping complexity minimal as requested.
