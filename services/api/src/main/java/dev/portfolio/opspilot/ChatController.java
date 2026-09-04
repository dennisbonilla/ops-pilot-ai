package dev.portfolio.opspilot;

import jakarta.validation.Valid;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins={"http://localhost:3000"})
class ChatController {
  private final ChatService service;
  ChatController(ChatService service) { this.service = service; }

  @GetMapping("/health") Map<String,String> health() { return Map.of("status", "UP"); }
  @PostMapping("/chat") ChatResponse chat(@Valid @RequestBody ChatRequest request) { return service.chat(request); }
  @PostMapping("/actions/{id}/approve") ApprovalResponse approve(@PathVariable String id) { return service.approve(id); }

  @ExceptionHandler(ActionNotFoundException.class)
  @ResponseStatus(HttpStatus.NOT_FOUND)
  Map<String,String> notFound(RuntimeException error) { return Map.of("error", error.getMessage()); }
}

