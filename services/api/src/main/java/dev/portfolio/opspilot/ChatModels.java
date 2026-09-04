package dev.portfolio.opspilot;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.util.List;
import java.util.Map;

record ChatRequest(@NotBlank @Size(max=100) String sessionId, @NotBlank @Size(min=2,max=2000) String message) {}
record AiRequest(String message, String session_id, String trace_id) {}
record Citation(String source, String excerpt, double score) {}
record ToolProposal(String name, Map<String,String> arguments, String risk) {}
record AiResponse(String answer, List<Citation> citations, double confidence, ToolProposal tool_proposal, String guardrail) {}
record ChatResponse(String traceId, String answer, List<Citation> citations, double confidence, PendingAction action, String guardrail) {}
record PendingAction(String id, String name, Map<String,String> arguments, String status) {}
record ApprovalResponse(String id, String status, Map<String,String> result) {}

