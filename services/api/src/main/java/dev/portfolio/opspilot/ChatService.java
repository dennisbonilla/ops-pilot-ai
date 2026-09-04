package dev.portfolio.opspilot;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
class ChatService {
  private static final Logger log = LoggerFactory.getLogger(ChatService.class);
  private final RestClient ai;
  private final Map<String, PendingAction> pending = new ConcurrentHashMap<>();

  ChatService(@Value("${ai.service-url}") String aiServiceUrl) {
    this.ai = RestClient.builder().baseUrl(aiServiceUrl).build();
  }

  ChatResponse chat(ChatRequest request) {
    String traceId = UUID.randomUUID().toString();
    AiResponse response = ai.post().uri("/v1/query").body(new AiRequest(request.message(), request.sessionId(), traceId)).retrieve().body(AiResponse.class);
    PendingAction action = null;
    if (response != null && response.tool_proposal() != null) {
      String id = UUID.randomUUID().toString();
      action = new PendingAction(id, response.tool_proposal().name(), response.tool_proposal().arguments(), "PENDING_APPROVAL");
      pending.put(id, action);
    }
    log.info("event=chat.completed traceId={} sessionId={} at={}", traceId, request.sessionId(), Instant.now());
    return new ChatResponse(traceId, response.answer(), response.citations(), response.confidence(), action, response.guardrail());
  }

  ApprovalResponse approve(String id) {
    PendingAction action = pending.remove(id);
    if (action == null) throw new ActionNotFoundException(id);
    if (!"create_incident".equals(action.name())) throw new UnsafeToolException(action.name());
    Map<String,String> result = Map.of("ticket", "INC-" + System.currentTimeMillis()%100000, "severity", action.arguments().getOrDefault("severity", "SEV-3"));
    log.info("event=action.approved actionId={} tool={} at={}", id, action.name(), Instant.now());
    return new ApprovalResponse(id, "EXECUTED", result);
  }
}

class ActionNotFoundException extends RuntimeException { ActionNotFoundException(String id) { super("Unknown or already executed action: " + id); } }
class UnsafeToolException extends RuntimeException { UnsafeToolException(String tool) { super("Tool is not allowed: " + tool); } }

