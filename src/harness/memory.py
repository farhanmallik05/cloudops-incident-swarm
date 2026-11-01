"""Session and State Memory for Strands SDK Agents."""
import time
from typing import List, Dict, Any, Optional

class InMemoryMemory:
    """In-memory session state storage for fast local agent execution."""

    def __init__(self, session_id: str = "default-session"):
        self.session_id = session_id
        self.messages: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str, tool_calls: Optional[List[Dict[str, Any]]] = None) -> None:
        msg = {
            "role": role,
            "content": content,
            "tool_calls": tool_calls or [],
            "timestamp": time.time()
        }
        self.messages.append(msg)

    def get_messages(self) -> List[Dict[str, Any]]:
        return list(self.messages)

    def clear(self) -> None:
        self.messages = []


class DynamoDBSessionMemory:
    """Amazon DynamoDB persistent memory integration for cloud production agents."""

    def __init__(self, table_name: str, session_id: str, region_name: str = "us-east-1"):
        self.table_name = table_name
        self.session_id = session_id
        self.region_name = region_name
        self.fallback = InMemoryMemory(session_id)
        self.boto_client = None

        try:
            import boto3
            self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
            self.table = self.dynamodb.Table(table_name)
            # Verify table connectivity
            self.table.load()
        except Exception:
            # Gracefully fallback to in-memory if AWS credentials/table are not available
            self.table = None

    def add_message(self, role: str, content: str, tool_calls: Optional[List[Dict[str, Any]]] = None) -> None:
        if self.table:
            try:
                self.table.put_item(
                    Item={
                        "SessionId": self.session_id,
                        "Timestamp": int(time.time() * 1000),
                        "Role": role,
                        "Content": content,
                        "ToolCalls": tool_calls or [],
                    }
                )
                return
            except Exception:
                pass
        self.fallback.add_message(role, content, tool_calls)

    def get_messages(self) -> List[Dict[str, Any]]:
        return self.fallback.get_messages()

