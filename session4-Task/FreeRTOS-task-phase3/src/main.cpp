#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include <queue.h>

// global queue handle 
QueueHandle_t stringQueue;

// Task Function Prototypes
void TaskConsumer(void *pvParameters);
void TaskProducerA(void *pvParameters);
void TaskProducerB(void *pvParameters);

void setup() {

  Serial.begin(9600);
  stringQueue = xQueueCreate(10, sizeof(char*));

  if (stringQueue != NULL) {
    //create the consumer task
    xTaskCreate(TaskConsumer, "Consumer", 128, NULL, 2, NULL);

    //create producer A task
    xTaskCreate(TaskProducerA, "ProducerA", 128, NULL, 1, NULL);

    //create producer B task
    xTaskCreate(TaskProducerB, "ProducerB", 128, NULL, 1, NULL);
    
    // The FreeRTOS scheduler starts automatically in the Arduino port.
  }
}

void loop() {
  
}

void TaskConsumer(void *pvParameters) {
  char *receivedMessage;

  while (1) {
    if (xQueueReceive(stringQueue, &receivedMessage, portMAX_DELAY) == pdPASS) {
      Serial.println(receivedMessage);
    }
  }
}

void TaskProducerA(void *pvParameters) {
  // The string message to send
  const char *msgA = "Task one is working";
  // Delay interval: 1000ms
  const TickType_t xDelay = pdMS_TO_TICKS(1000);

  while (1) {
    xQueueSend(stringQueue, &msgA, portMAX_DELAY);
    vTaskDelay(xDelay);
  }
}

void TaskProducerB(void *pvParameters) {
  
  const char *msgB = "Task two is working";
 
  const TickType_t xDelay = pdMS_TO_TICKS(1500);

  while (1) {
    // Send the string pointer to the queue
    xQueueSend(stringQueue, &msgB, portMAX_DELAY);
    
    // Non-blocking RTOS delay to control frequency[cite: 5]
    vTaskDelay(xDelay);
  }
}