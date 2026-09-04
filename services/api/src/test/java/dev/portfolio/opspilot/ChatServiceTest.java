package dev.portfolio.opspilot;

import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.Test;

class ChatServiceTest {
  @Test void rejectsUnknownApproval() {
    var service = new ChatService("http://localhost:1");
    assertThrows(ActionNotFoundException.class, () -> service.approve("missing"));
  }
}

