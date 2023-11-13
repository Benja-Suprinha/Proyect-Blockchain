import asyncio
from api import block_created_event, block_queue

# Asynchronous function to process blocks
async def process_blocks():
    while True:
        # Wait for the event to be set
        await block_created_event.wait()

        # Get the block from the queue
        block = await block_queue.get()

        # Reset the event
        block_created_event.clear()

        # Process the block as needed
        print("Received block:", block)

# Función principal para ejecutar el bucle de eventos
async def main():
    # Start the block processing in an asynchronous loop
    await asyncio.create_task(process_blocks())

# Ejecutar el bucle de eventos
if __name__ == "__main__":
    asyncio.run(main())
